# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Dict, Any
# from graph import build_graph
# import asyncio

# app = FastAPI()

# class DataRequest(BaseModel):
#     data_type: str
#     num_records: int
#     parameters: Dict[str, Any]

# @app.post("/generate")
# async def generate_data(request: DataRequest):
#     try:
#         graph = build_graph()
#         result = await asyncio.get_event_loop().run_in_executor(
#             None,
#             lambda: graph.invoke({
#                 "data_type": request.data_type,
#                 "num_records": request.num_records,
#                 "parameters": request.parameters
#             })
#         )
#         return {"data": result["output"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# from fastapi import FastAPI, HTTPException, Request
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from typing import Dict, Any, Optional
# from graph import build_graph
# import asyncio
# import sqlite3
# import pandas as pd
# import io
# import json
# from datetime import datetime

# app = FastAPI()

# class DataRequest(BaseModel):
#     data_type: str
#     num_records: int
#     parameters: Dict[str, Any]
#     query: Optional[str] = None
#     session_id: Optional[str] = None

# def init_db():
#     conn = sqlite3.connect("usage.db")
#     conn.execute("CREATE TABLE IF NOT EXISTS logs (data_type TEXT, num_records INTEGER, timestamp TEXT)")
#     conn.execute("CREATE TABLE IF NOT EXISTS sessions (session_id TEXT, data TEXT)")
#     conn.close()

# @app.post("/generate")
# async def generate_data(request: DataRequest):
#     init_db()
#     try:
#         graph = build_graph()
#         result = await asyncio.get_event_loop().run_in_executor(
#             None, lambda: graph.invoke(request.model_dump())
#         )
#         data = result["output"]
        
#         # Log request
#         conn = sqlite3.connect("usage.db")
#         conn.execute(
#             "INSERT INTO logs (data_type, num_records, timestamp) VALUES (?, ?, ?)",
#             (request.data_type, request.num_records, datetime.now().isoformat())
#         )
#         # Save to session
#         if request.session_id:
#             conn.execute(
#                 "INSERT OR REPLACE INTO sessions (session_id, data) VALUES (?, ?)",
#                 (request.session_id, json.dumps(data))
#             )
#         conn.commit()
#         conn.close()
        
#         # Handle export format
#         format = request.parameters.get("format", "json")
#         if format == "csv":
#             df = pd.DataFrame(data)
#             stream = io.StringIO()
#             df.to_csv(stream, index=False)
#             return StreamingResponse(
#                 io.BytesIO(stream.getvalue().encode("utf-8")),
#                 media_type="text/csv",
#                 headers={"Content-Disposition": "attachment; filename=data.csv"}
#             )
#         return {"data": data, "session_id": request.session_id}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/history")
# async def get_history(session_id: str):
#     try:
#         conn = sqlite3.connect("usage.db")
#         cursor = conn.execute("SELECT data FROM sessions WHERE session_id = ?", (session_id,))
#         history = [json.loads(row[0]) for row in cursor.fetchall()]
#         conn.close()
#         return {"history": history}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Dict, Any, Optional
from graph import build_graph
import sqlite3
import pandas as pd
import io
import json
from datetime import datetime
import logging
import traceback

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

USERS = {
    "admin-key-123": {"role": "admin", "username": "admin"},
    "user-key-456": {"role": "user", "username": "user"}
}

