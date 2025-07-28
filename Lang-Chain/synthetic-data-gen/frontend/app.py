# import streamlit as st
# import requests
# import json
# import pandas as pd

# st.title("Synthetic Data Generator")

# data_type = st.selectbox("Select Data Type", ["user", "product"])
# num_records = st.slider("Number of Records", 1, 100, 10)

# if data_type == "user":
#     age_min = st.number_input("Minimum Age", 18, 100, 18)
#     age_max = st.number_input("Maximum Age", 18, 100, 80)
#     parameters = {"age_min": age_min, "age_max": age_max}
# elif data_type == "product":
#     price_min = st.number_input("Minimum Price", 0.0, 10000.0, 10.0)
#     price_max = st.number_input("Maximum Price", 0.0, 10000.0, 1000.0)
#     categories = st.multiselect("Categories", ["Electronics", "Clothing", "Home", "Books"], ["Electronics", "Clothing"])
#     parameters = {"price_min": price_min, "price_max": price_max, "categories": categories}

# if st.button("Generate Data"):
#     try:
#         response = requests.post(
#             "http://localhost:8000/generate",
#             json={"data_type": data_type, "num_records": num_records, "parameters": parameters}
#         )
#         response.raise_for_status()
#         data = response.json()["data"]
        
#         st.write("Generated Data:")
#         df = pd.DataFrame(data)
#         st.dataframe(df)
        
#         st.download_button(
#             label="Download as JSON",
#             data=json.dumps(data, indent=2),
#             file_name="synthetic_data.json",
#             mime="application/json"
#         )
#     except requests.RequestException as e:
#         st.error(f"Error: {str(e)}")



# import streamlit as st
# import requests
# import json
# import pandas as pd
# import sqlite3
# import uuid

# st.set_page_config(page_title="Synthetic Data Generator", layout="wide")

# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Generate Data", "Analytics", "History"])

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# if page == "Generate Data":
#     st.title("Synthetic Data Generator")
    
#     query = st.text_input("Enter a query (e.g., 'Generate 10 employee records with names and phones')")
#     data_type = st.selectbox("Or select Data Type", ["user", "product", "custom", "weather"])
#     num_records = st.slider("Number of Records", 1, 100, 10)
#     locale = st.selectbox("Select Language", ["en_US", "fr_FR", "de_DE", "es_ES"], index=0)
#     export_format = st.selectbox("Export Format", ["json", "csv"])
    
#     parameters = {"locale": locale, "format": export_format}
    
#     if data_type == "user":
#         age_min = st.number_input("Minimum Age", 18, 100, 18)
#         age_max = st.number_input("Maximum Age", 18, 100, 80)
#         parameters.update({"age_min": age_min, "age_max": age_max})
#     elif data_type == "product":
#         price_min = st.number_input("Minimum Price", 0.0, 10000.0, 10.0)
#         price_max = st.number_input("Maximum Price", 0.0, 10000.0, 1000.0)
#         categories = st.multiselect("Categories", ["Electronics", "Clothing", "Home", "Books"], ["Electronics", "Clothing"])
#         parameters.update({"price_min": price_min, "price_max": price_max, "categories": categories})
#     elif data_type == "custom":
#         schema_input = st.text_area("Enter JSON Schema", '{"field_name": "field_type"}')
#         try:
#             schema = json.loads(schema_input)
#             parameters["schema"] = schema
#         except json.JSONDecodeError:
#             st.error("Invalid JSON schema")
#     elif data_type == "weather":
#         city = st.text_input("Enter City", "London")
#         weather_api_key = st.text_input("OpenWeatherMap API Key", type="password")
#         parameters.update({"city": city, "weather_api_key": weather_api_key})
    
#     if st.button("Generate Data"):
#         try:
#             response = requests.post(
#                 "http://localhost:8000/generate",
#                 json={
#                     "data_type": data_type,
#                     "num_records": num_records,
#                     "parameters": parameters,
#                     "query": query,
#                     "session_id": st.session_state.session_id
#                 }
#             )
#             response.raise_for_status()
#             if export_format == "csv":
#                 st.download_button(
#                     label="Download as CSV",
#                     data=response.content,
#                     file_name="synthetic_data.csv",
#                     mime="text/csv"
#                 )
#             else:
#                 data = response.json()["data"]
#                 df = pd.DataFrame(data)
#                 st.write("Edit Generated Data")
#                 edited_df = st.data_editor(df)
#                 st.download_button(
#                     label="Download Edited Data as JSON",
#                     data=edited_df.to_json(orient="records", indent=2),
#                     file_name="synthetic_data.json",
#                     mime="application/json"
#                 )
#         except requests.RequestException as e:
#             st.error(f"Error: {str(e)}")

