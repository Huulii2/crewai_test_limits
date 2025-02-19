from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.tools.math_tool import multiplication_tool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Tools():
	"""Tools crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=True,
			tools=[multiplication_tool],
		)

	@task
	def writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['writer_task'],
			output_file='outputs/homework.md',
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Tools crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			output_log_file="C:/melo/cyex/crewai_test_limits/tool/outputs/log.txt",
			step_callback=lambda step_output: print(f"Step output: {step_output.__dict__}"),
			task_callback=lambda task_output: print(f"Task output: {task_output}"),
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
