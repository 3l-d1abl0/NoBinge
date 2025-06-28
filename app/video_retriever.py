import logging
from pathlib import Path
from typing import List, Tuple
from logger import logger
from llama_index.core.schema import ImageNode

class VideoRetriever:
    
    def __init__(self, index):
        self.index = index
        self.logger = logger
        self.retriever_engine = self.index.as_retriever(
            similarity_top_k=5, image_similarity_top_k=5
        )

    def retrieve(self, query_str: str) -> Tuple[List[Path], List[str]]:
        try:
            self.logger.info(f"Processing query: {query_str}")
            retrieval_results = self.retriever_engine.retrieve(query_str)

            retrieved_images = []
            retrieved_texts = []

            for result in retrieval_results:
                if isinstance(result.node, ImageNode):
                    retrieved_images.append(Path(result.node.metadata["file_path"]))
                else:
                    #print("retrieval_texts: ", result.text)
                    retrieved_texts.append(result.text)

            self.logger.info(
                f"Retrieved {len(retrieved_images)} images and {len(retrieved_texts)} text segments"
            )

            return retrieved_images, retrieved_texts

        except Exception as e:
            self.logger.error(f"Error during retrieval: {str(e)}")
            raise
