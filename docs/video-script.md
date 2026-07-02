# okf-generator — Demo Video Script

**Format:** 60-90s screencast  
**Tone:** Professional, fast-paced, developer-focused  
**Music:** Lo-fi / electronic background

---

## 0. Thumbnail (w/ AI image generator)

**Prompt for Midjourney / DALL-E:**
> A futuristic developer workspace split in two halves. Left side: messy code files scattered everywhere. Right side: neat glowing folders arranged in a knowledge graph. A glowing purple arrow transforms chaos into order. Neon purple and cyan colors, dark theme, tech aesthetic. Text overlay: "Index your codebase for AI agents."

---

## 1. Hook (0-5s)

**Visual:** Terminal window, typing starts

```bash
# The problem:
# AI agents keep re-reading your entire codebase.
# One lookup is faster than one grep.
```

**VO:** "AI agents waste context re-reading your whole codebase. One command fixes that."

---

## 2. Generate (5-20s)

**Visual:** Real terminal recording

```bash
okf generate ./project ./okf_bundle
```

**Show output:** scanning files, progress bar, final summary (Classes, Functions, Dependencies)

**VO:** "Index your entire project — Python, TypeScript, Go, Rust, Java, Ruby, C, C++, C#, SQL — all at once."

---

## 3. Lookup (20-35s)

**Visual:** 
```bash
okf lookup PaymentService
```

**Show output:** full concept detail — type, signature, methods, calls, called-by, dependencies

**VO:** "Now your AI agent can look up any class or function instantly. Signature, docstring, parameters — even what calls it and what it calls."

---

## 4. Dependencies (35-45s)

**Visual:**
```bash
okf lookup --deps
okf lookup --tag ecosystem:pip
```

**Show output:** compact list of dependencies

**VO:** "Dependencies from requirements.txt, package.json, Cargo.lock, go.mod, and 15 other manifest formats — all searchable in milliseconds."

---

## 5. Visualize (45-55s)

**Visual:** Screen recording of the HTML explorer
- Click a concept in the tree → detail panel shows
- Hover the ego graph → neighbors highlighted
- Toggle light/dark theme

**VO:** "Generate an interactive HTML explorer. Tree navigation, local dependency graphs, clickable cross-references — no server required."

---

## 6. Serve (55-65s)

**Visual:**
```bash
okf serve ./okf_bundle --open
```

**Show output:** browser opens, viz.html loads automatically

**VO:** "Share with your team. `okf serve` launches a local server and auto-opens the visualization."

---

## 7. Diff (65-72s)

**Visual:**
```bash
# Before a PR
okf diff ./okf_bundle.bak ./okf_bundle --compact
```

**Show output:** Added 3 concepts, Removed 1, Changed 2

**VO:** "See what changed between bundles. Useful for PR reviews and release notes."

---

## 8. Install + Close (72-85s)

**Visual:**
```bash
pip install okf-generator
okf install all
```

**Show output:** installing for Claude Code, Cursor, Copilot, Windsurf, Cline, OpenCode

**VO:** "Install once, integrate with every AI coding agent. Pip install, generate your bundle, and your agent has the full picture."

**Final frame:** Banner + `okf-generator` + star count box

**VO:** "okf-generator — the knowledge layer for AI coding agents."
