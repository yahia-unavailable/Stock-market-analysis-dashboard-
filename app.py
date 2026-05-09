import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
 page_title="StockPulse · Market Analytics",
 page_icon=" ",
 layout="wide",
 initial_sidebar_state="expanded",
)
# ─────────────────────────────────────────
# GLOBAL CSS (dark, refined, financial)
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter/* ── Base ─────────────────────────────── */
html, body, [class*="css"] {
 font-family: 'Inter', sans-serif;
 background-color: #080c14;
 color: #e2e8f0;
}
/* ── Sidebar ──────────────────────────── */
[data-testid="stSidebar"] {
 background: #0d1321;
 border-right: 1px solid #1e2d45;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
 color: #94a3b8 !important;
 font-size: 0.82rem;
 letter-spacing: 0.06em;
 text-transform: uppercase;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select {
 background: #111827 !important;
 border: 1px solid #1e2d45 !important;
 border-radius: 6px !important;
 color: #f1f5f9 !important;
}
/* ── Main area ────────────────────────── */
.block-container {
 padding: 2rem 2.5rem 2rem 2.5rem;
 max-width: 1600px;
}
/* ── KPI Cards ────────────────────────── */
.kpi-card {
 background: linear-gradient(135deg, #0d1321 0%, #111827 100%);
 border: 1px solid #1e2d45;
 border-radius: 12px;
 padding: 1.25rem 1.5rem;
 position: relative;
 overflow: hidden;
}
.kpi-card::before {
 content: '';
 position: absolute;
 top: 0; left: 0; right: 0;
 height: 2px;
 background: linear-gradient(90deg, #3b82f6, #06b6d4);
}
.kpi-label {
 font-size: 0.7rem;
 letter-spacing: 0.12em;
 text-transform: uppercase;
 color: #64748b;
 margin-bottom: 0.4rem;
 font-family: 'IBM Plex Mono', monospace;
}
.kpi-value {
 font-size: 1.85rem;
 font-weight: 700;
 color: #f1f5f9;
 font-family: 'IBM Plex Mono', monospace;
 line-height: 1;
}
.kpi-delta-pos {
 font-size: 0.85rem;
 color: #10b981;
 font-family: 'IBM Plex Mono', monospace;
 margin-top: 0.35rem;
}
.kpi-delta-neg {
 font-size: 0.85rem;
 color: #ef4444;
 font-family: 'IBM Plex Mono', monospace;
 margin-top: 0.35rem;
}
/* ── Stat Cards ───────────────────────── */
.stat-card {
 background: #0d1321;
 border: 1px solid #1e2d45;
 border-radius: 10px;
 padding: 1rem 1.25rem;
 text-align: center;
}
.stat-label {
 font-size: 0.68rem;
 letter-spacing: 0.1em;
 text-transform: uppercase;
 color: #475569;
 margin-bottom: 0.3rem;
}
.stat-value {
 font-size: 1.2rem;
 font-weight: 600;
 color: #cbd5e1;
 font-family: 'IBM Plex Mono', monospace;
}
/* ── Section headers ──────────────────── */
.section-header {
 font-size: 0.72rem;
 letter-spacing: 0.14em;
 text-transform: uppercase;
 color: #3b82f6;
 font-family: 'IBM Plex Mono', monospace;
 margin-bottom: 0.75rem;
 padding-bottom: 0.5rem;
 border-bottom: 1px solid #1e2d45;
}
/* ── App title ────────────────────────── */
.app-title {
 font-size: 1.6rem;
 font-weight: 700;
 color: #f1f5f9;
 letter-spacing: -0.02em;
 display: inline-block;
}
.app-title span {
 color: #3b82f6;
}
.app-sub {
 font-size: 0.78rem;
 color: #475569;
 letter-spacing: 0.06em;
 text-transform: uppercase;
 margin-top: 0.1rem;
}
/* ── Trend badge ──────────────────────── */
.trend-badge-bull {
 display: inline-block;
 background: rgba(16,185,129,0.12);
 color: #10b981;
 border: 1px solid rgba(16,185,129,0.3);
 border-radius: 4px;
 padding: 2px 8px;
 font-size: 0.7rem;
 font-family: 'IBM Plex Mono', monospace;
 letter-spacing: 0.05em;
 text-transform: uppercase;
}
.trend-badge-bear {
 display: inline-block;
 background: rgba(239,68,68,0.12);
 color: #ef4444;
 border: 1px solid rgba(239,68,68,0.3);
 border-radius: 4px;
 padding: 2px 8px;
 font-size: 0.7rem;
 font-family: 'IBM Plex Mono', monospace;
 letter-spacing: 0.05em;
 text-transform: uppercase;
}
/* ── Divider ──────────────────────────── */
hr { border-color: #1e2d45; }
/* ── Plotly container ─────────────────── */
.js-plotly-plot .plotly {
 border-radius: 12px;
}
/* ── Expander ─────────────────────────── */
[data-testid="stExpander"] {
 background: #0d1321;
 border: 1px solid #1e2d45;
 border-radius: 10px;
}
/* ── Scrollbar ────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #1e2d45; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
PERIOD_MAP = {
 "7 Days": "7d",
 "1 Month": "1mo",
 "3 Months": "3mo",
 "6 Months": "6mo",
 "1 Year": "1y",
}
@st.cache_data(ttl=300)
def fetch_stock(symbol: str, period: str):
 ticker = yf.Ticker(symbol)
 df = ticker.history(period=period)
 info = ticker.info
 return df, info
def moving_average(df: pd.DataFrame, window: int) -> pd.Series:
 return df["Close"].rolling(window=window).mean()
def format_price(val: float) -> str:
 return f"${val:,.2f}"
def format_pct(val: float) -> str:
 sign = "+" if val >= 0 else ""
 return f"{sign}{val:.2f}%"
def build_price_chart(df: pd.DataFrame, symbol: str,
 show_ma: bool, ma_window: int,
 show_volume: bool, color_up="#10b981", color_dn="#ef4444"):
 rows = 2 if show_volume else 1
 row_heights = [0.7, 0.3] if show_volume else [1.0]
 fig = make_subplots(
 rows=rows, cols=1,
 shared_xaxes=True,
 vertical_spacing=0.04,
 row_heights=row_heights,
 )
 # Candlestick
 fig.add_trace(go.Candlestick(
 x=df.index,
 open=df["Open"], high=df["High"],
 low=df["Low"], close=df["Close"],
 name=symbol,
 increasing_line_color=color_up,
 decreasing_line_color=color_dn,
 increasing_fillcolor=color_up,
 decreasing_fillcolor=color_dn,
 line=dict(width=1),
 ), row=1, col=1)
 # Moving Average
 if show_ma:
 ma = moving_average(df, ma_window)
 fig.add_trace(go.Scatter(
 x=df.index, y=ma,
 name=f"MA {ma_window}",
 line=dict(color="#f59e0b", width=1.5, dash="dot"),
 opacity=0.85,
 ), row=1, col=1)
 # Volume
 if show_volume:
 vol_colors = [color_up if c >= o else color_dn
 for c, o in zip(df["Close"], df["Open"])]
 fig.add_trace(go.Bar(
 x=df.index, y=df["Volume"],
 name="Volume",
 marker_color=vol_colors,
 opacity=0.55,
 ), row=2, col=1)
 fig.update_layout(
 height=520,
 paper_bgcolor="#080c14",
 plot_bgcolor="#0d1321",
 font=dict(family="IBM Plex Mono", color="#64748b", size=11),
 legend=dict(
 bgcolor="rgba(13,19,33,0.9)",
 bordercolor="#1e2d45",
 borderwidth=1,
 font=dict(size=11),
 ),
 margin=dict(l=0, r=0, t=10, b=0),
 xaxis_rangeslider_visible=False,
 hovermode="x unified",
 hoverlabel=dict(
 bgcolor="#111827",
 bordercolor="#3b82f6",
 font=dict(color="#f1f5f9", family="IBM Plex Mono"),
 ),
 )
 fig.update_xaxes(
 gridcolor="#111827", showgrid=True,
 linecolor="#1e2d45", tickfont=dict(size=10),
 )
 fig.update_yaxes(
 gridcolor="#111827", showgrid=True,
 linecolor="#1e2d45", tickfont=dict(size=10),
 tickprefix="$",
 )
 if show_volume:
 fig.update_yaxes(tickprefix="", row=2, col=1)
 return fig
def build_comparison_chart(df1, df2, sym1, sym2):
 # Normalize to 100 for comparison
 n1 = (df1["Close"] / df1["Close"].iloc[0]) * 100
 n2 = (df2["Close"] / df2["Close"].iloc[0]) * 100
 fig = go.Figure()
 fig.add_trace(go.Scatter(
 x=df1.index, y=n1, name=sym1,
 line=dict(color="#3b82f6", width=2),
 fill="tozeroy",
 fillcolor="rgba(59,130,246,0.06)",
 ))
 fig.add_trace(go.Scatter(
 x=df2.index, y=n2, name=sym2,
 line=dict(color="#f59e0b", width=2),
 fill="tozeroy",
 fillcolor="rgba(245,158,11,0.06)",
 ))
 fig.update_layout(
 height=360,
 paper_bgcolor="#080c14",
 plot_bgcolor="#0d1321",
 font=dict(family="IBM Plex Mono", color="#64748b", size=11),
 legend=dict(
 bgcolor="rgba(13,19,33,0.9)",
 bordercolor="#1e2d45",
 borderwidth=1,
 ),
 yaxis_title="Indexed (base=100)",
 margin=dict(l=0, r=0, t=10, b=0),
 hovermode="x unified",
 hoverlabel=dict(
 bgcolor="#111827", bordercolor="#f59e0b",
 font=dict(color="#f1f5f9", family="IBM Plex Mono"),
 ),
 )
 fig.update_xaxes(gridcolor="#111827", linecolor="#1e2d45")
 fig.update_yaxes(gridcolor="#111827", linecolor="#1e2d45")
 return fig
# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
 st.markdown("## &nbsp;StockPulse")
 st.markdown("---")
 st.markdown("**PRIMARY SYMBOL**")
 symbol1 = st.text_input("", value="AAPL", placeholder="e.g. AAPL, TSLA, MSFT",
 key="sym1", label_visibility="collapsed").upper().strip()
 st.markdown("**TIME PERIOD**")
 period_label = st.selectbox("", list(PERIOD_MAP.keys()),
 index=2, key="period", label_visibility="collapsed")
 period = PERIOD_MAP[period_label]
 st.markdown("---")
 st.markdown("**CHART OPTIONS**")
 show_ma = st.checkbox("Moving Average", value=True)
 ma_window = st.slider("MA Window", 5, 50, 20, disabled=not show_ma)
 show_volume = st.checkbox("Volume Bars", value=True)
 st.markdown("---")
 st.markdown("**COMPARISON**")
 compare_on = st.checkbox("Compare with another stock")
 symbol2 = ""
 if compare_on:
 symbol2 = st.text_input("Second Symbol", value="MSFT",
 placeholder="e.g. MSFT").upper().strip()
 st.markdown("---")
 st.caption("Data via yfinance · Refreshed every 5 min")
# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
# Header
col_title, col_badge = st.columns([6, 1])
with col_title:
 st.markdown(
 f'<div class="app-title">Stock<span>Pulse</span> &nbsp;·&nbsp; {symbol1}</div>'
 f'<div class="app-sub">Real-Time Market Analytics · {period_label}</div>',
 unsafe_allow_html=True,
 )
st.markdown("---")
# ── Fetch primary data ────────────────────
try:
 df, info = fetch_stock(symbol1, period)
 if df.empty:
 st.error(f" No data found for **{symbol1}**. Please check the symbol and try again st.stop()
 current_price = df["Close"].iloc[-1]
 prev_price = df["Close"].iloc[-2] if len(df) > 1 else df["Close"].iloc[-1]
 price_change = current_price - prev_price
 pct_change = (price_change / prev_price) * 100
 high_price = df["High"].max()
 low_price = df["Low"].min()
 avg_price = df["Close"].mean()
 total_vol = df["Volume"].sum()
 trend_positive = pct_change >= 0
 company_name = info.get("longName", symbol1)
 currency = info.get("currency", "USD")
 # ── Badge ─────────────────────────────
 with col_badge:
 badge_class = "trend-badge-bull" if trend_positive else "trend-badge-bear"
 badge_text = "▲ BULLISH" if trend_positive else "▼ BEARISH"
 st.markdown(f'<br><div class="{badge_class}">{badge_text}</div>',
 unsafe_allow_html=True)
 # ── KPI Cards ─────────────────────────
 st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)
 k1, k2, k3, k4 = st.columns(4)
 def kpi(col, label, value, delta=None, delta_is_pct=False):
 if delta is None:
 delta_html = ""
 elif delta >= 0:
 sym = "%" if delta_is_pct else ""
 sign = "+"
 delta_html = f'<div class="kpi-delta-pos">▲ {sign}{abs(delta):.2f}{sym}</div>'
 else:
 sym = "%" if delta_is_pct else ""
 delta_html = f'<div class="kpi-delta-neg">▼ {abs(delta):.2f}{sym}</div>'
 col.markdown(f"""
 <div class="kpi-card">
 <div class="kpi-label">{label}</div>
 <div class="kpi-value">{value}</div>
 {delta_html}
 </div>""", unsafe_allow_html=True)
 kpi(k1, "Current Price", format_price(current_price), price_change)
 kpi(k2, "Day Change", format_price(abs(price_change)),
 price_change, delta_is_pct=False)
 kpi(k3, "% Change", format_pct(pct_change), pct_change, delta_is_pct=True)
 kpi(k4, "Period High", format_price(high_price))
 st.markdown("<br>", unsafe_allow_html=True)
 # ── Chart ─────────────────────────────
 st.markdown('<div class="section-header">Price Chart — Candlestick</div>',
 unsafe_allow_html=True)
 fig = build_price_chart(df, symbol1, show_ma, ma_window, show_volume)
 st.plotly_chart(fig, use_container_width=True)
 # ── Stats row ─────────────────────────
 st.markdown('<div class="section-header">Period Statistics</div>',
 unsafe_allow_html=True)
 s1, s2, s3, s4 = st.columns(4)
 def stat(col, label, value):
 col.markdown(f"""
 <div class="stat-card">
 <div class="stat-label">{label}</div>
 <div class="stat-value">{value}</div>
 </div>""", unsafe_allow_html=True)
 stat(s1, "Period High", format_price(high_price))
 stat(s2, "Period Low", format_price(low_price))
 stat(s3, "Avg Close", format_price(avg_price))
 stat(s4, "Total Volume", f"{total_vol:,.0f}")
 st.markdown("<br>", unsafe_allow_html=True)
 # ── Comparison ────────────────────────
 if compare_on and symbol2 and symbol2 != symbol1:
 try:
 df2, info2 = fetch_stock(symbol2, period)
 if df2.empty:
 st.warning(f"No data for {symbol2}")
 else:
 st.markdown(
 f'<div class="section-header">Comparison · {symbol1} vs {symbol2}</div>',
 unsafe_allow_html=True,
 )
 # Align dates
 common_idx = df.index.intersection(df2.index)
 fig_cmp = build_comparison_chart(
 df.loc[common_idx], df2.loc[common_idx], symbol1, symbol2
 )
 st.plotly_chart(fig_cmp, use_container_width=True)
 # Delta summary
 ret1 = ((df.loc[common_idx, "Close"].iloc[-1] /
 df.loc[common_idx, "Close"].iloc[0]) - 1) * 100
 ret2 = ((df2.loc[common_idx, "Close"].iloc[-1] /
 df2.loc[common_idx, "Close"].iloc[0]) - 1) * 100
 c1, c2 = st.columns(2)
 with c1:
 direction = "kpi-delta-pos" if ret1 >= 0 else "kpi-delta-neg"
 st.markdown(f"""
 <div class="stat-card">
 <div class="stat-label">{symbol1} Return ({period_label})</div>
 <div class="stat-value {direction}" style="font-size:1.4rem">
 {format_pct(ret1)}</div>
 </div>""", unsafe_allow_html=True)
 with c2:
 direction2 = "kpi-delta-pos" if ret2 >= 0 else "kpi-delta-neg"
 st.markdown(f"""
 <div class="stat-card">
 <div class="stat-label">{symbol2} Return ({period_label})</div>
 <div class="stat-value {direction2}" style="font-size:1.4rem">
 {format_pct(ret2)}</div>
 </div>""", unsafe_allow_html=True)
 st.markdown("<br>", unsafe_allow_html=True)
 except Exception as e:
 st.warning(f"Could not fetch comparison data for {symbol2}: {e}")
 # ── Raw data expander ──────────────────
 with st.expander(" Raw Market Data"):
 display_df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
 display_df.index = display_df.index.strftime("%Y-%m-%d")
 display_df = display_df.sort_index(ascending=False)
 for col in ["Open", "High", "Low", "Close"]:
 display_df[col] = display_df[col].map(lambda x: f"${x:,.2f}")
 display_df["Volume"] = display_df["Volume"].map(lambda x: f"{x:,.0f}")
 st.dataframe(display_df, use_container_width=True)
 # ── Company info ───────────────────────
 if info.get("longBusinessSummary"):
 with st.expander(" Company Overview"):
 st.markdown(f"""
 <p style="color:#94a3b8; font-size:0.85rem; line-height:1.7;">
 {info['longBusinessSummary'][:600]}…
 </p>""", unsafe_allow_html=True)
 meta_cols = st.columns(3)
 meta = [
 ("Sector", info.get("sector", "—")),
 ("Industry", info.get("industry", "—")),
 ("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B"
 if info.get("marketCap") else "—"),
 ]
 for i, (lbl, val) in enumerate(meta):
 meta_cols[i].markdown(
 f'<div class="stat-label">{lbl}</div>'
 f'<div style="color:#cbd5e1;font-size:0.9rem;font-weight:600">{val}</div>
 unsafe_allow_html=True,
 )
except Exception as e:
 st.error(f" Failed to load data for **{symbol1}**: {str(e)}")
 st.info("Please verify the ticker symbol is correct — e.g. AAPL, TSLA, GOOGL, M
