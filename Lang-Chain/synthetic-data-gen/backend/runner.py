# from graph import build_graph

# def run_test():
#     graph = build_graph()
#     test_cases = [
#         {
#             "data_type": "user",
#             "num_records": 3,
#             "parameters": {"age_min": 25, "age_max": 50}
#         },
#         {
#             "data_type": "product",
#             "num_records": 2,
#             "parameters": {
#                 "price_min": 50.0,
#                 "price_max": 500.0,
#                 "categories": ["Electronics", "Books"]
#             }
#         }
#     ]
    
#     for test_case in test_cases:
#         print(f"\nRunning test case: {test_case}")
#         result = graph.invoke(test_case)
#         print("Generated data:")
#         for record in result["output"]:
#             print(record)

# if __name__ == "__main__":
#     run_test()

from graph import build_graph

def run_test():
    graph = build_graph()
    test_cases = [
        {
            "data_type": "user",
            "num_records": 3,
            "parameters": {"age_min": 25, "age_max": 50, "locale": "en_US"}
        },
        {
            "data_type": "product",
            "num_records": 2,
            "parameters": {
                "price_min": 50.0,
                "price_max": 500.0,
                "categories": ["Electronics", "Books"],
                "locale": "de_DE"
            }
        },
        {
            "data_type": "custom",
            "num_records": 2,
            "parameters": {
                "schema": {"id": "uuid", "description": "text", "phone": "phone"},
                "locale": "fr_FR"
            },
            "query": "Generate 2 records with ids, descriptions, and phones"
        },
        {
            "data_type": "weather",
            "num_records": 1,
            "parameters": {"city": "Paris", "weather_api_key": "your_openweathermap_api_key"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\nRunning test case: {test_case}")
        result = graph.invoke(test_case)
        print("Generated data:")
        for record in result["output"]:
            print(record)

if __name__ == "__main__":
    run_test()
