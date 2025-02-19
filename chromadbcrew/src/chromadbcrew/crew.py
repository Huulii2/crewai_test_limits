from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from chromadbcrew.chromadb_knowledge_source import ChromaDBKnowledgeSource
from chromadbcrew.knowledge_loader import KnowledgeLoader


# # Initialize a persistent client pointing to the knowledge folder
# client = chromadb.PersistentClient(path="./knowledge/chromadb")

# # Create a collection
# collection = client.get_or_create_collection("knowledge_base")

# # Add sample documents
# collection.add(
#     ids=["doc1", "doc2"],
#     documents=["CrewAI is a framework for AI agent collaboration.",
#                "ChromaDB is a NoSQL vector database optimized for retrieval-augmented generation."]
# )




chroma_knowledge = ChromaDBKnowledgeSource(
    file_paths=["chromadb"],
)

knowledge_loader = KnowledgeLoader()
knowledge_list = knowledge_loader.load_knowledge()

@CrewBase
class Chromadbcrew():
	"""Chromadbcrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


	@agent
	def knowledge_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['knowledge_agent'],
			verbose=True,
			knowledge_sources=knowledge_list,#[chroma_knowledge],
				embedder={
					"provider": "ollama",  # Use Ollama as the embedding provider
					"config": {
					"model": "nomic-embed-text",  # Example embedding model for Ollama
						"api_key":"NA",
					}
				}
		)

	@task
	def knowledge_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['knowledge_agent_task'],
			output_file='outputs/report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Chromadbcrew crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