# elif page == "Analytics":
#     st.title("Usage Analytics")
#     try:
#         conn = sqlite3.connect("usage.db")
#         df = pd.read_sql_query("SELECT * FROM logs", conn)
#         conn.close()
#         st.dataframe(df)
#         chart_data = df.groupby("data_type")["num_records"].sum().reset_index()
#         st.bar_chart(chart_data.set_index("data_type"))
#     except Exception as e:
#         st.error(f"Error loading analytics: {str(e)}")

# elif page == "History":
#     st.title("Generation History")
#     try:
#         response = requests.get(f"http://localhost:8000/history?session_id={st.session_state.session_id}")
#         response.raise_for_status()
#         history = response.json()["history"]
#         for i, data in enumerate(history):
#             st.write(f"Dataset {i+1}")
#             st.dataframe(pd.DataFrame(data))
#     except requests.RequestException as e:
#         st.error(f"Error loading history: {str(e)}")


# import streamlit as st
# import requests
# import json
# import pandas as pd
# import sqlite3
# import uuid
# import logging
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # Set up logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# st.set_page_config(page_title="Synthetic Data Generator", layout="wide")

# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Generate Data", "Analytics", "History"])

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# API_BASE_URL = "http://localhost:8080"

# session = requests.Session()
# retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
# session.mount("http://", HTTPAdapter(max_retries=retries))

# if page == "Generate Data":
#     st.title("Synthetic Data Generator")
    
#     api_key = st.text_input("API Key", type="password", value="user-key-456")
#     headers = {"X-API-Key": api_key} if api_key else {}
    
#     query = st.text_input("Enter a query (e.g., 'Generate 10 employee records with names and phones')")
#     data_type = st.selectbox("Data Type", ["custom"])
#     num_records = st.slider("Number of Records", 1, 100, 10)
#     locale = st.selectbox("Select Language", ["en_US", "fr_FR", "de_DE", "es_ES"], index=0)
#     export_format = st.selectbox("Export Format", ["json", "csv"])
#     export_to_db = st.checkbox("Export to Database")
#     table_name = st.text_input("Table Name", "generated_data") if export_to_db else None
    
#     parameters = {"locale": locale, "format": export_format}
#     if export_to_db:
#         parameters["table_name"] = table_name
    
#     if data_type == "custom":
#         schema_input = st.text_area("Enter JSON Schema", '{"name": "name", "phone": "phone"}')
#         try:
#             schema = json.loads(schema_input)
#             parameters["schema"] = schema
#         except json.JSONDecodeError:
#             st.error("Invalid JSON schema")
    
#     if st.button("Generate Data"):
#         try:
#             with st.spinner("Generating data..."):
#                 endpoint = "/export_db" if export_to_db else "/generate"
#                 logger.info(f"Sending request to {API_BASE_URL}{endpoint} with headers {headers}, data_type: {data_type}, num_records: {num_records}")
#                 response = session.post(
#                     f"{API_BASE_URL}{endpoint}",
#                     json={
#                         "data_type": data_type,
#                         "num_records": num_records,
#                         "parameters": parameters,
#                         "query": query,
#                         "session_id": st.session_state.session_id
#                     },
#                     headers=headers,
#                     timeout=10
#                 )
#                 response.raise_for_status()
#                 logger.info(f"Received response: {response.status_code}")
#                 if export_to_db:
#                     st.success(response.json()["status"])
#                 elif export_format == "csv":
#                     st.download_button(
#                         label="Download as CSV",
#                         data=response.content,
#                         file_name="synthetic_data.csv",
#                         mime="text/csv"
#                     )
#                 else:
#                     data = response.json()["data"]
#                     df = pd.DataFrame(data)
#                     st.write("Generated Data")
#                     st.dataframe(df)
#                     st.download_button(
#                         label="Download as JSON",
#                         data=df.to_json(orient="records", indent=2),
#                         file_name="synthetic_data.json",
#                         mime="application/json"
#                     )
#         except requests.RequestException as e:
#             logger.error(f"Error in Generate Data: {str(e)}")
#             st.error(f"Error: {str(e)}")

