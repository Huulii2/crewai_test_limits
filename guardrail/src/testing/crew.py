from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Tuple, Union, Dict, Any
from pydantic import BaseModel, Field
import json

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def validate_blog_content(result: str) -> Tuple[bool, Any]:
	"""Validate blog content meets requirements."""
	try:
		print("Validating blog content...")
		print("The variable, result is of type:", type(result))
		print("The variable, result description is of type:", type(result.description))
		print("The variable, result raw is of type:", type(result.raw))
		print("The variable, result agent is of type:", type(result.agent))
		
		blog= result.raw

		# Check word count
		word_count = len(blog.split())
		print("The variable, word_count is of type:", type(word_count), "and its value is:", word_count)
		if word_count > 150:
			return (False, json.dumps({
				"error": "Blog content exceeds 150 words",
				"code": "WORD_COUNT_ERROR",
				"context": {"word_count": word_count}
			}))

		# Additional validation logic here
		return (True, blog.strip())
	except Exception as e:
		return (False, json.dump({
			"error": "Unexpected error during validation",
			"code": "SYSTEM_ERROR"
		}))

class BlogValidationError(Exception):
    """Blog content error"""
    def __init__(self, message):
        super().__init__(message)


def validate_content(blog: str):
	print(blog)
	word_count = len(blog.split())
	print(word_count)
	if word_count > 150:
		raise BlogValidationError(json.dumps({
			"error": "Blog content exceeds 150 words",
			"code": "WORD_COUNT_ERROR",
			"context": {"word_count": word_count}
		}))
	return blog

def format_output(blog: str):
	data = json.loads(blog)
	return blog

def complex_validation(result: str) -> Tuple[bool, Any]:
	"""Chain multiple validation steps."""
	# Step 1: Basic validation
	if not result:
		return (False, json.dumps({
			"error": "Empty result",
			"code": "EMPTY_INPUT"
		}))

	# Step 2: Content validation
	blog = result.raw
	try:
		validated = validate_content(blog)
  
		# Step 3: Format validation
		formatted = format_output(validated)
		return (True, {"blog": formatted})
	except BlogValidationError as e:
		return (False, f"{e}")
	except json.JSONDecodeError as e:
		return (False, json.dumps({
			"error": "Invalid JSON format",
			"code": "JSON_ERROR",
			"context": {"line": e.lineno, "column": e.colno}
		}))

class BlogPost(BaseModel):
	Description: str = Field(contect="Blog post content")
 
@CrewBase
class Testing():
	"""Testing crew"""
 
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

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
			output_file='outputs/blog_post.json',
			guardrail=complex_validation,
			output_pydantic=BlogPost,
			max_retries=3 #default
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the Testing crew"""

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
