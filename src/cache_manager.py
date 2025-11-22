import sqlite3
import json
import numpy as np
import os
from datetime import datetime
from .config import DB_PATH

class CacheManager:
    def __init__(self):
        # FIX: Ensure the directory exists before connecting
        db_folder = os.path.dirname(DB_PATH)
        if db_folder:
            os.makedirs(db_folder, exist_ok=True)

        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            filename TEXT,
            doc_hash TEXT,
            embedding BLOB,
            text_content TEXT,
            updated_at TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def get_document(self, filename):
        cursor = self.conn.execute("SELECT doc_hash, embedding, text_content FROM documents WHERE filename = ?", (filename,))
        return cursor.fetchone()

    def upsert_document(self, doc_id, filename, doc_hash, embedding, text_content):
        # Store embedding as bytes
        embedding_bytes = embedding.tobytes()
        updated_at = datetime.now().isoformat()
        
        query = """
        INSERT OR REPLACE INTO documents (doc_id, filename, doc_hash, embedding, text_content, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (doc_id, filename, doc_hash, embedding_bytes, text_content, updated_at))
        self.conn.commit()

    def get_all_embeddings(self):
        """Retrieve all for FAISS index building."""
        cursor = self.conn.execute("SELECT doc_id, embedding, text_content FROM documents")
        results = []
        for doc_id, emb_blob, text in cursor.fetchall():
            emb = np.frombuffer(emb_blob, dtype=np.float32)
            results.append({"doc_id": doc_id, "embedding": emb, "text": text})
        return results