# elif page == "Analytics":
#     st.title("Usage Analytics")
#     api_key = st.text_input("API Key (Admin Only)", type="password", value="admin-key-123")
#     headers = {"X-API-Key": api_key} if api_key else {}
#     try:
#         logger.info(f"Sending request to {API_BASE_URL}/analytics with headers {headers}")
#         response = session.get(f"{API_BASE_URL}/analytics", headers=headers, timeout=10)
#         response.raise_for_status()
#         logs = response.json()["logs"]
#         logger.info(f"Received analytics logs: {len(logs)} entries")
#         df = pd.DataFrame(logs)
#         st.dataframe(df)
#         if not df.empty:
#             chart_data = df.groupby("data_type")["num_records"].sum().reset_index()
#             st.bar_chart(chart_data.set_index("data_type"))
#         else:
#             st.write("No analytics data available. Generate some data first.")
#     except requests.RequestException as e:
#         logger.error(f"Error in Analytics: {str(e)}")
#         st.error(f"Error loading analytics: {str(e)}")

# elif page == "History":
#     st.title("Generation History")
#     api_key = st.text_input("API Key (Admin Only)", type="password", value="admin-key-123")
#     headers = {"X-API-Key": api_key} if api_key else {}
#     try:
#         logger.info(f"Sending request to {API_BASE_URL}/history?session_id={st.session_state.session_id}")
#         response = session.get(
#             f"{API_BASE_URL}/history?session_id={st.session_state.session_id}",
#             headers=headers,
#             timeout=10
#         )
#         response.raise_for_status()
#         history = response.json()["history"]
#         logger.info(f"Received history: {len(history)} datasets")
#         for i, data in enumerate(history):
#             st.write(f"Dataset {i+1}")
#             st.dataframe(pd.DataFrame(data))
#     except requests.RequestException as e:
#         logger.error(f"Error in History: {str(e)}")
#         st.error(f"Error loading history: {str(e)}")



# import streamlit as st
# import requests
# import json
# import pandas as pd
# import sqlite3
# import uuid
# import logging
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# st.set_page_config(page_title="Synthetic Data Generator", layout="wide")

# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to", ["Generate Data", "Analytics", "History"])

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# if "chat_state" not in st.session_state:
#     st.session_state.chat_state = {
#         "step": "start",
#         "api_key": "",
#         "data_type": "",
#         "num_records": 0,
#         "schema": {},
#         "current_field": "",
#         "fields_needed": 0,
#         "current_field_num": 0,
#         "messages": [{"role": "assistant", "content": "Welcome! Please enter your API key to start."}]
#     }

# API_BASE_URL = "http://localhost:8080"

# session = requests.Session()
# retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
# session.mount("http://", HTTPAdapter(max_retries=retries))

# if page == "Generate Data":
#     st.title("Synthetic Data Generator Chatbot")

#     for msg in st.session_state.chat_state["messages"]:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     if user_input := st.chat_input("Type your message..."):
#         st.session_state.chat_state["messages"].append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.write(user_input)
        
#         with st.chat_message("assistant"):
#             if st.session_state.chat_state["step"] == "start":
#                 st.session_state.chat_state["api_key"] = user_input
#                 st.session_state.chat_state["step"] = "choose_dataset"
#                 response = "API key received. Choose a dataset (framingham, credit_card_fraud, diabetes, customer) or type 'custom' for a new dataset."
            
