import chromadb
from chromadb.config import Settings

class DocumentStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        # Initialize a persistent local Chroma client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or load our two primary collections
        self.style_collection = self.client.get_or_create_collection(
            name="video_styles",
            metadata={"description": "Visual treatments and tone guides"}
        )
        
        self.remotion_collection = self.client.get_or_create_collection(
            name="remotion_api",
            metadata={"description": "Remotion API reference snippets"}
        )

    def add_documents(self, collection_name: str, documents: list[str], metadatas: list[dict], ids: list[str]):
        """Helper to inject documents into the specified collection."""
        collection = self.client.get_collection(name=collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {len(documents)} documents to '{collection_name}'.")

    def query_documents(self, collection_name: str, query_text: str, n_results: int = 2):
        """Retrieve the most relevant context for the agents."""
        collection = self.client.get_collection(name=collection_name)
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

# Quick test initialization
if __name__ == "__main__":
    store = DocumentStore()
    print("ChromaDB initialized and collections are ready!")