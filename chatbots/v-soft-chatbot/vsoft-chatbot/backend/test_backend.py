import requests
import time

def test_backend():
    backend_url = "http://127.0.0.1:8000"
    endpoints = ["/health", "/query"]
    
    for endpoint in endpoints:
        try:
            url = backend_url + endpoint
            print(f"Testing {url}...")
            
            if endpoint == "/query":
                response = requests.post(url, json={"question": "Test connection"}, timeout=5)
            else:
                response = requests.get(url, timeout=5)
                
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}\n")
            
        except Exception as e:
            print(f"Error testing {endpoint}: {str(e)}\n")
            return False
    
    return True

if __name__ == "__main__":
    if test_backend():
        print("✅ Backend is working properly")
    else:
        print("❌ Backend connection failed")