#             elif st.session_state.chat_state["step"] == "choose_dataset":
#                 st.session_state.chat_state["data_type"] = user_input.lower()
#                 if st.session_state.chat_state["data_type"] in ["framingham", "credit_card_fraud", "diabetes", "customer"]:
#                     schemas = {
#                         "framingham": {
#                             "age": {"type": "integer", "min": 30, "max": 80},
#                             "sex": {"type": "integer", "min": 0, "max": 1},
#                             "total_cholesterol": {"type": "integer", "min": 150, "max": 300},
#                             "hdl_cholesterol": {"type": "integer", "min": 20, "max": 100},
#                             "systolic_bp": {"type": "integer", "min": 90, "max": 180},
#                             "diastolic_bp": {"type": "integer", "min": 60, "max": 110},
#                             "smoking": {"type": "binary", "min": 0, "max": 1},
#                             "diabetes": {"type": "binary", "min": 0, "max": 1},
#                             "chd_risk": {"type": "binary", "min": 0, "max": 1}
#                         },
#                         "credit_card_fraud": {
#                             "transaction_id": {"type": "integer", "min": 1, "max": 1000000},
#                             "amount": {"type": "number", "min": 0, "max": 5000},
#                             "time": {"type": "integer", "min": 0, "max": 86400},
#                             "v1": {"type": "number", "min": -5, "max": 5},
#                             "v2": {"type": "number", "min": -5, "max": 5},
#                             "v3": {"type": "number", "min": -5, "max": 5},
#                             "v4": {"type": "number", "min": -5, "max": 5},
#                             "merchant_category": {"type": "integer", "min": 0, "max": 4},
#                             "fraud": {"type": "binary", "min": 0, "max": 1}
#                         },
#                         "diabetes": {
#                             "pregnancies": {"type": "integer", "min": 0, "max": 15},
#                             "glucose": {"type": "integer", "min": 50, "max": 200},
#                             "blood_pressure": {"type": "integer", "min": 50, "max": 120},
#                             "skin_thickness": {"type": "integer", "min": 0, "max": 50},
#                             "insulin": {"type": "integer", "min": 0, "max": 300},
#                             "bmi": {"type": "number", "min": 15, "max": 50},
#                             "age": {"type": "integer", "min": 20, "max": 80},
#                             "diabetes": {"type": "binary", "min": 0, "max": 1}
#                         },
#                         "customer": {
#                             "customer_id": {"type": "integer", "min": 1, "max": 100000},
#                             "name_id": {"type": "name", "min": 1001, "max": 999999},
#                             "email_id": {"type": "email", "min": 100000, "max": 999999},
#                             "phone": {"type": "phone", "min": 1000000000, "max": 9999999999},
#                             "age": {"type": "integer", "min": 18, "max": 80},
#                             "purchase_amount": {"type": "number", "min": 0, "max": 1000}
#                         }
#                     }
#                     st.session_state.chat_state["schema"] = schemas[st.session_state.chat_state["data_type"]]
#                     st.session_state.chat_state["step"] = "num_records"
#                     response = f"Selected {st.session_state.chat_state['data_type']}. How many records do you want to generate?"
#                 elif st.session_state.chat_state["data_type"] == "custom":
#                     st.session_state.chat_state["step"] = "num_fields"
#                     response = "Creating a custom dataset. How many fields do you want?"
#                 else:
#                     response = "Invalid dataset. Choose 'framingham', 'credit_card_fraud', 'diabetes', 'customer', or 'custom'."
            
#             elif st.session_state.chat_state["step"] == "num_records":
#                 try:
#                     st.session_state.chat_state["num_records"] = int(user_input)
#                     if st.session_state.chat_state["num_records"] < 1:
#                         raise ValueError
#                     st.session_state.chat_state["step"] = "export_options"
#                     response = "Export to database? Type 'yes' or 'no'."
#                 except ValueError:
#                     response = "Please enter a positive integer for the number of records."
            
#             elif st.session_state.chat_state["step"] == "export_options":
#                 export_to_db = user_input.lower() == "yes"
#                 export_format = "json"
#                 try:
#                     with st.spinner("Generating data..."):
#                         endpoint = "/export_db" if export_to_db else "/generate"
#                         payload = {
#                             "data_type": st.session_state.chat_state["data_type"],
#                             "num_records": st.session_state.chat_state["num_records"],
#                             "parameters": {
#                                 "locale": "en_US",
#                                 "format": export_format,
#                                 "schema": st.session_state.chat_state["schema"]
#                             },
#                             "session_id": st.session_state.session_id
#                         }
#                         headers = {"X-API-Key": st.session_state.chat_state["api_key"]}
#                         logger.info(f"Sending request to {API_BASE_URL}{endpoint} with payload: {json.dumps(payload)}")
#                         response_api = session.post(
#                             f"{API_BASE_URL}{endpoint}",
#                             json=payload,
#                             headers=headers,
#                             timeout=30
#                         )
#                         response_api.raise_for_status()
#                         logger.info(f"Received response: {response_api.status_code}")
                        
#                         if export_to_db:
#                             st.success(response_api.json().get("status"))
#                         else:
#                             data = response_api.json()["data"]
#                             df = pd.DataFrame(data)
#                             st.write("Generated Data")
#                             st.dataframe(df)
#                             st.download_button(
#                                 label="Download as JSON",
#                                 data=df.to_json(orient="records", indent=2),
#                                 file_name=f"{st.session_state.chat_state['data_type']}.json",
#                                 mime="application/json"
#                             )
                        
