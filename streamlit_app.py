"""
TalentIQ v4.0 — Redesigned Premium Dashboard
NLP-Based Resume Analyzer & Job Role Recommendation Platform

Complete UI/UX Redesign v4:
- Glassmorphism cards with depth layers
- Unified indigo/lavender design system
- Compact metric strips with animated rings
- Split-panel dashboard with clear hierarchy
- Animated section reveals & micro-interactions
- Streamlined 7-tab layout (merged JD+ATS)
- Responsive grid with CSS custom properties
- Performance-optimized: fewer DOM nodes, lazy charts

Run:  streamlit run streamlit_app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import plotly.graph_objects as go
import time
import math
import html

# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="TalentIQ — AI Resume Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# Design System v4 — Complete CSS
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* ─── Fonts ────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ─── CSS Custom Properties ────────────────────────────────────────── */
:root {
    --primary: #6366F1;
    --primary-light: #818CF8;
    --primary-dark: #4F46E5;
    --primary-bg: #EEF2FF;
    --secondary: #A78BFA;
    --accent: #14B8A6;
    --accent-bg: #F0FDFA;
    --success: #10B981;
    --success-bg: #ECFDF5;
    --warning: #F59E0B;
    --warning-bg: #FFFBEB;
    --danger: #EF4444;
    --danger-bg: #FEF2F2;
    --surface: #FFFFFF;
    --surface-alt: #F8FAFC;
    --surface-raised: #FFFFFF;
    --border: #E2E8F0;
    --border-light: #F1F5F9;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.08);
    --shadow-glow: 0 4px 20px rgba(99,102,241,0.15);
    --transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}

/* ─── Global Reset ─────────────────────────────────────────────────── */
html, body, .main, .stApp {
    background: var(--surface-alt) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}
/* Sidebar toggle icon font */
[data-testid="collapsedControl"] span,
[data-testid="stSidebar"] button[kind="header"] span,
button[kind="headerNoPadding"] span {
    font-family: 'Material Symbols Rounded' !important;
    font-size: 24px !important; overflow: hidden !important;
    width: 24px !important; height: 24px !important;
    display: inline-block !important;
}
.main { padding: 0 !important; }
.block-container {
    padding: 1rem 2.5rem 3rem 2.5rem !important;
    max-width: 100% !important;
}
* { scrollbar-width: thin; scrollbar-color: #CBD5E1 transparent; }
*::-webkit-scrollbar { width: 5px; height: 5px; }
*::-webkit-scrollbar-track { background: transparent; }
*::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }

/* ─── Hide Streamlit Chrome ────────────────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }
button[kind="header"] { visibility: visible !important; }
[data-testid="collapsedControl"] { visibility: visible !important; display: flex !important; }

/* ─── Top Banner ───────────────────────────────────────────────────── */
.top-banner {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 30%, #818CF8 60%, #A78BFA 100%);
    border-radius: var(--radius-xl);
    padding: 1.4rem 2rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 8px 32px rgba(99,102,241,0.25);
    position: relative; overflow: hidden;
    margin: 1.8rem 0 1.4rem 0;
}
.top-banner::before {
    content: ''; position: absolute; top: -60%; right: -10%;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
    border-radius: 50%; pointer-events: none;
}
.top-banner::after {
    content: ''; position: absolute; bottom: -50%; left: 5%;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, transparent 70%);
    border-radius: 50%; pointer-events: none;
}
.banner-left { display: flex; align-items: center; gap: 14px; z-index: 1; }
.banner-logo {
    width: 52px; height: 52px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    border: 1.5px solid rgba(255,255,255,0.25);
    border-radius: var(--radius-md);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
}
.banner-title {
    font-size: 1.8rem; font-weight: 800; color: #FFF;
    letter-spacing: -0.4px; margin: 0;
    text-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.banner-sub {
    font-size: 0.9rem; color: rgba(255,255,255,0.8);
    font-weight: 500; margin: 3px 0 0 0;
}
.banner-right { display: flex; align-items: center; gap: 12px; z-index: 1; }
.banner-pill {
    background: rgba(255,255,255,0.14);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    color: #FFF; font-size: 0.85rem; font-weight: 600;
    padding: 7px 16px; border-radius: var(--radius-sm);
    display: flex; align-items: center; gap: 6px;
}
.banner-dot {
    width: 7px; height: 7px; background: #4ADE80;
    border-radius: 50%; display: inline-block;
    box-shadow: 0 0 6px rgba(74,222,128,0.5);
    animation: pulse-dot 2s ease infinite;
}
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 0 rgba(74,222,128,0.4); }
    50% { box-shadow: 0 0 0 6px rgba(74,222,128,0); }
}

/* ─── Score Ring (CSS only) ────────────────────────────────────────── */
.ring-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 0.6rem 0;
}
.ring-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1rem 1.2rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    position: relative; overflow: hidden;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
/* Bottom KPI row - equal height cards */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 0.6rem 0;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem 1rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    position: relative; overflow: hidden;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow);
    border-color: #C7D2FE;
}
.kpi-card::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
}
.kpi-card.kc-green::after   { background: linear-gradient(90deg,#10B981,#34D399); }
.kpi-card.kc-coral::after   { background: linear-gradient(90deg,#F87171,#FCA5A5); }
.kpi-card.kc-amber::after   { background: linear-gradient(90deg,#F59E0B,#FBBF24); }
.ring-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow);
    border-color: #C7D2FE;
}
.ring-card::after {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
}
.ring-card.rc-indigo::after  { background: linear-gradient(90deg,#6366F1,#818CF8); }
.ring-card.rc-teal::after    { background: linear-gradient(90deg,#14B8A6,#5EEAD4); }
.ring-card.rc-blue::after    { background: linear-gradient(90deg,#3B82F6,#60A5FA); }
.ring-card.rc-purple::after  { background: linear-gradient(90deg,#8B5CF6,#A78BFA); }
.ring-card.rc-amber::after   { background: linear-gradient(90deg,#F59E0B,#FBBF24); }
.ring-card.rc-green::after   { background: linear-gradient(90deg,#10B981,#34D399); }
.ring-card.rc-coral::after   { background: linear-gradient(90deg,#F87171,#FCA5A5); }

.ring-svg { width: 90px; height: 90px; margin: 0 auto 8px auto; display: block; }
.ring-track { fill: none; stroke: #F1F5F9; stroke-width: 6; }
.ring-fill {
    fill: none; stroke-width: 6; stroke-linecap: round;
    transition: stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1);
    transform: rotate(-90deg); transform-origin: center;
}
.ring-pct {
    font-size: 1.05rem; font-weight: 800;
    fill: var(--text-primary);
    dominant-baseline: central; text-anchor: middle;
}
.ring-label {
    font-size: 0.82rem; font-weight: 700; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.5px; margin: 0;
}
.ring-sub {
    font-size: 0.75rem; color: var(--text-muted);
    margin-top: 3px;
}

/* ─── Section Headers ──────────────────────────────────────────────── */
.sec-header {
    display: flex; align-items: center; gap: 12px;
    margin: 1.2rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
}
.sec-icon {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem;
}
.sec-title {
    font-size: 1.2rem; font-weight: 700;
    color: var(--text-primary); margin: 0;
}
.sec-badge {
    margin-left: auto;
    font-size: 0.82rem; font-weight: 700;
    padding: 4px 14px; border-radius: 20px;
}

/* ─── Glass Panel ──────────────────────────────────────────────────── */
.glass-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    margin-bottom: 0;
}
.glass-panel:hover {
    box-shadow: var(--shadow-md);
}
.glass-panel-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 0; padding-bottom: 0;
}
.gp-icon {
    width: 38px; height: 38px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.gp-title {
    font-size: 1.08rem; font-weight: 700;
    color: var(--text-primary); margin: 0;
}
.gp-count {
    margin-left: auto;
    font-size: 0.85rem; font-weight: 600;
    color: var(--primary); background: var(--primary-bg);
    padding: 4px 14px; border-radius: 10px;
}

/* ─── Profile Cards (Candidate Profile) ────────────────────────────── */
.profile-grid {
    display: grid;
    gap: 1.2rem;
}
.profile-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 0;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
}
.profile-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: #C7D2FE;
}
.profile-card-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 1.2rem 1.2rem 1rem 1.2rem;
    border-bottom: 1px solid var(--border-light);
    background: linear-gradient(to bottom, var(--surface) 0%, var(--surface-alt) 100%);
}
.pc-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
    box-shadow: var(--shadow-sm);
}
.pc-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.pc-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.2;
}
.pc-count {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--primary);
    margin: 0;
}
.profile-card-body {
    padding: 1.2rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.pc-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 6px 0;
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.5;
}
.pc-item-secondary {
    font-size: 0.88rem;
    color: var(--text-muted);
}
.pc-dot {
    width: 6px;
    height: 6px;
    background: var(--primary);
    border-radius: 50%;
    margin-top: 8px;
    flex-shrink: 0;
}
.pc-dot-secondary {
    width: 5px;
    height: 5px;
    background: var(--text-muted);
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}
.pc-divider {
    height: 1px;
    background: var(--border-light);
    margin: 8px 0;
}
.pc-section-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 4px 0 6px 0;
}
.pc-highlight {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: var(--primary-bg);
    border-radius: var(--radius-sm);
    margin-bottom: 4px;
}
.pc-highlight-label {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-secondary);
}
.pc-highlight-value {
    font-size: 0.9rem;
    font-weight: 800;
    color: var(--primary);
}
.pc-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.pc-empty {
    color: var(--text-muted);
    font-style: italic;
    text-align: center;
    padding: 20px 0;
    font-size: 0.92rem;
}
.pc-more {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-align: center;
    font-style: italic;
    margin-top: 8px;
}

/* ─── Report Section (rendered via components.html) ─────────────────── */

/* ─── Chips ────────────────────────────────────────────────────────── */
.chip-wrap { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
    display: inline-flex; align-items: center;
    padding: 7px 14px; border-radius: 8px;
    font-size: 0.88rem; font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    cursor: default;
}
.chip:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.chip-default  { background: #EEF2FF; color: #4338CA; border: 1px solid #DDD6FE; }
.chip-matched  { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.chip-missing  { background: #FFF7ED; color: #C2410C; border: 1px solid #FED7AA; }
.chip-soft     { background: #F0F9FF; color: #0369A1; border: 1px solid #BAE6FD; }
.chip-trending { background: #FDF4FF; color: #A21CAF; border: 1px solid #F0ABFC; }

/* ─── Badges ───────────────────────────────────────────────────────── */
.badge {
    display: inline-flex; align-items: center;
    padding: 5px 14px; border-radius: 7px;
    font-weight: 700; font-size: 0.85rem; letter-spacing: 0.2px;
}
.badge-excellent { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.badge-good      { background: #FFFBEB; color: #A16207; border: 1px solid #FDE68A; }
.badge-fair      { background: #FFF7ED; color: #C2410C; border: 1px solid #FED7AA; }
.badge-low       { background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; }

.badge-priority-high   { background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; }
.badge-priority-medium { background: #FFFBEB; color: #A16207; border: 1px solid #FDE68A; }
.badge-priority-low    { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.badge-promotion { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
.badge-lateral   { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
.badge-pivot     { background: #FFFBEB; color: #A16207; border: 1px solid #FDE68A; }

/* ─── Insight Rows ─────────────────────────────────────────────────── */
.insight-row {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 10px 14px; border-radius: var(--radius-sm);
    margin: 10px 0; font-size: 1rem; color: var(--text-secondary);
    line-height: 1.6; border-left: 4px solid transparent;
    transition: background 0.15s ease;
}
.insight-row:hover { background: var(--surface-alt); }
.insight-row.ir-blue   { border-color: #60A5FA; background: #F0F7FF; }
.insight-row.ir-green  { border-color: #34D399; background: #F0FDF8; }
.insight-row.ir-amber  { border-color: #FBBF24; background: #FFFDF0; }
.insight-row.ir-red    { border-color: #F87171; background: #FFF5F5; }

/* ─── Big Score Hero ───────────────────────────────────────────────── */
.score-hero {
    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
    border-radius: var(--radius-lg);
    padding: 1.8rem; text-align: center;
    border: 1px solid #C7D2FE;
}
.score-hero-val {
    font-size: 3.8rem; font-weight: 900; line-height: 1; margin: 0;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.score-hero-label { font-size: 1.05rem; color: var(--primary); font-weight: 600; margin-top: 6px; }
.score-hero-sub { font-size: 0.9rem; color: var(--text-muted); margin-top: 3px; }

/* ─── Breakdown Bars ───────────────────────────────────────────────── */
.bd-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.bd-item {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 14px 16px;
    transition: var(--transition);
}
.bd-item:hover { box-shadow: 0 4px 14px rgba(99,102,241,0.08); }
.bd-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.bd-label { font-size: 0.95rem; font-weight: 600; color: var(--text-secondary); display: flex; align-items: center; gap: 8px; }
.bd-val { font-size: 1.15rem; font-weight: 800; }
.bd-track { height: 8px; background: #F1F5F9; border-radius: 99px; overflow: hidden; }
.bd-fill { height: 100%; border-radius: 99px; transition: width 1s cubic-bezier(0.4,0,0.2,1); }
.bd-foot { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }
.bd-tag { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 3px 10px; border-radius: 99px; }

/* ─── Profile Info Items ───────────────────────────────────────────── */
.pi-item {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 6px 0; font-size: 0.95rem;
}
.pi-item:last-child { }
.pi-bullet { color: var(--primary); font-weight: 800; margin-top: 2px; }
.pi-label { font-weight: 600; color: var(--text-primary); min-width: 130px; }
.pi-value { color: var(--text-secondary); flex: 1; }

/* ─── Check Items ──────────────────────────────────────────────────── */
.ck-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 14px; border-radius: var(--radius-sm);
    margin: 4px 0; font-size: 0.98rem; font-weight: 500;
    transition: background 0.15s;
}
.ck-item:hover { background: var(--surface-alt); }
.ck-pass { color: #047857; }
.ck-fail { color: #DC2626; }

/* ─── Role Match v5 — Redesign ─────────────────────────────────────── */
/* Hero Card */
.rm-hero {
    position: relative;
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 50%, #EEF2FF 100%);
    border: 1.5px solid #E0E7FF;
    border-radius: var(--radius-xl);
    padding: 2rem 2.2rem;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.rm-hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
}
.rm-hero::after {
    content: '';
    position: absolute; top: -80px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,102,241,0.06) 0%, transparent 70%);
    border-radius: 50%; pointer-events: none;
}
.rm-hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    color: #92400E; padding: 6px 16px; border-radius: 99px;
    font-size: 0.82rem; font-weight: 700; border: 1px solid #FCD34D;
    margin-bottom: 1.2rem;
}
.rm-hero-body {
    display: flex; align-items: center; justify-content: space-between;
    gap: 2rem; flex-wrap: wrap; position: relative; z-index: 1;
}
.rm-hero-info { flex: 1; min-width: 260px; }
.rm-hero-cat {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.82rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px; margin-bottom: 0.5rem;
}
.rm-hero-role {
    font-size: 1.9rem; font-weight: 900; color: var(--text-primary);
    line-height: 1.15; margin: 0 0 1rem 0;
    letter-spacing: -0.3px;
}
.rm-hero-target {
    display: inline-flex; align-items: center; gap: 6px;
    background: #ECFDF5; color: #065F46;
    padding: 6px 14px; border-radius: 8px;
    font-size: 0.82rem; font-weight: 700; border: 1px solid #A7F3D0;
}
.rm-hero-score {
    flex-shrink: 0; text-align: center;
}
.rm-hero-pct {
    font-size: 3.2rem; font-weight: 900; line-height: 1;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.rm-hero-pct-label {
    font-size: 0.85rem; font-weight: 600; color: var(--text-muted);
    margin-top: 4px;
}
.rm-hero-breakdown {
    display: grid; grid-template-columns: 1fr;
    gap: 0; margin-top: 0.5rem; padding-top: 0;
    border-top: none;
    position: relative; z-index: 1;
}
.rm-hero-breakdown .rm-bd-item {
    min-height: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
}
.rm-bd-item { text-align: center; }
.rm-bd-val {
    font-size: 1.2rem; font-weight: 800; line-height: 1;
}
.rm-bd-label {
    font-size: 0.72rem; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.4px; margin-top: 4px;
}
.rm-bd-bar {
    height: 4px; background: #F1F5F9; border-radius: 99px;
    margin-top: 6px; overflow: hidden;
}
.rm-bd-fill {
    height: 100%; border-radius: 99px;
    transition: width 1s cubic-bezier(0.4,0,0.2,1);
}
.rm-hero-footer {
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 1rem; padding-top: 1rem;
    border-top: 1px solid var(--border-light);
    position: relative; z-index: 1;
}
.rm-strength-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 16px; border-radius: 8px;
    font-size: 0.88rem; font-weight: 700;
}
.rm-rank-label {
    font-size: 0.85rem; font-weight: 600; color: var(--text-muted);
}

/* Sub Header */
.rm-sub-header {
    margin: 0.2rem 0 0.8rem 0;
}
.rm-sub-title {
    font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0;
}
.rm-sub-desc {
    font-size: 0.82rem; color: var(--text-muted); margin: 2px 0 0 0;
}

/* Role Cards Grid */
.rm-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
}
.rm-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem 1.3rem;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    min-height: 150px;
}
.rm-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow);
    border-color: #C7D2FE;
}
.rm-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--primary-light), var(--secondary));
    opacity: 0; transition: opacity 0.3s;
}
.rm-card:hover::before { opacity: 1; }
.rm-card-top {
    display: flex; align-items: center; justify-content: space-between;
}
.rm-card-rank {
    font-size: 0.82rem; font-weight: 800; color: var(--text-muted);
    background: var(--surface-alt); padding: 3px 10px; border-radius: 6px;
}
.rm-card-cat {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 6px;
    font-size: 0.72rem; font-weight: 700;
}
.rm-card-role {
    font-size: 1.05rem; font-weight: 700; color: var(--text-primary);
    line-height: 1.35; margin: 0;
}
.rm-card-target-tag {
    display: inline-flex; align-items: center; gap: 4px;
    background: #ECFDF5; color: #065F46;
    padding: 3px 10px; border-radius: 6px;
    font-size: 0.72rem; font-weight: 700; border: 1px solid #A7F3D0;
}
.rm-card-score-row {
    display: flex; align-items: center; gap: 12px;
    margin-top: auto; padding-top: 0.7rem;
    border-top: 1px solid var(--border-light);
}
.rm-card-pct {
    font-size: 1.5rem; font-weight: 900;
    line-height: 1; min-width: 55px;
}
.rm-card-bar-wrap { flex: 1; }
.rm-card-bar-track {
    height: 8px; background: #F1F5F9; border-radius: 99px;
    overflow: hidden;
}
.rm-card-bar-fill {
    height: 100%; border-radius: 99px;
    transition: width 1s cubic-bezier(0.4,0,0.2,1);
}
.rm-card-strength {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.3px; margin-top: 4px;
}
/* Mini breakdown row inside card */
.rm-card-bd {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 6px; margin-top: 0.3rem;
}
.rm-card-bd-item { text-align: center; }
.rm-card-bd-val {
    font-size: 0.78rem; font-weight: 800; line-height: 1;
}
.rm-card-bd-label {
    font-size: 0.62rem; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.3px;
}
.rm-card-bd-bar {
    height: 3px; background: #F1F5F9; border-radius: 99px;
    margin-top: 3px; overflow: hidden;
}
.rm-card-bd-fill {
    height: 100%; border-radius: 99px;
}
/* More roles pill */
.rm-more {
    display: flex; align-items: center; justify-content: center;
    gap: 8px; padding: 1rem; margin-top: 0.8rem;
    background: var(--surface-alt); border: 1px dashed var(--border);
    border-radius: var(--radius-lg);
    color: var(--text-muted); font-size: 0.9rem; font-weight: 600;
}

/* ─── Career Path Timeline ─────────────────────────────────────────── */
.cp-container {
    background: white; border: 1px solid #E2E8F0; border-radius: 14px;
    padding: 24px 28px; margin-top: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.cp-item {
    display: flex; gap: 18px; margin-bottom: 28px; position: relative;
}
.cp-item.cp-last { margin-bottom: 0; }

.cp-timeline {
    position: relative; display: flex; flex-direction: column; align-items: center;
    width: 20px; flex-shrink: 0;
}
.cp-node {
    width: 14px; height: 14px; border-radius: 50%;
    background: #FFFFFF; border: 3px solid #6366F1;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.12);
    z-index: 2;
}
.cp-line {
    position: absolute; top: 14px; left: 50%;
    transform: translateX(-50%);
    width: 2px; height: calc(100% + 28px);
    background: linear-gradient(180deg, #C7D2FE 0%, #E0E7FF 100%);
}

.cp-content { flex: 1; }
.cp-from {
    font-size: 0.75rem; font-weight: 600; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px;
}
.cp-to {
    font-size: 1.15rem; font-weight: 700; color: #0F172A;
    margin-bottom: 10px; line-height: 1.3;
}
.cp-meta {
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}
.cp-badge {
    display: inline-block; padding: 5px 12px; border-radius: 6px;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.4px;
}
.cp-badge-green { background: #D1FAE5; color: #065F46; }
.cp-badge-blue { background: #DBEAFE; color: #1E40AF; }
.cp-badge-orange { background: #FED7AA; color: #9A3412; }
.cp-overlap {
    font-size: 0.78rem; color: #64748B; font-weight: 500;
}

/* ─── Action Cards ─────────────────────────────────────────────────── */
.act-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 1rem 1.2rem;
    margin-bottom: 10px; display: flex; align-items: flex-start; gap: 14px;
    transition: var(--transition);
}
.act-card:hover { border-color: #C7D2FE; box-shadow: 0 2px 10px rgba(99,102,241,0.08); }
.act-icon {
    width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem; flex-shrink: 0;
}
.act-icon-high   { background: #FEF2F2; }
.act-icon-medium { background: #FFFBEB; }
.act-icon-low    { background: #ECFDF5; }
.act-body { flex: 1; }
.act-top { display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }
.act-cat {
    font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.4px; color: var(--primary);
    background: var(--primary-bg); padding: 3px 10px; border-radius: 5px;
}
.act-msg { font-size: 1rem; color: #334155; font-weight: 500; line-height: 1.55; margin: 0; }
.act-impact { font-size: 0.88rem; color: var(--text-muted); margin-top: 4px; }

/* ─── Role Row ─────────────────────────────────────────────────────── */
.role-row {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 10px;
    transition: background 0.15s;
}
.role-row:hover { background: var(--surface-alt); }
.role-rank { width: 34px; text-align: center; font-size: 1.05rem; }
.role-name { font-weight: 600; color: var(--text-primary); font-size: 1.02rem; }

/* ─── Hero Section (Landing) ───────────────────────────────────────── */
.hero { text-align: center; padding: 3rem 1rem 2rem 1rem; }
.hero-title {
    font-size: 2.8rem; font-weight: 800; color: var(--text-primary);
    margin: 0 0 0.8rem 0; letter-spacing: -0.5px; line-height: 1.2;
}
.hero-title em {
    font-style: normal;
    background: linear-gradient(135deg,#6366F1,#8B5CF6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-size: 1.15rem; color: var(--text-secondary); font-weight: 400;
    max-width: 680px; margin: 0 auto; line-height: 1.65;
}

/* ─── Feature Cards (Landing) ──────────────────────────────────────── */
.feat-card {
    background: var(--surface); border-radius: var(--radius-lg);
    padding: 1.5rem 1.2rem; border: 1px solid var(--border);
    box-shadow: var(--shadow-sm); text-align: center;
    height: 100%; transition: var(--transition);
}
.feat-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-glow); border-color: #C7D2FE;
}
.feat-icon {
    width: 60px; height: 60px; border-radius: var(--radius-md);
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 1.6rem; margin-bottom: 0.8rem;
}
.feat-title { font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0 0 0.6rem 0; }
.feat-desc { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6; margin: 0; }

/* ─── Tabs ─────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px; background: var(--surface);
    border-radius: var(--radius-md); padding: 4px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm); overflow-x: auto;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    height: 46px; border-radius: var(--radius-sm);
    color: var(--text-secondary); font-weight: 600; font-size: 0.95rem;
    padding: 0 20px; white-space: nowrap;
    border-bottom: none !important; transition: var(--transition);
}
.stTabs [data-baseweb="tab"]:hover { background: var(--surface-alt); color: var(--text-primary); }
.stTabs [aria-selected="true"] {
    background: var(--primary) !important; color: white !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3);
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem; }

/* ─── Buttons ──────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg,#6366F1,#818CF8) !important;
    color: white !important; border: none !important;
    border-radius: var(--radius-md) !important; font-weight: 700 !important;
    padding: 0.85rem 1.8rem !important; font-size: 1rem !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
    background: linear-gradient(135deg,#4F46E5,#6366F1) !important;
}
.stButton > button p, .stButton > button span { color: white !important; }

.stDownloadButton > button {
    background: var(--surface) !important; color: var(--primary) !important;
    border: 1.5px solid #C7D2FE !important; border-radius: var(--radius-md) !important;
    font-weight: 600 !important; transition: var(--transition) !important;
}
.stDownloadButton > button:hover {
    background: var(--primary-bg) !important; border-color: var(--primary) !important;
    transform: translateY(-1px) !important;
}
.stDownloadButton > button p, .stDownloadButton > button span { color: var(--primary) !important; }

/* ─── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.2rem 1rem !important; }

.sb-header {
    display: flex; align-items: center; gap: 10px;
    padding: 0.5rem 0 1rem 0;
    margin-bottom: 1rem;
}
.sb-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg,#6366F1,#818CF8);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3);
}
.sb-name { font-size: 1.15rem; font-weight: 800; color: var(--text-primary); }
.sb-tag { font-size: 0.78rem; color: var(--text-muted); font-weight: 500; }

.sb-section {
    background: var(--surface-alt); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 0.9rem;
    margin-bottom: 0.8rem;
}
.sb-sec-title {
    font-size: 1rem; font-weight: 700; color: var(--text-primary);
    margin: 0 0 3px 0; display: flex; align-items: center; gap: 7px;
}
.sb-sec-desc { font-size: 0.88rem; color: var(--text-muted); margin-bottom: 0.5rem; line-height: 1.45; }

/* ─── Sidebar Inputs ───────────────────────────────────────────────── */
[data-testid="stFileUploader"] section {
    border: 1.5px dashed #C7D2FE !important;
    border-radius: var(--radius-sm) !important; background: #FAFAFF !important;
    padding: 0.7rem !important; transition: var(--transition) !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: var(--primary-light) !important; background: #F5F3FF !important;
}
[data-baseweb="select"] > div {
    border: 1.5px solid var(--border) !important; border-radius: var(--radius-sm) !important;
    background: var(--surface) !important; transition: border-color 0.2s !important;
    font-size: 0.88rem !important;
}
[data-baseweb="select"] > div:hover { border-color: var(--primary-light) !important; }
[data-baseweb="popover"], [data-baseweb="select"] [role="listbox"], [data-baseweb="menu"] { z-index: 999999 !important; }
[data-testid="stSidebar"] [data-baseweb="popover"] { z-index: 999999 !important; }
[data-testid="stSidebar"] .stFileUploader label,
[data-testid="stSidebar"] .stTextArea label,
[data-testid="stSidebar"] .stSelectbox label { font-size: 0.88rem !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stTextArea textarea {
    border: 1.5px solid var(--border) !important; border-radius: var(--radius-sm) !important;
    background: var(--surface) !important; padding: 0.75rem !important;
    font-size: 0.88rem !important; transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--primary-light) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* ─── Progress Bar ─────────────────────────────────────────────────── */
.stProgress > div > div { background: #E8E0F0 !important; border-radius: 6px !important; height: 6px !important; }
.stProgress > div > div > div {
    background: linear-gradient(90deg,#818CF8,#A78BFA) !important;
    border-radius: 6px !important;
}

/* ─── Expander ─────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--surface-alt) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; font-weight: 600 !important;
    color: var(--text-secondary) !important; font-size: 0.84rem !important;
}

/* ─── Typography ───────────────────────────────────────────────────── */
h1,h2,h3,h4,h5,h6 { color: var(--text-primary) !important; font-family: 'Inter', sans-serif !important; }
p, li, span { font-family: 'Inter', sans-serif !important; }

/* ─── Utilities ────────────────────────────────────────────────────── */
.divider { height: 0; background: none; margin: 1.5rem 0; }
.spacer-xs { height: 0.25rem; }
.spacer-sm { height: 0.5rem; }
.spacer-md { height: 0.8rem; }
.spacer-lg { height: 1.2rem; }

/* ─── Responsive ───────────────────────────────────────────────────── */
@media (max-width: 1024px) {
    .ring-row { grid-template-columns: repeat(3, 1fr); }
    .kpi-row { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
    .top-banner { padding: 1rem; border-radius: var(--radius-md); flex-wrap: wrap; gap: 10px; }
    .banner-right { flex-wrap: wrap; }
    .block-container { padding: 0.8rem 1rem 2rem 1rem !important; }
    .ring-row { grid-template-columns: repeat(2, 1fr); }
    .kpi-row { grid-template-columns: repeat(3, 1fr); }
    .ring-card { min-height: 140px; }
    .kpi-card { min-height: 100px; }
    .bd-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
    .ring-row { grid-template-columns: repeat(2, 1fr); }
    .kpi-row { grid-template-columns: 1fr; }
}

/* ─── Role Matches Redesign ───────────────────────────────────────── */
.featured-role-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 2px solid #E2E8F0;
    border-radius: var(--radius-xl);
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(99, 102, 241, 0.12);
    position: relative;
    overflow: hidden;
    transition: var(--transition);
}
.featured-role-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #6366F1, #8B5CF6, #A78BFA);
}
.featured-role-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 50px rgba(99, 102, 241, 0.18);
    border-color: #C7D2FE;
}
.featured-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #FEF3C7, #FDE68A);
    color: #92400E;
    padding: 8px 16px;
    border-radius: 99px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    border: 1px solid #FCD34D;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
}
.featured-role-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    flex-wrap: wrap;
}
.featured-role-info {
    flex: 1;
    min-width: 300px;
}
.featured-role-category {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
}
.featured-role-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 1rem 0;
    line-height: 1.2;
    letter-spacing: -0.5px;
}
.target-badge-featured {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    color: #065F46;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 700;
    border: 1px solid #A7F3D0;
}
.featured-score-ring {
    flex-shrink: 0;
}
.featured-role-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-light);
    flex-wrap: wrap;
    gap: 1rem;
}
.match-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: var(--radius-md);
    font-size: 0.95rem;
    font-weight: 700;
    border: 1px solid currentColor;
    border-opacity: 0.2;
}
.match-rank {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 600;
}
.section-header-minimal {
    margin: 1.5rem 0 1rem 0;
}
.role-match-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.role-match-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
    border-color: #C7D2FE;
}
.role-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}
.role-card-rank {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-muted);
    min-width: 32px;
}
.role-card-category {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid currentColor;
    border-opacity: 0.15;
}
.role-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.4;
    flex: 1;
}
.target-badge-card {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: #ECFDF5;
    color: #065F46;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid #A7F3D0;
}
.role-card-score {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid var(--border-light);
}
.mini-progress-ring {
    display: flex;
    align-items: center;
    justify-content: center;
}
.role-card-strength {
    font-size: 0.85rem;
    font-weight: 700;
    text-align: center;
}
.more-roles-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 1.2rem;
    margin-top: 1rem;
    background: var(--surface-alt);
    border: 1px dashed var(--border);
    border-radius: var(--radius-lg);
    color: var(--text-secondary);
    font-size: 0.95rem;
    font-weight: 600;
}

/* ─── Animations ───────────────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
.anim-up { animation: fadeUp 0.5s ease forwards; }
.anim-fade { animation: fadeIn 0.6s ease forwards; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def _fetch_roles_cached():
    """Fetch roles from API. Only called when API is confirmed reachable."""
    resp = requests.get(f"{API_BASE}/roles", timeout=10)
    resp.raise_for_status()
    roles = resp.json().get("roles", [])
    if not roles:
        raise ValueError("Empty roles list")
    return roles


def fetch_roles():
    """
    Fetch roles with retry logic.
    Never caches empty/failed results — retries until API is ready.
    """
    try:
        return _fetch_roles_cached()
    except Exception:
        # API not ready or failed — don't cache, try direct call
        for attempt in range(3):
            try:
                time.sleep(1)
                resp = requests.get(f"{API_BASE}/roles", timeout=10)
                resp.raise_for_status()
                roles = resp.json().get("roles", [])
                if roles:
                    # Clear the bad cache and re-cache with good data
                    _fetch_roles_cached.clear()
                    return _fetch_roles_cached()
                return roles
            except Exception:
                continue
        return []


def _clr(score: float) -> str:
    if score >= 80: return "#10B981"
    if score >= 60: return "#F59E0B"
    return "#EF4444"


def _label(score: float) -> str:
    if score >= 90: return "Excellent"
    if score >= 80: return "Strong"
    if score >= 70: return "Good"
    if score >= 60: return "Fair"
    if score >= 50: return "Needs Work"
    return "Low"


def _badge_cls(score: float) -> str:
    if score >= 80: return "badge-excellent"
    if score >= 60: return "badge-good"
    if score >= 40: return "badge-fair"
    return "badge-low"


def _color_for_score(score: float) -> str:
    """Return color based on score for progress bars."""
    if score >= 80: return "#10B981"  # Green
    if score >= 60: return "#6366F1"  # Indigo
    if score >= 40: return "#F59E0B"  # Amber
    return "#F87171"  # Red


# ─── SVG Ring Builder ──────────────────────────────────────────────────

def ring_svg(pct: float, color: str, size: int = 90, stroke: int = 6) -> str:
    r = (size - stroke) / 2
    circ = 2 * math.pi * r
    offset = circ * (1 - min(pct, 100) / 100)
    return (
        f'<svg class="ring-svg" viewBox="0 0 {size} {size}">'
        f'<circle class="ring-track" cx="{size/2}" cy="{size/2}" r="{r}"/>'
        f'<circle class="ring-fill" cx="{size/2}" cy="{size/2}" r="{r}" '
        f'stroke="{color}" stroke-dasharray="{circ}" stroke-dashoffset="{offset}"/>'
        f'<text class="ring-pct" x="{size/2}" y="{size/2}">{pct:.0f}%</text>'
        f'</svg>'
    )


def render_ring_card(pct, label, sub, color, accent_cls):
    return (
        f'<div class="ring-card {accent_cls}">'
        f'{ring_svg(pct, color)}'
        f'<div class="ring-label">{label}</div>'
        f'<div class="ring-sub">{sub}</div>'
        f'</div>'
    )


# ─── Chart Builders ───────────────────────────────────────────────────────

def make_radar(categories, values, title=""):
    """Create a modern radar/spider chart matching the UI theme."""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], 
        theta=categories + [categories[0]],
        fill="toself", 
        fillcolor="rgba(99,102,241,0.12)",
        line=dict(color="#6366F1", width=3),
        marker=dict(size=8, color="#6366F1", symbol='circle', line=dict(color='white', width=2)), 
        name="Score",
        hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 100], 
                gridcolor="#E2E8F0",
                gridwidth=1,
                linecolor="#CBD5E1", 
                tickfont=dict(size=11, color="#94A3B8", family="Inter"),
                tickmode='linear',
                tick0=0,
                dtick=20
            ),
            angularaxis=dict(
                gridcolor="#E2E8F0", 
                gridwidth=1,
                linecolor="#CBD5E1",
                tickfont=dict(size=12, color="#475569", family="Inter", weight=600)
            ),
            bgcolor="rgba(255, 255, 255, 0.6)",
        ),
        showlegend=False,
        title=dict(
            text=title, 
            x=0, 
            xanchor='left', 
            font=dict(size=15, color="#475569", family="Inter", weight=700)
        ) if title and title.strip() else {},
        height=500, 
        margin=dict(l=80, r=80, t=60, b=60),
        paper_bgcolor="rgba(0,0,0,0)", 
        font={"family": "Inter, sans-serif"},
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#0F172A")
        )
    )
    return fig


def make_bar(labels, values, title="", color="auto"):
    """Create a modern horizontal bar chart matching the UI theme."""
    bar_colors = []
    for v in values:
        if v >= 80:   bar_colors.append("#10B981")
        elif v >= 60: bar_colors.append("#6366F1")
        elif v >= 40: bar_colors.append("#F59E0B")
        else:         bar_colors.append("#F87171")

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(
            color=bar_colors if color == "auto" else color, 
            cornerradius=6,
            line=dict(width=0)
        ),
        text=[f"{v:.0f}%" for v in values], 
        textposition="outside",
        textfont=dict(color="#475569", size=12, family="Inter", weight=600),
        hovertemplate="<b>%{y}</b><br>Match Score: %{x:.1f}%<extra></extra>",
    ))
    
    fig.update_layout(
        title=dict(
            text=title, 
            x=0, 
            xanchor='left',
            font=dict(size=14, color="#475569", family="Inter", weight=600)
        ) if title and title.strip() else {},
        xaxis=dict(
            range=[0, max(values) * 1.15 if values else 105], 
            showgrid=True,
            gridcolor="#F1F5F9", 
            gridwidth=1,
            linecolor="#E2E8F0", 
            linewidth=1,
            zeroline=False, 
            title="",
            tickfont=dict(size=10, color="#94A3B8", family="Inter"),
            ticksuffix="%",
            showticksuffix="all"
        ),
        yaxis=dict(
            linecolor="#E2E8F0",
            linewidth=1,
            tickfont=dict(size=12, color="#475569", family="Inter", weight=500), 
            automargin=True,
            showgrid=False
        ),
        height=max(220, len(labels) * 42 + 80),
        margin=dict(l=10, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(255, 255, 255, 0.5)",
        font={"family": "Inter, sans-serif"}, 
        bargap=0.25,
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(family="Inter", size=12, color="#0F172A")
        )
    )
    
    # Hide Plotly toolbar and make chart non-editable
    config = {
        'displayModeBar': False,
        'staticPlot': False,
        'responsive': True
    }
    fig.update_layout(
        modebar=dict(remove=['zoom', 'pan', 'select', 'lasso', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale'])
    )
    
    return fig


def make_gauge(value, title, max_val=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 13, "color": "#64748B", "family": "Inter"}},
        number={"suffix": "%", "font": {"size": 22, "color": _clr(value), "family": "Inter"}},
        gauge={
            "axis": {"range": [0, max_val], "tickwidth": 1, "tickcolor": "#E5E7EB",
                     "dtick": 25, "tickfont": {"size": 9, "color": "#94A3B8"}},
            "bar": {"color": _clr(value), "thickness": 0.45},
            "bgcolor": "#F8FAFC", "borderwidth": 0,
            "steps": [
                {"range": [0, 50],  "color": "#FEF2F2"},
                {"range": [50, 70], "color": "#FFFBEB"},
                {"range": [70, 100],"color": "#ECFDF5"},
            ],
            "threshold": {"line": {"color": "#6366F1", "width": 2}, "thickness": 0.7, "value": value},
        },
    ))
    fig.update_layout(
        height=185, margin=dict(l=18, r=18, t=40, b=5),
        paper_bgcolor="rgba(0,0,0,0)", font={"family": "Inter, sans-serif"},
    )
    return fig


# ─── Render Helpers ───────────────────────────────────────────────────────

def chips_html(skills, cls="chip-default"):
    c = "".join(f'<span class="chip {cls}">{s}</span>' for s in skills)
    return f'<div class="chip-wrap">{c}</div>'


def breakdown_html(breakdown: dict) -> str:
    _icons = {"skill": "🎯", "experience": "💼", "semantic": "🔗", "education": "🎓", "format": "📝"}
    _bg = {"skill": "#EEF2FF", "experience": "#FEF3C7", "semantic": "#F0FDFA", "education": "#FDF2F8", "format": "#F5F3FF"}
    # Explicit labels to avoid confusion with other metrics (e.g. "Skill Match" from SkillGapEngine)
    _labels = {
        "skill_score": "Skill Relevance (ATS)",
        "experience_score": "Experience Fit (ATS)",
        "semantic_score": "Semantic Match (ATS)",
    }
    html = '<div class="bd-grid">'
    for k, v in breakdown.items():
        label = _labels.get(k, k.replace("_", " ").title())
        val = v if isinstance(v, (int, float)) else 0
        key_lower = k.lower().split("_")[0]
        icon = _icons.get(key_lower, "📊")
        bg = _bg.get(key_lower, "#F1F5F9")
        if val >= 70:
            grad, col, tag_bg, tag_txt, tag_label = "linear-gradient(90deg,#34D399,#10B981)", "#10B981", "#ECFDF5", "#065F46", "Strong"
        elif val >= 45:
            grad, col, tag_bg, tag_txt, tag_label = "linear-gradient(90deg,#FBBF24,#F59E0B)", "#F59E0B", "#FFFBEB", "#92400E", "Average"
        else:
            grad, col, tag_bg, tag_txt, tag_label = "linear-gradient(90deg,#F87171,#EF4444)", "#EF4444", "#FEF2F2", "#991B1B", "Low"
        html += f'''
        <div class="bd-item">
            <div class="bd-head">
                <div class="bd-label"><span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:6px;background:{bg};font-size:0.7rem;">{icon}</span> {label}</div>
                <div class="bd-val" style="color:{col};">{val:.0f}%</div>
            </div>
            <div class="bd-track"><div class="bd-fill" style="width:{min(val,100):.0f}%;background:{grad};"></div></div>
            <div class="bd-foot">
                <span class="bd-tag" style="background:{tag_bg};color:{tag_txt};">{tag_label}</span>
                <span style="font-size:0.6rem;color:#94A3B8;">0 — 100</span>
            </div>
        </div>'''
    html += '</div>'
    return html


# ═══════════════════════════════════════════════════════════════════════════
# TOP BANNER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="top-banner anim-up">
  <div class="banner-left">
    <div class="banner-logo">🧠</div>
    <div>
      <div class="banner-title">TalentIQ</div>
      <div class="banner-sub">AI Resume Intelligence Platform</div>
    </div>
  </div>
  <div class="banner-right">
    <span class="banner-pill">⚙️ 19 AI Engines</span>
    <span class="banner-pill">🗂️ 86 Roles</span>
    <span class="banner-pill"><span class="banner-dot"></span> Online</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sb-header">
        <div class="sb-logo">🧠</div>
        <div>
            <div class="sb-name">TalentIQ</div>
            <div class="sb-tag">Career Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    st.markdown("""
    <div class="sb-section">
        <div class="sb-sec-title">📄 Resume Upload</div>
        <div class="sb-sec-desc">PDF or DOCX — max 10 MB</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload resume", type=["pdf", "docx"],
        help="Maximum file size: 10 MB", label_visibility="collapsed",
    )

    # Target role
    st.markdown("""
    <div class="sb-section">
        <div class="sb-sec-title">🎯 Target Role</div>
        <div class="sb-sec-desc">Select a role or let AI auto-detect</div>
    </div>
    """, unsafe_allow_html=True)
    roles_data = fetch_roles()
    if roles_data:
        role_names = ["Auto-detect (Best Match)"] + [r["role_name"] for r in roles_data]
    else:
        role_names = ["Auto-detect (Best Match)"]
        st.warning("⚠️ Could not load roles from API. Make sure the backend is running.")
    selected_role = st.selectbox("Select target role", role_names, index=0, label_visibility="collapsed")
    if selected_role == "Auto-detect (Best Match)":
        selected_role = "Auto-detect (best match)"

    # JD
    st.markdown("""
    <div class="sb-section">
        <div class="sb-sec-title">📋 Job Description</div>
        <div class="sb-sec-desc">Optional — paste JD for comparison</div>
    </div>
    """, unsafe_allow_html=True)
    jd_text = st.text_area(
        "Paste job description", height=100,
        placeholder="Paste the job description here for precise matching...",
        label_visibility="collapsed",
    )

    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
    analyze_btn = st.button("🚀  Analyze Resume", type="primary", use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# LANDING STATE
# ═══════════════════════════════════════════════════════════════════════════

if not uploaded_file and not analyze_btn:
    st.markdown("""
    <div class="hero anim-up">
        <div class="hero-title">Welcome to <em>TalentIQ</em></div>
        <div class="hero-desc">
            Upload your resume to unlock AI-powered career insights — skill gap analysis,
            role matching, ATS optimization, and personalized improvement roadmaps.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feat-card anim-up">
            <div class="feat-icon" style="background:#EEF2FF;">📊</div>
            <div class="feat-title">Smart Analysis</div>
            <div class="feat-desc">19 specialized AI engines analyze your resume — from ATS compatibility to skill gaps and career trajectory.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feat-card anim-up" style="animation-delay:0.1s;">
            <div class="feat-icon" style="background:#F0FDFA;">🎯</div>
            <div class="feat-title">Intelligent Matching</div>
            <div class="feat-desc">Semantic matching across 86 engineering & management roles using FAISS vector search technology.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feat-card anim-up" style="animation-delay:0.2s;">
            <div class="feat-icon" style="background:#FFFBEB;">📋</div>
            <div class="feat-title">JD Comparison</div>
            <div class="feat-desc">Compare your resume against job descriptions with keyword analysis and section-by-section scoring.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
    st.info("👈 **Get Started** — Upload your resume in the sidebar and click **Analyze Resume**")


# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

elif analyze_btn and uploaded_file:
    with st.spinner("Analyzing your resume with 19 AI engines..."):
        progress_bar = st.progress(0)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        form_data = {}
        if selected_role != "Auto-detect (best match)":
            form_data["target_role"] = selected_role
        if jd_text and jd_text.strip():
            form_data["jd_text"] = jd_text.strip()
        progress_bar.progress(10)
        try:
            resp = requests.post(f"{API_BASE}/analyze", files=files, data=form_data, timeout=120)
            progress_bar.progress(90)
            resp.raise_for_status()
            report = resp.json()
            progress_bar.progress(100)
            time.sleep(0.3)
            progress_bar.empty()
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to TalentIQ API. Ensure the server is running on port 8000.")
            st.code("python run.py", language="bash")
            st.stop()
        except requests.exceptions.HTTPError as e:
            st.error(f"API Error: {e.response.text}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()
    if "error" in report and len(report) == 1:
        st.error(f"Analysis failed: {report['error']}")
        st.stop()
    st.session_state["report"] = report
    st.session_state["analyzed"] = True


# ═══════════════════════════════════════════════════════════════════════════
# RESULTS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════

if st.session_state.get("analyzed") and "report" in st.session_state:
    report = st.session_state["report"]

    # ── Extract Data ──────────────────────────────────────────────
    meta          = report.get("meta", {})
    target_role   = meta.get("target_role", "N/A")
    jd_source     = meta.get("jd_source", "N/A")
    pipeline_time = meta.get("pipeline_time_seconds", 0)
    engines_count = meta.get("engines_executed", 19)

    ats            = report.get("ats_score", {})
    skill_gap      = report.get("skill_gap", {})
    soft_skill     = report.get("soft_skill", {})
    improvements   = report.get("improvements", {})
    industry       = report.get("industry_alignment", {})
    certifications = report.get("certifications", {})
    explanation    = report.get("explanation", {})
    career         = report.get("career_paths", {})
    role_matches   = report.get("role_matches", {})
    profile        = report.get("candidate_profile", {})
    jd_comp        = report.get("jd_comparison", {})
    ats_sim        = report.get("ats_simulation", {})

    ats_score_val     = ats.get("final_score", 0)
    coverage_pct      = skill_gap.get("coverage_percent", 0)
    jd_match_pct      = jd_comp.get("overall_match_percent", 0)
    ats_sim_score     = ats_sim.get("ats_compatibility_score", 0)
    soft_score        = soft_skill.get("composite_score", 0) if isinstance(soft_skill.get("composite_score"), (int, float)) else 50
    industry_score    = industry.get("alignment_score", 0) if isinstance(industry.get("alignment_score"), (int, float)) else 50
    improvement_score = improvements.get("improvement_score", 0)

    # ══════════════════════════════════════════════════════════════
    # Pipeline + Target + Quality KPIs (above tabs)
    # ══════════════════════════════════════════════════════════════
    display_role = target_role if len(target_role) <= 22 else target_role[:20] + "…"
    st.markdown(f'''
    <div class="kpi-row anim-up">
        <div class="kpi-card kc-green">
            <div style="font-size:2rem;font-weight:800;color:#10B981;margin-bottom:4px;">{pipeline_time:.1f}s</div>
            <div class="ring-label">Pipeline Time</div>
            <div class="ring-sub">{engines_count} engines executed</div>
        </div>
        <div class="kpi-card kc-coral">
            <div style="font-size:1.4rem;font-weight:800;color:#F87171;margin-bottom:4px;">{display_role}</div>
            <div class="ring-label">Target Role</div>
            <div class="ring-sub">{jd_source.replace("_"," ").title()}</div>
        </div>
        <div class="kpi-card kc-amber">
            <div style="font-size:2rem;font-weight:800;color:#F59E0B;margin-bottom:4px;">{improvement_score:.0f}<span style="font-size:1.05rem;color:#94A3B8;">/100</span></div>
            <div class="ring-label">Resume Quality</div>
            <div class="ring-sub">{_label(improvement_score)}</div>
        </div>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════════════════════════

    tabs = st.tabs([
        "📊 Overview",
        "🎯 Role Match",
        "📋 JD & ATS",
        "🔧 Skills & Gaps",
        "📈 Career",
        "💡 Improve",
        "📄 Report",
    ])

    # ─────────────────────────────────────────────────────────
    # TAB 1 — Overview
    # ─────────────────────────────────────────────────────────
    with tabs[0]:
        # ══════════════════════════════════════════════════════════════
        #  SCORE RING STRIP — 3x2 KPI grid at top of Overview
        # ══════════════════════════════════════════════════════════════
        rings = [
            (ats_score_val, "ATS Score",       _label(ats_score_val),    _clr(ats_score_val),    "rc-indigo"),
            (coverage_pct,  "Skill Coverage",  f"{len(skill_gap.get('matched_skills',[]))} found",  _clr(coverage_pct),  "rc-teal"),
            (jd_match_pct,  "JD Match",        _label(jd_match_pct),     _clr(jd_match_pct),     "rc-blue"),
            (ats_sim_score, "ATS Simulation",  _label(ats_sim_score),    _clr(ats_sim_score),    "rc-purple"),
            (soft_score,    "Soft Skills",     _label(soft_score),       _clr(soft_score),       "rc-green"),
            (industry_score,"Industry Fit",    _label(industry_score),   _clr(industry_score),   "rc-amber"),
        ]
        ring_cards = "".join(render_ring_card(p, l, s, c, a) for p, l, s, c, a in rings)
        st.markdown(f'<div class="ring-row anim-up">{ring_cards}</div>', unsafe_allow_html=True)

        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

        ov_l, ov_r = st.columns([1, 1], gap="medium")

        # Left: Radar + Gauges
        with ov_l:
            st.markdown('''
            <div class="glass-panel">
                <div class="glass-panel-header">
                    <div class="gp-icon" style="background:#EEF2FF;">🧬</div>
                    <div class="gp-title">Multi-Dimension Assessment</div>
                </div>
            </div>''', unsafe_allow_html=True)
            radar_cats = ["ATS Score", "Skill Coverage", "JD Match", "ATS Simulation", "Soft Skills", "Industry Fit"]
            radar_vals = [ats_score_val, coverage_pct, jd_match_pct, ats_sim_score, soft_score, industry_score]
            st.plotly_chart(
                make_radar(radar_cats, radar_vals, title="Performance Metrics"), 
                use_container_width=True, 
                key="radar_ov",
                config={'displayModeBar': False, 'staticPlot': False, 'responsive': True}
            )

        # Right: Role Explanation + ATS Breakdown
        with ov_r:
            st.markdown('''
            <div class="glass-panel">
                <div class="glass-panel-header">
                    <div class="gp-icon" style="background:#F0FDFA;">🎯</div>
                    <div class="gp-title">Role Match Explanation</div>
                </div>
            </div>''', unsafe_allow_html=True)

            verdict   = explanation.get("verdict", "")
            reasoning = explanation.get("reasoning", [])
            if verdict:
                st.markdown(f'<div style="margin-top: 1.2rem; font-weight: 700; font-size: 1.05rem;">{verdict}</div>', unsafe_allow_html=True)
            if reasoning:
                colors = ["ir-blue", "ir-green", "ir-amber", "ir-blue", "ir-green", "ir-amber"]
                for i, r in enumerate(reasoning):
                    cls = colors[i % len(colors)]
                    st.markdown(f'<div class="insight-row {cls}">{r}</div>', unsafe_allow_html=True)

        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

        # ATS Breakdown - Full Width
        ats_bd = ats.get("breakdown", {})
        if ats_bd:
            st.markdown('''
            <div class="sec-header">
                <div class="sec-icon" style="background:#EEF2FF;">📊</div>
                <div class="sec-title">ATS Score Breakdown</div>
            </div>''', unsafe_allow_html=True)
            st.markdown(breakdown_html(ats_bd), unsafe_allow_html=True)

        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

        # ── Candidate Profile ──────────────────────────────────
        st.markdown('''
        <div class="sec-header">
            <div class="sec-icon" style="background:#ECFDF5;">👤</div>
            <div class="sec-title">Candidate Profile</div>
        </div>''', unsafe_allow_html=True)

        # Prepare all data first
        edu = profile.get("education", {})
        exp = profile.get("experience", {})
        raw_skills = profile.get("skills_normalized", profile.get("skills_raw", []))
        kw = profile.get("keywords", [])
        
        # Build Education HTML
        if isinstance(edu, dict):
            degrees = edu.get("degrees", [])
            institutions = edu.get("institutions", [])
            deg_count = len(degrees) if degrees else 0
            edu_html = f'''
            <div class="profile-card">
                <div class="profile-card-header">
                    <div class="pc-icon" style="background:#EEF2FF;">🎓</div>
                    <div class="pc-info">
                        <div class="pc-title">Education</div>
                        <div class="pc-count">{deg_count} Degree(s)</div>
                    </div>
                </div>
                <div class="profile-card-body">'''
            if degrees:
                for d in degrees:
                    edu_html += f'<div class="pc-item"><span class="pc-dot"></span><span>{d}</span></div>'
            else:
                edu_html += '<div class="pc-empty">No degrees detected</div>'
            if institutions:
                edu_html += '<div class="pc-divider"></div><div class="pc-section-label">INSTITUTIONS</div>'
                for inst in institutions[:4]:
                    edu_html += f'<div class="pc-item pc-item-secondary"><span class="pc-dot-secondary"></span><span>{inst}</span></div>'
            edu_html += '</div></div>'
        else:
            edu_html = ''

        # Build Experience HTML
        if isinstance(exp, dict):
            max_yrs = exp.get("max_years", 0)
            job_titles = exp.get("job_titles", [])
            exp_html = f'''
            <div class="profile-card">
                <div class="profile-card-header">
                    <div class="pc-icon" style="background:#FEF3C7;">💼</div>
                    <div class="pc-info">
                        <div class="pc-title">Experience</div>
                        <div class="pc-count">{max_yrs} Year(s)</div>
                    </div>
                </div>
                <div class="profile-card-body">
                    <div class="pc-highlight">
                        <span class="pc-highlight-label">Total Experience</span>
                        <span class="pc-highlight-value">{max_yrs} years</span>
                    </div>'''
            if job_titles:
                exp_html += '<div class="pc-divider"></div><div class="pc-section-label">ROLES HELD</div>'
                for jt in job_titles[:5]:
                    exp_html += f'<div class="pc-item"><span class="pc-dot"></span><span>{jt}</span></div>'
                if len(job_titles) > 5:
                    exp_html += f'<div class="pc-more">…and {len(job_titles)-5} more</div>'
            exp_html += '</div></div>'
        else:
            exp_html = ''

        # Build Skills HTML
        skills_count = len(raw_skills)
        sk_html = f'''
        <div class="profile-card">
            <div class="profile-card-header">
                <div class="pc-icon" style="background:#F0FDFA;">🔧</div>
                <div class="pc-info">
                    <div class="pc-title">Technical Skills</div>
                    <div class="pc-count">{skills_count} Skill(s)</div>
                </div>
            </div>
            <div class="profile-card-body">'''
        if raw_skills:
            sk_html += f'<div class="pc-chips">{chips_html(raw_skills[:40])}</div>'
            if len(raw_skills) > 40:
                sk_html += f'<div class="pc-more">…and {len(raw_skills)-40} more</div>'
        else:
            sk_html += '<div class="pc-empty">No skills detected</div>'
        sk_html += '</div></div>'

        # Build Keywords HTML
        if kw:
            kw_html = f'''
            <div class="profile-card">
                <div class="profile-card-header">
                    <div class="pc-icon" style="background:#FDF2F8;">🏷️</div>
                    <div class="pc-info">
                        <div class="pc-title">Domain Keywords</div>
                        <div class="pc-count">{len(kw)} Keyword(s)</div>
                    </div>
                </div>
                <div class="profile-card-body">
                    <div class="pc-chips">{chips_html(kw[:20])}</div>'''
            if len(kw) > 20:
                kw_html += f'<div class="pc-more">…and {len(kw)-20} more</div>'
            kw_html += '</div></div>'
        else:
            kw_html = ''

        # Display in balanced 2x2 grid
        st.markdown('<div class="profile-grid">', unsafe_allow_html=True)
        
        pr_row1_col1, pr_row1_col2 = st.columns(2, gap="medium")
        with pr_row1_col1:
            st.markdown(edu_html, unsafe_allow_html=True)
        with pr_row1_col2:
            st.markdown(sk_html, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.2rem 0;"></div>', unsafe_allow_html=True)
        
        pr_row2_col1, pr_row2_col2 = st.columns(2, gap="medium")
        with pr_row2_col1:
            st.markdown(exp_html, unsafe_allow_html=True)
        with pr_row2_col2:
            if kw_html:
                st.markdown(kw_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────
    # TAB 2 — Role Matching (v5 Redesign — Pure Markdown)
    # ─────────────────────────────────────────────────────────
    with tabs[1]:
        top_roles = role_matches.get("top_roles", [])
        if top_roles:
            # ── Helpers ──
            def _match_strength(score):
                if score >= 70: return ("Excellent", "#10B981", "#ECFDF5")
                if score >= 50: return ("Good", "#6366F1", "#EEF2FF")
                if score >= 30: return ("Moderate", "#F59E0B", "#FFF7ED")
                return ("Low", "#EF4444", "#FEF2F2")

            def _role_cat(name):
                lo = name.lower()
                if any(x in lo for x in ["engineer", "developer", "programmer", "architect"]):
                    return ("Engineering", "⚙️", "#3B82F6")
                if any(x in lo for x in ["analyst", "data", "bi", "scientist", "ml", "ai"]):
                    return ("Analytics", "📊", "#8B5CF6")
                if any(x in lo for x in ["manager", "lead", "director", "head"]):
                    return ("Leadership", "👔", "#EC4899")
                if any(x in lo for x in ["designer", "ux", "ui", "creative"]):
                    return ("Design", "🎨", "#F59E0B")
                return ("General", "💼", "#6B7280")

            # ═══════════════════════════════════════════════
            # Hero — #1 Best Match
            # ═══════════════════════════════════════════════
            top = top_roles[0]
            t_score = top["score"] * 100
            is_target_top = target_role.lower() == top["role_name"].lower()
            s_label, s_color, s_bg = _match_strength(t_score)
            c_name, c_icon, c_color = _role_cat(top["role_name"])

            target_tag = '<div class="rm-hero-target">🎯 Your Target Role</div>' if is_target_top else ''

            # Breakdown metrics (compact, derived from overall match)
            bd_overall = int(t_score)

            hero_html = f'''<div class="rm-hero">
<div class="rm-hero-badge">⭐ Best Match</div>
<div class="rm-hero-body">
<div class="rm-hero-info">
<div class="rm-hero-cat" style="color:{c_color};">{c_icon} {html.escape(c_name)}</div>
<div class="rm-hero-role">{html.escape(top["role_name"])}</div>
{target_tag}
</div>
<div class="rm-hero-score">
<div class="rm-hero-pct">{t_score:.0f}%</div>
<div class="rm-hero-pct-label">Match Score</div>
</div>
</div>
<div class="rm-hero-footer">
<div class="rm-strength-badge" style="background:{s_bg};color:{s_color};">● {s_label} Match</div>
<div class="rm-rank-label">#1 of {len(top_roles)} matched roles</div>
</div>

<div class="rm-hero-breakdown">
    <div class="rm-card-score-row" style="border-top:none; padding-top:0;">
        <div class="rm-card-bar-wrap">
            <div class="rm-card-bar-track"><div class="rm-card-bar-fill" style="width:{bd_overall}%;background:linear-gradient(90deg,{s_color},{s_color}88);"></div></div>
        </div>
    </div>
</div>

</div>'''
            st.markdown(hero_html, unsafe_allow_html=True)

            # ═══════════════════════════════════════════════
            # Grid — Remaining Role Cards
            # ═══════════════════════════════════════════════
            remaining = top_roles[1:13]
            if remaining:
                st.markdown('''<div class="rm-sub-header"><div class="rm-sub-title">More Career Opportunities</div><div class="rm-sub-desc">Explore other roles aligned with your profile</div></div>''', unsafe_allow_html=True)

                cards_html = '<div class="rm-grid">'
                for idx, role in enumerate(remaining):
                    rank = idx + 2
                    sc = role["score"] * 100
                    sl, scol, sbg = _match_strength(sc)
                    cn, ci, cc = _role_cat(role["role_name"])
                    is_target = target_role.lower() == role["role_name"].lower()

                    rank_icon = "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                    tgt_html = '<div class="rm-card-target-tag">🎯 Target</div>' if is_target else ''

                    cards_html += f'''<div class="rm-card"> 
<div class="rm-card-top">
<span class="rm-card-rank">{rank_icon}</span>
<span class="rm-card-cat" style="background:{cc}12;color:{cc};">{ci} {html.escape(cn)}</span>
</div>
<div class="rm-card-role">{html.escape(role["role_name"])}</div>
{tgt_html}
<div class="rm-card-score-row">
<div class="rm-card-pct" style="color:{scol};">{sc:.0f}%</div>
<div class="rm-card-bar-wrap">
<div class="rm-card-bar-track"><div class="rm-card-bar-fill" style="width:{sc:.0f}%;background:linear-gradient(90deg,{scol},{scol}88);"></div></div>
<div class="rm-card-strength" style="color:{scol};">{sl}</div>
</div>
</div>
</div>'''

                cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)

            # Show overflow indicator
            if len(top_roles) > 13:
                extra = len(top_roles) - 13
                st.markdown(f'<div class="rm-more">+{extra} more role{"s" if extra > 1 else ""} matched to your profile</div>', unsafe_allow_html=True)
        else:
            st.info("No role matching data available.")

    # ─────────────────────────────────────────────────────────
    # TAB 3 — JD & ATS Analysis (Complete Redesign)
    # ─────────────────────────────────────────────────────────
    with tabs[2]:
        if jd_comp or ats_sim:
            # Extract all data — use the SAME scores as the Overview tab
            overall = jd_match_pct  # from overview: jd_comp.get("overall_match_percent", 0)
            matched_kw = jd_comp.get("matched_keywords", []) if jd_comp else []
            missing_kw = jd_comp.get("missing_keywords", []) if jd_comp else []
            section_scores = jd_comp.get("section_scores", {}) if jd_comp else {}
            
            ats_compat = ats_sim_score  # from overview: ats_sim.get("ats_compatibility_score", 0)
            kw_report = ats_sim.get("keyword_report", {}) if ats_sim else {}
            sections_complete = ats_sim.get("section_completeness", {}) if ats_sim else {}
            readability = ats_sim.get("readability", {}) if ats_sim else {}
            risks = ats_sim.get("formatting_risks", []) if ats_sim else []
            alerts = ats_sim.get("alerts", []) if ats_sim else []
            
            # Calculate combined score using same values as overview
            combined_score = (overall + ats_compat) / 2 if (overall and ats_compat) else (overall or ats_compat)
            
            # Determine grade
            def get_grade(score):
                if score >= 90: return ("A+", "#10B981", "Exceptional")
                elif score >= 80: return ("A", "#10B981", "Excellent")
                elif score >= 70: return ("B+", "#6366F1", "Very Good")
                elif score >= 60: return ("B", "#6366F1", "Good")
                elif score >= 50: return ("C+", "#F59E0B", "Average")
                elif score >= 40: return ("C", "#F59E0B", "Below Average")
                else: return ("D", "#EF4444", "Needs Work")
            
            grade, grade_color, grade_label = get_grade(combined_score)
            
            # ═══════════════════════════════════════════════════════════
            # TOP SECTION: Score Dashboard with 3 Metric Cards
            # ═══════════════════════════════════════════════════════════
            
            score_dashboard_html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                    .dashboard {{
                        display: grid;
                        grid-template-columns: 1fr 2fr 1fr;
                        gap: 1.5rem;
                        padding: 1rem 0;
                    }}
                    .metric-card {{
                        background: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 16px;
                        padding: 1.5rem;
                        text-align: center;
                        position: relative;
                        overflow: hidden;
                    }}
                    .metric-card::before {{
                        content: '';
                        position: absolute;
                        top: 0; left: 0; right: 0;
                        height: 3px;
                    }}
                    .card-jd::before {{ background: linear-gradient(90deg, #6366F1, #8B5CF6); }}
                    .card-grade::before {{ background: linear-gradient(90deg, #F59E0B, #FBBF24); }}
                    .card-ats::before {{ background: linear-gradient(90deg, #10B981, #34D399); }}
                    
                    .metric-label {{ font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }}
                    .metric-value {{ font-size: 2.5rem; font-weight: 800; line-height: 1; margin-bottom: 0.25rem; }}
                    .metric-sub {{ font-size: 0.85rem; color: #6B7280; font-weight: 500; }}
                    
                    .grade-card {{
                        background: linear-gradient(135deg, #FEFCE8 0%, #FEF9C3 100%);
                        border: 2px solid #FDE68A;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                    }}
                    .grade-value {{ font-size: 4rem; font-weight: 900; color: {grade_color}; line-height: 1; }}
                    .grade-label {{ font-size: 1rem; font-weight: 700; color: {grade_color}; margin-top: 0.5rem; }}
                    
                    .ring-container {{ position: relative; width: 100px; height: 100px; margin: 0 auto 0.75rem; }}
                </style>
            </head>
            <body>
                <div class="dashboard">
                    <div class="metric-card card-jd">
                        <div class="metric-label">JD Match</div>
                        <div class="ring-container">
                            <svg width="100" height="100" viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#E5E7EB" stroke-width="8"/>
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#6366F1" stroke-width="8"
                                        stroke-dasharray="{overall * 2.51} 251" 
                                        stroke-linecap="round" 
                                        transform="rotate(-90 50 50)"/>
                                <text x="50" y="55" text-anchor="middle" font-size="20" font-weight="800" fill="#1F2937">{overall:.0f}%</text>
                            </svg>
                        </div>
                        <div class="metric-sub">Resume vs Job Description</div>
                    </div>
                    
                    <div class="metric-card grade-card">
                        <div class="metric-label">Overall Grade</div>
                        <div class="grade-value">{grade}</div>
                        <div class="grade-label">{grade_label}</div>
                    </div>
                    
                    <div class="metric-card card-ats">
                        <div class="metric-label">ATS Simulation</div>
                        <div class="ring-container">
                            <svg width="100" height="100" viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#E5E7EB" stroke-width="8"/>
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#10B981" stroke-width="8"
                                        stroke-dasharray="{ats_compat * 2.51} 251" 
                                        stroke-linecap="round" 
                                        transform="rotate(-90 50 50)"/>
                                <text x="50" y="55" text-anchor="middle" font-size="20" font-weight="800" fill="#1F2937">{ats_compat:.0f}%</text>
                            </svg>
                        </div>
                        <div class="metric-sub">ATS Compatibility Score</div>
                    </div>
                </div>
            </body>
            </html>
            '''
            components.html(score_dashboard_html, height=220)
            
            # ═══════════════════════════════════════════════════════════
            # KEYWORD ANALYSIS - Dual Panel with Visual Indicators
            # ═══════════════════════════════════════════════════════════
            
            total_kw = len(matched_kw) + len(missing_kw)
            match_rate = (len(matched_kw) / total_kw * 100) if total_kw > 0 else 0
            
            # Build matched keywords HTML
            matched_chips = ''.join([f'<span class="kw-chip matched">{kw}</span>' for kw in matched_kw[:20]])
            more_matched = f'<span class="kw-more">+{len(matched_kw) - 20} more</span>' if len(matched_kw) > 20 else ''
            
            # Build missing keywords HTML
            missing_chips = ''.join([f'<span class="kw-chip missing">{kw}</span>' for kw in missing_kw[:15]])
            more_missing = f'<span class="kw-more">+{len(missing_kw) - 15} more</span>' if len(missing_kw) > 15 else ''
            
            keyword_html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                    .kw-section {{
                        background: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 16px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                    }}
                    .kw-header {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        margin-bottom: 1rem;
                        padding-bottom: 1rem;
                        border-bottom: 1px solid #F1F5F9;
                    }}
                    .kw-title-area {{ display: flex; align-items: center; gap: 12px; }}
                    .kw-icon {{
                        width: 40px; height: 40px;
                        border-radius: 10px;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 1.2rem;
                    }}
                    .kw-icon-green {{ background: #ECFDF5; }}
                    .kw-icon-red {{ background: #FEF2F2; }}
                    .kw-title {{ font-size: 1.1rem; font-weight: 700; color: #1F2937; }}
                    .kw-stats {{ display: flex; align-items: center; gap: 1rem; }}
                    .kw-stat {{
                        display: flex; align-items: center; gap: 6px;
                        padding: 6px 14px;
                        border-radius: 99px;
                        font-size: 0.85rem;
                        font-weight: 700;
                    }}
                    .kw-stat-green {{ background: #ECFDF5; color: #047857; }}
                    .kw-stat-red {{ background: #FEF2F2; color: #DC2626; }}
                    .kw-stat-blue {{ background: #EFF6FF; color: #1D4ED8; }}
                    
                    .kw-content {{ display: flex; gap: 1.5rem; }}
                    .kw-panel {{ flex: 1; }}
                    .kw-panel-title {{
                        font-size: 0.75rem;
                        font-weight: 700;
                        color: #6B7280;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                        gap: 6px;
                    }}
                    .kw-chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
                    .kw-chip {{
                        padding: 6px 12px;
                        border-radius: 6px;
                        font-size: 0.85rem;
                        font-weight: 600;
                    }}
                    .kw-chip.matched {{ background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }}
                    .kw-chip.missing {{ background: #FEF2F2; color: #DC2626; border: 1px solid #FECACA; }}
                    .kw-more {{ font-size: 0.8rem; color: #6B7280; font-style: italic; padding: 6px; }}
                    
                    .kw-progress {{
                        margin-top: 1rem;
                        padding-top: 1rem;
                        border-top: 1px solid #F1F5F9;
                    }}
                    .kw-progress-label {{
                        font-size: 0.85rem;
                        font-weight: 600;
                        color: #475569;
                        margin-bottom: 0.5rem;
                        display: flex;
                        justify-content: space-between;
                    }}
                    .kw-progress-bar {{
                        height: 8px;
                        background: #FEE2E2;
                        border-radius: 99px;
                        overflow: hidden;
                    }}
                    .kw-progress-fill {{
                        height: 100%;
                        background: linear-gradient(90deg, #10B981, #34D399);
                        border-radius: 99px;
                        width: {match_rate}%;
                    }}
                </style>
            </head>
            <body>
                <div class="kw-section">
                    <div class="kw-header">
                        <div class="kw-title-area">
                            <div class="kw-icon kw-icon-green">🔑</div>
                            <div class="kw-title">Keyword Analysis</div>
                        </div>
                        <div class="kw-stats">
                            <div class="kw-stat kw-stat-green">✓ {len(matched_kw)} Found</div>
                            <div class="kw-stat kw-stat-red">✗ {len(missing_kw)} Missing</div>
                            <div class="kw-stat kw-stat-blue">{match_rate:.0f}% Match Rate</div>
                        </div>
                    </div>
                    
                    <div class="kw-content">
                        <div class="kw-panel">
                            <div class="kw-panel-title">
                                <span style="color:#10B981;">●</span> Keywords Found in Resume
                            </div>
                            <div class="kw-chips">
                                {matched_chips}
                                {more_matched}
                            </div>
                        </div>
                        <div class="kw-panel">
                            <div class="kw-panel-title">
                                <span style="color:#EF4444;">●</span> Keywords to Add
                            </div>
                            <div class="kw-chips">
                                {missing_chips}
                                {more_missing}
                            </div>
                        </div>
                    </div>
                    
                    <div class="kw-progress">
                        <div class="kw-progress-label">
                            <span>Keyword Coverage</span>
                            <span style="font-weight:800;color:#10B981;">{match_rate:.0f}%</span>
                        </div>
                        <div class="kw-progress-bar">
                            <div class="kw-progress-fill"></div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            '''
            
            # Calculate height based on content
            kw_height = 320 if (len(matched_kw) > 10 or len(missing_kw) > 8) else 280
            components.html(keyword_html, height=kw_height)
            
            # ═══════════════════════════════════════════════════════════
            # SECTION COVERAGE - Horizontal Progress Bars with Icons
            # ═══════════════════════════════════════════════════════════
            
            if section_scores:
                section_icons = {
                    "skills": "💻",
                    "experience": "📈",
                    "education": "🎓",
                    "tools": "🔧",
                    "certifications": "📜",
                    "projects": "🚀"
                }
                # Labels clarified to distinguish from ATS breakdown & overview metrics
                section_display_labels = {
                    "skills": "JD Skills Relevance",
                    "experience": "JD Experience Relevance",
                    "education": "JD Education Relevance",
                    "tools": "JD Tools Relevance",
                    "certifications": "JD Certifications Relevance",
                    "projects": "JD Projects Relevance",
                }
                section_order = ["skills", "experience", "education"]
                
                section_bars_html = ''
                for key in section_order:
                    if key in section_scores:
                        val = section_scores[key]
                        if isinstance(val, dict):
                            val = val.get("relevance_percent", 0)
                        val = max(0, min(100, float(val) if isinstance(val, (int, float)) else 0))
                        
                        # Color based on value
                        if val >= 70:
                            bar_color = "#10B981"
                        elif val >= 50:
                            bar_color = "#6366F1"
                        elif val >= 30:
                            bar_color = "#F59E0B"
                        else:
                            bar_color = "#EF4444"
                        
                        icon = section_icons.get(key, "📊")
                        label = section_display_labels.get(key, key.title())
                        
                        section_bars_html += f'''
                        <div class="sec-row">
                            <div class="sec-info">
                                <span class="sec-icon">{icon}</span>
                                <span class="sec-name">{label}</span>
                            </div>
                            <div class="sec-bar-container">
                                <div class="sec-bar-track">
                                    <div class="sec-bar-fill" style="width:{val}%;background:{bar_color};"></div>
                                </div>
                            </div>
                            <div class="sec-value" style="color:{bar_color};">{val:.0f}%</div>
                        </div>
                        '''
                
                section_html = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                        .section-card {{
                            background: #FFFFFF;
                            border: 1px solid #E2E8F0;
                            border-radius: 16px;
                            padding: 1.5rem;
                        }}
                        .section-title {{
                            font-size: 1.1rem;
                            font-weight: 700;
                            color: #1F2937;
                            margin-bottom: 1.25rem;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                        }}
                        .section-title-icon {{
                            width: 36px; height: 36px;
                            background: #F5F3FF;
                            border-radius: 10px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1.1rem;
                        }}
                        .sec-row {{
                            display: flex;
                            align-items: center;
                            gap: 1rem;
                            padding: 0.75rem 0;
                            border-bottom: 1px solid #F8FAFC;
                        }}
                        .sec-row:last-child {{ border-bottom: none; }}
                        .sec-info {{
                            display: flex;
                            align-items: center;
                            gap: 10px;
                            min-width: 140px;
                        }}
                        .sec-icon {{ font-size: 1.25rem; }}
                        .sec-name {{ font-size: 0.95rem; font-weight: 600; color: #374151; }}
                        .sec-bar-container {{ flex: 1; }}
                        .sec-bar-track {{
                            height: 10px;
                            background: #F1F5F9;
                            border-radius: 99px;
                            overflow: hidden;
                        }}
                        .sec-bar-fill {{
                            height: 100%;
                            border-radius: 99px;
                            transition: width 0.8s ease;
                        }}
                        .sec-value {{
                            font-size: 1rem;
                            font-weight: 800;
                            min-width: 50px;
                            text-align: right;
                        }}
                    </style>
                </head>
                <body>
                    <div class="section-card">
                        <div class="section-title">
                            <div class="section-title-icon">📊</div>
                            JD Section Coverage
                        </div>
                        {section_bars_html}
                    </div>
                </body>
                </html>
                '''
                # Dynamic height based on number of sections
                section_count = len([k for k in section_order if k in section_scores])
                section_height = 100 + (section_count * 52)
                components.html(section_html, height=section_height)
            
            # ═══════════════════════════════════════════════════════════
            # ATS DEEP DIVE - Expandable Sections
            # ═══════════════════════════════════════════════════════════
            
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
            
            # Resume Health Checklist
            if sections_complete or readability:
                checklist_items = ''
                check_count = 0
                total_checks = 0
                
                # Section completeness
                for sec_name, found in sections_complete.items():
                    label = sec_name.replace("_", " ").title()
                    icon = "✓" if found else "✗"
                    color = "#10B981" if found else "#EF4444"
                    bg = "#ECFDF5" if found else "#FEF2F2"
                    if found:
                        check_count += 1
                    total_checks += 1
                    checklist_items += f'<div class="check-item" style="background:{bg};"><span style="color:{color};font-weight:700;">{icon}</span> {label}</div>'
                
                # Readability metrics
                readability_score = readability.get("score", 0)
                bullet_count = readability.get("bullet_count", 0)
                action_verbs = readability.get("action_verb_count", 0)
                quantified = readability.get("quantified_achievements", 0)
                
                health_score = (check_count / total_checks * 100) if total_checks > 0 else 0
                
                health_html = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                        .health-container {{
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            gap: 1rem;
                        }}
                        .health-card {{
                            background: #FFFFFF;
                            border: 1px solid #E2E8F0;
                            border-radius: 16px;
                            padding: 1.25rem;
                        }}
                        .health-title {{
                            font-size: 0.95rem;
                            font-weight: 700;
                            color: #1F2937;
                            margin-bottom: 1rem;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                        }}
                        .health-title-icon {{
                            width: 32px; height: 32px;
                            border-radius: 8px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1rem;
                        }}
                        .check-grid {{
                            display: grid;
                            grid-template-columns: repeat(2, 1fr);
                            gap: 8px;
                        }}
                        .check-item {{
                            padding: 8px 12px;
                            border-radius: 8px;
                            font-size: 0.85rem;
                            font-weight: 500;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                        }}
                        .metric-grid {{
                            display: grid;
                            grid-template-columns: repeat(2, 1fr);
                            gap: 12px;
                        }}
                        .metric-box {{
                            background: #F8FAFC;
                            border-radius: 12px;
                            padding: 1rem;
                            text-align: center;
                        }}
                        .metric-val {{ font-size: 1.5rem; font-weight: 800; color: #1F2937; }}
                        .metric-label {{ font-size: 0.75rem; color: #6B7280; font-weight: 600; margin-top: 4px; }}
                    </style>
                </head>
                <body>
                    <div class="health-container">
                        <div class="health-card">
                            <div class="health-title">
                                <div class="health-title-icon" style="background:#ECFDF5;">✓</div>
                                Resume Checklist ({check_count}/{total_checks})
                            </div>
                            <div class="check-grid">
                                {checklist_items}
                            </div>
                        </div>
                        <div class="health-card">
                            <div class="health-title">
                                <div class="health-title-icon" style="background:#EEF2FF;">📖</div>
                                Readability Metrics
                            </div>
                            <div class="metric-grid">
                                <div class="metric-box">
                                    <div class="metric-val">{readability_score:.0f}%</div>
                                    <div class="metric-label">Readability Score</div>
                                </div>
                                <div class="metric-box">
                                    <div class="metric-val">{bullet_count}</div>
                                    <div class="metric-label">Bullet Points</div>
                                </div>
                                <div class="metric-box">
                                    <div class="metric-val">{action_verbs}</div>
                                    <div class="metric-label">Action Verbs</div>
                                </div>
                                <div class="metric-box">
                                    <div class="metric-val">{quantified}</div>
                                    <div class="metric-label">Quantified Results</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                '''
                # Dynamic height based on number of checklist items
                checklist_count = total_checks
                health_height = max(280, 140 + (checklist_count * 25))
                components.html(health_html, height=health_height)
            
            # Alerts & Risks Section
            if risks or alerts:
                alert_items = ''
                for risk in risks:
                    alert_items += f'<div class="alert-item warning"><span class="alert-icon">⚠️</span><span>{risk}</span></div>'
                for alert in alerts:
                    alert_items += f'<div class="alert-item danger"><span class="alert-icon">🚨</span><span>{alert}</span></div>'
                
                alerts_html = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                        .alerts-card {{
                            background: #FFFFFF;
                            border: 1px solid #E2E8F0;
                            border-radius: 16px;
                            padding: 1.25rem;
                            margin-top: 1rem;
                        }}
                        .alerts-title {{
                            font-size: 0.95rem;
                            font-weight: 700;
                            color: #1F2937;
                            margin-bottom: 1rem;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                        }}
                        .alerts-title-icon {{
                            width: 32px; height: 32px;
                            background: #FEF2F2;
                            border-radius: 8px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1rem;
                        }}
                        .alert-item {{
                            display: flex;
                            align-items: flex-start;
                            gap: 12px;
                            padding: 12px 16px;
                            border-radius: 10px;
                            margin-bottom: 8px;
                            font-size: 0.9rem;
                            line-height: 1.5;
                        }}
                        .alert-item:last-child {{ margin-bottom: 0; }}
                        .alert-item.warning {{ background: #FFFBEB; color: #92400E; border-left: 3px solid #F59E0B; }}
                        .alert-item.danger {{ background: #FEF2F2; color: #991B1B; border-left: 3px solid #EF4444; }}
                        .alert-icon {{ flex-shrink: 0; }}
                    </style>
                </head>
                <body>
                    <div class="alerts-card">
                        <div class="alerts-title">
                            <div class="alerts-title-icon">⚠️</div>
                            Issues to Address ({len(risks) + len(alerts)})
                        </div>
                        {alert_items}
                    </div>
                </body>
                </html>
                '''
                alert_height = 120 + (len(risks) + len(alerts)) * 50
                components.html(alerts_html, height=min(alert_height, 350))
        
        else:
            st.info("No JD comparison data — paste a job description in the sidebar.")

    # ─────────────────────────────────────────────────────────
    # TAB 4 — Skills & Gaps (Complete Redesign)
    # ─────────────────────────────────────────────────────────
    with tabs[3]:
        # Extract all skill data — use the SAME coverage as the Overview tab
        matched_skills = skill_gap.get("matched_skills", [])
        missing_skills = skill_gap.get("missing_skills", [])
        total_skills = len(matched_skills) + len(missing_skills)
        skill_coverage = coverage_pct  # from overview: skill_gap.get("coverage_percent", 0)
        
        detected_soft = soft_skill.get("detected", soft_skill.get("soft_skills", []))
        if isinstance(detected_soft, dict):
            detected_soft = [item for items in detected_soft.values() for item in (items if isinstance(items, list) else [items])]
        
        ia_score = industry_score  # from overview: reuse the same value
        aligned_skills = industry.get("aligned_skills", [])
        trending_skills = industry.get("trending_skills", [])
        
        cert_list = certifications.get("suggestions", certifications.get("certifications", []))
        
        # ═══════════════════════════════════════════════════════════
        # SKILL OVERVIEW DASHBOARD - Hero Stats
        # ═══════════════════════════════════════════════════════════
        
        # Determine skill health status
        if skill_coverage >= 80:
            health_status = "Excellent"
            health_color = "#10B981"
            health_emoji = "🌟"
        elif skill_coverage >= 60:
            health_status = "Good"
            health_color = "#6366F1"
            health_emoji = "👍"
        elif skill_coverage >= 40:
            health_status = "Needs Work"
            health_color = "#F59E0B"
            health_emoji = "⚠️"
        else:
            health_status = "Critical Gap"
            health_color = "#EF4444"
            health_emoji = "🚨"
        
        dashboard_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                .skill-dashboard {{
                    display: grid;
                    grid-template-columns: 1.5fr 1fr 1fr 1fr;
                    gap: 1rem;
                }}
                .stat-card {{
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 16px;
                    padding: 1.25rem;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                .stat-card.featured {{
                    background: linear-gradient(135deg, #FAFAFA 0%, #F5F3FF 100%);
                    border: 2px solid #E0E7FF;
                    display: flex;
                    align-items: center;
                    gap: 1.25rem;
                    text-align: left;
                }}
                .featured-ring {{
                    flex-shrink: 0;
                }}
                .featured-content {{ flex: 1; }}
                .featured-title {{ font-size: 0.75rem; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
                .featured-status {{ font-size: 1.75rem; font-weight: 900; color: {health_color}; line-height: 1; margin-bottom: 4px; }}
                .featured-label {{ font-size: 0.85rem; color: #475569; font-weight: 600; }}
                
                .stat-icon {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
                .stat-value {{ font-size: 2rem; font-weight: 800; color: #1F2937; line-height: 1; }}
                .stat-label {{ font-size: 0.8rem; color: #6B7280; font-weight: 600; margin-top: 0.25rem; }}
                .stat-badge {{
                    display: inline-block;
                    padding: 4px 10px;
                    border-radius: 99px;
                    font-size: 0.7rem;
                    font-weight: 700;
                    margin-top: 0.5rem;
                }}
                .badge-green {{ background: #ECFDF5; color: #047857; }}
                .badge-amber {{ background: #FFFBEB; color: #92400E; }}
                .badge-red {{ background: #FEF2F2; color: #DC2626; }}
            </style>
        </head>
        <body>
            <div class="skill-dashboard">
                <div class="stat-card featured">
                    <div class="featured-ring">
                        <svg width="90" height="90" viewBox="0 0 90 90">
                            <circle cx="45" cy="45" r="38" fill="none" stroke="#E5E7EB" stroke-width="7"/>
                            <circle cx="45" cy="45" r="38" fill="none" stroke="{health_color}" stroke-width="7"
                                    stroke-dasharray="{skill_coverage * 2.39} 239" 
                                    stroke-linecap="round" 
                                    transform="rotate(-90 45 45)"/>
                            <text x="45" y="50" text-anchor="middle" font-size="18" font-weight="800" fill="#1F2937">{skill_coverage:.0f}%</text>
                        </svg>
                    </div>
                    <div class="featured-content">
                        <div class="featured-title">Skill Coverage</div>
                        <div class="featured-status">{health_emoji} {health_status}</div>
                        <div class="featured-label">{len(matched_skills)}/{total_skills} skills matched</div>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">✅</div>
                    <div class="stat-value" style="color:#10B981;">{len(matched_skills)}</div>
                    <div class="stat-label">Skills You Have</div>
                    <div class="stat-badge badge-green">Ready</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">📚</div>
                    <div class="stat-value" style="color:#EF4444;">{len(missing_skills)}</div>
                    <div class="stat-label">Skills to Learn</div>
                    <div class="stat-badge badge-{'red' if len(missing_skills) > 5 else 'amber'}">{('High' if len(missing_skills) > 5 else 'Medium') + ' Priority'}</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">💼</div>
                    <div class="stat-value" style="color:#6366F1;">{ia_score:.0f}%</div>
                    <div class="stat-label">Industry Fit Score</div>
                    <div class="stat-badge badge-{'green' if ia_score >= 60 else 'amber'}">{'Strong' if ia_score >= 60 else 'Growing'}</div>
                </div>
            </div>
        </body>
        </html>
        '''
        components.html(dashboard_html, height=165)
        
        # ═══════════════════════════════════════════════════════════
        # SKILL COMPARISON - Two Column Layout
        # ═══════════════════════════════════════════════════════════
        
        # Build skill chips HTML
        matched_chips = ''.join([f'<div class="skill-chip matched"><span class="chip-icon">✓</span>{skill}</div>' for skill in matched_skills[:15]])
        more_matched = f'<div class="more-indicator">+{len(matched_skills) - 15} more skills</div>' if len(matched_skills) > 15 else ''
        
        missing_chips = ''.join([f'<div class="skill-chip missing"><span class="chip-icon">+</span>{skill}</div>' for skill in missing_skills[:10]])
        more_missing = f'<div class="more-indicator">+{len(missing_skills) - 10} more to learn</div>' if len(missing_skills) > 10 else ''
        
        comparison_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                .compare-container {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 1rem;
                }}
                .compare-panel {{
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 16px;
                    padding: 1.25rem;
                    position: relative;
                }}
                .compare-panel.has {{ border-left: 4px solid #10B981; }}
                .compare-panel.needs {{ border-left: 4px solid #EF4444; }}
                
                .panel-header {{
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 1rem;
                    padding-bottom: 0.75rem;
                    border-bottom: 1px solid #F1F5F9;
                }}
                .panel-title {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                .panel-icon {{
                    width: 36px; height: 36px;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.1rem;
                }}
                .panel-icon.green {{ background: #ECFDF5; }}
                .panel-icon.red {{ background: #FEF2F2; }}
                .panel-label {{ font-size: 1rem; font-weight: 700; color: #1F2937; }}
                .panel-count {{
                    padding: 6px 14px;
                    border-radius: 99px;
                    font-size: 0.85rem;
                    font-weight: 800;
                }}
                .count-green {{ background: #ECFDF5; color: #047857; }}
                .count-red {{ background: #FEF2F2; color: #DC2626; }}
                
                .skill-grid {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }}
                .skill-chip {{
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    padding: 8px 14px;
                    border-radius: 8px;
                    font-size: 0.88rem;
                    font-weight: 600;
                    transition: transform 0.15s;
                }}
                .skill-chip:hover {{ transform: translateY(-2px); }}
                .skill-chip.matched {{
                    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
                    color: #047857;
                    border: 1px solid #A7F3D0;
                }}
                .skill-chip.missing {{
                    background: linear-gradient(135deg, #FEF2F2 0%, #FECACA 100%);
                    color: #DC2626;
                    border: 1px solid #FECACA;
                }}
                .chip-icon {{
                    font-size: 0.75rem;
                    font-weight: 900;
                }}
                .more-indicator {{
                    padding: 8px 14px;
                    font-size: 0.85rem;
                    color: #6B7280;
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            <div class="compare-container">
                <div class="compare-panel has">
                    <div class="panel-header">
                        <div class="panel-title">
                            <div class="panel-icon green">✓</div>
                            <span class="panel-label">Skills You Have</span>
                        </div>
                        <div class="panel-count count-green">{len(matched_skills)}</div>
                    </div>
                    <div class="skill-grid">
                        {matched_chips if matched_chips else '<span style="color:#6B7280;font-size:0.9rem;">No matched skills found</span>'}
                        {more_matched}
                    </div>
                </div>
                
                <div class="compare-panel needs">
                    <div class="panel-header">
                        <div class="panel-title">
                            <div class="panel-icon red">+</div>
                            <span class="panel-label">Skills to Develop</span>
                        </div>
                        <div class="panel-count count-red">{len(missing_skills)}</div>
                    </div>
                    <div class="skill-grid">
                        {missing_chips if missing_chips else '<span style="color:#10B981;font-size:0.9rem;font-weight:600;">🎉 Great! You have all required skills!</span>'}
                        {more_missing}
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        # Dynamic height based on content - tighter calculation
        matched_rows = (min(len(matched_skills), 15) + 3) // 4
        missing_rows = (min(len(missing_skills), 10) + 3) // 4
        max_rows = max(matched_rows, missing_rows, 1)
        comparison_height = 100 + (max_rows * 45)
        components.html(comparison_html, height=comparison_height)
        
        # ═══════════════════════════════════════════════════════════
        # SOFT SKILLS & INDUSTRY INSIGHTS - Combined Section
        # ═══════════════════════════════════════════════════════════
        
        # Build soft skills chips
        soft_chips = ''.join([f'<span class="soft-chip">{skill}</span>' for skill in (detected_soft[:10] if isinstance(detected_soft, list) else [])])
        
        # Build aligned skills chips
        aligned_chips = ''.join([f'<span class="aligned-chip">{skill}</span>' for skill in aligned_skills[:8]])
        
        # Build trending skills chips
        trending_chips = ''.join([f'<span class="trend-chip">🔥 {skill}</span>' for skill in trending_skills[:8]])
        
        insights_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                .insights-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1.5fr;
                    gap: 1rem;
                }}
                .insight-card {{
                    background: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-radius: 16px;
                    padding: 1.25rem;
                }}
                .insight-header {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 1rem;
                }}
                .insight-icon {{
                    width: 36px; height: 36px;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.1rem;
                }}
                .insight-title {{ font-size: 1rem; font-weight: 700; color: #1F2937; }}
                
                .soft-grid {{ display: flex; flex-wrap: wrap; gap: 8px; }}
                .soft-chip {{
                    padding: 8px 14px;
                    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
                    color: #4338CA;
                    border: 1px solid #C7D2FE;
                    border-radius: 8px;
                    font-size: 0.85rem;
                    font-weight: 600;
                }}
                
                .industry-section {{
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }}
                .industry-meter {{
                    background: #F8FAFC;
                    border-radius: 12px;
                    padding: 1rem;
                }}
                .meter-label {{ font-size: 0.85rem; font-weight: 600; color: #475569; margin-bottom: 0.5rem; display: flex; justify-content: space-between; }}
                .meter-track {{
                    height: 10px;
                    background: #E2E8F0;
                    border-radius: 99px;
                    overflow: hidden;
                }}
                .meter-fill {{
                    height: 100%;
                    border-radius: 99px;
                    background: linear-gradient(90deg, #6366F1, #8B5CF6);
                    width: {ia_score}%;
                }}
                
                .skill-section {{ margin-top: 0.75rem; }}
                .skill-section-title {{
                    font-size: 0.75rem;
                    font-weight: 700;
                    color: #6B7280;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 0.5rem;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }}
                .skill-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
                .aligned-chip {{
                    padding: 6px 12px;
                    background: #ECFDF5;
                    color: #047857;
                    border: 1px solid #A7F3D0;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    font-weight: 600;
                }}
                .trend-chip {{
                    padding: 6px 12px;
                    background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
                    color: #C2410C;
                    border: 1px solid #FDBA74;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <div class="insights-grid">
                <div class="insight-card">
                    <div class="insight-header">
                        <div class="insight-icon" style="background:#EEF2FF;">💬</div>
                        <span class="insight-title">Soft Skills Detected</span>
                    </div>
                    <div class="soft-grid">
                        {soft_chips if soft_chips else '<span style="color:#6B7280;font-size:0.9rem;">No soft skills detected</span>'}
                    </div>
                </div>
                
                <div class="insight-card">
                    <div class="insight-header">
                        <div class="insight-icon" style="background:#F0FDF4;">📊</div>
                        <span class="insight-title">Industry Alignment</span>
                    </div>
                    <div class="industry-section">
                        <div class="industry-meter">
                            <div class="meter-label">
                                <span>Market Relevance</span>
                                <span style="font-weight:800;color:#6366F1;">{ia_score:.0f}%</span>
                            </div>
                            <div class="meter-track">
                                <div class="meter-fill"></div>
                            </div>
                        </div>
                        
                        <div class="skill-section">
                            <div class="skill-section-title">
                                <span style="color:#10B981;">●</span> High-Demand Skills You Have
                            </div>
                            <div class="skill-chips">
                                {aligned_chips if aligned_chips else '<span style="color:#6B7280;font-size:0.85rem;">—</span>'}
                            </div>
                        </div>
                        
                        <div class="skill-section">
                            <div class="skill-section-title">
                                <span style="color:#F97316;">●</span> Trending in Industry
                            </div>
                            <div class="skill-chips">
                                {trending_chips if trending_chips else '<span style="color:#6B7280;font-size:0.85rem;">—</span>'}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        # Calculate insight height based on content - tighter
        soft_rows = (len(detected_soft) + 3) // 4 if isinstance(detected_soft, list) else 1
        aligned_rows = (len(aligned_skills) + 5) // 6 if aligned_skills else 0
        trending_rows = (len(trending_skills) + 5) // 6 if trending_skills else 0
        insights_height = 185 + (soft_rows * 32) + (aligned_rows * 32) + (trending_rows * 40)
        insights_height = max(insights_height, 260) if (aligned_skills or trending_skills) else max(insights_height, 160)
        components.html(insights_html, height=insights_height)
        
        # ═══════════════════════════════════════════════════════════
        # CERTIFICATION ROADMAP - Modern Card Layout
        # ═══════════════════════════════════════════════════════════
        
        if isinstance(cert_list, list) and cert_list:
            cert_cards = ''
            for i, cert in enumerate(cert_list[:6]):
                if isinstance(cert, dict):
                    name = cert.get("name", cert.get("certification", ""))
                    provider = cert.get("provider", "")
                    skill = cert.get("for_skill", cert.get("skill", ""))
                    
                    # Assign priority based on position
                    if i < 2:
                        priority = "high"
                        priority_color = "#EF4444"
                        priority_bg = "#FEF2F2"
                    elif i < 4:
                        priority = "medium"
                        priority_color = "#F59E0B"
                        priority_bg = "#FFFBEB"
                    else:
                        priority = "optional"
                        priority_color = "#6B7280"
                        priority_bg = "#F3F4F6"
                    
                    cert_cards += f'''
                    <div class="cert-card">
                        <div class="cert-priority" style="background:{priority_bg};color:{priority_color};">{priority.upper()}</div>
                        <div class="cert-content">
                            <div class="cert-name">{name}</div>
                            <div class="cert-provider">{provider}</div>
                        </div>
                        <div class="cert-skill">
                            <span class="skill-tag">For: {skill}</span>
                        </div>
                    </div>
                    '''
            
            cert_html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ font-family: 'Inter', -apple-system, sans-serif; background: transparent; }}
                    .cert-section {{
                        background: #FFFFFF;
                        border: 1px solid #E2E8F0;
                        border-radius: 16px;
                        padding: 1.25rem;
                    }}
                    .cert-header {{
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        margin-bottom: 1rem;
                        padding-bottom: 0.75rem;
                        border-bottom: 1px solid #F1F5F9;
                    }}
                    .cert-icon {{
                        width: 36px; height: 36px;
                        background: #FDF4FF;
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.1rem;
                    }}
                    .cert-title {{ font-size: 1rem; font-weight: 700; color: #1F2937; }}
                    
                    .cert-grid {{
                        display: grid;
                        grid-template-columns: repeat(3, 1fr);
                        gap: 12px;
                    }}
                    .cert-card {{
                        background: #FAFAFA;
                        border: 1px solid #E2E8F0;
                        border-radius: 12px;
                        padding: 1rem;
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                        transition: transform 0.15s, box-shadow 0.15s;
                    }}
                    .cert-card:hover {{
                        transform: translateY(-3px);
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    }}
                    .cert-priority {{
                        display: inline-block;
                        padding: 4px 10px;
                        border-radius: 6px;
                        font-size: 0.65rem;
                        font-weight: 800;
                        letter-spacing: 0.5px;
                        width: fit-content;
                    }}
                    .cert-content {{ flex: 1; }}
                    .cert-name {{
                        font-size: 0.92rem;
                        font-weight: 700;
                        color: #1F2937;
                        line-height: 1.3;
                        margin-bottom: 4px;
                    }}
                    .cert-provider {{
                        font-size: 0.8rem;
                        color: #6B7280;
                    }}
                    .cert-skill {{
                        padding-top: 8px;
                        border-top: 1px solid #E5E7EB;
                    }}
                    .skill-tag {{
                        display: inline-block;
                        padding: 4px 10px;
                        background: #ECFDF5;
                        color: #047857;
                        border-radius: 6px;
                        font-size: 0.75rem;
                        font-weight: 600;
                    }}
                </style>
            </head>
            <body>
                <div class="cert-section">
                    <div class="cert-header">
                        <div class="cert-icon">🏆</div>
                        <span class="cert-title">Recommended Certifications</span>
                    </div>
                    <div class="cert-grid">
                        {cert_cards}
                    </div>
                </div>
            </body>
            </html>
            '''
            cert_count = min(len(cert_list), 6)
            cert_rows = (cert_count + 2) // 3
            cert_height = 100 + (cert_rows * 180)
            components.html(cert_html, height=cert_height)

    # ─────────────────────────────────────────────────────────
    # TAB 5 — Career Path
    # ─────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('''
        <div class="glass-panel">
            <div class="glass-panel-header">
                <div class="gp-icon" style="background:#ECFDF5;">📈</div>
                <div class="gp-title">Career Progression Paths</div>
            </div>
        </div>''', unsafe_allow_html=True)

        paths = career.get("paths", career.get("career_paths", []))
        if isinstance(paths, list) and paths:
            # Build the timeline HTML
            timeline_html = ''
            for idx, path in enumerate(paths):
                if isinstance(path, dict):
                    from_role  = html.escape(str(path.get("from_role", path.get("current", ""))))
                    to_role    = html.escape(str(path.get("to_role", path.get("next", ""))))
                    transition = html.escape(str(path.get("transition_type", path.get("type", ""))))
                    overlap = path.get("skill_overlap", 0)
                    
                    # Determine badge color
                    if "promotion" in transition.lower():
                        badge_class = "cp-badge-green"
                    elif "lateral" in transition.lower():
                        badge_class = "cp-badge-blue"
                    else:
                        badge_class = "cp-badge-orange"
                    
                    is_last = idx == len(paths) - 1
                    item_class = "cp-item cp-last" if is_last else "cp-item"
                    line_html = "" if is_last else '<div class="cp-line"></div>'
                    overlap_html = f'<span class="cp-overlap">{overlap:.0f}% match</span>' if overlap else ""
                    
                    timeline_html += f'<div class="{item_class}"><div class="cp-timeline"><div class="cp-node"></div>{line_html}</div><div class="cp-content"><div class="cp-from">From: {from_role}</div><div class="cp-to">{to_role}</div><div class="cp-meta"><span class="cp-badge {badge_class}">{transition}</span>{overlap_html}</div></div></div>'
            
            st.markdown(f'<div class="cp-container">{timeline_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No career path data available for this role.")

        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

        # Role explanation
        st.markdown('''
        <div class="glass-panel">
            <div class="glass-panel-header">
                <div class="gp-icon" style="background:#EEF2FF;">🎯</div>
                <div class="gp-title">Role Match Reasoning</div>
            </div>
        </div>''', unsafe_allow_html=True)
        verdict = explanation.get("verdict", "")
        if verdict:
            st.markdown(f'<div style="margin-top: 1.2rem; font-weight: 700; font-size: 1.05rem;">{html.escape(str(verdict))}</div>', unsafe_allow_html=True)
        detail = explanation.get("detail", explanation.get("reasoning", []))
        if isinstance(detail, list):
            for d in detail:
                st.markdown(f'<div class="insight-row ir-blue">{html.escape(str(d))}</div>', unsafe_allow_html=True)
        elif isinstance(detail, str):
            st.markdown(html.escape(detail))

    # ─────────────────────────────────────────────────────────
    # TAB 6 — Improvements
    # ─────────────────────────────────────────────────────────
    with tabs[5]:
        if improvement_score:
            st.markdown(f'''
            <div class="score-hero anim-up">
                <div class="score-hero-val">{improvement_score:.0f}<span style="font-size:1.5rem;color:#94A3B8;">/100</span></div>
                <div class="score-hero-label">Resume Quality</div>
                <div class="score-hero-sub">{_label(improvement_score)}</div>
            </div>''', unsafe_allow_html=True)
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)

        st.markdown('''
        <div class="sec-header">
            <div class="sec-icon" style="background:#FFFBEB;">💡</div>
            <div class="sec-title">Improvement Suggestions</div>
        </div>''', unsafe_allow_html=True)

        suggestions = improvements.get("suggestions", improvements.get("improvements", []))
        if isinstance(suggestions, list) and suggestions:
            for s in suggestions:
                if isinstance(s, dict):
                    cat      = s.get("category", "General")
                    msg      = s.get("suggestion", s.get("message", ""))
                    priority = s.get("priority", "medium")
                    impact   = s.get("impact", "")
                    p_icon = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                    icon_cls = f"act-icon-{priority}"
                    badge_cls = f"badge-priority-{priority}"
                    impact_h = f'<div class="act-impact">💡 {impact}</div>' if impact else ""
                    st.markdown(f'''
                    <div class="act-card">
                        <div class="act-icon {icon_cls}">{p_icon}</div>
                        <div class="act-body">
                            <div class="act-top">
                                <span class="act-cat">{cat.replace("_"," ").title()}</span>
                                <span class="badge {badge_cls}">{priority.upper()}</span>
                            </div>
                            <p class="act-msg">{msg}</p>
                            {impact_h}
                        </div>
                    </div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f"• {s}")
        elif suggestions:
            st.markdown(str(suggestions))
        else:
            st.success("Your resume looks excellent! No major improvements needed.")

        # Feedback
        feedback_data = report.get("feedback", {})
        if feedback_data:
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            st.markdown('''
            <div class="glass-panel">
                <div class="glass-panel-header">
                    <div class="gp-icon" style="background:#F0FDFA;">💬</div>
                    <div class="gp-title">Overall Feedback</div>
                </div>
            </div>''', unsafe_allow_html=True)
            summary = feedback_data.get("summary", "")
            if summary:
                st.markdown(summary)

    # ─────────────────────────────────────────────────────────
    # TAB 7 — Full Report (Redesigned)
    # ─────────────────────────────────────────────────────────
    with tabs[6]:
        # ---- Prepare data ----
        # Reuse the SAME scores extracted for the Overview tab
        r_ats_score = ats_score_val
        r_skill_coverage = coverage_pct
        r_jd_match = jd_match_pct
        r_ats_sim = ats_sim_score
        r_soft = soft_score
        r_industry = industry_score
        r_quality = improvement_score

        r_matched = skill_gap.get("matched_skills", [])
        r_missing = skill_gap.get("missing_skills", [])
        r_suggestions = improvements.get("suggestions", [])[:8]
        r_top_roles = role_matches.get("top_roles", [])[:5]
        r_career = career.get("paths", [])[:4]
        r_certs = certifications.get("suggestions", certifications.get("recommended", []))[:6]

        r_edu = profile.get("education", {})
        r_exp = profile.get("experience", {})
        r_degrees = r_edu.get("degrees", []) if isinstance(r_edu, dict) else []
        r_institutions = r_edu.get("institutions", []) if isinstance(r_edu, dict) else []
        r_max_yrs = r_exp.get("max_years", 0) if isinstance(r_exp, dict) else 0
        r_titles = r_exp.get("job_titles", []) if isinstance(r_exp, dict) else []

        # ---- Score summary bar ----
        scores_data = [
            ("ATS Score", r_ats_score, _clr(r_ats_score)),
            ("Skill Coverage", r_skill_coverage, _clr(r_skill_coverage)),
            ("JD Match", r_jd_match, _clr(r_jd_match)),
            ("ATS Simulation", r_ats_sim, _clr(r_ats_sim)),
            ("Soft Skills", r_soft, _clr(r_soft)),
            ("Industry Fit", r_industry, _clr(r_industry)),
            ("Resume Quality", r_quality, _clr(r_quality)),
        ]
        score_cells = ""
        for label, val, color in scores_data:
            score_cells += f'''<div class="rpt-score-cell">
                <div class="rpt-score-val" style="color:{color}">{val:.0f}%</div>
                <div class="rpt-score-lbl">{label}</div>
            </div>'''

        # ---- Matched skills chips ----
        matched_chips = ""
        for s in r_matched[:20]:
            matched_chips += f'<span class="rpt-chip rpt-chip-green">{s}</span>'
        if not r_matched:
            matched_chips = '<span class="rpt-empty">None detected</span>'

        # ---- Missing skills chips ----
        missing_chips = ""
        for s in r_missing[:15]:
            name = s if isinstance(s, str) else s.get("skill", "")
            missing_chips += f'<span class="rpt-chip rpt-chip-red">{name}</span>'
        if not r_missing:
            missing_chips = '<span class="rpt-empty">No gaps found</span>'

        # ---- Top roles rows ----
        roles_rows = ""
        for i, role in enumerate(r_top_roles):
            rname = role.get("role_name", "Unknown")
            rscore = role.get("score", 0) * 100
            rcolor = _clr(rscore)
            roles_rows += f'''<div class="rpt-table-row">
                <span class="rpt-rank">#{i+1}</span>
                <span class="rpt-role-name">{rname}</span>
                <span class="rpt-role-score" style="color:{rcolor}">{rscore:.0f}%</span>
            </div>'''
        if not r_top_roles:
            roles_rows = '<div class="rpt-empty">No role matches</div>'

        # ---- Suggestions ----
        suggestion_rows = ""
        for imp in r_suggestions:
            if isinstance(imp, dict):
                msg = imp.get("suggestion", imp.get("message", ""))
                pri = imp.get("priority", "medium")
            else:
                msg = str(imp)
                pri = "medium"
            pri_clr = "#EF4444" if pri == "high" else "#F59E0B" if pri == "medium" else "#6366F1"
            suggestion_rows += f'''<div class="rpt-suggestion">
                <div class="rpt-sug-dot" style="background:{pri_clr}"></div>
                <div class="rpt-sug-text">{msg}</div>
            </div>'''
        if not r_suggestions:
            suggestion_rows = '<div class="rpt-empty">No suggestions</div>'

        # ---- Education & Experience ----
        edu_items = ""
        for d in r_degrees:
            edu_items += f'<div class="rpt-list-item">{d}</div>'
        for inst in r_institutions[:3]:
            edu_items += f'<div class="rpt-list-item rpt-list-secondary">{inst}</div>'
        if not r_degrees:
            edu_items = '<div class="rpt-empty">Not detected</div>'

        title_items = ""
        for t in r_titles[:6]:
            title_items += f'<div class="rpt-list-item">{t}</div>'
        if not r_titles:
            title_items = '<div class="rpt-empty">Not detected</div>'

        # ---- Career paths ----
        career_items = ""
        badge_colors = {
            "Promotion": "badge-green",
            "Lateral Move": "badge-blue",
            "Career Pivot": "badge-orange",
            "Lateral": "badge-blue",
            "Pivot": "badge-orange"
        }
        for idx, p in enumerate(r_career):
            tgt = p.get("to_role", p.get("target_role", ""))
            trans = p.get("transition_type", p.get("timeline", ""))
            from_role = p.get("from_role", "Current Role")
            overlap = p.get("skill_overlap", 0)
            badge_class = badge_colors.get(trans, "badge-blue")
            is_last = idx == len(r_career) - 1
            career_items += f'''<div class="career-path-item {"last-item" if is_last else ""}">
                <div class="career-timeline">
                    <div class="timeline-node"></div>
                    {"" if is_last else '<div class="timeline-line"></div>'}
                </div>
                <div class="career-content">
                    <div class="career-from">From: {from_role}</div>
                    <div class="career-to">{tgt}</div>
                    <div class="career-meta">
                        <span class="career-badge {badge_class}">{trans}</span>
                        {f'<span class="career-overlap">{overlap:.0f}% match</span>' if overlap else ""}
                    </div>
                </div>
            </div>'''
        if not r_career:
            career_items = '<div class="rpt-empty">No paths available</div>'

        # ---- Certifications ----
        cert_items = ""
        for c in r_certs:
            if isinstance(c, dict):
                cname = c.get("certification", c.get("name", ""))
            else:
                cname = str(c)
            if cname:
                cert_items += f'<span class="rpt-chip rpt-chip-purple">{cname}</span>'
        if not cert_items:
            cert_items = '<span class="rpt-empty">None recommended</span>'

        # ---- Compute height ----
        chip_rows_matched = max(len(r_matched[:20]) // 4 + 1, 1)
        chip_rows_missing = max(len(r_missing[:15]) // 4 + 1, 1)
        skills_h = max(chip_rows_matched, chip_rows_missing) * 34 + 80
        roles_h = max(len(r_top_roles), 1) * 44 + 60
        suggestions_h = max(len(r_suggestions), 1) * 48 + 60
        mid_h = max(roles_h, suggestions_h)
        edu_h = max(len(r_degrees) + len(r_institutions[:3]), 1) * 32 + 55
        exp_h = 75
        career_h = max(len(r_career), 1) * 95 + 65
        cert_chip_rows = max(len(r_certs) // 3 + 1, 1)
        cert_h = cert_chip_rows * 36 + 55
        left_h = edu_h + exp_h + 16
        right_h = career_h + cert_h + 16
        detail_h = max(left_h, right_h)
        total_h = 90 + skills_h + 20 + mid_h + 30 + detail_h + 10

        report_html = f'''<!DOCTYPE html>
<html><head><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Inter',sans-serif; background:transparent; color:#1E293B; }}

.rpt-score-bar {{
    display:grid; grid-template-columns:repeat(7,1fr); gap:12px;
    background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px;
    padding:20px 24px; margin-bottom:24px;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}}
.rpt-score-cell {{ text-align:center; }}
.rpt-score-val {{ font-size:1.35rem; font-weight:800; line-height:1.2; }}
.rpt-score-lbl {{ font-size:0.72rem; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px; margin-top:4px; }}

.rpt-section {{
    font-size:0.78rem; font-weight:700; color:#6366F1; text-transform:uppercase;
    letter-spacing:1px; margin:20px 0 10px 0;
    padding-bottom:6px; border-bottom:2px solid #EEF2FF;
}}

.rpt-grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; }}

.rpt-card {{
    background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px;
    padding:16px 20px;
    box-shadow:0 1px 2px rgba(0,0,0,0.03);
}}
.rpt-card-title {{
    font-size:0.82rem; font-weight:700; color:#475569; margin-bottom:12px;
    display:flex; align-items:center; gap:8px;
}}
.rpt-card-title span {{ font-size:1rem; }}

.rpt-chip-wrap {{ display:flex; flex-wrap:wrap; gap:6px; }}
.rpt-chip {{
    display:inline-block; padding:5px 12px; border-radius:6px;
    font-size:0.78rem; font-weight:600;
}}
.rpt-chip-green {{ background:#ECFDF5; color:#047857; }}
.rpt-chip-red {{ background:#FEF2F2; color:#B91C1C; }}
.rpt-chip-purple {{ background:#F5F3FF; color:#6D28D9; }}

.rpt-table-row {{
    display:flex; align-items:center; gap:10px;
    padding:10px 0; border-bottom:1px solid #F1F5F9;
}}
.rpt-table-row:last-child {{ border-bottom:none; }}
.rpt-rank {{
    font-size:0.75rem; font-weight:700; color:#94A3B8;
    width:28px; text-align:center;
}}
.rpt-role-name {{ flex:1; font-size:0.85rem; font-weight:600; color:#334155; }}
.rpt-role-score {{ font-size:0.88rem; font-weight:800; }}

.rpt-suggestion {{
    display:flex; align-items:flex-start; gap:10px;
    padding:10px 0; border-bottom:1px solid #F1F5F9;
}}
.rpt-suggestion:last-child {{ border-bottom:none; }}
.rpt-sug-dot {{
    width:7px; height:7px; border-radius:50%; margin-top:6px; flex-shrink:0;
}}
.rpt-sug-text {{ font-size:0.82rem; color:#475569; line-height:1.5; }}

.rpt-list-item {{
    font-size:0.83rem; color:#334155; padding:6px 0;
    border-bottom:1px solid #F8FAFC; font-weight:500;
}}
.rpt-list-item:last-child {{ border-bottom:none; }}
.rpt-list-secondary {{ color:#94A3B8; font-size:0.78rem; font-weight:400; }}

.career-path-item {{
    display:flex; gap:14px; margin-bottom:16px; position:relative;
}}
.career-path-item.last-item {{ margin-bottom:0; }}

.career-timeline {{
    position:relative; display:flex; flex-direction:column; align-items:center;
    width:20px; flex-shrink:0;
}}
.timeline-node {{
    width:12px; height:12px; border-radius:50%;
    background:#FFFFFF; border:3px solid #6366F1;
    box-shadow:0 0 0 3px rgba(99,102,241,0.1);
    z-index:2;
}}
.timeline-line {{
    position:absolute; top:12px; left:50%;
    transform:translateX(-50%);
    width:2px; height:calc(100% + 16px);
    background:linear-gradient(180deg, #C7D2FE 0%, #E0E7FF 100%);
}}

.career-content {{ flex:1; }}
.career-from {{
    font-size:0.7rem; font-weight:600; color:#94A3B8;
    text-transform:uppercase; letter-spacing:0.3px; margin-bottom:3px;
}}
.career-to {{
    font-size:0.95rem; font-weight:700; color:#0F172A;
    margin-bottom:8px; line-height:1.3;
}}
.career-meta {{
    display:flex; align-items:center; gap:8px; flex-wrap:wrap;
}}
.career-badge {{
    display:inline-block; padding:4px 10px; border-radius:5px;
    font-size:0.7rem; font-weight:700; letter-spacing:0.3px;
}}
.badge-green {{ background:#D1FAE5; color:#065F46; }}
.badge-blue {{ background:#DBEAFE; color:#1E40AF; }}
.badge-orange {{ background:#FED7AA; color:#9A3412; }}
.career-overlap {{
    font-size:0.72rem; color:#64748B; font-weight:500;
}}

.rpt-empty {{ color:#CBD5E1; font-size:0.82rem; font-style:italic; padding:8px 0; }}
</style></head><body>

<div class="rpt-score-bar">{score_cells}</div>

<div class="rpt-section">Skills Analysis</div>
<div class="rpt-grid-2">
    <div class="rpt-card">
        <div class="rpt-card-title"><span>✅</span> Matched Skills ({len(r_matched)})</div>
        <div class="rpt-chip-wrap">{matched_chips}</div>
    </div>
    <div class="rpt-card">
        <div class="rpt-card-title"><span>⚠️</span> Skills to Acquire ({len(r_missing)})</div>
        <div class="rpt-chip-wrap">{missing_chips}</div>
    </div>
</div>

<div class="rpt-grid-2">
    <div class="rpt-card">
        <div class="rpt-card-title"><span>🎯</span> Top Role Matches</div>
        {roles_rows}
    </div>
    <div class="rpt-card">
        <div class="rpt-card-title"><span>💡</span> Key Improvements</div>
        {suggestion_rows}
    </div>
</div>

<div class="rpt-section">Profile Details</div>
<div class="rpt-grid-2">
    <div>
        <div class="rpt-card" style="margin-bottom:12px;">
            <div class="rpt-card-title"><span>🎓</span> Education</div>
            {edu_items}
        </div>
        <div class="rpt-card">
            <div class="rpt-card-title"><span>💼</span> Experience</div>
            <div style="text-align:center;padding:8px 0;">
                <span style="font-size:1.8rem;font-weight:800;color:#F59E0B;">{r_max_yrs}</span>
                <span style="font-size:0.9rem;font-weight:600;color:#94A3B8;"> years</span>
            </div>
        </div>
    </div>
    <div>
        <div class="rpt-card" style="margin-bottom:12px;">
            <div class="rpt-card-title"><span>📈</span> Career Paths</div>
            {career_items}
        </div>
        <div class="rpt-card">
            <div class="rpt-card-title"><span>🏅</span> Recommended Certifications</div>
            <div class="rpt-chip-wrap">{cert_items}</div>
        </div>
    </div>
</div>

</body></html>'''

        components.html(report_html, height=total_h, scrolling=False)

        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])
        with col_dl2:
            st.download_button(
                label="📥  Download Report (JSON)",
                data=json.dumps(report, indent=2, default=str),
                file_name=f"talentiq_report_{target_role.replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True,
            )
        
       


# ── No File Warning ──────────────────────────────────────────────────────

elif analyze_btn and not uploaded_file:
    st.warning("Please upload a resume file in the sidebar first.")
