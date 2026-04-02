import streamlit as st
import tempfile
import os
import time
import sys                                          
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))  # ← add this

st.set_page_config(
    page_title="Finance Analyst",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:         #f5f0e8;
    --bg2:        #ede7db;
    --surface:    #faf8f4;
    --border:     #d6cfc3;
    --border2:    #c4bbb0;
    --muted:      #a09080;
    --soft:       #6e6050;
    --text:       #2c2318;
    --accent:     #5c7a4e;
    --accent-lt:  #eaf2e6;
    --accent-bd:  #b8d4b0;
    --amber:      #8b5e2e;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header, [data-testid="stSidebar"],
[data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    padding: 0 1.5rem 5rem !important;
    max-width: 760px !important;
    margin: 0 auto !important;
}

/* ════════════════════════════════
   HEADER
════════════════════════════════ */
.site-header {
    padding: 3.5rem 0 2rem;
    text-align: center;
    border-bottom: 2px solid var(--border2);
    margin-bottom: 3.5rem;
}
.site-title {
    font-family: 'Lora', serif;
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.site-title span {
    color: var(--accent);
}
.site-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 1.15rem;
    font-weight: 400;
    color: var(--soft);
    margin-top: 0.8rem;
    line-height: 1.6;
    letter-spacing: 0.01em;
}

/* ════════════════════════════════
   FIELD LABELS
════════════════════════════════ */
.field-label {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--soft);
    margin-bottom: 0.7rem;
    letter-spacing: 0.01em;
}

/* ════════════════════════════════
   UPLOAD ZONE
════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2.5px dashed var(--border2) !important;
    border-radius: 14px !important;
    padding: 3rem 2rem !important;
    transition: border-color 0.2s, background 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    background: #f7fbf5 !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] > div > label {
    display: none !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div > span {
    font-size: 1.15rem !important;
    color: var(--soft) !important;
    font-weight: 400 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzoneInstructions"] div > small {
    font-size: 0.88rem !important;
    color: var(--muted) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] button,
[data-testid="stFileUploader"] button {
    font-size: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--accent) !important;
    background: var(--accent-lt) !important;
    border: 1px solid var(--accent-bd) !important;
    border-radius: 6px !important;
    padding: 0.4rem 1rem !important;
}

/* ════════════════════════════════
   FILE META
════════════════════════════════ */
.file-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--soft);
    margin: 0.7rem 0 0.4rem;
    background: var(--bg2);
    border-radius: 6px;
    padding: 0.4rem 0.8rem;
    display: inline-block;
}

/* ════════════════════════════════
   BUTTONS
════════════════════════════════ */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 1.8rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    letter-spacing: 0.01em !important;
    transition: background 0.15s, transform 0.1s !important;
    box-shadow: 0 2px 8px rgba(92,122,78,0.18) !important;
}
.stButton > button:hover {
    background: #4a6840 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ════════════════════════════════
   DOC PILL
════════════════════════════════ */
.doc-pill {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-left: 5px solid var(--accent);
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.doc-pill-name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
}
.doc-pill-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 0.25rem;
}
.doc-pill-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    background: var(--accent-lt);
    color: var(--accent);
    padding: 0.25rem 0.7rem;
    border-radius: 99px;
    border: 1px solid var(--accent-bd);
    letter-spacing: 0.06em;
    white-space: nowrap;
}

/* ════════════════════════════════
   QUESTION INPUT
════════════════════════════════ */
.stTextInput > div > div > input {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    padding: 0.9rem 1.1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(92,122,78,0.12) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--muted) !important;
    font-size: 1rem !important;
}
.stTextInput label { display: none !important; }

/* ════════════════════════════════
   ANSWER CARD
════════════════════════════════ */
.answer-wrap { margin-top: 2.2rem; }
.answer-q {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1.25rem;
    color: var(--soft);
    margin-bottom: 0.9rem;
    line-height: 1.5;
}
.answer-body {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-top: 4px solid var(--accent);
    border-radius: 0 0 12px 12px;
    padding: 1.6rem 1.8rem;
    font-size: 1.05rem;
    line-height: 1.9;
    color: var(--text);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.answer-footer {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.page-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    background: var(--accent-lt);
    color: var(--accent);
    border: 1px solid var(--accent-bd);
    border-radius: 5px;
    padding: 0.22rem 0.6rem;
}
.elapsed {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    margin-left: auto;
}
.history-sep {
    border: none;
    border-top: 1.5px solid var(--border);
    margin: 2.5rem 0;
}

/* ════════════════════════════════
   EXPANDER
════════════════════════════════ */
[data-testid="stExpander"] summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    letter-spacing: 0.04em !important;
}
.excerpt-item {
    border-bottom: 1px solid var(--border);
    padding: 0.75rem 0;
    font-size: 0.9rem;
    color: var(--soft);
    line-height: 1.7;
}
.excerpt-item:last-child { border-bottom: none; }
.excerpt-pg {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--accent);
    margin-bottom: 0.3rem;
    font-weight: 500;
}

