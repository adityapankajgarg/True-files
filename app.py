import gradio as gr
from agent import run_agent

# ── Dark aesthetic CSS ──────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

* { box-sizing: border-box; }

body, .gradio-container {
    background: #080b0f !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e2e8f0 !important;
}

.gradio-container {
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 2rem 1.5rem !important;
}

/* Header */
.header-block {
    text-align: center;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid #1a2535;
    margin-bottom: 2rem;
}
.header-block h1 {
    font-family: 'Space Mono', monospace !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
    color: #f1f5f9 !important;
    margin: 0 0 0.4rem !important;
}
.header-block h1 span { color: #3b82f6; }
.header-sub {
    font-size: 0.9rem;
    color: #64748b;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.05em;
}

/* Input area */
.input-wrap textarea {
    background: #0f1623 !important;
    border: 1px solid #1e2d42 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    padding: 1rem !important;
    resize: none !important;
    transition: border-color 0.2s;
}
.input-wrap textarea:focus {
    border-color: #3b82f6 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}
.input-wrap label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}

/* Button */
.check-btn {
    background: #1d4ed8 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s !important;
    width: 100% !important;
    margin-top: 0.75rem !important;
}
.check-btn:hover { background: #2563eb !important; transform: translateY(-1px) !important; }
.check-btn:active { transform: translateY(0) !important; }

/* Output */
.output-wrap {
    margin-top: 1.5rem;
}
.output-wrap label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}

/* Result HTML block */
#result-display {
    background: #0f1623;
    border: 1px solid #1e2d42;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 0.5rem;
}