#                         conn = sqlite3.connect("data.db")
#                         try:
#                             df = pd.read_sql_query(f"SELECT * FROM {st.session_state.chat_state['data_type']}", conn)
#                             st.write("Data in Database")
#                             st.dataframe(df)
#                         except:
#                             st.write("No data found in database for this dataset.")
#                         conn.close()
                        
#                         conn = sqlite3.connect("mappings.db")
#                         try:
#                             df = pd.read_sql_query(
#                                 f"SELECT field_name, original_value, numerical_id FROM mappings WHERE data_type = ?",
#                                 conn,
#                                 params=(st.session_state.chat_state["data_type"],)
#                             )
#                             st.write("Name/Email Mappings")
#                             st.dataframe(df)
#                         except:
#                             st.write("No mappings found.")
#                         conn.close()
                        
#                         st.session_state.chat_state["step"] = "start"
#                         st.session_state.chat_state["schema"] = {}
#                         st.session_state.chat_state["messages"] = [{"role": "assistant", "content": "Data generated! Enter your API key to start again."}]
#                         response = "Data generated! Enter your API key to start again."
                
#                 except requests.RequestException as e:
#                     logger.error(f"Error in Generate Data: {str(e)}")
#                     response = f"Error: {str(e)}"
            
#             elif st.session_state.chat_state["step"] == "num_fields":
#                 try:
#                     st.session_state.chat_state["fields_needed"] = int(user_input)
#                     if st.session_state.chat_state["fields_needed"] < 1:
#                         raise ValueError
#                     st.session_state.chat_state["step"] = "field_name"
#                     st.session_state.chat_state["current_field_num"] = 1
#                     response = f"Field 1: What's the field name?"
#                 except ValueError:
#                     response = "Please enter a positive integer for the number of fields."
            
#             elif st.session_state.chat_state["step"] == "field_name":
#                 st.session_state.chat_state["current_field"] = user_input
#                 st.session_state.chat_state["step"] = "field_type"
#                 response = f"Field '{st.session_state.chat_state['current_field']}': Choose type (integer, number, binary, name, email, phone)."
            
#             elif st.session_state.chat_state["step"] == "field_type":
#                 if user_input.lower() in ["integer", "number", "binary", "name", "email", "phone"]:
#                     st.session_state.chat_state["schema"][st.session_state.chat_state["current_field"]] = {"type": user_input.lower()}
#                     st.session_state.chat_state["step"] = "field_range"
#                     response = f"Field '{st.session_state.chat_state['current_field']}': Enter range (e.g., '0,100' for min,max)."
#                 else:
#                     response = "Invalid type. Choose 'integer', 'number', 'binary', 'name', 'email', or 'phone'."
            
#             elif st.session_state.chat_state["step"] == "field_range":
#                 try:
#                     min_val, max_val = map(float, user_input.split(","))
#                     if min_val >= max_val:
#                         raise ValueError
#                     st.session_state.chat_state["schema"][st.session_state.chat_state["current_field"]]["min"] = min_val
#                     st.session_state.chat_state["schema"][st.session_state.chat_state["current_field"]]["max"] = max_val
                    
#                     st.session_state.chat_state["current_field_num"] += 1
#                     if st.session_state.chat_state["current_field_num"] > st.session_state.chat_state["fields_needed"]:
#                         st.session_state.chat_state["step"] = "num_records"
#                         response = f"Schema defined: {json.dumps(st.session_state.chat_state['schema'], indent=2)}. How many records do you want to generate?"
#                     else:
#                         st.session_state.chat_state["step"] = "field_name"
#                         response = f"Field {st.session_state.chat_state['current_field_num']}: What's the field name?"
#                 except ValueError:
#                     response = "Invalid range. Enter min,max (e.g., '0,100')."
            
#             st.session_state.chat_state["messages"].append({"role": "assistant", "content": response})
#             st.write(response)

