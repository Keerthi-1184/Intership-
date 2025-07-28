# from langgraph.graph import StateGraph, END
# from typing import TypedDict, List, Dict, Any
# import random
# import faker

# class GraphState(TypedDict):
#     data_type: str
#     num_records: int
#     parameters: Dict[str, Any]
#     output: List[Dict[str, Any]]

# def initialize_data(state: GraphState) -> GraphState:
#     state["output"] = []
#     return state

# def generate_synthetic_data(state: GraphState) -> GraphState:
#     fake = faker.Faker()
#     data_type = state["data_type"]
#     num_records = state["num_records"]
#     parameters = state["parameters"]
    
#     output = []
#     if data_type == "user":
#         for _ in range(num_records):
#             record = {
#                 "name": fake.name(),
#                 "email": fake.email(),
#                 "age": random.randint(parameters.get("age_min", 18), parameters.get("age_max", 80)),
#                 "city": fake.city()
#             }
#             output.append(record)
#     elif data_type == "product":
#         for _ in range(num_records):
#             record = {
#                 "product_id": fake.uuid4(),
#                 "name": fake.word().capitalize() + " " + fake.word().capitalize(),
#                 "price": round(random.uniform(parameters.get("price_min", 10.0), parameters.get("price_max", 1000.0)), 2),
#                 "category": random.choice(parameters.get("categories", ["Electronics", "Clothing", "Home"]))
#             }
#             output.append(record)
#     else:
#         raise ValueError(f"Unsupported data type: {data_type}")
    
#     state["output"] = output
#     return state

# def build_graph():
#     workflow = StateGraph(GraphState)
#     workflow.add_node("initialize", initialize_data)
#     workflow.add_node("generate", generate_synthetic_data)
    
#     workflow.set_entry_point("initialize")
#     workflow.add_edge("initialize", "generate")
#     workflow.add_edge("generate", END)
    
#     return workflow.compile()

# if __name__ == "__main__":
#     graph = build_graph()
#     result = graph.invoke({
#         "data_type": "user",
#         "num_records": 5,
#         "parameters": {"age_min": 20, "age_max": 60}
#     })
#     print(result["output"])


# from langgraph.graph import StateGraph, END
# from typing import TypedDict, List, Dict, Any
# import random
# import faker
# import spacy
# import requests

# class GraphState(TypedDict):
#     data_type: str
#     num_records: int
#     parameters: Dict[str, Any]
#     query: str
#     output: List[Dict[str, Any]]

# nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])  # Optimize for performance

# def parse_query(state: GraphState) -> GraphState:
#     query = state.get("query", "")
#     if query:
#         doc = nlp(query.lower())
#         parameters = state["parameters"].copy()
#         schema = parameters.get("schema", {})
        
#         # Enhanced parsing for field names
#         field_keywords = {
#             "name": ["name", "names", "employee", "employees"],
#             "phone": ["phone", "phones", "phone number", "phone numbers"],
#             "email": ["email", "emails"],
#             "city": ["city", "cities", "location"],
#             "address": ["address", "addresses"],
#             "company": ["company", "companies"],
#         }
        
#         for token in doc:
#             for field, keywords in field_keywords.items():
#                 if any(keyword in token.text for keyword in keywords):
#                     schema[field] = field
#             if token.pos_ == "NUM" and any(t.text.lower() in ["records", "employees"] for t in doc):
#                 state["num_records"] = int(token.text)
        
#         parameters["schema"] = schema
#         state["parameters"] = parameters
#         if schema and state["data_type"] != "weather":
#             state["data_type"] = "custom"
#     return state

# def initialize_data(state: GraphState) -> GraphState:
#     state["output"] = []
#     return state

# def fetch_external_data(state: GraphState) -> GraphState:
#     data_type = state["data_type"]
#     if data_type == "weather":
#         city = state["parameters"].get("city", "London")
#         api_key = state["parameters"].get("weather_api_key", "your_openweathermap_api_key")
#         response = requests.get(
#             f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
#         )
#         if response.status_code == 200:
#             state["output"] = [response.json()]
#         else:
#             state["output"] = [{"error": "Failed to fetch weather data"}]
#     return state