/* Examples */
.gr-examples {
    margin-top: 1.5rem;
}
.gr-examples label {
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
.gr-examples button {
    background: #0f1623 !important;
    border: 1px solid #1e2d42 !important;
    color: #94a3b8 !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0.4rem 0.8rem !important;
    transition: all 0.15s !important;
}
.gr-examples button:hover {
    border-color: #3b82f6 !important;
    color: #e2e8f0 !important;
    background: #131d2e !important;
}

/* Footer */
.footer-note {
    text-align: center;
    margin-top: 2.5rem;
    color: #334155;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.04em;
}
"""

# ── Result HTML builder ─────────────────────────────────────────────────────
def make_result_html(data: dict) -> str:
    verdict = data.get("verdict", "UNVERIFIED")
    confidence = data.get("confidence", 0)
    summary = data.get("summary", "")
    supporting = data.get("supporting", [])
    contradicting = data.get("contradicting", [])
    sources = data.get("sources", [])
    ask_source = data.get("ask_for_source", False)

    verdict_colors = {
        "TRUE":        ("#22c55e", "#052e16", "✓ VERIFIED TRUE"),
        "FALSE":       ("#ef4444", "#2d0707", "✗ LIKELY FALSE"),
        "MISLEADING":  ("#f59e0b", "#2d1f07", "⚠ MISLEADING"),
        "UNVERIFIED":  ("#6366f1", "#1a1b3d", "? UNVERIFIED"),
    }
    col, bg, label = verdict_colors.get(verdict, ("#6366f1", "#1a1b3d", "? UNVERIFIED"))

    # Confidence bar color
    if confidence >= 70:
        bar_col = "#22c55e"
    elif confidence >= 40:
        bar_col = "#f59e0b"
    else:
        bar_col = "#ef4444"

    # Supporting points
    sup_html = ""
    if supporting:
        items = "".join(f'<li style="margin:0.3rem 0;color:#94a3b8;font-size:0.88rem;">{s}</li>' for s in supporting)
        sup_html = f"""
        <div style="margin-top:1.2rem;">
            <div style="font-size:0.75rem;letter-spacing:0.08em;color:#64748b;font-family:Space Mono,monospace;margin-bottom:0.5rem;">SUPPORTING EVIDENCE</div>
            <ul style="padding-left:1.2rem;margin:0;">{items}</ul>
        </div>"""

    # Contradicting points
    con_html = ""
    if contradicting:
        items = "".join(f'<li style="margin:0.3rem 0;color:#94a3b8;font-size:0.88rem;">{c}</li>' for c in contradicting)
        con_html = f"""
        <div style="margin-top:1.2rem;">
            <div style="font-size:0.75rem;letter-spacing:0.08em;color:#64748b;font-family:Space Mono,monospace;margin-bottom:0.5rem;">CONTRADICTING EVIDENCE</div>
            <ul style="padding-left:1.2rem;margin:0;">{items}</ul>
        </div>"""

    # Sources
    src_html = ""
    if sources:
        links = "".join(
            f'<a href="{s.get("url","#")}" target="_blank" style="display:block;color:#3b82f6;font-size:0.82rem;margin:0.25rem 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;text-decoration:none;" onmouseover="this.style.textDecoration=\'underline\'" onmouseout="this.style.textDecoration=\'none\'">'
            f'↗ {s.get("title","Source")}</a>'
            for s in sources[:4]
        )
        src_html = f"""
        <div style="margin-top:1.2rem;padding-top:1.2rem;border-top:1px solid #1e2d42;">
            <div style="font-size:0.75rem;letter-spacing:0.08em;color:#64748b;font-family:Space Mono,monospace;margin-bottom:0.5rem;">SOURCES FOUND</div>
            {links}
        </div>"""

    # Ask for source
    ask_html = ""
    if ask_source:
        ask_html = f"""
        <div style="margin-top:1.2rem;padding:1rem;background:#1a1625;border:1px solid #4c1d95;border-radius:8px;">
            <div style="font-size:0.75rem;letter-spacing:0.08em;color:#a78bfa;font-family:Space Mono,monospace;margin-bottom:0.4rem;">⚠ NO SOURCES FOUND ONLINE</div>
            <div style="color:#94a3b8;font-size:0.88rem;">This claim could not be found on the internet. Please provide your source so we can investigate further.</div>
        </div>"""

    html = f"""
    <div style="font-family:Space Grotesk,sans-serif;">

        <!-- Verdict badge -->
        <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
            <div style="background:{bg};border:1px solid {col}33;border-radius:8px;padding:0.5rem 1.2rem;">
                <span style="font-family:Space Mono,monospace;font-weight:700;font-size:1rem;color:{col};">{label}</span>
            </div>
            <div style="flex:1;min-width:160px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
                    <span style="font-size:0.75rem;color:#64748b;font-family:Space Mono,monospace;letter-spacing:0.05em;">CONFIDENCE</span>
                    <span style="font-family:Space Mono,monospace;font-size:0.85rem;color:{bar_col};font-weight:700;">{confidence}%</span>
                </div>
                <div style="background:#1e2d42;border-radius:99px;height:6px;width:100%;">
                    <div style="background:{bar_col};width:{confidence}%;height:6px;border-radius:99px;transition:width 0.6s ease;"></div>
                </div>
            </div>
        </div>

        <!-- Summary -->
        <div style="margin-top:1.2rem;padding:1rem;background:#080b0f;border:1px solid #1e2d42;border-radius:8px;">
            <div style="font-size:0.75rem;letter-spacing:0.08em;color:#64748b;font-family:Space Mono,monospace;margin-bottom:0.5rem;">ANALYSIS SUMMARY</div>
            <div style="color:#cbd5e1;font-size:0.92rem;line-height:1.6;">{summary}</div>
        </div>

        {sup_html}
        {con_html}
        {src_html}
        {ask_html}

    </div>
    """
    return html


# ── Main check function ─────────────────────────────────────────────────────
def check_claim(claim: str):
    if not claim or not claim.strip():
        return make_result_html({
            "verdict": "UNVERIFIED",
            "confidence": 0,
            "summary": "Please enter a news claim to verify.",
            "supporting": [],
            "contradicting": [],
            "sources": [],
            "ask_for_source": False
        })
    result = run_agent(claim.strip())
    return make_result_html(result)


# ── Gradio UI ───────────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="VeritasAI — Fact Checker") as demo:

    gr.HTML("""
    <div class="header-block">
        <h1>VERIT<span>A</span>S<span style="color:#1e40af;">AI</span></h1>
        <div class="header-sub">INTELLIGENT FACT-CHECKING AGENT // POWERED BY GROQ + TAVILY</div>
    </div>
    """)

    with gr.Column(elem_classes="input-wrap"):
        claim_input = gr.Textbox(
            label="NEWS CLAIM TO VERIFY",
            placeholder='e.g. "Scientists discover water on Mars surface" or paste any news you heard...',
            lines=3,
            max_lines=6,
        )
        check_btn = gr.Button("⟳  VERIFY CLAIM", elem_classes="check-btn")

    result_output = gr.HTML(
        value='<div style="color:#334155;font-family:Space Mono,monospace;font-size:0.8rem;text-align:center;padding:2rem 0;">Enter a claim above and click VERIFY CLAIM</div>',
        label="",
        elem_id="result-display",
        elem_classes="output-wrap"
    )

    gr.Examples(
        examples=[
            ["NASA confirmed the Moon is made of cheese"],
            ["India launched its first solar mission Aditya-L1 in 2023"],
            ["5G towers are spreading COVID-19"],
            ["Scientists have created a black hole in a laboratory"],
        ],
        inputs=claim_input,
        label="TRY AN EXAMPLE",
    )

    gr.HTML('<div class="footer-note">VeritasAI searches the web in real-time. Results are AI-generated and should not be treated as legal or journalistic fact.</div>')

    check_btn.click(fn=check_claim, inputs=claim_input, outputs=result_output)
    claim_input.submit(fn=check_claim, inputs=claim_input, outputs=result_output)

if __name__ == "__main__":
    demo.launch(share=False)