# elif page == "Analytics":
#     st.title("Usage Analytics")
#     api_key = st.text_input("API Key (Admin Only)", type="password", value="admin-key-123")
#     headers = {"X-API-Key": api_key} if api_key else {}
#     try:
#         logger.info(f"Sending request to {API_BASE_URL}/analytics with headers {headers}")
#         response = session.get(f"{API_BASE_URL}/analytics", headers=headers, timeout=10)
#         response.raise_for_status()
#         logs = response.json()["logs"]
#         logger.info(f"Received analytics logs: {len(logs)} entries")
#         df = pd.DataFrame(logs)
#         st.dataframe(df)
#         if not df.empty:
#             chart_data = df.groupby("data_type")["num_records"].sum().reset_index()
#             st.bar_chart(chart_data.set_index("data_type"))
#         else:
#             st.write("No analytics data available. Generate some data first.")
#     except requests.RequestException as e:
#         logger.error(f"Error in Analytics: {str(e)}")
#         st.error(f"Error loading analytics: {str(e)}")

# elif page == "History":
#     st.title("Generation History")
#     api_key = st.text_input("API Key (Admin Only)", type="password", value="admin-key-123")
#     headers = {"X-API-Key": api_key} if api_key else {}
#     try:
#         logger.info(f"Sending request to {API_BASE_URL}/history?session_id={st.session_state.session_id}")
#         response = session.get(
#             f"{API_BASE_URL}/history?session_id={st.session_state.session_id}",
#             headers=headers,
#             timeout=10
#         )
#         response.raise_for_status()
#         history = response.json()["history"]
#         logger.info(f"Received history: {len(history)} datasets")
#         for i, data in enumerate(history):
#             st.write(f"Dataset {i+1}")
#             st.dataframe(pd.DataFrame(data))
#     except requests.RequestException as e:
#         logger.error(f"Error in History: {str(e)}")
#         st.error(f"Error loading history: {str(e)}")


import streamlit as st
import requests
import json
import pandas as pd
import sqlite3
import uuid
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Synthetic Data Generator", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Generate Data", "Analytics", "History"])

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_state" not in st.session_state:
    st.session_state.chat_state = {
        "step": "start",
        "api_key": "",
        "data_type": "",
        "num_records": 0,
        "schema": {},
        "current_field": "",
        "fields_needed": 0,
        "current_field_num": 0,
        "messages": [{"role": "assistant", "content": "Welcome! Please enter your API key to start."}]
    }

API_BASE_URL = "http://localhost:8080"

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))

