import os
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import MODEL_NAME, DATA_DIR
from .text_processor import clean_text, generate_hash
from .cache_manager import CacheManager

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.cache = CacheManager()

    def process_documents(self):
        """Reads files, checks cache, generates embeddings if needed."""
        files = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]
        
      
        
        processed_count = 0
        for filename in files:
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
                raw_text = f.read()
            
            cleaned_text = clean_text(raw_text)
            current_hash = generate_hash(cleaned_text)
            doc_id = filename.split('.')[0]

            cached_data = self.cache.get_document(filename)
            
            if cached_data:
                stored_hash, _, _ = cached_data
                if stored_hash == current_hash:
                    continue 

            embedding = self.model.encode(cleaned_text).astype(np.float32)
            
            self.cache.upsert_document(doc_id, filename, current_hash, embedding, cleaned_text)
            processed_count += 1
            
        print(f"Processed and updated {processed_count} documents.")

    def embed_query(self, query):
        return self.model.encode(query).astype(np.float32)