# def generate_synthetic_data(state: GraphState) -> GraphState:
#     locale = state["parameters"].get("locale", "en_US")
#     fake = faker.Faker(locale)
#     data_type = state["data_type"]
#     num_records = state["num_records"]
#     parameters = state["parameters"]
#     schema = parameters.get("schema", {})
    
#     output = []
#     if data_type == "user":
#         for _ in range(num_records):
#             record = {
#                 "name": fake.name(),
#                 "email": fake.email(),
#                 "age": random.randint(parameters.get("age_min", 18), parameters.get("age_max", 80)),
#                 "city": fake.city()
#             }
#             output.append(record)
#     elif data_type == "product":
#         for _ in range(num_records):
#             record = {
#                 "product_id": fake.uuid4(),
#                 "name": fake.word().capitalize() + " " + fake.word().capitalize(),
#                 "price": round(random.uniform(parameters.get("price_min", 10.0), parameters.get("price_max", 1000.0)), 2),
#                 "category": random.choice(parameters.get("categories", ["Electronics", "Clothing", "Home"]))
#             }
#             output.append(record)
#     elif data_type == "custom":
#         if not schema:
#             raise ValueError("No schema provided for custom data type")
#         for _ in range(num_records):
#             record = {}
#             for field, field_type in schema.items():
#                 if field_type == "name": record[field] = fake.name()
#                 elif field_type == "email": record[field] = fake.email()
#                 elif field_type == "city": record[field] = fake.city()
#                 elif field_type == "phone": record[field] = fake.phone_number()
#                 elif field_type == "address": record[field] = fake.address()
#                 elif field_type == "company": record[field] = fake.company()
#                 elif field_type == "number": record[field] = random.randint(
#                     parameters.get(f"{field}_min", 1), parameters.get(f"{field}_max", 100)
#                 )
#                 elif field_type == "text": record[field] = fake.text(max_nb_chars=200)
#                 else: record[field] = fake.word()
#             output.append(record)
#     else:
#         raise ValueError(f"Unsupported data type: {data_type}")
    
#     state["output"] = output
#     return state

# def build_graph():
#     workflow = StateGraph(GraphState)
#     workflow.add_node("parse", parse_query)
#     workflow.add_node("initialize", initialize_data)
#     workflow.add_node("fetch", fetch_external_data)
#     workflow.add_node("generate", generate_synthetic_data)
    
#     workflow.set_entry_point("parse")
#     workflow.add_edge("parse", "initialize")
#     workflow.add_conditional_edges(
#         "initialize",
#         lambda x: "fetch" if x["data_type"] == "weather" else "generate",
#         {"fetch": "fetch", "generate": "generate"}
#     )
#     workflow.add_edge("fetch", END)
#     workflow.add_edge("generate", END)
    
#     return workflow.compile()

# if __name__ == "__main__":
#     graph = build_graph()
#     result = graph.invoke({
#         "data_type": "custom",
#         "num_records": 5,
#         "parameters": {"schema": {"name": "name", "phone": "phone"}, "locale": "fr_FR"},
#         "query": "Generate 5 records with names and phones"
#     })
#     print(result["output"])


# from langgraph.graph import StateGraph
# from typing import TypedDict, Any, Dict
# from faker import Faker
# import logging
# import traceback

# # Set up logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# class GraphState(TypedDict):
#     data_type: str
#     num_records: int
#     parameters: Dict[str, Any]
#     query: str
#     output: list

# def generate_data(state: GraphState) -> GraphState:
#     logger.info(f"Generating data for state: {state}")
#     try:
#         data_type = state["data_type"]
#         num_records = state["num_records"]
#         parameters = state["parameters"]
#         locale = parameters.get("locale", "en_US")
        