if page == "Generate Data":
    st.title("Synthetic Data Generator Chatbot")

    for msg in st.session_state.chat_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Type your message..."):
        st.session_state.chat_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            if st.session_state.chat_state["step"] == "start":
                st.session_state.chat_state["api_key"] = user_input
                st.session_state.chat_state["step"] = "choose_dataset"
                response = "API key received. Choose a dataset (framingham, credit_card_fraud, diabetes, customer) or type 'custom' for a new dataset."
            
            elif st.session_state.chat_state["step"] == "choose_dataset":
                st.session_state.chat_state["data_type"] = user_input.lower()
                if st.session_state.chat_state["data_type"] in ["framingham", "credit_card_fraud", "diabetes", "customer"]:
                    schemas = {
                        "framingham": {
                            "age": {"type": "integer", "min": 30, "max": 80},
                            "sex": {"type": "integer", "min": 0, "max": 1},
                            "total_cholesterol": {"type": "integer", "min": 150, "max": 300},
                            "hdl_cholesterol": {"type": "integer", "min": 20, "max": 100},
                            "systolic_bp": {"type": "integer", "min": 90, "max": 180},
                            "diastolic_bp": {"type": "integer", "min": 60, "max": 110},
                            "smoking": {"type": "binary", "min": 0, "max": 1},
                            "diabetes": {"type": "binary", "min": 0, "max": 1},
                            "chd_risk": {"type": "binary", "min": 0, "max": 1}
                        },
                        "credit_card_fraud": {
                            "transaction_id": {"type": "integer", "min": 1, "max": 1000000},
                            "amount": {"type": "number", "min": 0, "max": 5000},
                            "time": {"type": "integer", "min": 0, "max": 86400},
                            "v1": {"type": "number", "min": -5, "max": 5},
                            "v2": {"type": "number", "min": -5, "max": 5},
                            "v3": {"type": "number", "min": -5, "max": 5},
                            "v4": {"type": "number", "min": -5, "max": 5},
                            "merchant_category": {"type": "integer", "min": 0, "max": 4},
                            "fraud": {"type": "binary", "min": 0, "max": 1}
                        },
                        "diabetes": {
                            "pregnancies": {"type": "integer", "min": 0, "max": 15},
                            "glucose": {"type": "integer", "min": 50, "max": 200},
                            "blood_pressure": {"type": "integer", "min": 50, "max": 120},
                            "skin_thickness": {"type": "integer", "min": 0, "max": 50},
                            "insulin": {"type": "integer", "min": 0, "max": 300},
                            "bmi": {"type": "number", "min": 15, "max": 50},
                            "age": {"type": "integer", "min": 20, "max": 80},
                            "diabetes": {"type": "binary", "min": 0, "max": 1}
                        },
                        "customer": {
                            "customer_id": {"type": "integer", "min": 1, "max": 100000},
                            "name": {"type": "name"},
                            "email": {"type": "email"},
                            "phone": {"type": "phone", "min": 1000000000, "max": 9999999999},
                            "age": {"type": "integer", "min": 18, "max": 80},
                            "purchase_amount": {"type": "number", "min": 0, "max": 1000}
                        }
                    }
                    st.session_state.chat_state["schema"] = schemas[st.session_state.chat_state["data_type"]]
                    st.session_state.chat_state["step"] = "num_records"
                    response = f"Selected {st.session_state.chat_state['data_type']}. How many records do you want to generate?"
                elif st.session_state.chat_state["data_type"] == "custom":
                    st.session_state.chat_state["step"] = "num_fields"
                    response = "Creating a custom dataset. How many fields do you want?"
                else:
                    response = "Invalid dataset. Choose 'framingham', 'credit_card_fraud', 'diabetes', 'customer', or 'custom'."
            
            elif st.session_state.chat_state["step"] == "num_records":
                try:
                    st.session_state.chat_state["num_records"] = int(user_input)
                    if st.session_state.chat_state["num_records"] < 1:
                        raise ValueError
                    st.session_state.chat_state["step"] = "export_options"
                    response = "Export to database? Type 'yes' or 'no'."
                except ValueError:
                    response = "Please enter a positive integer for the number of records."
            
            elif st.session_state.chat_state["step"] == "export_options":
                export_to_db = user_input.lower() == "yes"
                export_format = "json"
                try:
                    with st.spinner("Generating data..."):
                        endpoint = "/export_db" if export_to_db else "/generate"
                        payload = {
                            "data_type": st.session_state.chat_state["data_type"],
                            "num_records": st.session_state.chat_state["num_records"],
                            "parameters": {
                                "locale": "en_US",
                                "format": export_format,
                                "schema": st.session_state.chat_state["schema"]
                            },
                            "session_id": st.session_state.session_id
                        }
                        headers = {"X-API-Key": st.session_state.chat_state["api_key"]}
                        logger.info(f"Sending request to {API_BASE_URL}{endpoint} with payload: {json.dumps(payload)}")
                        response_api = session.post(
                            f"{API_BASE_URL}{endpoint}",
                            json=payload,
                            headers=headers,
                            timeout=30
                        )
                        response_api.raise_for_status()
                        logger.info(f"Received response: {response_api.status_code}")
                        
                        if export_to_db:
                            st.success(response_api.json().get("status"))
                        else:
                            data = response_api.json()["data"]
                            df = pd.DataFrame(data)
                            st.write("Generated Data")
                            st.dataframe(df)
                            st.download_button(
                                label="Download as JSON",
                                data=df.to_json(orient="records", indent=2),
                                file_name=f"{st.session_state.chat_state['data_type']}.json",
                                mime="application/json"
                            )
                        
                        conn = sqlite3.connect("data.db")
                        try:
                            df = pd.read_sql_query(f"SELECT * FROM {st.session_state.chat_state['data_type']}", conn)
                            st.write("Data in Database")
                            st.dataframe(df)
                        except:
                            st.write("No data found in database for this dataset.")
                        conn.close()
                        
                        st.session_state.chat_state["step"] = "start"
                        st.session_state.chat_state["schema"] = {}
                        st.session_state.chat_state["messages"] = [{"role": "assistant", "content": "Data generated! Enter your API key to start again."}]
                        response = "Data generated! Enter your API key to start again."
                
                except requests.RequestException as e:
                    logger.error(f"Error in Generate Data: {str(e)}")
                    response = f"Error: {str(e)}"
            
            elif st.session_state.chat_state["step"] == "num_fields":
                try:
                    st.session_state.chat_state["fields_needed"] = int(user_input)
                    if st.session_state.chat_state["fields_needed"] < 1:
                        raise ValueError
                    st.session_state.chat_state["step"] = "field_name"
                    st.session_state.chat_state["current_field_num"] = 1
                    response = f"Field 1: What's the field name?"
                except ValueError:
                    response = "Please enter a positive integer for the number of fields."
            
            elif st.session_state.chat_state["step"] == "field_name":
                st.session_state.chat_state["current_field"] = user_input
                st.session_state.chat_state["step"] = "field_type"
                response = f"Field '{st.session_state.chat_state['current_field']}': Choose type (integer, number, binary, name, email, phone)."
            
            elif st.session_state.chat_state["step"] == "field_type":
                if user_input.lower() in ["integer", "number", "binary", "name", "email", "phone"]:
                    st.session_state.chat_state["schema"][st.session_state.chat_state["current_field"]] = {"type": user_input.lower()}
                    if user_input.lower() in ["integer", "number", "binary", "phone"]:
                        st.session_state.chat_state["step"] = "field_range"
                        response = f"Field '{st.session_state.chat_state['current_field']}': Enter range (e.g., '0,100' for min,max)."
                    else:
                        st.session_state.chat_state["current_field_num"] += 1
                        if st.session_state.chat_state["current_field_num"] > st.session_state.chat_state["fields_needed"]:
                            st.session_state.chat_state["step"] = "num_records"
                            response = f"Schema defined: {json.dumps(st.session_state.chat_state['schema'], indent=2)}. How many records do you want to generate?"
                        else:
                            st.session_state.chat_state["step"] = "field_name"
                            response = f"Field {st.session_state.chat_state['current_field_num']}: What's the field name?"
                else:
                    response = "Invalid type. Choose 'integer', 'number', 'binary', 'name', 'email', or 'phone'."
            
            elif st.session_state.chat_state["step"] == "field_range":
                try:
                    min_val, max_val = map(float, user_input.split(","))
                    if min_val >= max_val:
                        raise ValueError
                    st.session_state.chat_state["schema"][st.session_state.chat_state["current_field"]]["min"] = min_val
                    st.session_state.chat_state["schema"][st.session_state.chat_state["current_field"]]["max"] = max_val
                    
                    st.session_state.chat_state["current_field_num"] += 1
                    if st.session_state.chat_state["current_field_num"] > st.session_state.chat_state["fields_needed"]:
                        st.session_state.chat_state["step"] = "num_records"
                        response = f"Schema defined: {json.dumps(st.session_state.chat_state['schema'], indent=2)}. How many records do you want to generate?"
                    else:
                        st.session_state.chat_state["step"] = "field_name"
                        response = f"Field {st.session_state.chat_state['current_field_num']}: What's the field name?"
                except ValueError:
                    response = "Invalid range. Enter min,max (e.g., '0,100')."
            
            st.session_state.chat_state["messages"].append({"role": "assistant", "content": response})
            st.write(response)

