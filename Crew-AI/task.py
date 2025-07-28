# from agents import blog_researcher, blog_writer

# def get_tasks(topic):
#     research_task = {
#         "description": f"Research in depth about: {topic}",
#         "expected_output": f"Detailed notes about {topic}",
#         "agent_func": blog_researcher
#     }

#     write_task = {
#         "description": f"Write a blog post about {topic} based on the research",
#         "expected_output": f"Complete blog post on {topic}",
#         "agent_func": blog_writer,
#         "output_file": "blog_output.md"
#     }

#     return [research_task, write_task]


from crewai import Task
from agents import researcher, writer

def research_task(topic):
    return Task(
        description=f"Research {topic}. Use simulated data: {topic.capitalize()} is a significant topic with cultural or natural importance.",
        expected_output="Key points summary.",
        agent=researcher
    )

def writing_task(topic):
    return Task(
        description=f"Write a 50-word blog on {topic} using research.",
        expected_output="A 50-word blog response.",
        agent=writer
    )