#         schema = parameters.get("schema", {})
#         if data_type == "custom" and not schema:
#             raise ValueError("Custom data type requires a non-empty schema")
        
#         fake = Faker(locale)
#         data = []
        
#         if data_type == "custom":
#             for _ in range(num_records):
#                 record = {}
#                 for field, field_type in schema.items():
#                     if not isinstance(field_type, str):
#                         raise ValueError(f"Invalid field type for {field}: {field_type}")
#                     if field_type == "name":
#                         record[field] = fake.name()
#                     elif field_type == "phone":
#                         record[field] = fake.phone_number()
#                     elif field_type == "email":
#                         record[field] = fake.email()
#                     elif field_type == "company":
#                         record[field] = fake.company()
#                     elif field_type == "city":
#                         record[field] = fake.city()
#                     else:
#                         record[field] = fake.text(max_nb_chars=20)
#                 data.append(record)
#         else:
#             raise ValueError(f"Unsupported data type: {data_type}")
        
#         state["output"] = data
#         logger.info(f"Generated {len(data)} records")
#         return state
#     except Exception as e:
#         logger.error(f"Error in generate_data: {str(e)}\n{traceback.format_exc()}")
#         raise

# def build_graph():
#     try:
#         workflow = StateGraph(GraphState)
#         workflow.add_node("generate", generate_data)
#         workflow.set_entry_point("generate")
#         workflow.set_finish_point("generate")
#         graph = workflow.compile()
#         logger.info("Graph built successfully")
#         return graph
#     except Exception as e:
#         logger.error(f"Error building graph: {str(e)}\n{traceback.format_exc()}")
#         raise


# from langgraph.graph import StateGraph
# from typing import TypedDict, Any, Dict
# from faker import Faker
# import random
# import logging
# import time
# import hashlib
# import sqlite3

# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
# logger = logging.getLogger(__name__)

# class GraphState(TypedDict):
#     data_type: str
#     num_records: int
#     parameters: Dict[str, Any]
#     output: list

