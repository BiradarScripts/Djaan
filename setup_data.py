import os
from sklearn.datasets import fetch_20newsgroups

def download_data():
    # Download only a subset to keep it lightweight (100-200 docs)
    print("Downloading 20 Newsgroups dataset...")
    newsgroups = fetch_20newsgroups(subset='train', categories=['sci.space', 'comp.graphics'], remove=('headers', 'footers', 'quotes'))
    
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Save first 200 documents
    for i, text in enumerate(newsgroups.data[:200]):
        filename = os.path.join(data_dir, f"doc_{i:03d}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
            
    print(f"Saved {min(len(newsgroups.data), 200)} documents to {data_dir}")

if __name__ == "__main__":
    download_data()