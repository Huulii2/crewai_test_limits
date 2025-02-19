from pathlib import Path
from crewai.utilities.constants import KNOWLEDGE_DIRECTORY  # Import CrewAI's knowledge directory constant
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from chromadbcrew.chromadb_knowledge_source import ChromaDBKnowledgeSource
from typing import List

class KnowledgeLoader:
    """Dynamically loads knowledge sources from the CrewAI knowledge folder."""
    
    def __init__(self):
        # Automatically use CrewAI's default knowledge directory if no path is provided
        self.path = Path(KNOWLEDGE_DIRECTORY).resolve()
        self.knowledge_sources = []

    def load_knowledge(self) -> List:
        """Detects file types in the folder and loads appropriate knowledge sources."""
        
        if not self.path.exists() or not self.path.is_dir():
            raise ValueError(f"Path does not exist or is not a directory: {self.path}")

        for file in self.path.iterdir():
            full_path = file.resolve()  # Get absolute path

            if file.suffix == ".txt":
                knowledge_source = TextFileKnowledgeSource(file_paths=[file.name])
            elif file.suffix == ".pdf":
                knowledge_source = PDFKnowledgeSource(file_paths=[file.name])
            elif file.suffix == ".csv":
                knowledge_source = CSVKnowledgeSource(file_paths=[file.name])
            elif file.suffix == ".xlsx":
                knowledge_source = ExcelKnowledgeSource(file_paths=[file.name])
            elif file.suffix == ".json":
                knowledge_source = JSONKnowledgeSource(file_paths=[file.name])
            elif file.name.lower() == "chromadb" and file.is_dir():
                knowledge_source = ChromaDBKnowledgeSource(file_paths=[file.name])
                print(f"✅ ChromaDB database loaded from: {full_path}")
            else:
                print(f"⚠️ Skipping unsupported file type: {file.name}")
                continue

            self.knowledge_sources.append(knowledge_source)

        return self.knowledge_sources
