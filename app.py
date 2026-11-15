import base64
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# SupeRR Selector Season 2 | Round 1
# Dashboard built from the baseline results in report.py.
# It displays the supplied ranking outputs; it does not
# recalculate the rankings from ball_by_ball.csv.
# ------------------------------------------------------------

st.set_page_config(
    page_title="SupeRR Selector | Player Reliability",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- DATA ----------------------------

BATTERS = [
    {"Rank": 1, "Player": "Sameer Rizvi", "Format": "T20", "Pressure Matches": 10, "Pressure Balls": 191, "Pressure SR": 172.77, "Normal SR": 92.16, "SR Improvement": 80.62, "Score": 0.882410},
    {"Rank": 2, "Player": "Reeza Hendricks", "Format": "T20I", "Pressure Matches": 12, "Pressure Balls": 245, "Pressure SR": 183.27, "Normal SR": 131.36, "SR Improvement": 51.91, "Score": 0.777476},
    {"Rank": 3, "Player": "Mohammad Nabi", "Format": "T20I", "Pressure Matches": 26, "Pressure Balls": 317, "Pressure SR": 153.63, "Normal SR": 107.94, "SR Improvement": 45.69, "Score": 0.679872},
    {"Rank": 4, "Player": "Babar Azam", "Format": "T20I", "Pressure Matches": 13, "Pressure Balls": 155, "Pressure SR": 169.03, "Normal SR": 127.78, "SR Improvement": 41.25, "Score": 0.654684},
    {"Rank": 5, "Player": "Fakhar Zaman", "Format": "T20I", "Pressure Matches": 14, "Pressure Balls": 169, "Pressure SR": 160.36, "Normal SR": 124.35, "SR Improvement": 36.00, "Score": 0.550095},
    {"Rank": 6, "Player": "Towhid Hridoy", "Format": "T20I", "Pressure Matches": 21, "Pressure Balls": 389, "Pressure SR": 139.59, "Normal SR": 116.02, "SR Improvement": 23.57, "Score": 0.520523},
    {"Rank": 7, "Player": "Sikandar Raza", "Format": "T20I", "Pressure Matches": 26, "Pressure Balls": 369, "Pressure SR": 156.10, "Normal SR": 120.72, "SR Improvement": 35.37, "Score": 0.518388},
    {"Rank": 8, "Player": "Anuj Rawat", "Format": "T20", "Pressure Matches": 9, "Pressure Balls": 115, "Pressure SR": 140.87, "Normal SR": 101.23, "SR Improvement": 39.63, "Score": 0.466720},
    {"Rank": 9, "Player": "Jimmy Neesham", "Format": "T20I", "Pressure Matches": 18, "Pressure Balls": 172, "Pressure SR": 159.30, "Normal SR": 118.47, "SR Improvement": 40.83, "Score": 0.443138},
    {"Rank": 10, "Player": "Mark Chapman", "Format": "T20I", "Pressure Matches": 22, "Pressure Balls": 340, "Pressure SR": 159.71, "Normal SR": 134.52, "SR Improvement": 25.18, "Score": 0.439513},
]

BOWLERS = [
    {"Rank": 1, "Player": "Mohit Sharma", "Format": "T20", "Pressure Matches": 23, "Pressure Legal Balls": 326, "Pressure Economy": 8.87, "Normal Economy": 10.42, "Wickets/100 Pressure Balls": 10.12, "Score": 0.877430},
    {"Rank": 2, "Player": "Gudakesh Motie", "Format": "T20I", "Pressure Matches": 20, "Pressure Legal Balls": 283, "Pressure Economy": 7.14, "Normal Economy": 8.90, "Wickets/100 Pressure Balls": 7.07, "Score": 0.583756},
    {"Rank": 3, "Player": "Mohammad Nawaz", "Format": "T20I", "Pressure Matches": 29, "Pressure Legal Balls": 337, "Pressure Economy": 6.43, "Normal Economy": 7.48, "Wickets/100 Pressure Balls": 9.50, "Score": 0.576966},
    {"Rank": 4, "Player": "Jamie Overton", "Format": "T20, T20I", "Pressure Matches": 15, "Pressure Legal Balls": 162, "Pressure Economy": 6.44, "Normal Economy": 9.74, "Wickets/100 Pressure Balls": 10.49, "Score": 0.504167},
    {"Rank": 5, "Player": "Umran Malik", "Format": "T20, T20I", "Pressure Matches": 13, "Pressure Legal Balls": 173, "Pressure Economy": 8.60, "Normal Economy": 10.40, "Wickets/100 Pressure Balls": 10.98, "Score": 0.503690},
    {"Rank": 6, "Player": "Krunal Pandya", "Format": "T20", "Pressure Matches": 31, "Pressure Legal Balls": 422, "Pressure Economy": 7.42, "Normal Economy": 8.01, "Wickets/100 Pressure Balls": 6.40, "Score": 0.469252},
    {"Rank": 7, "Player": "Jimmy Neesham", "Format": "T20I", "Pressure Matches": 15, "Pressure Legal Balls": 168, "Pressure Economy": 8.43, "Normal Economy": 9.28, "Wickets/100 Pressure Balls": 10.12, "Score": 0.456927},
    {"Rank": 8, "Player": "Barry McCarthy", "Format": "T20I", "Pressure Matches": 18, "Pressure Legal Balls": 191, "Pressure Economy": 7.95, "Normal Economy": 9.00, "Wickets/100 Pressure Balls": 7.85, "Score": 0.434642},
    {"Rank": 9, "Player": "Zakary Foulkes", "Format": "T20I", "Pressure Matches": 10, "Pressure Legal Balls": 123, "Pressure Economy": 8.05, "Normal Economy": 10.13, "Wickets/100 Pressure Balls": 8.13, "Score": 0.411131},
    {"Rank": 10, "Player": "Jofra Archer", "Format": "T20, T20I", "Pressure Matches": 29, "Pressure Legal Balls": 253, "Pressure Economy": 7.57, "Normal Economy": 9.41, "Wickets/100 Pressure Balls": 9.09, "Score": 0.404404},
]

BATTER_DF = pd.DataFrame(BATTERS)
BOWLER_DF = pd.DataFrame(BOWLERS)

# --------------------------- IMAGES ---------------------------
# Folder layout next to app.py:
#   assets/theme_1_bat_ball.svg ... theme_4_pressure.svg   (theme images)
#   assets/top_batter.(jpg|jpeg|png|webp)                  (your photo of the top batter)
#   assets/top_bowler.(jpg|jpeg|png|webp)                  (your photo of the top bowler)
# If a player photo is missing, an initials placeholder is shown instead.

ASSETS = Path(__file__).parent / "assets"
MIME = {".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp"}

THEME_IMAGES = [
    ("theme_1_bat_ball.svg", "Batting"),
    ("theme_2_stumps.svg", "Bowling"),
    ("theme_3_stadium.svg", "Match day"),
    ("theme_4_pressure.svg", "Under pressure"),
]


def find_image(stem_or_name):
    """Return a path for an exact file name, or for a stem with any known extension."""
    exact = stem_or_name
    if exact.suffix and exact.exists():
        return exact
    for ext in MIME:
        p = f"{stem_or_name}{ext}"
        if p.exists():
            return p
    return None


def data_uri(path):
    mime = MIME.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def placeholder_uri(name, color):
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'>"
        f"<rect width='300' height='300' fill='{color}'/>"
        "<circle cx='150' cy='115' r='55' fill='#ffffff' opacity='.25'/>"
        "<ellipse cx='150' cy='265' rx='95' ry='80' fill='#ffffff' opacity='.25'/>"
        f"<text x='150' y='170' text-anchor='middle' font-family='sans-serif' "
        f"font-size='72' font-weight='bold' fill='#ffffff'>{initials}</text></svg>"
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def show_image(src_uri, caption=None, radius=14, height=None):
    style = f"width:100%;border-radius:{radius}px;display:block;"
    if height:
        style += f"height:{height}px;object-fit:cover;"
    html = f'<img src="{src_uri}" style="{style}">'
    if caption:
        html += f'<div class="small-note" style="text-align:center;margin-top:.3rem;">{caption}</div>'
    st.markdown(html, unsafe_allow_html=True)


def theme_strip():
    cols = st.columns(4)
    for col, (fname, caption) in zip(cols, THEME_IMAGES):
        path = find_image(fname)
        with col:
            if path:
                show_image(data_uri(path))  # label is already drawn inside the image
            else:
                st.caption(f"Missing {fname}")


def player_photo(stem, name, color, caption=None):
    path = find_image(stem)
    uri = data_uri(path) if path else placeholder_uri(name, color)
    show_image(uri, name if caption is None else caption, height=260)
    if not path:
        st.caption(f"Add {stem}.jpg to show a photo.")


# -------------------------- STYLING ---------------------------

st.markdown(
    """
    <style>
      .main {background-color: #f7f9fc;}
      .block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
      .hero {
        background: linear-gradient(120deg, #102a43 0%, #1d4e70 100%);
        padding: 1.5rem 1.7rem; border-radius: 16px; color: white;
        margin-bottom: 1.2rem;
      }
      .hero h1 {color: white; margin: 0; font-size: 2.15rem;}
      .hero p {color: #d9e8f2; margin: .35rem 0 0 0;}
      .small-note {color: #94a3b8; font-size: .86rem;}
      div[data-testid="stMetric"] {
        background: white; border: 1px solid #e5eaf0;
        padding: 12px 16px; border-radius: 12px;
      }
      /* Metric cards are white, so force dark text (fixes invisible text in dark theme) */
      div[data-testid="stMetricLabel"],
      div[data-testid="stMetricLabel"] * {color: #475569 !important;}
      div[data-testid="stMetricValue"],
      div[data-testid="stMetricValue"] * {color: #102a43 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------- SIDEBAR ---------------------------

st.sidebar.title("🏏 SupeRR Selector")
st.sidebar.caption("Season 2 · Round 1")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Top 10 Batters", "Top 10 Bowlers", "Player Explorer", "Methodology & Sensitivity"],
)
st.sidebar.divider()
st.sidebar.caption("Dataset period: 2022 onwards")
st.sidebar.caption("Formats: T20 and T20I")

# --------------------------- HEADER ---------------------------

st.markdown(
    """
    <div class="hero">
      <h1>Identifying the Most Reliable Players Under Pressure</h1>
      <p>Delivery-level performance analysis · T20 and T20I · Round 1</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------- HELPERS ---------------------------

def format_filter(df, key):
    formats = sorted(df["Format"].unique().tolist())
    selected = st.multiselect("Filter by format", formats, default=formats, key=key)
    if not selected:
        st.info("Select at least one format to display players.")
        return df.iloc[0:0]
    return df[df["Format"].isin(selected)].copy()


def show_dataframe(df, hide_score=False):
    display = df.copy()
    if hide_score and "Score" in display.columns:
        display = display.drop(columns=["Score"])
    st.dataframe(display, use_container_width=True, hide_index=True)


# ---------------------------- PAGES ---------------------------

if page == "Overview":
    st.subheader("Dashboard overview")
    # The four theme images replace the four white metric cards; each figure sits under its image.
    overview_stats = [
        ("theme_1_bat_ball.svg", "10", "Top batters"),
        ("theme_2_stumps.svg", "10", "Top bowlers"),
        ("theme_3_stadium.svg", "883", "Matches in source"),
        ("theme_4_pressure.svg", "200,999", "Ball-by-ball records"),
    ]
    for col, (fname, value, label) in zip(st.columns(4), overview_stats):
        path = find_image(fname)
        with col:
            if path:
                show_image(data_uri(path))
            st.markdown(
                f"<div style='text-align:center;margin-top:.4rem;'>"
                f"<span style='font-size:1.8rem;font-weight:700;'>{value}</span><br>"
                f"<span class='small-note'>{label}</span></div>",
                unsafe_allow_html=True,
            )
    st.write("")

    st.markdown(
        """
        This dashboard presents the baseline top-10 batter and bowler rankings
        produced by the analysis. Players are evaluated by comparing their
        performance in pressure situations with their performance in normal
        situations. An exposure-based reliability multiplier reduces the
        influence of players with limited evidence.
        """
    )

    left, right = st.columns(2)
    with left:
        st.markdown("#### Highest-ranked batter")
        img_col, txt_col = st.columns([1, 1.4])
        with img_col:
            player_photo("top_batter", BATTERS[0]["Player"], "#1d4e70", "")
        with txt_col:
            st.markdown("### Sameer Rizvi")
            st.markdown("**T20 · Rank 1**")
            st.write("Pressure strike rate: **172.77**")
            st.write("Normal strike rate: **92.16**")
            st.write("Pressure exposure: **191 balls across 10 matches**")
    with right:
        st.markdown("#### Highest-ranked bowler")
        img_col, txt_col = st.columns([1, 1.4])
        with img_col:
            player_photo("top_bowler", BOWLERS[0]["Player"], "#2f7d4f", "")
        with txt_col:
            st.markdown("### Mohit Sharma")
            st.markdown("**T20 · Rank 1**")
            st.write("Pressure economy: **8.87**")
            st.write("Normal economy: **10.42**")
            st.write("Pressure exposure: **326 legal balls across 23 matches**")

    st.info(
        "Interpretation: these are relative rankings under the documented "
        "baseline method and supplied dataset. They are not guarantees of "
        "future performance or universal player-quality ratings."
    )

    st.markdown("#### Ranking snapshot")
    bcol, wcol = st.columns(2)
    with bcol:
        st.markdown("**Top 5 batters**")
        show_dataframe(BATTER_DF.head(5)[["Rank", "Player", "Format", "Score"]])
    with wcol:
        st.markdown("**Top 5 bowlers**")
        show_dataframe(BOWLER_DF.head(5)[["Rank", "Player", "Format", "Score"]])


elif page == "Top 10 Batters":
    st.subheader("Top 10 batters")
    filtered = format_filter(BATTER_DF, "batter_formats")
    if not filtered.empty:
        top = BATTERS[0]
        photo_col, info_col = st.columns([1, 3])
        with photo_col:
            player_photo("top_batter", top["Player"], "#1d4e70", f"#1 · {top['Player']}")
        with info_col:
            st.markdown(f"### 🥇 {top['Player']}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Pressure SR", f"{top['Pressure SR']:.2f}")
            m2.metric("Normal SR", f"{top['Normal SR']:.2f}")
            m3.metric("SR improvement", f"+{top['SR Improvement']:.2f}")

        st.caption("Rankings use the baseline batting score. Higher strike rate improvement is only one component of the score.")
        show_dataframe(filtered)

        chart = px.bar(
            filtered.sort_values("Rank"),
            x="Player", y=["Pressure SR", "Normal SR"],
            barmode="group", title="Strike rate: pressure vs normal",
            labels={"value": "Strike rate", "variable": "Situation"},
        )
        chart.update_layout(legend_title_text="", xaxis_tickangle=-35, height=480)
        st.plotly_chart(chart, use_container_width=True)

        improvement = px.bar(
            filtered.sort_values("SR Improvement", ascending=True),
            x="SR Improvement", y="Player", orientation="h",
            title="Strike-rate improvement under pressure",
            labels={"SR Improvement": "Pressure SR − Normal SR"},
        )
        improvement.update_layout(height=430)
        st.plotly_chart(improvement, use_container_width=True)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download batter rankings (CSV)", csv, "supeRR_top_10_batters.csv", "text/csv")


elif page == "Top 10 Bowlers":
    st.subheader("Top 10 bowlers")
    filtered = format_filter(BOWLER_DF, "bowler_formats")
    if not filtered.empty:
        top = BOWLERS[0]
        photo_col, info_col = st.columns([1, 3])
        with photo_col:
            player_photo("top_bowler", top["Player"], "#2f7d4f", f"#1 · {top['Player']}")
        with info_col:
            st.markdown(f"### 🥇 {top['Player']}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Pressure economy", f"{top['Pressure Economy']:.2f}")
            m2.metric("Normal economy", f"{top['Normal Economy']:.2f}")
            m3.metric("Wkts/100 balls", f"{top['Wickets/100 Pressure Balls']:.2f}")

        st.caption("Lower economy is better. Wicket rate and dot-ball rate also contribute to the final bowling score.")
        show_dataframe(filtered)

        chart = px.bar(
            filtered.sort_values("Rank"),
            x="Player", y=["Pressure Economy", "Normal Economy"],
            barmode="group", title="Economy: pressure vs normal",
            labels={"value": "Runs conceded per over", "variable": "Situation"},
        )
        chart.update_layout(legend_title_text="", xaxis_tickangle=-35, height=480)
        st.plotly_chart(chart, use_container_width=True)

        wickets = px.bar(
            filtered.sort_values("Wickets/100 Pressure Balls", ascending=True),
            x="Wickets/100 Pressure Balls", y="Player", orientation="h",
            title="Wickets per 100 legal balls under pressure",
        )
        wickets.update_layout(height=430)
        st.plotly_chart(wickets, use_container_width=True)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download bowler rankings (CSV)", csv, "supeRR_top_10_bowlers.csv", "text/csv")


elif page == "Player Explorer":
    st.subheader("Player explorer")
    all_names = sorted(set(BATTER_DF["Player"]).union(set(BOWLER_DF["Player"])))
    selected_player = st.selectbox("Choose a player", all_names)

    batter_row = BATTER_DF[BATTER_DF["Player"] == selected_player]
    bowler_row = BOWLER_DF[BOWLER_DF["Player"] == selected_player]

    if not batter_row.empty:
        st.markdown("#### Batting record")
        is_top = int(batter_row.iloc[0]["Rank"]) == 1
        if is_top:
            pc, tc = st.columns([1, 4])
            with pc:
                player_photo("top_batter", selected_player, "#1d4e70")
            with tc:
                show_dataframe(batter_row)
        else:
            show_dataframe(batter_row)
        row = batter_row.iloc[0]
        fig = px.bar(
            pd.DataFrame({
                "Situation": ["Pressure", "Normal"],
                "Strike rate": [row["Pressure SR"], row["Normal SR"]],
            }),
            x="Situation", y="Strike rate", title=f"{selected_player} · batting strike rate",
        )
        st.plotly_chart(fig, use_container_width=True)

    if not bowler_row.empty:
        st.markdown("#### Bowling record")
        is_top = int(bowler_row.iloc[0]["Rank"]) == 1
        if is_top:
            pc, tc = st.columns([1, 4])
            with pc:
                player_photo("top_bowler", selected_player, "#2f7d4f")
            with tc:
                show_dataframe(bowler_row)
        else:
            show_dataframe(bowler_row)
        row = bowler_row.iloc[0]
        fig = px.bar(
            pd.DataFrame({
                "Situation": ["Pressure", "Normal"],
                "Economy": [row["Pressure Economy"], row["Normal Economy"]],
            }),
            x="Situation", y="Economy", title=f"{selected_player} · bowling economy",
        )
        st.plotly_chart(fig, use_container_width=True)

    if batter_row.empty and bowler_row.empty:
        st.warning("No ranking record is available for this player in the current top-10 outputs.")


elif page == "Methodology & Sensitivity":
    st.subheader("Methodology")
    st.markdown("### Pressure definition")

    st.markdown("**Second innings (chase)**")
    st.latex(r"\mathrm{RRR} = \frac{\mathrm{Runs\ required}\times 6}{\mathrm{Legal\ balls\ remaining}}")
    st.latex(r"P_{\mathrm{chase}}=100(0.50P_{\mathrm{RRR}}+0.25P_{\mathrm{Stage}}+0.25P_{\mathrm{Wicket}})")
    st.markdown(
        "- Required run rate is capped at 18 before normalisation.\n"
        "- Stage pressure increases as the innings progresses.\n"
        "- Wicket pressure increases as wickets are lost.\n"
        "- Deliveries after the target is reached are excluded from active chase pressure."
    )

    st.markdown("**First innings**")
    st.latex(r"P_{\mathrm{1st}}=100(0.50P_{\mathrm{Score}}+0.25P_{\mathrm{Wicket}}+0.25P_{\mathrm{Stage}})")
    st.markdown(
        "Expected first-innings scores are estimated separately for T20 and T20I "
        "at each legal-ball position. The score component measures how far the "
        "current score is below that expected score."
    )

    st.markdown("### Pressure categories and comparison groups")
    st.write("- Low pressure: score below 40")
    st.write("- Medium pressure: score from 40 to below 65")
    st.write("- High pressure: score 65 or above")
    st.write("- Player comparison: pressure score of 40 or above versus normal situations")

    st.markdown("### Baseline scoring weights")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Batting**")
        st.write("- Strike-rate improvement: 40%")
        st.write("- Dismissal-rate improvement: 20%")
        st.write("- Dot-ball-rate improvement: 20%")
        st.write("- Boundary-rate improvement: 20%")
    with col2:
        st.markdown("**Bowling**")
        st.write("- Economy improvement: 40%")
        st.write("- Wicket-rate improvement: 30%")
        st.write("- Dot-ball-rate improvement: 30%")

    st.markdown("### Eligibility and reliability")
    st.write(
        "Initial eligibility required at least 30 pressure balls/legal balls "
        "and 3 pressure matches, plus 60 normal balls/legal balls and 5 normal "
        "matches. The final evidence filter required at least 100 pressure balls "
        "and 8 pressure matches for batters, and 120 pressure legal balls and "
        "8 pressure matches for bowlers."
    )
    st.write(
        "Format-specific metric z-scores were clipped to −2.5 and +2.5. "
        "The weighted raw score was multiplied by an exposure-based reliability "
        "factor using pressure and normal exposure and match counts. Players "
        "eligible in both formats received the mean of their format-specific "
        "scores; otherwise the eligible format score was used."
    )

    st.markdown("### Sensitivity analysis")
    sensitivity = pd.DataFrame([
        {"Role": "Batters", "Baseline vs Alternative 1": "9 of 10 common", "Baseline vs Alternative 2": "10 of 10 common"},
        {"Role": "Bowlers", "Baseline vs Alternative 1": "8 of 10 common", "Baseline vs Alternative 2": "8 of 10 common"},
    ])
    show_dataframe(sensitivity)
    st.markdown(
        "**Batting alternatives:** Alternative 1 used weights 30/25/25/20 "
        "(strike rate/dismissal/dot/boundary); George Dockrell entered and "
        "Jimmy Neesham left. Alternative 2 used 50/20/15/15 and retained all "
        "ten baseline batters."
    )
    st.markdown(
        "**Bowling alternatives:** Alternative 1 used 30/40/30 "
        "(economy/wicket/dot); Mustafizur Rahman and Yash Thakur entered, "
        "while Jofra Archer and Zakary Foulkes left. Alternative 2 used "
        "50/25/25; Abrar Ahmed and Cameron Green entered, while Barry McCarthy "
        "and Jimmy Neesham left."
    )

    st.markdown("### Limitations")
    limitations = [
        "First-innings and chase pressure use different contextual measures.",
        "Pressure-component and metric weights are modelling choices; other reasonable choices may change rankings.",
        "The reliability multiplier and minimum exposure requirements reduce, but do not remove, small-sample uncertainty.",
        "Format-specific standardisation does not adjust for every competition condition or player role.",
        "Batting position, opposition strength, venue, pitch conditions, and bowling phase are not fully adjusted for.",
        "Some extra-delivery categories required classification assumptions when deriving legal balls and bowler runs conceded.",
        "The score measures relative improvement in this dataset under this method; it is not a guarantee of future performance.",
    ]
    for item in limitations:
        st.markdown(f"- {item}")

st.divider()