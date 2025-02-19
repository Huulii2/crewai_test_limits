from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from memory_0.tools.json_tools import read_fruits_json, read_fruits_details_json, edit_fruits_json, edit_fruits_details_json
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# load_dotenv()
# llm = LLM(
#     model="openrouter/google/gemini-2.0-flash-exp:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPEN_ROUTER_API_KEY"),
# )
@CrewBase
class Memory0():
	"""Memory0 crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	
 
	#################################################
	# Entity memory testing
 
	# @agent	
	# def fruit_vendor(self) -> Agent:
	# 	json_source = JSONKnowledgeSource(
	# 		file_paths=["fruits.json"]
	# 	)
	# 	return Agent(
	# 		config=self.agents_config['fruit_vendor'],
	# 		verbose=True,
   	# 		memory=True,
	# 		knowledge_sources=[json_source],
  	# 		 embedder={
	# 			"provider": "ollama",  # Use Ollama as the embedding provider
	# 			"config": {
	# 				"model": "nomic-embed-text",  # Example embedding model for Ollama
    #  				"api_key":"NA",
	# 			}
	# 		}
	# 	)
  
	# @task
	# def fruit_vendor_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['fruit_vendor_task'],
	# 		output_file='outputs/report.md'
	# 	)
 
	#################################################
	# Knowledgebase testing

	@agent
	def json_manager(self) -> Agent:
		fruits_json = JSONKnowledgeSource(
			file_paths=["fruits.json"]
		)
		fruits_details_json = JSONKnowledgeSource(
			file_paths=["fruits_details.json"]
		)
		return Agent(
			config=self.agents_config['json_manager'],
			tools=[read_fruits_json,read_fruits_details_json,edit_fruits_json, edit_fruits_details_json],
			verbose=True,
			memory=True,
			# llm=llm,
			# knowledge_sources=[fruits_json, fruits_details_json],
			#  embedder={
			# 	"provider": "ollama",  # Use Ollama as the embedding provider
			# 	"config": {
			# 		"model": "nomic-embed-text",  # Example embedding model for Ollama
			# 		"api_key":"NA",
			# 	}
			# }
		)

	@task
	def json_manager_task(self) -> Task:
		return Task(
			config=self.tasks_config['json_manager_task'],
		)

	@agent
	def answering_agent(self) -> Agent:
		fruits_details_json = JSONKnowledgeSource(
			file_paths=["fruits_details.json"]
		)
		return Agent(
			config=self.agents_config['answering_agent'],
			verbose=True,
			memory=True,
			# llm=llm,
			knowledge_sources=[fruits_details_json],
			 embedder={
				"provider": "ollama",  # Use Ollama as the embedding provider
				"config": {
					"model": "nomic-embed-text",  # Example embedding model for Ollama
					"api_key":"NA",
				}
			}
		)

	@task
	def answering_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['answering_agent_task'],
			output_file='outputs/report.md'
		)

	#################################################


	@crew
	def crew(self) -> Crew:
		"""Creates the Memory0 crew"""

		#################################################
		# Entity memory testing
  
		# json_source = JSONKnowledgeSource(
		# 	file_paths=["fruits.json"]
		# )
  
		#################################################
		# Knowledgebase testing
  
		fruits_json = JSONKnowledgeSource(
			file_paths=["fruits_details.json"]
		)
  
		#################################################
  
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			memory=True,
			output_log_file="fuit_logs.txt",
			# llm=llm,
			#################################################
			# Entity memory testing
   
			# knowledge_sources=[json_source],
			# embedder={
			# 	"provider": "ollama",  # Use Ollama as the embedding provider
			# 	"config": {
			# 		"model": "nomic-embed-text",  # Example embedding model for Ollama
     		# 		"api_key":"NA",
			# 	}
			# }
			#################################################
			# Knowledgebase testing
   
			knowledge_sources=[fruits_json],
				embedder={
					"provider": "ollama",  # Use Ollama as the embedding provider
					"config": {
					"model": "nomic-embed-text",  # Example embedding model for Ollama
						"api_key":"NA",
					}
				}

			#################################################
   
			# planning=True,
			# planning_llm="groq/llama-3.3-70b-versatile",
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
