from typing import List
from pydantic import BaseModel
from crewai import Agent, Crew, Process
from crewai.task import Task
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from datetime import datetime
import os

# Define an output model to capture the research task output
class BulletPointOutput(BaseModel):
    bullet_points: List[str]

# Condition function for the conditional task
def needs_processing(output: TaskOutput) -> bool:
    lenght = len(output.pydantic.bullet_points)
    return lenght != 5  # Run only if there are more than 5 bullet points

@CrewBase
class Taskcrew:
    """Taskcrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    output_file = "outputs/blog_post.md"

    # Agent Definitions
    @agent
    def blog_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_researcher'],
            verbose=True
        )

    @agent
    def data_processor(self) -> Agent:
        return Agent(
            config=self.agents_config['data_processor'],
            verbose=True
        )

    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['blog_writer'],
            verbose=True
        )

    # Task Definitions
    @task
    def blog_researcher_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_researcher_task'],
            output_pydantic=BulletPointOutput,  # Capturing structured output
        )
        
        
    # Conditional Task: Runs only if the research output has more than 5 bullet points
    @task
    def data_processor_task(self) -> ConditionalTask:
        return ConditionalTask(
            config=self.tasks_config['data_processor_task'],
            condition=needs_processing,
        )

    @task
    def blog_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_writer_task'],
            output_file=self.output_file,
            human_input=True,
        )


    # Crew Definition
    @crew
    def crew(self) -> Crew:
        """Creates the Taskcrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
