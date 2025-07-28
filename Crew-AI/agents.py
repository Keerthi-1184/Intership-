# # from crewai import Agent
# # from local_model_tool import local_model_generate

# # # Assign models as per your list
# # RESEARCHER_MODEL = "llama3.2-vision:11b"   # big & detailed research
# # WRITER_MODEL = "qwen2.5-coder:0.5b"        # code-capable, good for structured writing

# # def researcher_tool(prompt):
# #     return local_model_generate(RESEARCHER_MODEL, prompt)

# # def writer_tool(prompt):
# #     return local_model_generate(WRITER_MODEL, prompt)

# # # Create a blog content researcher agent
# # blog_researcher = Agent(
# #     role='Blog Researcher',
# #     goal='Research and collect valuable insights on the topic {topic}',
# #     verbose=True,
# #     memory=True,
# #     backstory=(
# #         "An expert in AI, ML, and GenAI, known for breaking down complex topics into structured research summaries."
# #     ),
# #     tools=[]
# # )

# # # Create a blog writer agent
# # blog_writer = Agent(
# #     role='Blog Writer',
# #     goal='Write an engaging blog post on {topic} using insights from the researcher',
# #     verbose=True,
# #     memory=True,
# #     backstory=(
# #         "You turn technical insights into captivating blog posts that are clear, informative, and enjoyable to read."
# #     ),
# #     tools=[]
# # )


# import requests

# def blog_researcher(prompt, max_tokens=512):
#     url = "http://localhost:8000/models/llama3.2-vision:11b/generate"
#     response = requests.post(url, json={"prompt": prompt, "max_tokens": max_tokens})
#     response.raise_for_status()
#     return response.json().get("generated_text", "")

# def blog_writer(prompt, max_tokens=512):
#     url = "http://localhost:8000/models/qwen2.5-coder:0.5b/generate"
#     response = requests.post(url, json={"prompt": prompt, "max_tokens": max_tokens})
#     response.raise_for_status()
#     return response.json().get("generated_text", "")


from crewai import Agent

researcher = Agent(
    role="Researcher",
    goal="Summarize topic info",
    backstory="Expert at finding key points.",
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="Writer",
    goal="Write a short blog response",
    backstory="Skilled at concise content.",
    verbose=True,
    allow_delegation=False
)