# from crewai import Crew, Process
# from agents import blog_researcher, blog_writer
# from task import get_tasks

# topic = input("Enter a topic to generate a blog about: ")

# tasks = get_tasks(topic)

# crew = Crew(
#     agents=[blog_researcher, blog_writer],
#     tasks=tasks,
#     process=Process.sequential,
#     memory=True,
#     cache=True,
#     max_rpm=100,
#     share_crew=True
# )

# result = crew.kickoff()
# print(result)


from crewai import Crew, Process
from agents import researcher, writer
from task import research_task, writing_task

def main():
    topic = input("Enter topic: ")
    
    # Create tasks
    research = research_task(topic)
    writing = writing_task(topic)
    writing.context = [research]  # Pass research output to writing task

    # Create crew with sequential process
    crew = Crew(
        agents=[researcher, writer],  # Extract agents from tasks
        tasks=[research, writing],
        verbose=1,
        process=Process.sequential
    )
    
    # Run crew and print result
    print("\nOutput:", crew.kickoff())

if __name__ == "__main__":
    main()