from crewai.knowledge.source.base_file_knowledge_source import BaseFileKnowledgeSource
import chromadb
from pathlib import Path
from typing import Dict, Any


class ChromaDBKnowledgeSource(BaseFileKnowledgeSource):
    """Knowledge source that fetches all data from a specified ChromaDB directory."""

    def load_content(self) -> Dict[Path, str]:
        """Loads data from ChromaDB located in the specified directory."""
        try:
            # Get the valid ChromaDB directory from file_paths
            chroma_db_path = self._get_chroma_db_path()

            if not chroma_db_path:
                raise FileNotFoundError("No valid ChromaDB directory found in file_paths.")

            # Connect to ChromaDB
            client = chromadb.PersistentClient(path=str(chroma_db_path))

            # Get all collections
            collections = client.list_collections()
            if not collections:
                raise ValueError("No collections found in ChromaDB.")

            formatted_data = ""

            for collection in collections:
                coll = client.get_collection(collection.name)

                # Retrieve all stored documents & metadata
                results = coll.get(include=["documents", "metadatas"])
                documents = results.get("documents", [])
                metadatas = results.get("metadatas", [None] * len(documents))  # Handle missing metadata

                formatted_data += self._format_results(collection.name, documents, metadatas)

            return {chroma_db_path: formatted_data}

        except Exception as e:
            raise ValueError(f"Failed to retrieve data from ChromaDB: {str(e)}")

    def _get_chroma_db_path(self) -> Path:
        """Extracts the ChromaDB directory from file_paths."""
        for path in self.safe_file_paths:
            if path.is_dir():
                return path  # Return the first valid directory
        return None  # No valid ChromaDB directory found

    def validate_content(self):
        """Validate the ChromaDB directory paths."""
        for path in self.safe_file_paths:
            if not path.exists():
                self._logger.log("error", f"Directory not found: {path}", color="red")
                raise FileNotFoundError(f"Directory not found: {path}")
            if not path.is_dir():
                self._logger.log("error", f"Path is not a directory: {path}", color="red")
                raise ValueError(f"Path is not a directory: {path}")

    def _format_results(self, collection_name: str, documents: list, metadatas: list) -> str:
        """Format ChromaDB results into readable text."""
        formatted = f"\nCollection: {collection_name}\n"
        formatted += "-" * 40 + "\n"

        for doc, meta in zip(documents, metadatas):
            metadata_str = f"Metadata: {meta}" if meta else "Metadata: None"
            formatted += f"- {doc}\n  {metadata_str}\n"

        return formatted

    def add(self) -> None:
        """Processes and stores the fetched ChromaDB records."""
        content = self.load_content()
        if not isinstance(content, dict):
            raise ValueError("Invalid content format retrieved from ChromaDB.")

        for _, text in content.items():
            chunks = self._chunk_text(text)
            self.chunks.extend(chunks)

        self._save_documents()
