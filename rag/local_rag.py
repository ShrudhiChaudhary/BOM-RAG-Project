import os
import json
import faiss
import requests
from sentence_transformers import SentenceTransformer


class LocalRAG:
    def __init__(self, index_dir="vector_store", model="phi3"):
        self.model = model

        # Embedding model
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load metadata
        with open(os.path.join(index_dir, "metadatas.json"), "r", encoding="utf-8") as f:
            self.meta = json.load(f)

        # Load FAISS index
        self.index = faiss.read_index(os.path.join(index_dir, "index.faiss"))

    # --------------------------
    # EMBEDDINGS
    # --------------------------
    def _embed(self, texts):
        emb = self.embed_model.encode(texts, convert_to_numpy=True)
        faiss.normalize_L2(emb)
        return emb

    # --------------------------
    # RETRIEVAL
    # --------------------------
    def retrieve(self, question, top_k=3):
        q_emb = self._embed([question])
        D, I = self.index.search(q_emb, top_k)

        results = []
        for idx in I[0]:
            if idx >= 0:
                results.append({
                    "id": idx,
                    "text": self.meta["texts"][idx]
                })

        return results

    # --------------------------
    # PROMPT CREATION
    # --------------------------
    def build_prompt(self, question, contexts):
        ctx_text = "\n\n".join([f"[Chunk {c['id']}]\n{c['text']}" for c in contexts])

        prompt = f"""
Use ONLY the context below to answer the question.
If the answer is not available in the context, say "Not available in documents."

### CONTEXT:
{ctx_text}

### QUESTION:
{question}

### ANSWER:
"""
        return prompt.strip()

    # --------------------------
    # LLM CALL (Ollama)
    # --------------------------
    def call_llm(self, prompt):
        url = "http://localhost:11434/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,

            # ⚡ FAST & CLEAN OUTPUT
            "options": {
                "num_ctx": 1200,        # Larger context window
                "temperature": 0.2,     # Cleaner output
                "top_k": 40,            
                "top_p": 0.8,
                "repeat_penalty": 1.1
            }
        }

        r = requests.post(url, json=payload)
        data = r.json()

        if "response" in data:
            return data["response"]
        else:
            return str(data)

    # --------------------------
    # FULL PIPELINE
    # --------------------------
    def answer(self, query):
        contexts = self.retrieve(query, top_k=3)
        prompt = self.build_prompt(query, contexts)
        response = self.call_llm(prompt)

        return response, contexts
