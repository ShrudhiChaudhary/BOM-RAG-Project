import json
import os

index_dir = "vector_store"     # your folder
output_dir = "data_processed"  # final submission folder

os.makedirs(output_dir, exist_ok=True)

# ---- Load existing metadata ----
with open(os.path.join(index_dir, "metadatas.json"), "r", encoding="utf-8") as f:
    meta = json.load(f)

texts = meta["texts"]

# ---- 1. Create cleaned_text.json ----
cleaned_text = "\n\n".join(texts)

with open(os.path.join(output_dir, "cleaned_text.json"), "w", encoding="utf-8") as f:
    json.dump({"cleaned_text": cleaned_text}, f, indent=4, ensure_ascii=False)

print("✔ cleaned_text.json created!")


# ---- 2. Create chunks.json ----
chunks = []

for i, t in enumerate(texts):
    chunks.append({
        "id": i,
        "text": t
    })

with open(os.path.join(output_dir, "chunks.json"), "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4, ensure_ascii=False)

print("✔ chunks.json created!")


# ---- 3. Copy index.faiss and metadatas.json into data_processed ----
import shutil

shutil.copy(os.path.join(index_dir, "index.faiss"), os.path.join(output_dir, "index.faiss"))
shutil.copy(os.path.join(index_dir, "metadatas.json"), os.path.join(output_dir, "metadatas.json"))

print("✔ index.faiss & metadatas.json copied to data_processed/")
