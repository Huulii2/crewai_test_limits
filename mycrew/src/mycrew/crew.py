from crewai import Agent, Crew, Process, Task
from crewai.crews.crew_output import CrewOutput
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from typing import Optional, Dict, Any
from datetime import datetime
import os

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Mycrew():
	"""Mycrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	output_file = "outputs/blog_post.md"
 
	@before_kickoff
	def validate_inputs(self, inputs: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
		"""Validate and preprocess inputs before the crew starts."""
		if inputs is None:
			return None
			
		if 'topic' not in inputs:
			raise ValueError("Topic is required")
		
		# Add additional context
		inputs['timestamp'] = datetime.now().isoformat()
		inputs['topic'] = inputs['topic'].strip().lower()
		return inputs

	@agent
	def blog_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['blog_writer'],
			verbose=True
		)

	@task
	def blog_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['blog_writer_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Mycrew crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			output_log_file="C:/melo/cyex/crewai_test_limits/mycrew/outputs/log.txt",
			step_callback=lambda step_output: print(f"Step output: {step_output.__dict__}"),
			task_callback=lambda task_output: print(f"Task output: {task_output}"),
		)

	@after_kickoff
	def process_results(self, result):
		"""Modify output after task execution and save to file"""
		modified_output = f"""# Research Results\nGenerated on: {datetime.now().isoformat()}\n\n{result}"""

		with open(self.output_file, "w", encoding="utf-8") as file:
			file.write(modified_output)

		return modified_output
