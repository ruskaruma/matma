import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from scripts.reranker import rerank

# Load model
model_name = "HuggingFaceH4/zephyr-7b-beta"  # or one of the open-access options
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto", use_auth_token=True)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Token budget for context passages
MAX_CONTEXT_TOKENS = 1024

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text, add_special_tokens=False))

def generate_answer(query: str, passages: list):
    # Extract passage texts
    texts = [doc["text"] for doc in passages]

    # Rerank top 3
    reranked = rerank(query, texts, top_k=3)

    # Build context with token limit
    context = ""
    token_count = 0
    sources = []

    for passage, score in reranked:
        t = count_tokens(passage)
        if token_count + t > MAX_CONTEXT_TOKENS:
            break
        context += passage + "\n"
        token_count += t
        sources.append(passage)

    prompt = f"Context:\n{context}\n\nAnswer the question: {query}"

    output = generator(prompt, max_new_tokens=256, do_sample=True, temperature=0.7)[0]["generated_text"]
    answer = output.split("Answer the question:")[1].strip() if "Answer the question:" in output else output.strip()

    return {
        "query": query,
        "answer": answer,
        "sources": sources
    }
