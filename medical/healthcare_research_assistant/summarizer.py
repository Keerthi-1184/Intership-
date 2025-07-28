# from transformers import pipeline

# # Load summarization pipeline once
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# def summarize_text(text, max_length=130, min_length=30):
#     try:
#         summary_list = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
#         return summary_list[0]['summary_text']
#     except Exception as e:
#         return "Summary failed: " + str(e)

from langchain_community.llms.ollama import Ollama

def summarize_text(text, max_length=150, min_length=50):
    if not text or len(text.strip()) < 50:
        return "Text too short or empty."
    
    try:
        llm = Ollama(model="deepseek-r1:1.5b", base_url="http://localhost:11434")
        prompt = f"Summarize the following text in exactly 2 or 3 sentences, no more, no less:\n{text}"
        summary = llm.invoke(prompt)
        # Post-process to ensure 2-3 sentences
        sentences = [s.strip() for s in summary.split('.') if s.strip()]
        if len(sentences) > 3:
            summary = '. '.join(sentences[:3]) + '.'
        elif len(sentences) < 2:
            summary = summary + " No additional details provided."
        return summary
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Summary unavailable."