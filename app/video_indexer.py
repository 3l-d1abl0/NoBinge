from pathlib import Path
from logger import logger
from config import get_envs
import qdrant_client
from llama_index.core import load_index_from_storage
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore


class VideoIndexer:
    
    def __init__(self, embed_model: str, indexing_path: str):
        self.embed_model = embed_model
        self.indexing_path = indexing_path
        self.logger = logger
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=get_envs().embed_model
        )
        self.client = None
        
    def create_multimodal_index(self, filename_no_extenstion: str, frames_directory: Path, session_subtitle_file: Path):

        try:
            self.logger.info("Creating new multimodal index...")
            
            #Connect to Qdrant
            self.client = qdrant_client.QdrantClient(path=self.indexing_path )

            #vector store for text
            text_store = QdrantVectorStore(
                client = self.client, collection_name=f"text_{filename_no_extenstion}"
            )
            #vector store for images
            image_store = QdrantVectorStore(
                client=self.client, collection_name=f"image_{filename_no_extenstion}"
            )

            # Create storage context
            storage_context = StorageContext.from_defaults(
                vector_store=text_store, image_store=image_store
            )

            self.logger.info("STORAGE_CONTEXT: ")
            self.logger.info(storage_context)
            from llama_index.core.schema import Document, ImageDocument
            
            # Create a minimal document for initialization
            #documents = [Document(text="placeholder")]
            documents = SimpleDirectoryReader(str(frames_directory)).load_data()
            # Create index
            index = MultiModalVectorStoreIndex.from_documents(
                documents=documents,
                storage_context=storage_context,
            )

            self.logger.info("Successfully created multimodal index")
            return index

        except Exception as e:
            self.logger.error(f"Failed to create multimodal index: {str(e)}")
            raise

    def get_multimodal_index(self, filename_no_extension: str) -> MultiModalVectorStoreIndex | None:
        """
        Check if a multimodal index exists for the given filename, and return it if it does.
        
        Args:
            filename_no_extension: The filename without extension to check for existing index
            
        Returns:
            MultiModalVectorStoreIndex if found, None otherwise
        """
        try:
            self.logger.info(f"Checking if multimodal index exists for {filename_no_extension}...")
            
            # Connect to Qdrant if not already connected
            if self.client is None:
                self.client = qdrant_client.QdrantClient(path=self.indexing_path)

            # Check if the collections exist
            text_collection_name = f"text_{filename_no_extension}"
            image_collection_name = f"image_{filename_no_extension}"
            
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            
            if text_collection_name in collection_names and image_collection_name in collection_names:
                self.logger.info(f"Found existing multimodal index for {filename_no_extension}")
                
                # Create vector stores from existing collections
                text_store = QdrantVectorStore(
                    client=self.client, collection_name=text_collection_name
                )
                image_store = QdrantVectorStore(
                    client=self.client, collection_name=image_collection_name
                )
                
                # Create storage context
                storage_context = StorageContext.from_defaults(
                    vector_store=text_store, image_store=image_store
                )
                

                self.logger.info("STORAGE CONTEXT: ", storage_context)
                # Load the index from the existing storage
                # index = MultiModalVectorStoreIndex.from_vector_store(
                #     vector_store=text_store,
                #     image_vector_store=image_store,
                #     storage_context=storage_context
                # )
                
                index = MultiModalVectorStoreIndex.from_documents(
                    vector_store=text_store,
                    image_vector_store=image_store,
                )

                return index
            else:
                self.logger.info(f"No existing multimodal index found for {filename_no_extension}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error checking for existing multimodal index: {str(e)}")
            return None