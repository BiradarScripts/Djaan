import faiss
import numpy as np
import os
from .config import FAISS_INDEX_PATH, EMBEDDING_DIM
from .cache_manager import CacheManager
from .embedder import Embedder
from .text_processor import expand_query

class SearchEngine:
    def __init__(self):
        self.embedder = Embedder()
        self.cache = CacheManager()
        self.index = None
        self.doc_map = {} # Maps FAISS index ID to real doc_id
        self.load_or_build_index()

    def load_or_build_index(self):
        """Loads FAISS index from disk or builds from DB."""
        # Trigger embedding update first
        self.embedder.process_documents()
        
        all_docs = self.cache.get_all_embeddings()
        if not all_docs:
            print("No documents found.")
            return

        # Prepare data for FAISS
        embeddings = np.array([d["embedding"] for d in all_docs])
        self.doc_map = {i: d for i, d in enumerate(all_docs)}
        
        # Normalize for Cosine Similarity (Inner Product on normalized vectors) [cite: 61, 64]
        faiss.normalize_L2(embeddings)
        
        self.index = faiss.IndexFlatIP(EMBEDDING_DIM) # [cite: 60]
        self.index.add(embeddings)
        
        # Persistence (Bonus) [cite: 101]
        os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, FAISS_INDEX_PATH)

    def search(self, query: str, top_k: int = 5, use_expansion: bool = False):
        # 1. Embed Query
        search_query = expand_query(query) if use_expansion else query
        query_vec = self.embedder.embed_query(search_query)
        faiss.normalize_L2(query_vec.reshape(1, -1))

        # 2. Search Vector Index
        distances, indices = self.index.search(query_vec.reshape(1, -1), top_k) # [cite: 79]

        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1: continue
            
            doc_data = self.doc_map[idx]
            score = float(distances[0][i])
            
            # 3. Ranking Explanation [cite: 93]
            explanation = self._generate_explanation(query, doc_data["text"], score)
            
            results.append({
                "doc_id": doc_data["doc_id"],
                "score": round(score, 4),
                "preview": doc_data["text"][:150] + "...",
                "explanation": explanation
            })
            
        return results

    def _generate_explanation(self, query, doc_text, score):
        """Generates reasoning for the result."""
        q_words = set(query.lower().split())
        d_words = set(doc_text.lower().split())
        overlap = q_words.intersection(d_words)
        
        return {
            "overlap_ratio": round(len(overlap) / len(q_words), 2) if q_words else 0, # [cite: 97]
            "common_words": list(overlap),
            "relevance_summary": f"High cosine similarity ({round(score, 2)}) with {len(overlap)} matching keywords."
        }