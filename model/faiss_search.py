#Code for  model/faiss_search.py

import faiss
import numpy as np
import json
import os

class FaissSearchEngine:
    def __init__(self, index_path: str, metadata_path: str):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found at {metadata_path}")

        self.index=faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = [json.loads(line) for line in f]

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        """
        Search using query embedding and return top-k matched metadata.
        """
        if query_embedding.ndim==1:
            query_embedding=query_embedding.reshape(1, -1)
        scores, indices=self.index.search(query_embedding, top_k)
        results=[]

        for i, idx in enumerate(indices[0]):
            if idx<len(self.metadata):
                item=self.metadata[idx]
                item['score']=float(scores[0][i])
                results.append(item)

        return results