# def init_mappings_db():
#     try:
#         conn = sqlite3.connect("mappings.db")
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS mappings (
#                 data_type TEXT,
#                 field_name TEXT,
#                 original_value TEXT,
#                 numerical_id INTEGER
#             )
#         """)
#         conn.commit()
#         conn.close()
#         logger.info("Mappings database initialized")
#     except Exception as e:
#         logger.error(f"Failed to initialize mappings database: {str(e)}")
#         raise

# def save_mapping(data_type, field_name, original_value, numerical_id):
#     try:
#         conn = sqlite3.connect("mappings.db")
#         conn.execute(
#             "INSERT INTO mappings (data_type, field_name, original_value, numerical_id) VALUES (?, ?, ?, ?)",
#             (data_type, field_name, original_value, numerical_id)
#         )
#         conn.commit()
#         conn.close()
#         logger.debug(f"Saved mapping: {data_type}, {field_name}, {original_value}, {numerical_id}")
#     except Exception as e:
#         logger.error(f"Failed to save mapping: {str(e)}")

# def generate_data(state: GraphState) -> GraphState:
#     start_time = time.time()
#     logger.info(f"Generating data for state: {state}")
#     try:
#         data_type = state["data_type"]
#         num_records = state["num_records"]
#         parameters = state["parameters"]
#         locale = parameters.get("locale", "en_US")
#         schema = parameters.get("schema", {})
        
#         if not schema:
#             logger.error("Schema is missing")
#             raise ValueError("Schema is required")
        
#         logger.debug(f"Processing schema: {schema}")
#         init_mappings_db()
#         fake = Faker(locale)
#         data = []
        
#         encodings = {
#             "sex": {"Male": 1, "Female": 0},
#             "merchant_category": {"Retail": 0, "Online": 1, "Travel": 2, "Food": 3, "Services": 4}
#         }
        
#         name_to_id = {}
#         email_to_id = {}
        
#         for i in range(num_records):
#             record = {}
#             for field, field_info in schema.items():
#                 field_type = field_info.get("type")
#                 range_min = field_info.get("min")
#                 range_max = field_info.get("max")
                
#                 if not all([field_type, range_min is not None, range_max is not None]):
#                     logger.error(f"Invalid field info for {field}: {field_info}")
#                     raise ValueError(f"Missing type, min, or max for field {field}")
                
#                 try:
#                     if field_type == "integer":
#                         if data_type == "framingham" and field == "sex":
#                             record[field] = encodings["sex"][random.choice(["Male", "Female"])]
#                         elif data_type == "credit_card_fraud" and field == "transaction_id":
#                             record[field] = i + 1
#                         elif data_type == "credit_card_fraud" and field == "merchant_category":
#                             record[field] = encodings["merchant_category"][random.choice(["Retail", "Online", "Travel", "Food", "Services"])]
#                         else:
#                             record[field] = random.randint(int(range_min), int(range_max))
#                     elif field_type == "number":
#                         record[field] = round(random.uniform(float(range_min), float(range_max)), 4)
#                     elif field_type == "binary":
#                         if data_type == "credit_card_fraud" and field == "fraud":
#                             record[field] = 1 if random.random() < 0.01 else 0
#                         else:
#                             record[field] = random.choice([0, 1])
#                     elif field_type == "name":
#                         name = fake.name()
#                         if name not in name_to_id:
#                             name_to_id[name] = len(name_to_id) + int(range_min)
#                             save_mapping(data_type, field, name, name_to_id[name])
#                         record[field] = name_to_id[name]
#                     elif field_type == "email":
#                         username = fake.user_name() + str(random.randint(100, 999))
#                         email = f"{username}@gmail.com"
#                         if email not in email_to_id:
#                             email_to_id[email] = int(hashlib.md5(email.encode()).hexdigest(), 16) % (int(range_max) - int(range_min) + 1) + int(range_min)
#                             save_mapping(data_type, field, email, email_to_id[email])
#                         record[field] = email_to_id[email]
#                     elif field_type == "phone":
#                         phone = fake.phone_number()
#                         phone_digits = ''.join(c for c in phone if c.isdigit())[-10:]
#                         record[field] = int(phone_digits) if phone_digits else random.randint(int(range_min), int(range_max))
#                     else:
#                         logger.error(f"Unsupported field type: {field_type} for field: {field}")
#                         raise ValueError(f"Unsupported field type: {field_type}")
#                 except Exception as e:
#                     logger.error(f"Error processing field {field}: {str(e)}")
#                     raise ValueError(f"Error processing field {field}: {str(e)}")
            
#             if data_type == "framingham" and "chd_risk" in schema:
#                 risk_score = 0
#                 if record.get("age", 0) > 50:
#                     risk_score += 1
#                 if record.get("smoking", 0) == 1:
#                     risk_score += 1
#                 if record.get("total_cholesterol", 0) > 240:
#                     risk_score += 1
#                 if record.get("systolic_bp", 0) > 140:
#                     risk_score += 1
#                 if record.get("diabetes", 0) == 1:
#                     risk_score += 1
#                 record["chd_risk"] = 1 if risk_score >= 3 else 0
            
#             data.append(record)
        
#         state["output"] = data
#         logger.info(f"Generated {len(data)} records for {data_type} in {time.time() - start_time:.2f}s")
#         return state
#     except Exception as e:
#         logger.error(f"Error in generate_data: {str(e)}")
#         raise

# def build_graph():
#     try:
#         workflow = StateGraph(GraphState)
#         workflow.add_node("generate", generate_data)
#         workflow.set_entry_point("generate")
#         workflow.set_finish_point("generate")
#         return workflow.compile()
#     except Exception as e:
#         logger.error(f"Error building graph: {str(e)}")
#         raise


from langgraph.graph import StateGraph
from typing import TypedDict, Any, Dict
from faker import Faker
import random
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    data_type: str
    num_records: int
    parameters: Dict[str, Any]
    output: list

def generate_data(state: GraphState) -> GraphState:
    start_time = time.time()
    logger.info(f"Generating data for state: {state}")
    try:
        data_type = state["data_type"]
        num_records = state["num_records"]
        parameters = state["parameters"]
        locale = parameters.get("locale", "en_US")
        schema = parameters.get("schema", {})
        
        if not schema:
            logger.error("Schema is missing")
            raise ValueError("Schema is required")
        
        logger.debug(f"Processing schema: {schema}")
        fake = Faker(locale)
        data = []
        
        encodings = {
            "sex": {"Male": 1, "Female": 0},
            "merchant_category": {"Retail": 0, "Online": 1, "Travel": 2, "Food": 3, "Services": 4}
        }
        
        for i in range(num_records):
            record = {}
            for field, field_info in schema.items():
                field_type = field_info.get("type")
                range_min = field_info.get("min")
                range_max = field_info.get("max")
                
                logger.debug(f"Processing field: {field}, type: {field_type}")
                
                # Validate numerical fields only
                if field_type in ["integer", "number", "binary", "phone"]:
                    if not all([range_min is not None, range_max is not None]):
                        logger.error(f"Missing min/max for numerical field {field}: {field_info}")
                        raise ValueError(f"Missing min/max for field {field}")
                
                try:
                    if field_type == "integer":
                        if data_type == "framingham" and field == "sex":
                            record[field] = encodings["sex"][random.choice(["Male", "Female"])]
                        elif data_type == "credit_card_fraud" and field == "transaction_id":
                            record[field] = i + 1
                        elif data_type == "credit_card_fraud" and field == "merchant_category":
                            record[field] = encodings["merchant_category"][random.choice(["Retail", "Online", "Travel", "Food", "Services"])]
                        else:
                            record[field] = random.randint(int(range_min), int(range_max))
                    elif field_type == "number":
                        record[field] = round(random.uniform(float(range_min), float(range_max)), 4)
                    elif field_type == "binary":
                        if data_type == "credit_card_fraud" and field == "fraud":
                            record[field] = 1 if random.random() < 0.01 else 0
                        else:
                            record[field] = random.choice([0, 1])
                    elif field_type == "name":
                        record[field] = fake.name()
                    elif field_type == "email":
                        username = fake.user_name() + str(random.randint(100, 999))
                        record[field] = f"{username}@gmail.com"
                    elif field_type == "phone":
                        phone = fake.phone_number()
                        phone_digits = ''.join(c for c in phone if c.isdigit())[-10:]
                        record[field] = int(phone_digits) if phone_digits else random.randint(int(range_min), int(range_max))
                    else:
                        logger.error(f"Unsupported field type: {field_type} for field: {field}")
                        raise ValueError(f"Unsupported field type: {field_type}")
                except Exception as e:
                    logger.error(f"Error processing field {field}: {str(e)}")
                    raise ValueError(f"Error processing field {field}: {str(e)}")
            
            if data_type == "framingham" and "chd_risk" in schema:
                risk_score = 0
                if record.get("age", 0) > 50:
                    risk_score += 1
                if record.get("smoking", 0) == 1:
                    risk_score += 1
                if record.get("total_cholesterol", 0) > 240:
                    risk_score += 1
                if record.get("systolic_bp", 0) > 140:
                    risk_score += 1
                if record.get("diabetes", 0) == 1:
                    risk_score += 1
                record["chd_risk"] = 1 if risk_score >= 3 else 0
            
            data.append(record)
        
        state["output"] = data
        logger.info(f"Generated {len(data)} records for {data_type} in {time.time() - start_time:.2f}s")
        return state
    except Exception as e:
        logger.error(f"Error in generate_data: {str(e)}")
        raise

def build_graph():
    try:
        workflow = StateGraph(GraphState)
        workflow.add_node("generate", generate_data)
        workflow.set_entry_point("generate")
        workflow.set_finish_point("generate")
        return workflow.compile()
    except Exception as e:
        logger.error(f"Error building graph: {str(e)}")
        raise