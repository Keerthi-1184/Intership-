# def chunk_text(text, max_chunk_size=1000):
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + max_chunk_size
#         chunks.append(text[start:end])
#         start = end
#     return chunks

# def summarize_text(text, model_name):
#     prompt = f"Summarize the following text briefly:\n\n{text}"
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant that summarizes text."},
#         {"role": "user", "content": prompt}
#     ]
#     summary = query_model(model_name, messages)
#     return summary

# def summarize_overall(text, model_name):
#     chunks = chunk_text(text)
#     chunk_summaries = []
#     for chunk in chunks:
#         chunk_summary = summarize_text(chunk, model_name)
#         chunk_summaries.append(chunk_summary)
#     combined_summary = " ".join(chunk_summaries)
#     overall_summary = summarize_text(combined_summary, model_name)
#     return overall_summary

# def query_model(model_name, messages):
#     # Your existing logic to send messages to llama3.2-vision:11b and get reply
#     # Placeholder example (replace with actual llama3 model call)
#     last_user_message = ""
#     for msg in reversed(messages):
#         if msg.get("role") == "user":
#             last_user_message = msg.get("content", "")
#             break

#     return f"[Simulated {model_name} reply] {last_user_message}"


import requests

def query_model(model_name, messages):
    # Customize based on your local model API
    endpoint = "http://localhost:11434/api/generate"  # Example for Ollama

    payload = {
        "model": model_name,
        "prompt": "\n".join([msg['content'] for msg in messages]),
        "stream": False
    }

    response = requests.post(endpoint, json=payload, timeout=600)

    if response.status_code == 200:
        data = response.json()
        return data.get("response", "")
    else:
        raise RuntimeError(f"Model call failed: {response.status_code} - {response.text}")