elif page == "Analytics":
    st.title("Usage Analytics")
    api_key = st.text_input("API Key (Admin Only)", type="password", value="admin-key-123")
    headers = {"X-API-Key": api_key} if api_key else {}
    try:
        logger.info(f"Sending request to {API_BASE_URL}/analytics with headers {headers}")
        response = session.get(f"{API_BASE_URL}/analytics", headers=headers, timeout=10)
        response.raise_for_status()
        logs = response.json()["logs"]
        logger.info(f"Received analytics logs: {len(logs)} entries")
        df = pd.DataFrame(logs)
        st.dataframe(df)
        if not df.empty:
            chart_data = df.groupby("data_type")["num_records"].sum().reset_index()
            st.bar_chart(chart_data.set_index("data_type"))
        else:
            st.write("No analytics data available. Generate some data first.")
    except requests.RequestException as e:
        logger.error(f"Error in Analytics: {str(e)}")
        st.error(f"Error loading analytics: {str(e)}")

elif page == "History":
    st.title("Generation History")
    api_key = st.text_input("API Key (Admin Only)", type="password", value="admin-key-123")
    headers = {"X-API-Key": api_key} if api_key else {}
    try:
        logger.info(f"Sending request to {API_BASE_URL}/history?session_id={st.session_state.session_id}")
        response = session.get(
            f"{API_BASE_URL}/history?session_id={st.session_state.session_id}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        history = response.json()["history"]
        logger.info(f"Received history: {len(history)} datasets")
        for i, data in enumerate(history):
            st.write(f"Dataset {i+1}")
            st.dataframe(pd.DataFrame(data))
    except requests.RequestException as e:
        logger.error(f"Error in History: {str(e)}")
        st.error(f"Error loading history: {str(e)}")