# ─────────────────────────────────────────────────────────────
#  FINANCIAL NEWS ANALYST AGENT — Dashboard
#  Course: Financial Modeling | American University
#  Author: Abd Alghani Rahmoun
# ─────────────────────────────────────────────────────────────

import gradio as gr
from agent import run_agent
from datetime import datetime

# ── Sentiment styling ─────────────────────────────────────────
ICONS = {
    "BULLISH":  "🟢",
    "BEARISH":  "🔴",
    "NEUTRAL":  "🟡"
}

COLORS = {
    "BULLISH":  "#0a2e1a",
    "BEARISH":  "#2e0a0f",
    "NEUTRAL":  "#1a1a0a"
}

BADGE_COLORS = {
    "BULLISH":  "#00e5a0",
    "BEARISH":  "#ff4d6d",
    "NEUTRAL":  "#ffb700"
}


# ── Build one card per headline ───────────────────────────────
def build_card(result):
    sentiment    = result["sentiment"]
    icon         = ICONS.get(sentiment, "🟡")
    bg_color     = COLORS.get(sentiment, "#1a1a2e")
    badge_color  = BADGE_COLORS.get(sentiment, "#ffb700")

    return f"""
    <div style="
        background: {bg_color};
        border: 1px solid {badge_color};
        border-left: 4px solid {badge_color};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        font-family: 'Segoe UI', Arial, sans-serif;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="color: #7fa8c9; font-size: 11px; font-weight: 600; letter-spacing: 1px;">
                {result['source'].upper()}
            </span>
            <span style="
                background: {badge_color};
                color: #0a1628;
                font-size: 11px;
                font-weight: 700;
                padding: 3px 10px;
                border-radius: 20px;
                letter-spacing: 1px;
            ">
                {icon} {sentiment}
            </span>
        </div>

        <div style="color: #ffffff; font-size: 15px; font-weight: 600; margin-bottom: 12px; line-height: 1.4;">
            {result['title']}
        </div>

        <div style="color: #a8c4d8; font-size: 13px; margin-bottom: 8px; line-height: 1.6;">
            <strong style="color: #7fa8c9;">📝 Summary:</strong> {result['summary']}
        </div>

        <div style="color: #a8c4d8; font-size: 13px; margin-bottom: 12px; line-height: 1.6;">
            <strong style="color: #7fa8c9;">💡 Reason:</strong> {result['reason']}
        </div>

        <a href="{result['url']}" target="_blank" style="
            color: #00c9c8;
            font-size: 12px;
            text-decoration: none;
        ">🔗 Read full article →</a>
    </div>
    """


# ── Main function — runs when professor clicks the button ─────
def run_dashboard():
    now     = datetime.now().strftime("%A, %B %d %Y  —  %I:%M %p")
    results = run_agent()

    if not results:
        return "<p style='color: red;'>Could not fetch news. Check API keys.</p>"

    # Count sentiments for the summary bar
    counts = {"BULLISH": 0, "BEARISH": 0, "NEUTRAL": 0}
    for r in results:
        counts[r["sentiment"]] = counts.get(r["sentiment"], 0) + 1

    # Build the header
    html = f"""
    <div style="
        background: #0a1628;
        min-height: 100vh;
        padding: 24px;
        font-family: 'Segoe UI', Arial, sans-serif;
    ">
        <div style="
            background: #0d2b55;
            border-radius: 10px;
            padding: 24px;
            margin-bottom: 24px;
        ">
            <h1 style="color: #ffffff; margin: 0 0 6px 0; font-size: 24px; letter-spacing: 1px;">
                📊 FINANCIAL NEWS ANALYST AGENT
            </h1>
            <p style="color: #7fa8c9; margin: 0 0 16px 0; font-size: 13px;">
                Powered by Llama-3.3-70b · NewsAPI · Built by Abd Alghani Rahmoun
            </p>
            <p style="color: #a8c4d8; margin: 0 0 16px 0; font-size: 12px;">
                🕐 {now}
            </p>

            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <div style="background: #0a2e1a; border: 1px solid #00e5a0; border-radius: 6px; padding: 10px 18px;">
                    <span style="color: #00e5a0; font-weight: 700; font-size: 20px;">{counts['BULLISH']}</span>
                    <span style="color: #7fa8c9; font-size: 12px; margin-left: 6px;">🟢 BULLISH</span>
                </div>
                <div style="background: #2e0a0f; border: 1px solid #ff4d6d; border-radius: 6px; padding: 10px 18px;">
                    <span style="color: #ff4d6d; font-weight: 700; font-size: 20px;">{counts['BEARISH']}</span>
                    <span style="color: #7fa8c9; font-size: 12px; margin-left: 6px;">🔴 BEARISH</span>
                </div>
                <div style="background: #1a1a0a; border: 1px solid #ffb700; border-radius: 6px; padding: 10px 18px;">
                    <span style="color: #ffb700; font-weight: 700; font-size: 20px;">{counts['NEUTRAL']}</span>
                    <span style="color: #7fa8c9; font-size: 12px; margin-left: 6px;">🟡 NEUTRAL</span>
                </div>
            </div>
        </div>
    """

    # Build a card for each headline
    for result in results:
        html += build_card(result)

    html += "</div>"
    return html


# ── Gradio interface ──────────────────────────────────────────
with gr.Blocks(
    title="Financial News Analyst Agent",
    theme=gr.themes.Base(),
    css="""
        body { background: #0a1628 !important; }
        .gradio-container { background: #0a1628 !important; max-width: 860px !important; }
        button { background: #00c9c8 !important; color: #0a1628 !important; font-weight: 700 !important; }
    """
) as demo:

    gr.Markdown("""
    # 📊 Financial News Analyst Agent
    **Course:** Financial Modeling | American University, Washington Semester Program

    Click the button below to fetch live financial headlines and analyze them
    using Llama-3.3-70b. Each story is classified as Bullish, Bearish, or Neutral.
    """)

    run_btn = gr.Button("▶  RUN AGENT — Fetch & Analyze Latest Headlines", scale=1)
    output  = gr.HTML()

    run_btn.click(fn=run_dashboard, inputs=[], outputs=output)

if __name__ == "__main__":
    demo.launch()