"""
Chunking utility: split consolidated text into overlapping chunks and save metadata.
Usage:
  python chunker.py --input ../knowledge_base/loan_data.txt --out_json ../knowledge_base/chunks.json
"""
import json
import argparse
import os
import math

def chunk_text(text, chunk_size=800, overlap=200):
    tokens = text.split()
    chunks = []
    i = 0
    n = len(tokens)
    while i < n:
        chunk_tokens = tokens[i:i+chunk_size]
        chunk_text = " ".join(chunk_tokens)
        chunks.append(chunk_text)
        i += chunk_size - overlap
    return chunks

def main(input_path, out_json, chunk_size=300, overlap=60):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    data = [{"id": i, "text": c} for i,c in enumerate(chunks)]
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(data)} chunks to {out_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../knowledge_base/loan_data.txt")
    parser.add_argument("--out_json", default="../knowledge_base/chunks.json")
    parser.add_argument("--chunk_size", type=int, default=300)
    parser.add_argument("--overlap", type=int, default=60)
    args = parser.parse_args()
    main(args.input, args.out_json, args.chunk_size, args.overlap)
