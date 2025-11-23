import re
import hashlib
import nltk
from nltk.corpus import wordnet

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def clean_text(text: str) -> str:
    """Lowercase, remove extra spaces, remove HTML tags."""
    text = text.lower() 
    text = re.sub(r'<[^>]+>', '', text) 
    text = re.sub(r'\s+', ' ', text).strip() 
    return text

def generate_hash(text: str) -> str:
    """Generate SHA256 hash for cache lookup."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest() 

def expand_query(query: str) -> str:
    """Bonus: Query expansion using WordNet synonyms."""
    words = query.split()
    expanded = set(words)
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name().replace('_', ' '))
    return " ".join(list(expanded))