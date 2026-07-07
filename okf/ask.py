"""okf ask — LLM-powered Q&A over your knowledge bundle.

Asks a natural language question about your codebase. The bundle is searched
for relevant concepts, then sent as context to the configured LLM for an answer.

Requires an LLM provider configured in .okfconfig (llm.api_key, llm.base_url).

Usage:
  okf ask "how does the payment service work"
  okf ask "what dependencies does this project use" --bundle ./my_bundle
"""

import sys
from pathlib import Path

STOP_WORDS = {
    "how", "does", "do", "is", "are", "was", "were", "the", "a", "an",
    "in", "on", "at", "to", "for", "of", "with", "by", "and", "or",
    "it", "its", "what", "where", "when", "why", "which", "who", "that",
    "this", "these", "those", "i", "you", "we", "they", "he", "she",
    "me", "my", "your", "all", "can", "will", "would", "could", "should",
    "has", "have", "had", "been", "being", "am", "are", "was", "were",
    "get", "got", "find", "show", "list", "tell", "describe", "explain",
    "tell", "describe", "explain",
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(1 if len(sys.argv) < 2 else 0)

    bundle_dir = Path("okf_bundle").resolve()
    query_parts = []
    skip_next = False
    for i, a in enumerate(sys.argv[1:], 1):
        if skip_next:
            skip_next = False
            continue
        if a == "--bundle" and i + 1 < len(sys.argv):
            bundle_dir = Path(sys.argv[i + 1]).resolve()
            skip_next = True
        elif not a.startswith("-"):
            query_parts.append(a)

    if not query_parts:
        print("Please provide a question.", file=sys.stderr)
        sys.exit(1)

    if not bundle_dir.exists():
        print(f"Bundle not found: {bundle_dir}", file=sys.stderr)
        print("Generate one first: okf generate", file=sys.stderr)
        sys.exit(1)

    # Load config and LLM client
    from okf.config import load as load_config, _get
    cfg = load_config()
    api_key = _get(cfg, "llm.api_key", "")
    base_url = _get(cfg, "llm.base_url", "http://localhost:8080/v1")
    model = _get(cfg, "llm.model", "local-model")

    if not api_key:
        print("No LLM configured. Set llm.api_key in .okfconfig or OKF_API_KEY env.", file=sys.stderr)
        print("Without an LLM, use okf lookup instead for static search.", file=sys.stderr)
        sys.exit(1)

    # Search bundle for relevant concepts
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle_dir)
    tokens = [t for t in query_parts if t.lower() not in STOP_WORDS]
    if not tokens:
        tokens = query_parts[-3:]
    results = search(concepts, tokens=tokens, limit=8)

    if not results:
        print(f"No relevant concepts found for: {' '.join(query_parts)}")
        print("Try different keywords or check the bundle is up to date.")
        sys.exit(1)

    # Build context from concepts
    context_parts = []
    for c in results:
        sig = c.get("sections", {}).get("signature", "")
        desc = c.get("description", "")
        related = c.get("sections", {}).get("related", "")[:200]
        entry = f"--- {c['type']}: {c['title']} ---\nFile: {c.get('resource', '')}\nDescription: {desc}\nSignature: {sig}\nRelated: {related}"
        context_parts.append(entry)
    context = "\n\n".join(context_parts)

    # Ask LLM
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = f"""You are a codebase expert. Answer the user's question based on the code concepts below.

Context from the knowledge bundle:
{context}

Question: {' '.join(query_parts)}

Answer concisely based only on the context above. If the context doesn't contain enough information, say so."""
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.1,
        )
        answer = resp.choices[0].message.content or ""
    except Exception as e:
        print(f"LLM call failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n  Q: {' '.join(query_parts)}\n")
    print(answer)
    print(f"\nSources:")
    for i, c in enumerate(results, 1):
        desc = c.get("description", "")[:80]
        desc_str = f" — {desc}" if desc else ""
        print(f"  [{i}] {c['type']}: {c['title']}{desc_str}")
        print(f"      {c.get('resource', '')}")
    print(f"\n  Run okf lookup <Name> for full detail.")
