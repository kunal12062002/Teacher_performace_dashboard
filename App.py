# =====================================================
# myNalanda Dashboard 
# School: Ideal International School
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="myNalanda Dashboard", page_icon="🎓",
                   layout="wide", initial_sidebar_state="expanded")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif !important; }
#MainMenu,footer{ visibility:hidden; }
header{ visibility:visible !important; background:transparent !important; }
.block-container{ padding:1.5rem 2rem !important; max-width:100% !important; }

[data-testid="collapsedControl"]{
    display:flex !important; visibility:visible !important;
    background:#1e293b !important; border:1px solid #334155 !important;
    border-radius:0 8px 8px 0 !important; color:#38bdf8 !important;
    top:50% !important; z-index:9999 !important;
}
[data-testid="collapsedControl"]:hover{ background:#334155 !important; }
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button{
    display:flex !important; visibility:visible !important;
    color:#64748b !important; background:transparent !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover{
    color:#38bdf8 !important; background:rgba(56,189,248,.1) !important; border-radius:6px !important;
}
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%) !important;
    border-right:1px solid #334155;
}
[data-testid="stSidebar"] *{ color:#cbd5e1 !important; }
[data-testid="stSidebar"] .stRadio label{ font-size:13px !important; }

div[data-testid="metric-container"]{
    background:#1e293b; border:1px solid #334155; border-radius:14px;
    padding:16px 18px !important; border-left:4px solid #38bdf8; transition:transform .2s;
}
div[data-testid="metric-container"]:hover{ transform:translateY(-2px); }
div[data-testid="metric-container"] label{
    color:#64748b !important; font-size:10px !important;
    text-transform:uppercase; letter-spacing:.8px;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{
    color:#f1f5f9 !important; font-size:24px !important; font-weight:800 !important;
}
.stSelectbox label{ color:#64748b !important; font-size:11px !important; text-transform:uppercase; }
.stDataFrame{ border:1px solid #334155 !important; border-radius:10px !important; }
.stProgress > div > div{ background-color:#38bdf8 !important; border-radius:20px; }
.stProgress > div{ background-color:#0f172a !important; border-radius:20px; }

.card{
    background:#1e293b; border:1px solid #334155; border-radius:14px;
    padding:18px 20px; margin-bottom:14px;
}
.card-title{
    font-size:11px; font-weight:700; color:#38bdf8;
    text-transform:uppercase; letter-spacing:.8px; margin-bottom:10px;
}
.info-row{
    display:flex; justify-content:space-between; font-size:13px;
    padding:5px 0; border-bottom:1px solid #0f172a; color:#94a3b8;
}
.info-row b{ color:#e2e8f0; }
.sec-title{
    font-size:20px; font-weight:800; color:#f1f5f9;
    padding-bottom:6px; border-bottom:2px solid #38bdf8;
    margin-bottom:20px; display:inline-block;
}
.chart-title{
    font-size:13px; font-weight:700; color:#f1f5f9; margin-bottom:14px;
}
.badge{ display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.badge-red   { background:rgba(239,68,68,.15);  color:#f87171; border:1px solid rgba(239,68,68,.3); }
.badge-yellow{ background:rgba(234,179,8,.15);  color:#facc15; border:1px solid rgba(234,179,8,.3); }
.badge-green { background:rgba(34,197,94,.15);  color:#4ade80; border:1px solid rgba(34,197,94,.3); }
.badge-blue  { background:rgba(56,189,248,.15); color:#38bdf8; border:1px solid rgba(56,189,248,.3); }
.stDownloadButton button{
    background:linear-gradient(90deg,#0284c7,#38bdf8) !important;
    color:#fff !important; border:none !important; border-radius:8px !important; font-weight:600 !important;
}
.login-logo{ text-align:center; margin:40px 0 28px; }
.login-logo .brand{ font-size:32px; font-weight:800; color:#f1f5f9; }
.login-logo .brand span{ color:#38bdf8; }
.login-logo .tagline{ font-size:13px; color:#64748b; margin-top:4px; }
.sidebar-brand{ text-align:center; padding:16px 0 20px; border-bottom:1px solid #334155; margin-bottom:16px; }
.sidebar-brand .name{ font-size:18px; font-weight:800; color:#f1f5f9 !important; }
.sidebar-brand .name span{ color:#38bdf8 !important; }
.sidebar-brand .school{ font-size:10px; color:#64748b !important; margin-top:2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def perf_label(s):
    return "Excellent" if s >= 85 else "Good" if s >= 70 else "Needs Improvement" if s >= 55 else "Poor"

def comp_label(s):
    return "Highly Compliant" if s >= 8 else "Compliant" if s >= 6 else "Partial" if s >= 4 else "Non-Compliant"

def cca_label(s):
    return "Excellent" if s >= 8 else "Good" if s >= 6 else "Needs Improvement" if s >= 4 else "Poor"

def risk_badge(score):
    score = float(score)
    if score >= 3:   return '<span class="badge badge-red">🔴 High Risk</span>'
    elif score >= 2: return '<span class="badge badge-yellow">🟡 Medium</span>'
    elif score >= 1: return '<span class="badge badge-blue">🔵 Low Risk</span>'
    else:            return '<span class="badge badge-green">🟢 Stable</span>'

def dark_layout(height=300, margin=None):
    m = margin or dict(t=40, b=50, l=55, r=20)
    return dict(
        height=height, margin=m,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", size=11, family="DM Sans"),
        hoverlabel=dict(bgcolor="#1e293b", bordercolor="#334155",
                        font=dict(color="#f1f5f9", size=12)),
    )

XAXIS_STYLE = dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b", size=10))
YAXIS_STYLE = dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b", size=10))
LEGEND_STYLE = dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11))

def apply_axes(fig):
    fig.update_xaxes(**XAXIS_STYLE)
    fig.update_yaxes(**YAXIS_STYLE)
    fig.update_layout(legend=LEGEND_STYLE)
    return fig

def ctitle(text):
    st.markdown(f'<p class="chart-title">{text}</p>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
MONTHS = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

def month_year(m):
    """Return correct calendar year for a month in the Indian academic year (Apr 2025 – Mar 2026)."""
    return 2026 if m in ["Jan", "Feb", "Mar"] else 2025

HOD_POOL = [
    "Activity-based learning", "Better assessments", "Parent communication",
    "Use of technology", "Improve lesson planning", "Peer collaboration",
    "Student feedback integration", "Timely report submission",
    "Differentiated instruction", "Professional development", "Class discipline",
    "Regular student counselling"
]

DUTY_PARAMS = [
    ("Academic Board",   "Curriculum & board meetings"),
    ("Exam Portfolio",   "Managing exam papers"),
    ("Admissions",       "New student onboarding"),
    ("Affiliations",     "External board coordination"),
]

@st.cache_data
def generate_data():
    np.random.seed(42)
    first = ["Linda","James","Emily","Robert","Sarah","David","Jessica","Kevin",
             "Patricia","Matthew","Rajesh","Priya","Amit","Sunita","Vikram",
             "Neha","Ravi","Pooja","Arjun","Meena"]
    last  = ["Martinez","Wilson","Johnson","Brown","Taylor","Garcia","Adams","Young",
             "Turner","Evans","Sharma","Verma","Singh","Patel","Gupta",
             "Joshi","Mehta","Rao","Kumar","Shah"]
    subjects = ["Mathematics","Science","English","Social Studies","Computer Science",
                "Physics","Chemistry","Biology","Art","Physical Education"]
    sections = ["Sec A","Sec B","Sec C","Sec D","Sec E"]
    quals    = ["M.Ed","B.Ed","M.Sc B.Ed","MA B.Ed","Ph.D"]

    teachers = []
    for i in range(20):
        rng = np.random.RandomState(i * 7 + 13)
        duties = {p: bool(rng.choice([True, True, False])) for p, _ in DUTY_PARAMS}
        hod_exp = list(np.random.choice(HOD_POOL, size=3, replace=False))
        teachers.append({
            "teacher_id":          f"T{str(i+1).zfill(3)}",
            "teacher_name":        f"{first[i]} {last[i]}",
            "subject":             np.random.choice(subjects),
            "section":             np.random.choice(sections),
            "qualification":       np.random.choice(quals),
            "experience_current":  int(np.random.randint(2, 18)),
            "experience_previous": int(np.random.randint(0, 10)),
            "classes_per_week":    int(np.random.randint(18, 35)),
            "duties":              duties,
            "hod_expectations":    hod_exp,
        })
    tdf = pd.DataFrame(teachers)

    perf = []
    for _, t in tdf.iterrows():
        bd = np.random.uniform(52, 88)   
        bc = np.random.uniform(4.5, 9)   
        ba = np.random.uniform(4.5, 9)   
        for mi, m in enumerate(MONTHS):
            
            bm_val = round(min(100, max(35, bd + np.random.uniform(-3, 3))), 1)

           
            season_boost = 2.0 * np.sin(np.pi * mi / 11)
            curr_val = round(min(100, max(35, bd + np.random.uniform(-8, 8) + season_boost)), 1)

            comp_trend = mi * 0.04   
            comp_val = round(min(10, max(2, bc + np.random.uniform(-0.8, 0.8) + comp_trend)), 1)

            cca_trend = mi * 0.03
            cca_val = round(min(10, max(2, ba + np.random.uniform(-0.8, 0.8) + cca_trend)), 1)

            perf.append({
                "teacher_id":             t.teacher_id,
                "teacher_name":           t.teacher_name,
                "subject":                t.subject,
                "section":                t.section,
                "month":                  m,
                "month_num":              mi + 1,
                "teaching_delivery_bm":   bm_val,
                "teaching_delivery_curr": curr_val,
                "compliance_score":       comp_val,
                "cca_score":              cca_val,
            })
    pdf = pd.DataFrame(perf)

    SUMMER_BREAK = ["May"]
    late = []
    for _, t in tdf.iterrows():
        for mi, m in enumerate(MONTHS):
            if m in SUMMER_BREAK:
                late_val = 0   # school not running — no late data
            else:
                late_val = max(0, int(np.random.poisson(1.5)))
            late.append({
                "teacher_id":   t.teacher_id,
                "teacher_name": t.teacher_name,
                "month":        m,
                "month_num":    mi + 1,
                "late_count":   late_val,
            })
    ldf = pd.DataFrame(late)

    attr_exp = {
        3.0: "Actively job-hunting; high stress reported",
        2.0: "Disengaged; not motivated",
        1.0: "Minor resistance to feedback",
        0.0: "Committed and stable",
    }
    attr = []
    for _, t in tdf.iterrows():
        s = float(np.random.choice([0, 0, 0, 1, 1, 2, 2, 3]))
        total_exp = t.experience_current + t.experience_previous
        
        if s > 0:
            if total_exp >= 25:
                exit_type = np.random.choice(["Voluntary","Involuntary","Retirement","Structural"])
            else:
                exit_type = np.random.choice(["Voluntary","Involuntary","Structural"])
        else:
            exit_type = "None"
        attr.append({
            "teacher_id":            t.teacher_id,
            "teacher_name":          t.teacher_name,
            "attrition_score":       s,
            "attrition_type":        exit_type,
            "attrition_explanation": attr_exp[s],
            "risk_level":            {3:"High", 2:"Medium", 1:"Low", 0:"None"}[int(s)],
        })
    adf = pd.DataFrame(attr)

    cdf = pd.DataFrame([{
        "teacher_id":                  t.teacher_id,
        "training_hours":              int(np.random.randint(8, 50)),
        "training_max":                50,
        "assignment_correction_stars": int(np.random.randint(1, 6)),   
    } for _, t in tdf.iterrows()])

    ccadf = pd.DataFrame([{
        "teacher_id":          t.teacher_id,
        
        "activities_completed": int(np.random.randint(3, 9)),
        "activities_total":     int(np.random.randint(10, 15)),
        "quality":              np.random.choice(["Excellent","Good","Needs Improvement"]),
    } for _, t in tdf.iterrows()])

    aldf = pd.DataFrame([{
        "teacher_id": t.teacher_id,
        "stakeholder": sh,
        "stars": int(np.random.randint(1, 6)),   
    } for _, t in tdf.iterrows() for sh in ["Head","Peer","Student","Parent"]])

    return tdf, pdf, ldf, adf, cdf, ccadf, aldf

tdf, pdf, ldf, adf, cdf, ccadf, aldf = generate_data()


# ─────────────────────────────────────────────────────────────────────────────
# PDF REPORT GENERATOR  
# ─────────────────────────────────────────────────────────────────────────────
def generate_pdf_report(teacher, section, subject, sel_m, bm, curr, comp, cca, overall, risk_level, late_cnt):
    """Generate a simple PDF teacher report using reportlab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                topMargin=2*cm, bottomMargin=2*cm,
                                leftMargin=2*cm, rightMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle('title', parent=styles['Title'],
                                     fontSize=18, textColor=colors.HexColor('#0284c7'),
                                     spaceAfter=6)
        story.append(Paragraph("myNalanda — Teacher Performance Report", title_style))

        sub_style = ParagraphStyle('sub', parent=styles['Normal'],
                                   fontSize=10, textColor=colors.HexColor('#64748b'),
                                   spaceAfter=20)
        story.append(Paragraph(f"Ideal International School  ·  {sel_m} {month_year(sel_m)}  ·  Academic Year 2025–26", sub_style))
        story.append(Spacer(1, 0.3*cm))

        # Data table
        data = [
            ["Metric", "Value"],
            ["Teacher Name",      teacher],
            ["Section",           section],
            ["Subject",           subject],
            ["Month",             sel_m],
            ["Benchmark Score",   f"{bm:.1f}%"],
            ["Actual Score",      f"{curr:.1f}%"],
            ["Compliance",        f"{comp:.1f}/10  ({comp_label(comp)})"],
            ["CCA Score",         f"{cca:.1f}/10  ({cca_label(cca)})"],
            ["Overall Score",     f"{overall:.1f}%  ({perf_label(overall)})"],
            ["Attrition Risk",    risk_level],
            ["Late Arrivals",     str(late_cnt)],
        ]

        table = Table(data, colWidths=[7*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND',   (0, 0), (-1, 0),  colors.HexColor('#0284c7')),
            ('TEXTCOLOR',    (0, 0), (-1, 0),  colors.white),
            ('FONTNAME',     (0, 0), (-1, 0),  'Helvetica-Bold'),
            ('FONTSIZE',     (0, 0), (-1, 0),  11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
            ('FONTNAME',     (0, 1), (0, -1),  'Helvetica-Bold'),
            ('FONTSIZE',     (0, 1), (-1, -1), 10),
            ('TEXTCOLOR',    (0, 1), (0, -1),  colors.HexColor('#334155')),
            ('TEXTCOLOR',    (1, 1), (-1, -1), colors.HexColor('#1e293b')),
            ('GRID',         (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWPADDING',   (0, 0), (-1, -1), 8),
            ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.8*cm))

        footer_style = ParagraphStyle('footer', parent=styles['Normal'],
                                      fontSize=8, textColor=colors.HexColor('#94a3b8'))
        story.append(Paragraph(
            "Generated by myNalanda Solutions & Services Pvt. Ltd.  ·  Updated: 23 Jan 2026  ·  Demo Dashboard",
            footer_style))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    except ImportError:
        # Fallback: plain text if reportlab not installed
        lines = [
            "myNalanda — Teacher Performance Report",
            f"Ideal International School · {sel_m} {month_year(sel_m)} · Academic Year 2025–26",
            "",
            f"Teacher:        {teacher}",
            f"Section:        {section}",
            f"Subject:        {subject}",
            f"Month:          {sel_m}",
            f"Benchmark:      {bm:.1f}%",
            f"Actual Score:   {curr:.1f}%",
            f"Compliance:     {comp:.1f}/10 ({comp_label(comp)})",
            f"CCA Score:      {cca:.1f}/10 ({cca_label(cca)})",
            f"Overall Score:  {overall:.1f}% ({perf_label(overall)})",
            f"Attrition Risk: {risk_level}",
            f"Late Arrivals:  {late_cnt}",
            "",
            "Generated by myNalanda Solutions & Services Pvt. Ltd.",
        ]
        return "\n".join(lines).encode("utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────────
def login_page():
    _, c, _ = st.columns([1, 1.4, 1])
    with c:
        st.markdown("""
        <div class="login-logo">
            <div style="font-size:52px;">🎓</div>
            <div class="brand"><span>my</span>Nalanda</div>
            <div class="tagline">Skills Analytics for Schools</div>
            <div style="font-size:12px;color:#334155;margin-top:6px;">myNalanda Solutions & Services Pvt. Ltd.</div>
        </div>""", unsafe_allow_html=True)
        with st.form("lf"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            r = st.selectbox("Login as", ["myN Admin","School Admin","Teacher"])
            if st.form_submit_button("🔐  Login", use_container_width=True):
                if u == "admin" and p == "1234":
                    st.session_state.logged_in = True
                    st.session_state.role = r
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials  —  admin / 1234")

if not st.session_state.logged_in:
    login_page()
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="name"><span>my</span>Nalanda</div>
        <div class="school">Ideal International School</div>
    </div>""", unsafe_allow_html=True)
    st.success(f"✅ {st.session_state.role}")

    page = st.radio("Nav", ["👩‍🏫 Dashboard","👤 Teacher Profile","⏰Late count & Attrition"],
                    label_visibility="collapsed")

    st.markdown("---")

    st.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;'
                'letter-spacing:.8px;margin-bottom:6px;">📅 Select Month</div>', unsafe_allow_html=True)
    sel_month = st.selectbox("Month", MONTHS, index=MONTHS.index("Dec"),
                             label_visibility="collapsed", key="global_month")

    st.markdown(f"""
    <div style="margin-top:12px;padding:12px;background:#0f172a;border-radius:8px;
         font-size:11px;color:#64748b;border:1px solid #334155;">
        <b style="color:#cbd5e1;">Period:</b> {sel_month} {month_year(sel_month)}<br>
        <b style="color:#cbd5e1;">Acad. Year:</b> 2025–26<br>
        <b style="color:#cbd5e1;">Teachers:</b> {len(tdf)}<br>
        <b style="color:#cbd5e1;">Updated:</b> 23 Jan 2026
    </div>""", unsafe_allow_html=True)

    if st.button("⏎  Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

sel_data = pdf[pdf["month"] == sel_month].copy()

_late_month = ldf[ldf.month == sel_month]
kpi = {
    "teachers":          len(tdf),
    "avg_bm":            round(sel_data["teaching_delivery_bm"].mean(), 1),
    "avg_curr":          round(sel_data["teaching_delivery_curr"].mean(), 1),
    "avg_comp":          round(sel_data["compliance_score"].mean(), 1),
    "avg_cca":           round(sel_data["cca_score"].mean(), 1),
    "attr_risk":         len(adf[adf.attrition_score >= 2]),
    "late_sel":          int(_late_month["late_count"].sum()),
    "late_teachers_sel": int((_late_month["late_count"] > 0).sum()),  # FIX 2: teachers affected
}


# =====================================================
# PAGE 1 — DASHBOARD
# =====================================================
if page == "👩‍🏫 Dashboard":
    st.markdown('<p class="sec-title">👩‍🏫 Staff Performance Dashboard</p>', unsafe_allow_html=True)

    st.caption(f"Ideal International School  ·  {sel_month} {month_year(sel_month)}  ·  Academic Year 2025–26")

    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:1px solid #334155;
                border-left:4px solid #38bdf8;border-radius:12px;padding:16px 20px;margin:10px 0 18px;">
        <div style="font-size:13px;font-weight:700;color:#38bdf8;letter-spacing:.6px;margin-bottom:6px;">
            📌 ABOUT THIS DASHBOARD
        </div>
        <div style="font-size:13px;color:#cbd5e1;line-height:1.7;">
            This dashboard monitors <b style="color:#f1f5f9;">teacher performance</b> at Ideal International School
            across five dimensions — helping school leadership identify quality gaps and make data-driven decisions.
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px;">
            <span style="background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.25);
                         border-radius:20px;padding:4px 12px;font-size:11px;color:#38bdf8;">
                📚 Teaching Quality — Is each teacher delivering lessons at the expected level?
            </span>
            <span style="background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.25);
                         border-radius:20px;padding:4px 12px;font-size:11px;color:#a78bfa;">
                🔏 Admin Compliance — Are teachers completing training, submitting reports & marking on time?
            </span>
            <span style="background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.25);
                         border-radius:20px;padding:4px 12px;font-size:11px;color:#4ade80;">
                🎭 CCA Participation — Are teachers actively contributing to co-curricular activities?
            </span>
            <span style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);
                         border-radius:20px;padding:4px 12px;font-size:11px;color:#f87171;">
                ⚠️ Attrition Risk — Which teachers are at risk of resigning or leaving the school?
            </span>
            <span style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.25);
                         border-radius:20px;padding:4px 12px;font-size:11px;color:#facc15;">
                ⏰ Punctuality — Are teachers arriving on time consistently?
            </span>
        </div>
        <div style="margin-top:10px;font-size:11px;color:#475569;">
            Overall Score = <b style="color:#94a3b8;">60% Teaching Quality</b> +
            <b style="color:#94a3b8;">25% Admin Compliance</b> +
            <b style="color:#94a3b8;">15% CCA Participation</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👩‍🏫 Total Teachers",              kpi["teachers"])
    m2.metric("⚠️ At-Risk of Leaving",            kpi["attr_risk"],
              help="Teachers at medium or high attrition risk — need HR attention")
    m3.metric(f"⏰ Late Arrivals ({sel_month})",   kpi["late_sel"],
              help=f"{kpi['late_sel']} total late instances · {kpi['late_teachers_sel']} of {kpi['teachers']} teachers affected in {sel_month} {month_year(sel_month)}")

    st.caption(f"↳ {kpi['late_teachers_sel']} of {kpi['teachers']} teachers had ≥1 late arrival", )
    m4.metric("🎓 Avg Overall Score",
              f"{round(sel_data['teaching_delivery_curr'].mean()*0.6 + sel_data['compliance_score'].mean()/10*25 + sel_data['cca_score'].mean()/10*15, 1)}%",
              help="Weighted composite: 60% Teaching Quality + 25% Admin Compliance + 15% CCA")

    st.markdown("---")

    # 4 Gauges
    g1, g2, g3, g4 = st.columns(4)
    gauge_data = [
        ("Teaching Quality\n(Expected Benchmark)", kpi["avg_bm"],   100, "%"),
        ("Teaching Quality\n(Observed Actual)",    kpi["avg_curr"], 100, "%"),
        ("Admin Compliance\n(Training & Marking)", kpi["avg_comp"],  10, "/10"),
        ("CCA Participation\n(Co-curricular)",     kpi["avg_cca"],   10, "/10"),
    ]
    for col, (title, val, mx, unit) in zip([g1, g2, g3, g4], gauge_data):
        pct   = val / mx
        color = "#4ade80" if pct > .75 else "#38bdf8" if pct > .5 else "#facc15" if pct > .3 else "#f87171"
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=round(val, 1),
            number={"font": {"color": "#38bdf8", "size": 30}, "suffix": unit},
            title={"text": f"<b>{title}</b>", "font": {"color": "#94a3b8", "size": 12}, "align": "center"},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, mx], "tickcolor": "#334155", "tickfont": {"color": "#64748b", "size": 9}},
                "bar":  {"color": color, "thickness": .35},
                "bgcolor": "#0f172a", "borderwidth": 0,
                "steps": [
                    {"range": [0, mx*.4],      "color": "rgba(239,68,68,.08)"},
                    {"range": [mx*.4, mx*.65], "color": "rgba(234,179,8,.08)"},
                    {"range": [mx*.65, mx],    "color": "rgba(34,197,94,.08)"},
                ],
                "threshold": {"line": {"color": "#f1f5f9", "width": 2}, "thickness": .75, "value": val},
            }
        ))
        fig.update_layout(**dark_layout(height=240, margin=dict(t=60, b=10, l=30, r=30)), autosize=True)
        with col:
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    trend = (pdf.groupby("month")
               .agg(curr=("teaching_delivery_curr","mean"),
                    bm=("teaching_delivery_bm","mean"),
                    comp=("compliance_score","mean"))
               .reindex(MONTHS).reset_index())

    ctitle(f"📈 School-wide Monthly Performance Trend — Academic Year 2025–26  |  Selected: {sel_month}")
    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(x=trend.month, y=trend.curr, name="Actual Teaching Score",
        mode="lines", line=dict(color="#38bdf8", width=3),
        fill="tozeroy", fillcolor="rgba(56,189,248,.08)",
        hovertemplate="<b>%{x}</b> · Actual: %{y:.1f}%<extra></extra>"))
    fig_t.add_trace(go.Scatter(x=trend.month, y=trend.bm, name="Benchmark",
        mode="lines", line=dict(color="#8b5cf6", width=2, dash="dot"),
        hovertemplate="<b>%{x}</b> · Benchmark: %{y:.1f}%<extra></extra>"))
    fig_t.add_trace(go.Scatter(x=trend.month, y=trend.comp * 10, name="Compliance (×10 for scale)",
        mode="lines", line=dict(color="#4ade80", width=2),
        customdata=trend.comp,
        hovertemplate="<b>%{x}</b> · Compliance (actual): %{customdata:.1f}/10  (plotted ×10 for scale)<extra></extra>"))

    if sel_month in MONTHS:
        sel_month_idx = MONTHS.index(sel_month)
        fig_t.add_shape(type="line", x0=sel_month_idx, x1=sel_month_idx,
                        y0=0, y1=1, xref="x", yref="paper",
                        line=dict(color="#facc15", width=2, dash="dash"))
        fig_t.add_annotation(x=sel_month_idx, y=1, xref="x", yref="paper",
                             text=f" {sel_month}", showarrow=False,
                             font=dict(color="#facc15", size=11), xanchor="left")

    fig_t.update_layout(**dark_layout(height=300, margin=dict(t=10, b=60, l=55, r=20)),
                        yaxis_title="Score (0–100)", xaxis_title="Month")
    apply_axes(fig_t)
    fig_t.update_layout(legend=dict(orientation="h", y=-0.22, bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)))
    st.plotly_chart(fig_t, use_container_width=True)
    st.markdown("---")

    sec = (sel_data.groupby("section")
              .agg(delivery=("teaching_delivery_curr","mean"),
                   comp=("compliance_score","mean"),
                   cca=("cca_score","mean"),
                   n=("teacher_id","nunique"))
              .reset_index())

    col_a, col_b = st.columns(2)
    with col_a:
        ctitle(f"🏫 Teaching Quality vs Admin Compliance by Section ({sel_month} {month_year(sel_month)})")
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(x=sec.section, y=sec.delivery, name="Teaching Score (%)",
            marker_color="#38bdf8",
            hovertemplate="<b>%{x}</b> · Teaching: %{y:.1f}%<extra></extra>"))
        fig_s.add_trace(go.Bar(x=sec.section, y=sec.comp * 10, name="Compliance (×10)",
            marker_color="#8b5cf6",
            hovertemplate="<b>%{x}</b> · Compliance: %{y:.1f} (raw ÷10)<extra></extra>"))
        fig_s.update_layout(**dark_layout(height=280, margin=dict(t=10, b=50, l=55, r=20)),
                            barmode="group", yaxis_range=[0, 100],
                            xaxis_title="Section", yaxis_title="Score")
        apply_axes(fig_s)
        st.plotly_chart(fig_s, use_container_width=True)

    with col_b:
        ctitle("🔵 Admin Compliance vs CCA Participation by Section  (bubble = no. of teachers)")
        fig_sc = px.scatter(sec, x="comp", y="cca", text="section", size="n",
                            color_discrete_sequence=["#38bdf8"])
        fig_sc.update_traces(textposition="top center",
            hovertemplate="<b>%{text}</b> · Compliance:%{x:.1f}  CCA:%{y:.1f}<extra></extra>")
        fig_sc.update_layout(**dark_layout(height=280, margin=dict(t=10, b=50, l=65, r=20)),
                             xaxis_title="Compliance (0–10)", yaxis_title="CCA Score (0–10)")
        apply_axes(fig_sc)
        st.plotly_chart(fig_sc, use_container_width=True)

    # Top / Bottom 5
    t_sel = (sel_data.groupby("teacher_name")["teaching_delivery_curr"].mean()
               .reset_index().sort_values("teaching_delivery_curr", ascending=False))

    col_top, col_bot = st.columns(2)
    with col_top:
        ctitle(f"🏆 Top 5 Teachers — {sel_month}")
        top5 = t_sel.head(5)
        fig_tp = go.Figure(go.Bar(x=top5.teaching_delivery_curr, y=top5.teacher_name,
            orientation="h", marker_color="#4ade80",
            text=top5.teaching_delivery_curr.map("{:.1f}%".format), textposition="outside",
            hovertemplate="<b>%{y}</b> · %{x:.1f}%<extra></extra>"))
        fig_tp.update_layout(**dark_layout(height=260, margin=dict(l=130, r=70, t=10, b=40)),
                             xaxis_range=[0, 115], xaxis_title="Teaching Score (%)")
        apply_axes(fig_tp)
        st.plotly_chart(fig_tp, use_container_width=True)

    with col_bot:
        ctitle("🔴 Bottom 5 Teachers — Need Support")
        bot5 = t_sel.tail(5)
        fig_bt = go.Figure(go.Bar(x=bot5.teaching_delivery_curr, y=bot5.teacher_name,
            orientation="h", marker_color="#f87171",
            text=bot5.teaching_delivery_curr.map("{:.1f}%".format), textposition="outside",
            hovertemplate="<b>%{y}</b> · %{x:.1f}%<extra></extra>"))
        fig_bt.update_layout(**dark_layout(height=260, margin=dict(l=130, r=70, t=10, b=40)),
                             xaxis_range=[0, 115], xaxis_title="Teaching Score (%)")
        apply_axes(fig_bt)
        st.plotly_chart(fig_bt, use_container_width=True)

    st.markdown("---")

    # Attrition Distribution
    ctitle("⚠️ Attrition Risk Distribution")
    rc = (adf["risk_level"].value_counts()
            .reindex(["High","Medium","Low","None"], fill_value=0).reset_index())
    rc.columns = ["label","count"]
    rc_colors = {"High":"#f87171","Medium":"#facc15","Low":"#38bdf8","None":"#4ade80"}

    col_pie, col_bar = st.columns(2)
    with col_pie:
        fig_pie = go.Figure(go.Pie(
            labels=rc.label, values=rc["count"],
            marker=dict(colors=[rc_colors[l] for l in rc.label]),
            hole=.45, textinfo="label+value",
            textfont=dict(color="#f1f5f9", size=12),
            hovertemplate="<b>%{label}</b> · %{value} teachers · %{percent}<extra></extra>"))
        fig_pie.update_layout(**dark_layout(height=290, margin=dict(t=20, b=20, l=20, r=20)),
                              annotations=[dict(text="Risk<br>Level", x=.5, y=.5,
                                               font_size=12, showarrow=False, font_color="#94a3b8")])
        apply_axes(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("🔴 High = leave soon  🟡 Medium = at risk  🔵 Low = minor concern  🟢 Stable")

    with col_bar:
        tc = (adf[adf.attrition_score > 0]["attrition_type"].value_counts().reset_index())
        tc.columns = ["type","count"]
        fig_ab = go.Figure(go.Bar(x=tc.type, y=tc["count"], marker_color="#8b5cf6",
            text=tc["count"], textposition="outside", textfont=dict(color="#f1f5f9", size=11),
            hovertemplate="<b>%{x}</b> · %{y} teachers<extra></extra>"))
        fig_ab.update_layout(**dark_layout(height=290, margin=dict(t=20, b=60, l=55, r=20)),
                             xaxis_title="Exit Type", yaxis_title="No. of Teachers",
                             yaxis_range=[0, tc["count"].max() + 2])
        apply_axes(fig_ab)
        st.plotly_chart(fig_ab, use_container_width=True)
        st.caption("Voluntary = teacher's choice  |  Involuntary = school decision  |  Structural = role removed")


# =====================================================
# PAGE 2 — TEACHER PROFILE
# =====================================================
elif page == "👤 Teacher Profile":
    st.markdown('<p class="sec-title">👤 Teacher Performance Profile</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1e293b;border:1px solid #334155;border-left:4px solid #8b5cf6;
                border-radius:12px;padding:12px 18px;margin-bottom:16px;">
        <span style="font-size:12px;color:#a78bfa;font-weight:700;">📋 HOW TO READ THIS PAGE &nbsp;·&nbsp;</span>
        <span style="font-size:12px;color:#94a3b8;">
            Select a teacher below to view their full profile for the month selected in the sidebar.
            Teaching delivery vs expected benchmark, administrative compliance (training hours + marking quality),
            co-curricular participation, stakeholder ratings from Head / Peers / Students / Parents,
            punctuality record, and attrition risk level.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Teacher selector (month now comes from global sidebar filter)
    teacher = st.selectbox("Select Teacher", sorted(pdf.teacher_name.unique()))
    sel_m = sel_month  # Use global month from sidebar

    t_row  = tdf[tdf.teacher_name == teacher].iloc[0]
    t_perf = pdf[(pdf.teacher_name == teacher) & (pdf.month == sel_m)]
    t_hist = pdf[pdf.teacher_name == teacher].copy()
    t_late = ldf[(ldf.teacher_name == teacher) & (ldf.month == sel_m)]
    t_comp = cdf[cdf.teacher_id == t_row.teacher_id].iloc[0]
    t_cca  = ccadf[ccadf.teacher_id == t_row.teacher_id].iloc[0]
    t_al   = aldf[aldf.teacher_id == t_row.teacher_id].set_index("stakeholder")["stars"]
    t_attr = adf[adf.teacher_id == t_row.teacher_id].iloc[0]

    if t_perf.empty:
        st.warning(f"No data for {sel_m}.")
        st.stop()

    tp       = t_perf.iloc[0]
    bm       = tp.teaching_delivery_bm
    curr     = tp.teaching_delivery_curr
    comp     = tp.compliance_score
    cca      = tp.cca_score
    late_cnt = int(t_late.late_count.values[0]) if len(t_late) else 0
    overall  = min(100, curr * .6 + comp / 10 * 25 + cca / 10 * 15)
    diff     = curr - bm

    # Row 1: Late | Gauge | Info
    h1, h2, h3 = st.columns([1.4, 1, 1.4])

    with h1:
        boxes = "".join([
            f'<div style="width:20px;height:20px;border-radius:4px;margin:2px;display:inline-block;'
            f'background:{"#f87171" if i < late_cnt else "#1e293b"};border:1px solid #334155;"></div>'
            for i in range(12)])
        status = "✅ No issues" if late_cnt == 0 else "⚠️ Monitor" if late_cnt > 2 else "🟡 Minor"
        st.markdown(f"""
        <div class="card">
            <div class="card-title">⏰ Late Arrivals — {sel_m}</div>
            <div style="font-size:40px;font-weight:800;color:#f87171;line-height:1;">{late_cnt}</div>
            <div style="font-size:12px;color:#64748b;margin:6px 0 10px;">
                times late &nbsp;·&nbsp; <b style="color:#f1f5f9;">{status}</b>
            </div>
            <div style="font-size:10px;color:#475569;margin-bottom:5px;">Monthly tracker (🔴 = late)</div>
            {boxes}
        </div>""", unsafe_allow_html=True)

    with h2:
        fig_ov = go.Figure(go.Indicator(
            mode="gauge+number", value=round(overall, 1),
            number={"font": {"color": "#38bdf8", "size": 32}, "suffix": "%"},
            title={"text": "<b>Overall Score</b>", "font": {"color": "#94a3b8", "size": 13}, "align": "center"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#334155", "tickfont": {"color": "#64748b", "size": 9}},
                "bar":  {"color": "#38bdf8", "thickness": .4},
                "bgcolor": "#0f172a", "borderwidth": 0,
                "steps": [
                    {"range": [0,  40], "color": "rgba(239,68,68,.1)"},
                    {"range": [40, 65], "color": "rgba(234,179,8,.1)"},
                    {"range": [65, 100],"color": "rgba(34,197,94,.1)"},
                ],
            }))
        fig_ov.update_layout(**dark_layout(height=240, margin=dict(t=60, b=10, l=30, r=30)), autosize=True)
        st.plotly_chart(fig_ov, use_container_width=True)
        st.caption(f"60% Teaching + 25% Compliance + 15% CCA  ·  **{perf_label(overall)}**")

    with h3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Teacher Info</div>
            <div class="info-row"><span>Qualification</span><b>{t_row.qualification}</b></div>
            <div class="info-row"><span>Experience (Here)</span><b>{t_row.experience_current} yrs</b></div>
            <div class="info-row"><span>Prior Experience</span><b>{t_row.experience_previous} yrs</b></div>
            <div class="info-row"><span>Section</span><b>{t_row.section}</b></div>
            <div class="info-row"><span>Subject</span><b>{t_row.subject}</b></div>
            <div class="info-row"><span>Classes / Week</span><b>{t_row.classes_per_week}</b></div>
            <div class="info-row"><span>Attrition Risk</span><b>{risk_badge(t_attr.attrition_score)}</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Score cards
    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown('<div class="card-title">🔏 Compliance <span style="font-size:10px;color:#475569;font-weight:400;">(Year-to-date · Static annual data)</span></div>', unsafe_allow_html=True)
        st.progress(float(t_comp.training_hours / t_comp.training_max),
                    f"Training: {t_comp.training_hours}/{t_comp.training_max} hrs")
        sf = int(t_comp.assignment_correction_stars)
        st.markdown(f"**Assignment Marking:** {'⭐'*sf}{'☆'*(5-sf)}  ({sf}/5)")
        _school_avg_comp = round(sel_data["compliance_score"].mean(), 1)
        st.metric("Compliance Score", f"{comp:.1f}/10",
                  delta=f"{comp - _school_avg_comp:.1f} vs school avg ({_school_avg_comp}/10)",
                  delta_color="normal")
        st.caption(f"Status: **{comp_label(comp)}**")

    with s2:
        st.markdown('<div class="card-title">📚 Teaching Score — Benchmark</div>', unsafe_allow_html=True)
        st.caption("Expected score based on experience & historical data")
        st.progress(float(bm / 100))
        st.metric("Expected", f"{bm:.1f}%")
        st.caption(f"Level: **{perf_label(bm)}**  ·  Target ≥ 70%")
        for m in ["Lesson Plan","Worksheet Quality","Time Management","Teaching Methods","Lesson Flow"]:
            st.caption(f"  · {m}")

    with s3:
        dc, da = ("#4ade80","▲") if diff >= 0 else ("#f87171","▼")
        st.markdown('<div class="card-title">📝 Teaching Score — Actual</div>', unsafe_allow_html=True)
        st.caption("Observed score this month from classroom evaluation")
        st.progress(float(curr / 100))
        st.metric("Actual", f"{curr:.1f}%",
                  delta=f"{diff:.1f}% vs benchmark", delta_color="normal")
        st.markdown(f"<span style='color:{dc};font-size:13px;font-weight:600;'>"
                    f"{da} {abs(diff):.1f}% {'above' if diff >= 0 else 'below'} benchmark</span>",
                    unsafe_allow_html=True)
        st.caption(f"Level: **{perf_label(curr)}**")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        # FIX #7: CCA labeled as Year-to-date
        st.markdown('<div class="card-title">🎭 CCA Contribution <span style="font-size:10px;color:#475569;font-weight:400;">(Year-to-date · Static annual data)</span></div>', unsafe_allow_html=True)
        ap = t_cca.activities_completed / max(t_cca.activities_total, 1)
        st.progress(float(ap), f"{t_cca.activities_completed}/{t_cca.activities_total} activities")
        qc = {"Excellent":"#4ade80","Good":"#38bdf8"}.get(t_cca.quality,"#facc15")
        st.markdown(f"Quality: <b style='color:{qc}'>{t_cca.quality}</b>", unsafe_allow_html=True)
        st.metric("CCA Score", f"{cca:.1f}/10")
        st.caption(f"Level: **{cca_label(cca)}**")

    with c2:
        st.markdown('<div class="card-title">🤝 Stakeholder Ratings</div>', unsafe_allow_html=True)
        for sh in ["Head","Peer","Student","Parent"]:
            s = int(t_al.get(sh, 3))
            st.markdown(f"**{sh}** &nbsp; {'⭐'*s}{'☆'*(5-s)} **{s}/5**", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card-title">🎯 HOD Expectations</div>', unsafe_allow_html=True)
        for e in t_row.hod_expectations:
            st.markdown(f"📌 {e}")
        st.markdown("---")
        st.markdown('<div class="card-title" style="margin-top:6px;">🏫 School Duties</div>', unsafe_allow_html=True)
        for param, desc in DUTY_PARAMS:
            icon = "✅" if t_row.duties[param] else "❌"
            st.markdown(f"{icon} **{param}**")
            st.caption(f"  _{desc}_")

    st.markdown("---")

    col_ch, col_sup = st.columns([1.6, 1])

    with col_ch:
        ctitle("📈 Individual Performance Trend — Full Academic Year 2025–26")
        t_hist["month"] = pd.Categorical(t_hist.month, categories=MONTHS, ordered=True)
        ths = t_hist.sort_values("month")
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Scatter(x=ths.month, y=ths.teaching_delivery_bm,
            name="Benchmark", mode="lines+markers",
            line=dict(color="#8b5cf6", width=2), marker=dict(size=5),
            hovertemplate="%{x} · Benchmark: %{y:.1f}%<extra></extra>"))
        fig_tr.add_trace(go.Scatter(x=ths.month, y=ths.teaching_delivery_curr,
            name="Actual", mode="lines+markers",
            line=dict(color="#38bdf8", width=2), marker=dict(size=5),
            hovertemplate="%{x} · Actual: %{y:.1f}%<extra></extra>"))
        fig_tr.add_trace(go.Scatter(x=ths.month, y=ths.compliance_score * 10,
            name="Compliance (×10)", mode="lines",
            line=dict(color="#4ade80", width=2, dash="dot"),
            customdata=ths.compliance_score,
            hovertemplate="%{x} · Compliance (actual): %{customdata:.1f}/10  (plotted ×10 for scale)<extra></extra>"))
        # Highlight selected month 
        if sel_month in MONTHS:
            _idx = MONTHS.index(sel_month)
            fig_tr.add_shape(type="line", x0=_idx, x1=_idx, y0=0, y1=1,
                             xref="x", yref="paper",
                             line=dict(color="#facc15", width=2, dash="dash"))
            fig_tr.add_annotation(x=_idx, y=1, xref="x", yref="paper",
                                  text=f" {sel_month}", showarrow=False,
                                  font=dict(color="#facc15", size=11), xanchor="left")
        fig_tr.update_layout(**dark_layout(height=270, margin=dict(t=10, b=70, l=55, r=20)),
                             yaxis_title="Score (%)", xaxis_title="Month")
        apply_axes(fig_tr)
        fig_tr.update_layout(legend=dict(orientation="h", y=-0.32, bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11)))
        st.plotly_chart(fig_tr, use_container_width=True)

    with col_sup:
        ctitle("📊 Score Summary — Normalized to 0–100")
        norm_comp = (comp / 10) * 100
        norm_cca  = (cca  / 10) * 100
        sc_df = pd.DataFrame({
            "Metric": ["Benchmark\n(Teaching)", "Actual\n(Teaching)", "Compliance\n(Normalized)", "CCA\n(Normalized)"],
            "Score":  [bm,       curr,      norm_comp,  norm_cca],
            "Raw":    [f"{bm:.1f}%", f"{curr:.1f}%", f"{comp:.1f}/10", f"{cca:.1f}/10"],
            "Rating": [perf_label(bm), perf_label(curr), comp_label(comp), cca_label(cca)],
        })
        fig_sb = px.bar(sc_df, x="Metric", y="Score", color="Score", text="Raw",
                        color_continuous_scale=["#f87171","#facc15","#38bdf8","#4ade80"],
                        range_color=[0, 100],
                        custom_data=["Rating", "Raw"])
        fig_sb.update_traces(
            texttemplate="%{customdata[1]}",
            textposition="outside",
            textfont=dict(color="#f1f5f9"),
            hovertemplate="<b>%{x}</b><br>Normalized: %{y:.1f}/100<br>Raw: %{customdata[1]}<br>Rating: %{customdata[0]}<extra></extra>")
        fig_sb.update_layout(**dark_layout(height=300, margin=dict(t=20, b=20, l=55, r=20)),
                             showlegend=False, coloraxis_showscale=False,
                             yaxis_range=[0, 120], yaxis_title="Score (normalized 0–100)")
        apply_axes(fig_sb)
        st.plotly_chart(fig_sb, use_container_width=True)
        st.caption("All metrics converted to 0–100 scale for fair comparison. Raw values shown on bars.")

    pdf_bytes = generate_pdf_report(teacher, t_row.section, t_row.subject, sel_m,
                                    bm, curr, comp, cca, overall, t_attr.risk_level, late_cnt)

    # Detect if reportlab was available (PDF bytes start with %PDF)
    if isinstance(pdf_bytes, bytes) and pdf_bytes[:4] == b'%PDF':
        st.download_button("⬇  Download Teacher Report (PDF)",
                           pdf_bytes,
                           f"report_{t_row.teacher_id}_{sel_m}.pdf",
                           "application/pdf")
    else:
        # Fallback to text if reportlab not installed
        st.download_button("⬇  Download Teacher Report (TXT)",
                           pdf_bytes,
                           f"report_{t_row.teacher_id}_{sel_m}.txt",
                           "text/plain")
        st.caption("💡 Install `reportlab` (`pip install reportlab`) for PDF output.")


# =====================================================
# PAGE 3 — LATE & ATTRITION
# =====================================================
elif page == "⏰Late count & Attrition":
    st.markdown('<p class="sec-title">⏰ Teacher Punctuality & Retention Risk</p>', unsafe_allow_html=True)

    st.caption(f"Late arrival patterns · Teacher attrition & retention risk  ·  {sel_month} {month_year(sel_month)}")

    st.markdown("""
    <div style="background:#1e293b;border:1px solid #334155;border-left:4px solid #facc15;
                border-radius:12px;padding:12px 18px;margin:10px 0 16px;">
        <span style="font-size:12px;color:#facc15;font-weight:700;">📌 WHAT THIS PAGE SHOWS &nbsp;·&nbsp;</span>
        <span style="font-size:12px;color:#94a3b8;">
            <b style="color:#cbd5e1;">Left panel:</b> Track how often any individual teacher arrives late each month,
            plus the school-wide late arrival trend across the full academic year. &nbsp;|&nbsp;
            <b style="color:#cbd5e1;">Right panel:</b> Attrition risk scores flag teachers who may be planning to leave —
            scored 0 (Stable) to 3 (High Risk). These are <b style="color:#facc15;">annual snapshot scores</b>
            based on engagement levels, job-seeking signals, and qualitative HR observations —
            they do not vary by month. Use the exit-type filter to focus on voluntary vs involuntary departures.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col_l, col_a = st.columns([1, 1.6])

    with col_l:
        ctitle("⏰ Individual Teacher — Late Arrival History")
        sel_t = st.selectbox("Select Teacher", sorted(ldf.teacher_name.unique()), key="lt")
        tlh = ldf[ldf.teacher_name == sel_t].copy()
        tlh["month"] = pd.Categorical(tlh.month, categories=MONTHS, ordered=True)
        tlh = tlh.sort_values("month")

        tl1, tl2 = st.columns(2)
        tl1.metric("Total Lates (Year)", tlh["late_count"].sum())
        tl2.metric("Worst Month", tlh.loc[tlh["late_count"].idxmax(), "month"])

        fig_l = go.Figure(go.Scatter(
            x=tlh.month, y=tlh.late_count, mode="lines+markers",
            line=dict(color="#38bdf8", width=2),
            marker=dict(size=11, color=["#f87171" if v >= 3 else "#facc15" if v == 2 else "#38bdf8"
                                         for v in tlh.late_count]),
            fill="tozeroy", fillcolor="rgba(56,189,248,.07)",
            hovertemplate="<b>%{x}</b> · %{y} late(s)<extra></extra>"))

        if sel_month in MONTHS:
            _idx = MONTHS.index(sel_month)
            fig_l.add_shape(type="line", x0=_idx, x1=_idx, y0=0, y1=1,
                            xref="x", yref="paper",
                            line=dict(color="#facc15", width=2, dash="dash"))
            fig_l.add_annotation(x=_idx, y=1, xref="x", yref="paper",
                                 text=f" {sel_month}", showarrow=False,
                                 font=dict(color="#facc15", size=11), xanchor="left")

        fig_l.update_layout(**dark_layout(height=280, margin=dict(t=10, b=50, l=55, r=20)),
                            xaxis_title="Month", yaxis_title="Late Count",
                            yaxis_dtick=1)
        apply_axes(fig_l)
        st.plotly_chart(fig_l, use_container_width=True)
        st.caption("🔴 ≥3  🟡 =2  🔵 0–1")

        st.markdown("---")
        ctitle("🏫 School-wide Late Count — All Teachers per Month")
        sl = ldf.groupby("month")["late_count"].sum().reindex(MONTHS).reset_index()
        sl.columns = ["month","count"]
        avg_l = sl["count"].mean()
        fig_sl = go.Figure()
        fig_sl.add_trace(go.Bar(x=sl.month, y=sl["count"],
            marker_color=["#f87171" if v > avg_l * 1.3 else "#facc15" if v > avg_l else "#38bdf8"
                          for v in sl["count"]],
            text=sl["count"], textposition="outside",
            textfont=dict(color="#f1f5f9", size=9),
            hovertemplate="<b>%{x}</b> · %{y} total late arrivals<extra></extra>"))
        fig_sl.add_hline(y=avg_l, line_dash="dot", line_color="#94a3b8", line_width=1,
                         annotation_text=f"  avg {avg_l:.0f}", annotation_font_color="#94a3b8")

        # Highlight selected month (shape avoids categorical x-axis TypeError)
        if sel_month in MONTHS:
            _idx = MONTHS.index(sel_month)
            fig_sl.add_shape(type="line", x0=_idx-0.5, x1=_idx-0.5, y0=0, y1=1,
                             xref="x", yref="paper",
                             line=dict(color="#facc15", width=2, dash="dash"))
            fig_sl.add_annotation(x=_idx, y=1, xref="x", yref="paper",
                                  text=f" {sel_month}", showarrow=False,
                                  font=dict(color="#facc15", size=11), xanchor="left")

        fig_sl.update_layout(**dark_layout(height=250, margin=dict(t=10, b=50, l=55, r=20)),
                             xaxis_title="Month", yaxis_title="Total Late Count",
                             yaxis_range=[0, sl["count"].max() + 10])
        apply_axes(fig_sl)
        st.plotly_chart(fig_sl, use_container_width=True)
        st.caption("🔴 >130% avg  🟡 >avg  🔵 normal")

    with col_a:
        ctitle("⚠️ Attrition Risk — Annual Snapshot")

        st.markdown("""
        <div style="background:#0f172a;border:1px solid #334155;border-left:3px solid #facc15;
                    border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:11px;color:#64748b;">
            📌 <b style="color:#facc15;">Annual Snapshot</b> — Attrition risk scores are based on
            full-year HR observations and do not change when you switch months.
            This is expected behaviour, not a data issue.
        </div>
        """, unsafe_allow_html=True)

        st.caption("Score: 0 = Stable · 1 = Low · 2 = Medium · 3 = High (act now)")

        a1, a2, a3, a4 = st.columns(4)
        a1.metric("🔴 High",   len(adf[adf.attrition_score == 3]))
        a2.metric("🟡 Medium", len(adf[adf.attrition_score == 2]))
        a3.metric("🔵 Low",    len(adf[adf.attrition_score == 1]))
        a4.metric("🟢 Stable", len(adf[adf.attrition_score == 0]))

        attr_filter = st.selectbox("Filter by exit type",
            ["All","Voluntary","Involuntary","Retirement","Structural","None"])

        disp = adf.copy()
        if attr_filter != "All":
            disp = disp[disp.attrition_type == attr_filter]
        disp = disp.sort_values("attrition_score", ascending=False)

        ds = disp[["teacher_name","attrition_score","risk_level",
                   "attrition_type","attrition_explanation"]].copy()
        ds.columns = ["Teacher","Score","Risk Level","Exit Type","Reason"]

        def color_risk(row):
            c = {3: "rgba(239,68,68,.14)", 2: "rgba(234,179,8,.14)",
                 1: "rgba(56,189,248,.08)", 0: ""}
            bg = c.get(row["Score"], "")
            return [f"background-color:{bg}" if bg else "" for _ in row]

        st.dataframe(ds.style.apply(color_risk, axis=1), height=460, use_container_width=True)
        st.caption("🔴 High (3) · 🟡 Medium (2) · 🔵 Low (1) · White = Stable (0)")
        st.download_button("⬇  Download Attrition Report (CSV)",
                           disp.to_csv(index=False),
                           "attrition_report.csv", "text/csv")