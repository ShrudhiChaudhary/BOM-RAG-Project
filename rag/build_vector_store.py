"""
Builds FAISS vector store from chunks.json using sentence-transformers.
Output: vector_store/index.faiss and vector_store/metadatas.json
"""
import os
import json
import argparse
from sentence_transformers import SentenceTransformer
import numpy as np
try:
    import faiss
except Exception as e:
    raise ImportError("faiss library not found. Install faiss-cpu or faiss-gpu.") from e
from tqdm import tqdm

def load_chunks(chunks_json):
    with open(chunks_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def build_index(chunks_json, model_name="all-MiniLM-L6-v2", out_dir="../vector_store"):
    os.makedirs(out_dir, exist_ok=True)
    print("Loading chunks...")
    chunks = load_chunks(chunks_json)
    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]

    print("Loading embedder:", model_name)
    embedder = SentenceTransformer(model_name)
    embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True, batch_size=64)

    dim = embeddings.shape[1]
    print("Building FAISS index (dim=%d, n=%d)..." % (dim, len(embeddings)))
    index = faiss.IndexFlatIP(dim)
    # normalize for cosine
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    # Save index
    index_path = os.path.join(out_dir, "index.faiss")
    faiss.write_index(index, index_path)
    # Save metadatas
    metas = {"ids": ids, "texts": texts, "dim": dim}
    with open(os.path.join(out_dir, "metadatas.json"), "w", encoding="utf-8") as f:
        json.dump(metas, f, indent=2, ensure_ascii=False)
    print("Saved index to", index_path)
    return index_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", default="../knowledge_base/chunks.json")
    parser.add_argument("--out_dir", default="../vector_store")
    parser.add_argument("--model", default="all-MiniLM-L6-v2")
    args = parser.parse_args()
    build_index(args.chunks, args.model, args.out_dir)
