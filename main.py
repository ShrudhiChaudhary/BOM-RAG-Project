import argparse
from rag.local_rag import LocalRAG

def main(index_dir="vector_store"):
    print("Starting local RAG using Ollama...")
    rag = LocalRAG(index_dir=index_dir, model="phi3")

    while True:
        q = input("\n> ")
        if q.lower() in ("exit", "quit"):
            break

        answer, ctx = rag.answer(q)

        print("\n--- ANSWER ---\n")
        print(answer)

        print("\n--- SOURCES ---")
        for c in ctx:
            print(f"[{c['id']}] {c['text'][:200]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--index_dir", default="vector_store")
    args = parser.parse_args()
    main(args.index_dir)