def get_current_user(api_key: str = Security(api_key_header)):
    if api_key not in USERS:
        logger.error(f"Invalid API key: {api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return USERS[api_key]

def require_role(required_role: str):
    def role_checker(user: Dict[str, str] = Security(get_current_user)):
        if user["role"] != required_role and user["role"] != "admin":
            logger.error(f"Insufficient permissions for user: {user['username']}")
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

class DataRequest(BaseModel):
    data_type: str
    num_records: int
    parameters: Dict[str, Any]
    session_id: Optional[str] = None

def init_db():
    try:
        conn = sqlite3.connect("usage.db")
        conn.execute("CREATE TABLE IF NOT EXISTS logs (data_type TEXT, num_records INTEGER, timestamp TEXT, username TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS sessions (session_id TEXT, data TEXT, username TEXT)")
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")

@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.post("/generate")
async def generate_data(request: DataRequest, user: Dict[str, str] = Security(get_current_user), raw_request: Request = None):
    logger.info(f"Received /generate request from user: {user['username']}, method: {raw_request.method}, data_type: {request.data_type}, num_records: {request.num_records}")
    logger.debug(f"Request payload: {request.model_dump_json()}")
    init_db()
    try:
        if request.num_records < 1:
            logger.error("num_records must be positive")
            raise ValueError("num_records must be positive")
        if "schema" not in request.parameters:
            logger.error("Schema is required")
            raise ValueError("Schema is required")
        
        schema = request.parameters["schema"]
        for field, info in schema.items():
            if not isinstance(info, dict) or "type" not in info:
                logger.error(f"Invalid schema for field {field}: {info}")
                raise ValueError(f"Invalid schema for field {field}: missing type")
            if info["type"] in ["integer", "number", "binary", "phone"]:
                if "min" not in info or "max" not in info:
                    logger.error(f"Missing min/max for numerical field {field}: {info}")
                    raise ValueError(f"Missing min/max for field {field}")
        
        logger.debug(f"Schema validated: {schema}")
        graph = build_graph()
        result = graph.invoke(request.model_dump())
        data = result["output"]
        
        if not isinstance(data, list):
            logger.error("Graph output must be a list of records")
            raise ValueError("Graph output must be a list of records")
        
        conn = sqlite3.connect("usage.db")
        try:
            conn.execute(
                "INSERT INTO logs (data_type, num_records, timestamp, username) VALUES (?, ?, ?, ?)",
                (request.data_type, request.num_records, datetime.now().isoformat(), user["username"])
            )
            if request.session_id:
                conn.execute(
                    "INSERT OR REPLACE INTO sessions (session_id, data, username) VALUES (?, ?, ?)",
                    (request.session_id, json.dumps(data), user["username"])
                )
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
        
        format = request.parameters.get("format", "json")
        if format == "csv":
            df = pd.DataFrame(data)
            stream = io.StringIO()
            df.to_csv(stream, index=False)
            return StreamingResponse(
                io.BytesIO(stream.getvalue().encode("utf-8")),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={request.data_type}.csv"}
            )
        return {"data": data, "session_id": request.session_id}
    except Exception as e:
        logger.error(f"Error in /generate: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/export_db")
async def export_to_db(request: DataRequest, user: Dict[str, str] = Security(get_current_user), raw_request: Request = None):
    logger.info(f"Received /export_db request from user: {user['username']}, method: {raw_request.method}")
    init_db()
    try:
        if request.num_records < 1:
            logger.error("num_records must be positive")
            raise ValueError("num_records must be positive")
        if "schema" not in request.parameters:
            logger.error("Schema is required")
            raise ValueError("Schema is required")
        
        schema = request.parameters["schema"]
        for field, info in schema.items():
            if not isinstance(info, dict) or "type" not in info:
                logger.error(f"Invalid schema for field {field}: {info}")
                raise ValueError(f"Invalid schema for field {field}: missing type")
            if info["type"] in ["integer", "number", "binary", "phone"]:
                if "min" not in info or "max" not in info:
                    logger.error(f"Missing min/max for numerical field {field}: {info}")
                    raise ValueError(f"Missing min/max for field {field}")
        
        logger.debug(f"Schema validated: {schema}")
        graph = build_graph()
        result = graph.invoke(request.model_dump())
        data = result["output"]
        
        if not isinstance(data, list):
            logger.error("Graph output must be a list of records")
            raise ValueError("Graph output must be a list of records")
        
        table_name = request.data_type
        conn = sqlite3.connect("data.db")
        try:
            df = pd.DataFrame(data)
            df.to_sql(table_name, conn, if_exists="append", index=False)
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error in export: {str(e)}")
            raise
        finally:
            conn.close()
        return {"status": f"Data exported to table {table_name}"}
    except Exception as e:
        logger.error(f"Error in /export_db: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/history")
async def get_history(session_id: str, user: Dict[str, str] = Security(require_role("admin"))):
    logger.info(f"Received /history request from user: {user['username']}")
    try:
        conn = sqlite3.connect("usage.db")
        cursor = conn.execute(
            "SELECT data FROM sessions WHERE session_id = ? AND username = ?",
            (session_id, user["username"])
        )
        history = [json.loads(row[0]) for row in cursor.fetchall()]
        conn.close()
        return {"history": history}
    except Exception as e:
        logger.error(f"Error in /history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/analytics")
async def get_analytics(user: Dict[str, str] = Security(require_role("admin"))):
    logger.info(f"Received /analytics request from user: {user['username']}")
    try:
        conn = sqlite3.connect("usage.db")
        df = pd.read_sql_query("SELECT * FROM logs WHERE username = ?", conn, params=(user["username"],))
        conn.close()
        return {"logs": df.to_dict(orient="records")}
    except Exception as e:
        logger.error(f"Error in /analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on port 8080")
    uvicorn.run(app, host="0.0.0.0", port=8080, timeout_keep_alive=30)