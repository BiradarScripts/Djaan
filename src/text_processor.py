import re
import hashlib
import nltk
from nltk.corpus import wordnet

# Download wordnet for query expansion
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def clean_text(text: str) -> str:
    """Lowercase, remove extra spaces, remove HTML tags."""
    text = text.lower() # [cite: 25]
    text = re.sub(r'<[^>]+>', '', text) # Remove HTML [cite: 28]
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra spaces [cite: 27]
    return text

def generate_hash(text: str) -> str:
    """Generate SHA256 hash for cache lookup."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest() # [cite: 50]

def expand_query(query: str) -> str:
    """Bonus: Query expansion using WordNet synonyms."""
    words = query.split()
    expanded = set(words)
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name().replace('_', ' '))
    return " ".join(list(expanded))