/* ════════════════════════════════
   EMPTY STATE / HINTS
════════════════════════════════ */
.empty {
    text-align: center;
    padding: 3rem 0 1rem;
}
.empty-text {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: var(--muted);
}
.hint-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-top: 1.6rem;
    text-align: left;
}
.hint {
    font-size: 0.9rem;
    color: var(--soft);
    font-family: 'Inter', sans-serif;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 0.65rem 0.9rem;
    background: var(--surface);
    line-height: 1.4;
}

/* ════════════════════════════════
   PROGRESS + SPINNER
════════════════════════════════ */
.stProgress > div > div > div {
    background: var(--accent) !important;
    border-radius: 99px !important;
}
.stProgress > div > div {
    background: var(--border) !important;
    border-radius: 99px !important;
    height: 6px !important;
}
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ════════════════════════════════
   SCROLLBAR
════════════════════════════════ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────────────────
for k, v in [("collection", None), ("doc_name", None), ("doc_size", 0), ("history", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
    <div class="site-title">Finance <span>Analyst</span></div>
    <div class="site-tagline">
        Upload any financial document &nbsp;·&nbsp; Ask questions &nbsp;·&nbsp; Get cited answers
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# UPLOAD VIEW
# ════════════════════════════════════════════════════════
if not st.session_state["collection"]:

    st.markdown('<div class="field-label">Upload a document (PDF)</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your PDF here — 10-K, annual report, earnings release",
        type="pdf",
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.markdown(f"""
        <div class="file-meta">
            📄 &nbsp; {uploaded_file.name} &nbsp;·&nbsp; {uploaded_file.size / 1024:.0f} KB
        </div>
        """, unsafe_allow_html=True)

        if st.button("Analyse Document →"):
            from ingest import ingest_pdf
            col_name = uploaded_file.name.replace(".pdf", "").replace(" ", "_").lower()[:40]
            bar = st.progress(0, text="Reading pages…")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            bar.progress(35, text="Chunking text…")
            time.sleep(0.2)
            bar.progress(68, text="Embedding chunks…")
            ingest_pdf(tmp_path, col_name)
            os.unlink(tmp_path)
            bar.progress(100, text="Ready.")
            time.sleep(0.4)
            bar.empty()

            st.session_state.update({
                "collection": col_name,
                "doc_name":   uploaded_file.name,
                "doc_size":   uploaded_file.size,
                "history":    [],
            })
            st.rerun()

# ════════════════════════════════════════════════════════
# CHAT VIEW
# ════════════════════════════════════════════════════════
else:
    st.markdown(f"""
    <div class="doc-pill">
        <div>
            <div class="doc-pill-name">📄 &nbsp; {st.session_state['doc_name']}</div>
            <div class="doc-pill-meta">
                {st.session_state['doc_size'] / 1024:.0f} KB &nbsp;·&nbsp;
                {len(st.session_state['history'])} question(s) asked
            </div>
        </div>
        <div class="doc-pill-badge">● Active</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="field-label">Ask a question about this document</div>', unsafe_allow_html=True)

    question = st.text_input(
        "question",
        placeholder="e.g. What were the total revenues in 2023?",
        label_visibility="collapsed",
    )

    if question:
        from chain import answer_question
        with st.spinner("Thinking…"):
            t0 = time.time()
            result = answer_question(question, st.session_state["collection"])
            elapsed = time.time() - t0

        st.session_state["history"].insert(0, {
            "q":       question,
            "answer":  result["answer"],
            "sources": result["sources"],
            "elapsed": elapsed,
        })

    # ── Render Q&A history ──
    if st.session_state["history"]:
        for i, entry in enumerate(st.session_state["history"]):
            if i > 0:
                st.markdown('<hr class="history-sep">', unsafe_allow_html=True)

            chips = "".join(
                f'<span class="page-chip">pg. {s["page"]} · {s["score"]}</span>'
                for s in entry["sources"]
            )
            st.markdown(f"""
            <div class="answer-wrap">
                <div class="answer-q">"{entry['q']}"</div>
                <div class="answer-body">{entry['answer']}</div>
                <div class="answer-footer">
                    {chips}
                    <span class="elapsed">{entry['elapsed']:.2f}s</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View source excerpts"):
                for s in entry["sources"]:
                    st.markdown(f"""
                    <div class="excerpt-item">
                        <div class="excerpt-pg">Page {s['page']} &nbsp;·&nbsp; relevance {s['score']}</div>
                        {s['text'][:340]}…
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty">
            <div class="empty-text">Document ready — try one of these to get started</div>
            <div class="hint-grid">
                <div class="hint">What were the total revenues?</div>
                <div class="hint">Summarise the key risk factors.</div>
                <div class="hint">What is the net income trend?</div>
                <div class="hint">Who are the key executives?</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Load a different document"):
        st.session_state.update({"collection": None, "doc_name": None, "history": []})
        st.rerun()
        