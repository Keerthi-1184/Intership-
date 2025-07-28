from langchain_community.llms.ollama import Ollama

def generate_hypotheses(topic, num_hypotheses=3):
    try:
        llm = Ollama(model="deepseek-r1:1.5b", base_url="http://localhost:11434")
        prompt = f"Generate {num_hypotheses} research hypotheses about {topic}. Provide each hypothesis as a single sentence, numbered, and focused on medical research."
        hypotheses = llm.invoke(prompt)
        # Parse to ensure numbered list
        lines = [line.strip() for line in hypotheses.split('\n') if line.strip().startswith(tuple(str(i) for i in range(1, num_hypotheses + 1)))]
        return lines[:num_hypotheses] or ["No hypotheses generated."]
    except Exception as e:
        print(f"Error generating hypotheses: {e}")
        return ["Error generating hypotheses."]