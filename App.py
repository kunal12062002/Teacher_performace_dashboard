# =====================================================
# myNalanda Dashboard
# School: Ideal International School
# Roles: myN Admin / School Admin (4 sub-roles) / Teacher
# =====================================================

# ── Step 1: Imports ───────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# ── Step 2: Page config ───────────────────────────────────────────────────
st.set_page_config(page_title="myNalanda Dashboard", page_icon="🎓",
                   layout="wide", initial_sidebar_state="expanded")

# ── Step 3: Session state defaults ───────────────────────────────────────
for key, default in [("logged_in", False), ("role", None),
                     ("teacher_name", None), ("sub_role", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Step 4: CSS ───────────────────────────────────────────────────────────
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
    top:50% !important; z-index:9999 !important; }
[data-testid="collapsedControl"]:hover{ background:#334155 !important; }
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button{
    display:flex !important; visibility:visible !important;
    color:#64748b !important; background:transparent !important; }
[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button:hover{
    color:#38bdf8 !important; background:rgba(56,189,248,.1) !important; border-radius:6px !important; }
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0f172a 0%,#1e293b 100%) !important;
    border-right:1px solid #334155; }
[data-testid="stSidebar"] *{ color:#cbd5e1 !important; }
[data-testid="stSidebar"] .stRadio label{ font-size:13px !important; }
div[data-testid="metric-container"]{
    background:#1e293b; border:1px solid #334155; border-radius:14px;
    padding:16px 18px !important; border-left:4px solid #38bdf8; transition:transform .2s; }
div[data-testid="metric-container"]:hover{ transform:translateY(-2px); }
div[data-testid="metric-container"] label{
    color:#64748b !important; font-size:10px !important;
    text-transform:uppercase; letter-spacing:.8px; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"]{
    color:#f1f5f9 !important; font-size:24px !important; font-weight:800 !important; }
.stSelectbox label{ color:#64748b !important; font-size:11px !important; text-transform:uppercase; }
.stDataFrame{ border:1px solid #334155 !important; border-radius:10px !important; }
.stProgress > div > div{ background-color:#38bdf8 !important; border-radius:20px; }
.stProgress > div{ background-color:#0f172a !important; border-radius:20px; }
.card{ background:#1e293b; border:1px solid #334155; border-radius:14px; padding:18px 20px; margin-bottom:14px; }
.card-title{ font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:.8px; margin-bottom:10px; }
.info-row{ display:flex; justify-content:space-between; font-size:13px; padding:5px 0; border-bottom:1px solid #0f172a; color:#94a3b8; }
.info-row b{ color:#e2e8f0; }
.sec-title{ font-size:20px; font-weight:800; color:#f1f5f9; padding-bottom:6px;
    border-bottom:2px solid #38bdf8; margin-bottom:20px; display:inline-block; }
.chart-title{ font-size:13px; font-weight:700; color:#f1f5f9; margin-bottom:14px; }
.badge{ display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.badge-red   { background:rgba(239,68,68,.15);  color:#f87171; border:1px solid rgba(239,68,68,.3); }
.badge-yellow{ background:rgba(234,179,8,.15);  color:#facc15; border:1px solid rgba(234,179,8,.3); }
.badge-green { background:rgba(34,197,94,.15);  color:#4ade80; border:1px solid rgba(34,197,94,.3); }
.badge-blue  { background:rgba(56,189,248,.15); color:#38bdf8; border:1px solid rgba(56,189,248,.3); }
.stDownloadButton button{
    background:linear-gradient(90deg,#0284c7,#38bdf8) !important;
    color:#fff !important; border:none !important; border-radius:8px !important; font-weight:600 !important; }
.login-logo{ text-align:center; margin:40px 0 28px; }
.login-logo .brand{ font-size:32px; font-weight:800; color:#f1f5f9; }
.login-logo .brand span{ color:#38bdf8; }
.login-logo .tagline{ font-size:13px; color:#64748b; margin-top:4px; }
.sidebar-brand{ text-align:center; padding:16px 0 20px; border-bottom:1px solid #334155; margin-bottom:16px; }
.sidebar-brand .name{ font-size:18px; font-weight:800; color:#f1f5f9 !important; }
.sidebar-brand .name span{ color:#38bdf8 !important; }
.sidebar-brand .school{ font-size:10px; color:#64748b !important; margin-top:2px; }
.role-pill{ display:inline-block; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700; margin-top:6px; }
.role-admin  { background:rgba(56,189,248,.15); color:#38bdf8; border:1px solid rgba(56,189,248,.3); }
.role-school { background:rgba(139,92,246,.15); color:#a78bfa; border:1px solid rgba(139,92,246,.3); }
.role-teacher{ background:rgba(74,222,128,.15); color:#4ade80; border:1px solid rgba(74,222,128,.3); }
.readonly-banner{
    background:rgba(56,189,248,.07); border:1px solid rgba(56,189,248,.2);
    border-left:4px solid #38bdf8; border-radius:10px;
    padding:10px 16px; margin-bottom:16px; font-size:12px; color:#64748b; }
</style>""", unsafe_allow_html=True)

# ── Step 5: Helper functions ───────────────────────────────────────────────
def get_performance_label(score):
    return "Excellent" if score >= 85 else "Good" if score >= 70 else "Needs Improvement" if score >= 55 else "Poor"

def get_compliance_label(score):
    return "Highly Compliant" if score >= 8 else "Compliant" if score >= 6 else "Partial" if score >= 4 else "Non-Compliant"

def get_cca_label(score):
    return "Excellent" if score >= 8 else "Good" if score >= 6 else "Needs Improvement" if score >= 4 else "Poor"

def get_risk_badge_html(score):
    score = float(score)
    if score >= 3:   return '<span class="badge badge-red">🔴 High Risk</span>'
    elif score >= 2: return '<span class="badge badge-yellow">🟡 Medium</span>'
    elif score >= 1: return '<span class="badge badge-blue">🔵 Low Risk</span>'
    else:            return '<span class="badge badge-green">🟢 Stable</span>'

def get_dark_chart_layout(height=300, margin=None):
    """Returns a dark-themed layout dict for all Plotly charts."""
    m = margin or dict(t=40, b=50, l=55, r=20)
    return dict(height=height, margin=m,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8", size=11, family="DM Sans"),
                hoverlabel=dict(bgcolor="#1e293b", bordercolor="#334155",
                                font=dict(color="#f1f5f9", size=12)))

# Shared axis + legend styles applied to every chart
X_AXIS_STYLE = dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b", size=10))
Y_AXIS_STYLE = dict(gridcolor="#1e293b", zerolinecolor="#334155", tickfont=dict(color="#64748b", size=10))
LEGEND_STYLE = dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8", size=11))

def apply_dark_axes(fig):
    fig.update_xaxes(**X_AXIS_STYLE)
    fig.update_yaxes(**Y_AXIS_STYLE)
    fig.update_layout(legend=LEGEND_STYLE)
    return fig

def show_chart_title(text):
    st.markdown(f'<p class="chart-title">{text}</p>', unsafe_allow_html=True)

def add_month_vline(fig, selected_month, months_list):
    """Adds a yellow dashed vertical line on charts to mark the selected month."""
    if selected_month in months_list:
        idx = months_list.index(selected_month)
        fig.add_shape(type="line", x0=idx, x1=idx, y0=0, y1=1, xref="x", yref="paper",
                      line=dict(color="#facc15", width=2, dash="dash"))
        fig.add_annotation(x=idx, y=1, xref="x", yref="paper", text=f" {selected_month}",
                           showarrow=False, font=dict(color="#facc15", size=11), xanchor="left")

# ── Step 6: Constants ─────────────────────────────────────────────────────
MONTHS = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

def get_year_for_month(month):
    return 2026 if month in ["Jan","Feb","Mar"] else 2025

HOD_EXPECTATION_POOL = [
    "Activity-based learning","Better assessments","Parent communication",
    "Use of technology","Improve lesson planning","Peer collaboration",
    "Student feedback integration","Timely report submission",
    "Differentiated instruction","Professional development","Class discipline",
    "Regular student counselling"
]

DUTY_LIST = [
    ("Academic Board",  "Curriculum & board meetings"),
    ("Exam Portfolio",  "Managing exam papers"),
    ("Admissions",      "New student onboarding"),
    ("Affiliations",    "External board coordination"),
]

# ── Step 7: Generate fake demo data ───────────────────────────────────────
@st.cache_data
def generate_all_data():
    np.random.seed(42)
    first_names = ["Linda","James","Emily","Robert","Sarah","David","Jessica","Kevin",
                   "Patricia","Matthew","Rajesh","Priya","Amit","Sunita","Vikram",
                   "Neha","Ravi","Pooja","Arjun","Meena"]
    last_names  = ["Martinez","Wilson","Johnson","Brown","Taylor","Garcia","Adams","Young",
                   "Turner","Evans","Sharma","Verma","Singh","Patel","Gupta",
                   "Joshi","Mehta","Rao","Kumar","Shah"]
    subjects       = ["Mathematics","Science","English","Social Studies","Computer Science",
                      "Physics","Chemistry","Biology","Art","Physical Education"]
    sections       = ["Sec A","Sec B","Sec C","Sec D","Sec E"]
    qualifications = ["M.Ed","B.Ed","M.Sc B.Ed","MA B.Ed","Ph.D"]

    # Teachers table
    teachers_list = []
    for i in range(20):
        rng = np.random.RandomState(i * 7 + 13)
        teachers_list.append({
            "teacher_id":          f"T{str(i+1).zfill(3)}",
            "teacher_name":        f"{first_names[i]} {last_names[i]}",
            "subject":             np.random.choice(subjects),
            "section":             np.random.choice(sections),
            "qualification":       np.random.choice(qualifications),
            "experience_current":  int(np.random.randint(2, 18)),
            "experience_previous": int(np.random.randint(0, 10)),
            "classes_per_week":    int(np.random.randint(18, 35)),
            "duties":              {d: bool(rng.choice([True, True, False])) for d, _ in DUTY_LIST},
            "hod_expectations":    list(np.random.choice(HOD_EXPECTATION_POOL, size=3, replace=False)),
        })
    teachers_df = pd.DataFrame(teachers_list)

    # Monthly performance table
    perf_list = []
    for _, t in teachers_df.iterrows():
        base_d, base_c, base_a = np.random.uniform(52,88), np.random.uniform(4.5,9), np.random.uniform(4.5,9)
        for mi, m in enumerate(MONTHS):
            perf_list.append({
                "teacher_id":             t.teacher_id,
                "teacher_name":           t.teacher_name,
                "subject":                t.subject,
                "section":                t.section,
                "month":                  m,
                "month_num":              mi + 1,
                "teaching_delivery_bm":   round(min(100, max(35, base_d + np.random.uniform(-3,3))), 1),
                "teaching_delivery_curr": round(min(100, max(35, base_d + np.random.uniform(-8,8) + 2.0*np.sin(np.pi*mi/11))), 1),
                "compliance_score":       round(min(10,  max(2,  base_c + np.random.uniform(-.8,.8) + mi*.04)), 1),
                "cca_score":              round(min(10,  max(2,  base_a + np.random.uniform(-.8,.8) + mi*.03)), 1),
            })
    performance_df = pd.DataFrame(perf_list)

    # Late arrivals table (May = summer break → 0)
    late_list = []
    for _, t in teachers_df.iterrows():
        for mi, m in enumerate(MONTHS):
            late_list.append({
                "teacher_id": t.teacher_id, "teacher_name": t.teacher_name,
                "month": m, "month_num": mi + 1,
                "late_count": 0 if m == "May" else max(0, int(np.random.poisson(1.5))),
            })
    late_df = pd.DataFrame(late_list)

    # Attrition risk table
    attr_explanations = {3.0:"Actively job-hunting; high stress reported", 2.0:"Disengaged; not motivated",
                         1.0:"Minor resistance to feedback", 0.0:"Committed and stable"}
    risk_labels       = {3:"High", 2:"Medium", 1:"Low", 0:"None"}
    attrition_list = []
    for _, t in teachers_df.iterrows():
        score = float(np.random.choice([0,0,0,1,1,2,2,3]))
        total_exp = t.experience_current + t.experience_previous
        if score > 0:
            choices = ["Voluntary","Involuntary","Retirement","Structural"] if total_exp >= 25 \
                      else ["Voluntary","Involuntary","Structural"]
            exit_type = np.random.choice(choices)
        else:
            exit_type = "None"
        attrition_list.append({
            "teacher_id": t.teacher_id, "teacher_name": t.teacher_name,
            "attrition_score": score, "attrition_type": exit_type,
            "attrition_explanation": attr_explanations[score],
            "risk_level": risk_labels[int(score)],
        })
    attrition_df = pd.DataFrame(attrition_list)

    # Compliance details table
    compliance_df = pd.DataFrame([{
        "teacher_id":                  t.teacher_id,
        "training_hours":              int(np.random.randint(8, 50)),
        "training_max":                50,
        "assignment_correction_stars": int(np.random.randint(1, 6)),
    } for _, t in teachers_df.iterrows()])

    # CCA participation table
    cca_df = pd.DataFrame([{
        "teacher_id":           t.teacher_id,
        "activities_completed": int(np.random.randint(3, 9)),
        "activities_total":     int(np.random.randint(10, 15)),
        "quality":              np.random.choice(["Excellent","Good","Needs Improvement"]),
    } for _, t in teachers_df.iterrows()])

    # Stakeholder ratings table (4 raters per teacher)
    ratings_df = pd.DataFrame([{
        "teacher_id": t.teacher_id, "stakeholder": sh,
        "stars": int(np.random.randint(1, 6)),
    } for _, t in teachers_df.iterrows() for sh in ["Head","Peer","Student","Parent"]])

    return teachers_df, performance_df, late_df, attrition_df, compliance_df, cca_df, ratings_df

teachers_df, performance_df, late_df, attrition_df, compliance_df, cca_df, ratings_df = generate_all_data()
ALL_TEACHER_NAMES = sorted(teachers_df["teacher_name"].tolist())

# ── Step 8: PDF report generator ─────────────────────────────────────────
def generate_pdf_report(teacher_name, section, subject, selected_month,
                         benchmark, actual, compliance, cca, overall, risk_level, late_count):
    """Generates a PDF (or plain-text fallback) report for a teacher."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
        styles = getSampleStyleSheet()
        story  = []

        story.append(Paragraph("myNalanda — Teacher Performance Report",
            ParagraphStyle('t', parent=styles['Title'], fontSize=18,
                           textColor=colors.HexColor('#0284c7'), spaceAfter=6)))
        story.append(Paragraph(
            f"Ideal International School  ·  {selected_month} {get_year_for_month(selected_month)}  ·  Academic Year 2025–26",
            ParagraphStyle('s', parent=styles['Normal'], fontSize=10,
                           textColor=colors.HexColor('#64748b'), spaceAfter=20)))
        story.append(Spacer(1, 0.3*cm))

        table_data = [
            ["Metric","Value"],
            ["Teacher Name",   teacher_name],
            ["Section",        section],
            ["Subject",        subject],
            ["Month",          selected_month],
            ["Benchmark Score",f"{benchmark:.1f}%"],
            ["Actual Score",   f"{actual:.1f}%"],
            ["Compliance",     f"{compliance:.1f}/10  ({get_compliance_label(compliance)})"],
            ["CCA Score",      f"{cca:.1f}/10  ({get_cca_label(cca)})"],
            ["Overall Score",  f"{overall:.1f}%  ({get_performance_label(overall)})"],
            ["Attrition Risk", risk_level],
            ["Late Arrivals",  str(late_count)],
        ]
        tbl = Table(table_data, colWidths=[7*cm, 10*cm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,0),  colors.HexColor('#0284c7')),
            ('TEXTCOLOR',    (0,0),(-1,0),  colors.white),
            ('FONTNAME',     (0,0),(-1,0),  'Helvetica-Bold'),
            ('FONTSIZE',     (0,0),(-1,0),  11),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f8fafc'), colors.white]),
            ('FONTNAME',     (0,1),(0,-1),  'Helvetica-Bold'),
            ('FONTSIZE',     (0,1),(-1,-1), 10),
            ('TEXTCOLOR',    (0,1),(0,-1),  colors.HexColor('#334155')),
            ('TEXTCOLOR',    (1,1),(-1,-1), colors.HexColor('#1e293b')),
            ('GRID',         (0,0),(-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWPADDING',   (0,0),(-1,-1), 8),
            ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.8*cm))
        story.append(Paragraph(
            "Generated by myNalanda Solutions & Services Pvt. Ltd.  ·  Updated: 23 Jan 2026  ·  Demo Dashboard",
            ParagraphStyle('f', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#94a3b8'))))
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    except ImportError:
        lines = [
            "myNalanda — Teacher Performance Report",
            f"Ideal International School · {selected_month} {get_year_for_month(selected_month)} · Academic Year 2025–26",
            "", f"Teacher: {teacher_name}", f"Section: {section}", f"Subject: {subject}",
            f"Month: {selected_month}", f"Benchmark: {benchmark:.1f}%", f"Actual: {actual:.1f}%",
            f"Compliance: {compliance:.1f}/10 ({get_compliance_label(compliance)})",
            f"CCA Score: {cca:.1f}/10 ({get_cca_label(cca)})",
            f"Overall: {overall:.1f}% ({get_performance_label(overall)})",
            f"Attrition Risk: {risk_level}", f"Late Arrivals: {late_count}", "",
            "Generated by myNalanda Solutions & Services Pvt. Ltd.",
        ]
        return "\n".join(lines).encode("utf-8")

# ── Step 9: Access control ────────────────────────────────────────────────
SCHOOL_ADMIN_SUBROLES = [
    "Principal / Vice Principal",
    "HOD (Head of Department)",
    "Admin / Office Staff",
    "External Coordinator",
]

# What each sub-role can see (True = allowed, False = blocked)
SUBROLE_ACCESS = {
    "Principal / Vice Principal": dict(dashboard_full=True, top_bottom_5=True, attrition_kpi=True,
        attrition_charts=True, teacher_profile=True, profile_all_teachers=True,
        late_page=True, attrition_table=True, downloads=True),
    "HOD (Head of Department)":   dict(dashboard_full=True, top_bottom_5=True, attrition_kpi=True,
        attrition_charts=True, teacher_profile=True, profile_all_teachers=False,
        late_page=True, attrition_table=True, downloads=True),
    "Admin / Office Staff":       dict(dashboard_full=False, top_bottom_5=False, attrition_kpi=False,
        attrition_charts=False, teacher_profile=False, profile_all_teachers=False,
        late_page=True, attrition_table=False, downloads=True),
    "External Coordinator":       dict(dashboard_full=True, top_bottom_5=False, attrition_kpi=False,
        attrition_charts=False, teacher_profile=False, profile_all_teachers=False,
        late_page=False, attrition_table=False, downloads=False),
}

# ── Step 10: Login page ───────────────────────────────────────────────────
def show_login_page():
    _, center_col, _ = st.columns([1, 1.4, 1])
    with center_col:
        st.markdown("""
        <div class="login-logo">
            <div style="font-size:52px;">🎓</div>
            <div class="brand"><span>my</span>Nalanda</div>
            <div class="tagline">Skills Analytics for Schools</div>
            <div style="font-size:12px;color:#334155;margin-top:6px;">myNalanda Solutions & Services Pvt. Ltd.</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.7px;margin-bottom:4px;">Login as</div>', unsafe_allow_html=True)
        selected_role = st.selectbox("Login as", ["myN Admin","School Admin","Teacher"],
                                     label_visibility="collapsed", key="login_role")

        selected_subrole, selected_teacher_name = None, None

        if selected_role == "School Admin":
            st.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.7px;margin:10px 0 4px;">Your Role</div>', unsafe_allow_html=True)
            selected_subrole = st.selectbox("Sub-role", SCHOOL_ADMIN_SUBROLES,
                                            label_visibility="collapsed", key="login_subrole")
            access = SUBROLE_ACCESS.get(selected_subrole, {})
            pages  = (["📊 Dashboard"] if access.get("dashboard_full") or selected_subrole == "Admin / Office Staff" else []) + \
                     (["👤 Teacher Profile"] if access.get("teacher_profile") else []) + \
                     (["⏰ Late Count"] if access.get("late_page") else [])
            st.markdown(
                f'<div style="margin:10px 0 6px;padding:10px 12px;background:#0f172a;border:1px solid #334155;'
                f'border-left:3px solid #8b5cf6;border-radius:8px;font-size:11px;color:#64748b;">'
                f'<b style="color:#a78bfa;">Access preview:</b> {" · ".join(pages) or "Limited view"}'
                f'</div>', unsafe_allow_html=True)

        if selected_role == "Teacher":
            st.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.7px;margin:10px 0 4px;">Select Your Name</div>', unsafe_allow_html=True)
            selected_teacher_name = st.selectbox("Your Name", ALL_TEACHER_NAMES,
                                                 label_visibility="collapsed", key="login_teacher")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("🔐  Login", use_container_width=True):
                if selected_role == "Teacher" and not selected_teacher_name:
                    st.error("Please select your name above.")
                elif selected_role == "School Admin" and not selected_subrole:
                    st.error("Please select your role above.")
                elif username == "admin" and password == "1234":
                    st.session_state.update(logged_in=True, role=selected_role,
                                            sub_role=selected_subrole, hod_section=None,
                                            teacher_name=selected_teacher_name if selected_role == "Teacher" else None)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials  —  admin / 1234")

        st.markdown("""
        <div style="margin-top:16px;background:#0f172a;border:1px solid #1e293b;border-radius:8px;
                    padding:10px 14px;font-size:11px;color:#475569;">
            <b style="color:#64748b;">Demo credentials:</b><br>
            Username: <b style="color:#94a3b8;">admin</b> &nbsp;·&nbsp;
            Password: <b style="color:#94a3b8;">1234</b><br>
            <span style="color:#334155;font-size:10px;">
                myN Admin → full access &nbsp;·&nbsp; School Admin → pick your role &nbsp;·&nbsp; Teacher → select your name
            </span>
        </div>""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ── Step 11: Role variables & permission flags ────────────────────────────
role           = st.session_state.role
sub_role       = st.session_state.sub_role
logged_teacher = st.session_state.teacher_name

is_myn_admin = role == "myN Admin"
is_school    = role == "School Admin"
is_teacher   = role == "Teacher"
is_principal = is_school and sub_role == "Principal / Vice Principal"
is_hod       = is_school and sub_role == "HOD (Head of Department)"
is_office    = is_school and sub_role == "Admin / Office Staff"
is_external  = is_school and sub_role == "External Coordinator"

def check_access(key):
    """Returns True if the current user's sub-role has permission for 'key'."""
    if is_myn_admin: return True
    if is_teacher:   return False
    return SUBROLE_ACCESS.get(sub_role, {}).get(key, False) if is_school and sub_role else False

can_see_full_dashboard   = is_myn_admin or is_teacher or check_access("dashboard_full")
can_see_top_bottom_5     = is_myn_admin or check_access("top_bottom_5")
can_see_attrition_kpi    = is_myn_admin or check_access("attrition_kpi")
can_see_attrition_charts = is_myn_admin or check_access("attrition_charts")
can_see_teacher_profile  = is_myn_admin or is_teacher or check_access("teacher_profile")
can_pick_any_teacher     = is_myn_admin or check_access("profile_all_teachers")
can_see_late_page        = is_myn_admin or check_access("late_page")
can_see_attrition_table  = is_myn_admin or check_access("attrition_table")
can_download_reports     = is_myn_admin or is_teacher or check_access("downloads")

# ── Step 12: Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="name"><span>my</span>Nalanda</div>
        <div class="school">Ideal International School</div>
    </div>""", unsafe_allow_html=True)

    pill_css = "role-admin" if is_myn_admin else "role-school" if is_school else "role-teacher"
    role_icon = "🛡️" if is_myn_admin else "🏫" if is_school else "👩‍🏫"
    display_role_name = sub_role if (is_school and sub_role) else role
    st.markdown(f'<div style="text-align:center;margin-bottom:6px;"><span class="role-pill {pill_css}">{role_icon} {display_role_name}</span></div>', unsafe_allow_html=True)

    if is_teacher:
        st.markdown(f'<div style="text-align:center;font-size:12px;color:#64748b;margin-bottom:12px;">👤 {logged_teacher}</div>', unsafe_allow_html=True)

    # Navigation options depend on role
    if is_myn_admin or is_principal or is_hod:
        nav_options = ["👩‍🏫 Dashboard", "👤 Teacher Profile", "⏰Late count & Attrition"]
    elif is_office:
        nav_options = ["⏰Late count & Attrition"]
    elif is_external:
        nav_options = ["👩‍🏫 Dashboard"]
    else:  # Teacher
        nav_options = ["👩‍🏫 Dashboard", "👤 My Profile"]

    current_page = st.radio("Nav", nav_options, label_visibility="collapsed")
    st.markdown("---")

    st.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">📅 Select Month</div>', unsafe_allow_html=True)
    selected_month = st.selectbox("Month", MONTHS, index=MONTHS.index("Dec"),
                                  label_visibility="collapsed", key="global_month")
    st.markdown(f"""
    <div style="margin-top:12px;padding:12px;background:#0f172a;border-radius:8px;
         font-size:11px;color:#64748b;border:1px solid #334155;">
        <b style="color:#cbd5e1;">Period:</b> {selected_month} {get_year_for_month(selected_month)}<br>
        <b style="color:#cbd5e1;">Acad. Year:</b> 2025–26<br>
        <b style="color:#cbd5e1;">Teachers:</b> {len(teachers_df)}<br>
        <b style="color:#cbd5e1;">Updated:</b> 23 Jan 2026
    </div>""", unsafe_allow_html=True)

    if st.button("⏎  Logout", use_container_width=True):
        st.session_state.update(logged_in=False, teacher_name=None, sub_role=None)
        st.rerun()

# ── Step 13: Filter data for the selected month ───────────────────────────
data_for_selected_month = performance_df[performance_df["month"] == selected_month].copy()
late_for_selected_month = late_df[late_df.month == selected_month]

kpi_numbers = {
    "total_teachers":           len(teachers_df),
    "avg_benchmark_score":      round(data_for_selected_month["teaching_delivery_bm"].mean(), 1),
    "avg_actual_score":         round(data_for_selected_month["teaching_delivery_curr"].mean(), 1),
    "avg_compliance_score":     round(data_for_selected_month["compliance_score"].mean(), 1),
    "avg_cca_score":            round(data_for_selected_month["cca_score"].mean(), 1),
    "at_risk_teachers":         len(attrition_df[attrition_df.attrition_score >= 2]),
    "total_lates_this_month":   int(late_for_selected_month["late_count"].sum()),
    "teachers_late_this_month": int((late_for_selected_month["late_count"] > 0).sum()),
}


# =====================================================
# PAGE 1 — DASHBOARD
# =====================================================
if current_page == "👩‍🏫 Dashboard":
    st.markdown('<p class="sec-title">👩‍🏫 Staff Performance Dashboard</p>', unsafe_allow_html=True)
    st.caption(f"Ideal International School  ·  {selected_month} {get_year_for_month(selected_month)}  ·  Academic Year 2025–26")

    # Role-specific read-only banners
    if is_teacher:
        st.markdown('<div class="readonly-banner">👁️ <b style="color:#38bdf8;">Read-only view</b> — You are viewing school-wide averages. Switch to <b>My Profile</b> to see your personal data.</div>', unsafe_allow_html=True)
    elif is_external:
        st.markdown('<div class="readonly-banner">🌐 <b style="color:#38bdf8;">External Coordinator — Read-only</b> — School-wide aggregate data only. Individual teacher data is not accessible.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:1px solid #334155;
                border-left:4px solid #38bdf8;border-radius:12px;padding:16px 20px;margin:10px 0 18px;">
        <div style="font-size:13px;font-weight:700;color:#38bdf8;letter-spacing:.6px;margin-bottom:6px;">📌 ABOUT THIS DASHBOARD</div>
        <div style="font-size:13px;color:#cbd5e1;line-height:1.7;">
            This dashboard monitors <b style="color:#f1f5f9;">teacher performance</b> at Ideal International School
            across five dimensions — helping school leadership make data-driven decisions.
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px;">
            <span style="background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.25);border-radius:20px;padding:4px 12px;font-size:11px;color:#38bdf8;">📚 Teaching Quality</span>
            <span style="background:rgba(139,92,246,.1);border:1px solid rgba(139,92,246,.25);border-radius:20px;padding:4px 12px;font-size:11px;color:#a78bfa;">🔏 Admin Compliance</span>
            <span style="background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.25);border-radius:20px;padding:4px 12px;font-size:11px;color:#4ade80;">🎭 CCA Participation</span>
            <span style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);border-radius:20px;padding:4px 12px;font-size:11px;color:#f87171;">⚠️ Attrition Risk</span>
            <span style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.25);border-radius:20px;padding:4px 12px;font-size:11px;color:#facc15;">⏰ Punctuality</span>
        </div>
        <div style="margin-top:10px;font-size:11px;color:#475569;">
            Overall Score = <b style="color:#94a3b8;">60% Teaching Quality</b> + <b style="color:#94a3b8;">25% Admin Compliance</b> + <b style="color:#94a3b8;">15% CCA Participation</b>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI Cards ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👩‍🏫 Total Teachers", kpi_numbers["total_teachers"])
    if can_see_attrition_kpi:
        col2.metric("⚠️ At-Risk of Leaving", kpi_numbers["at_risk_teachers"],
                    help="Teachers at medium or high attrition risk")
    else:
        col2.metric("📅 Selected Month", selected_month)
    col3.metric(f"⏰ Late Arrivals ({selected_month})", kpi_numbers["total_lates_this_month"],
                help=f"{kpi_numbers['teachers_late_this_month']} of {kpi_numbers['total_teachers']} teachers affected")
    st.caption(f"↳ {kpi_numbers['teachers_late_this_month']} of {kpi_numbers['total_teachers']} teachers had ≥1 late arrival")
    weighted_overall = round(data_for_selected_month["teaching_delivery_curr"].mean()*0.6 +
                             data_for_selected_month["compliance_score"].mean()/10*25 +
                             data_for_selected_month["cca_score"].mean()/10*15, 1)
    col4.metric("🎓 Avg Overall Score", f"{weighted_overall}%",
                help="Weighted: 60% Teaching + 25% Compliance + 15% CCA")

    st.markdown("---")

    # ── 4 Gauge Charts ────────────────────────────────────────────────────
    gauge_cols = st.columns(4)
    gauge_data_list = [
        ("Teaching Quality\n(Expected Benchmark)", kpi_numbers["avg_benchmark_score"],  100, "%"),
        ("Teaching Quality\n(Observed Actual)",    kpi_numbers["avg_actual_score"],     100, "%"),
        ("Admin Compliance\n(Training & Marking)", kpi_numbers["avg_compliance_score"],  10, "/10"),
        ("CCA Participation\n(Co-curricular)",     kpi_numbers["avg_cca_score"],         10, "/10"),
    ]
    for col, (title, value, max_val, unit) in zip(gauge_cols, gauge_data_list):
        pct = value / max_val
        color = "#4ade80" if pct>.75 else "#38bdf8" if pct>.5 else "#facc15" if pct>.3 else "#f87171"
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=round(value,1),
            number={"font":{"color":"#38bdf8","size":30},"suffix":unit},
            title={"text":f"<b>{title}</b>","font":{"color":"#94a3b8","size":12},"align":"center"},
            domain={"x":[0,1],"y":[0,1]},
            gauge={
                "axis":{"range":[0,max_val],"tickcolor":"#334155","tickfont":{"color":"#64748b","size":9}},
                "bar":{"color":color,"thickness":.35},
                "bgcolor":"#0f172a","borderwidth":0,
                "steps":[{"range":[0,max_val*.4],"color":"rgba(239,68,68,.08)"},
                          {"range":[max_val*.4,max_val*.65],"color":"rgba(234,179,8,.08)"},
                          {"range":[max_val*.65,max_val],"color":"rgba(34,197,94,.08)"}],
                "threshold":{"line":{"color":"#f1f5f9","width":2},"thickness":.75,"value":value},
            }))
        fig.update_layout(**get_dark_chart_layout(height=240, margin=dict(t=60,b=10,l=30,r=30)), autosize=True)
        with col:
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Monthly Trend Line Chart ───────────────────────────────────────────
    monthly_trend = (performance_df.groupby("month")
                     .agg(actual=("teaching_delivery_curr","mean"),
                          benchmark=("teaching_delivery_bm","mean"),
                          compliance=("compliance_score","mean"))
                     .reindex(MONTHS).reset_index())

    show_chart_title(f"📈 School-wide Monthly Performance Trend — Academic Year 2025–26  |  Selected: {selected_month}")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=monthly_trend.month, y=monthly_trend.actual,
        name="Actual Teaching Score", mode="lines", line=dict(color="#38bdf8",width=3),
        fill="tozeroy", fillcolor="rgba(56,189,248,.08)",
        hovertemplate="<b>%{x}</b> · Actual: %{y:.1f}%<extra></extra>"))
    fig_trend.add_trace(go.Scatter(x=monthly_trend.month, y=monthly_trend.benchmark,
        name="Benchmark", mode="lines", line=dict(color="#8b5cf6",width=2,dash="dot"),
        hovertemplate="<b>%{x}</b> · Benchmark: %{y:.1f}%<extra></extra>"))
    fig_trend.add_trace(go.Scatter(x=monthly_trend.month, y=monthly_trend.compliance*10,
        name="Compliance (×10 for scale)", mode="lines", line=dict(color="#4ade80",width=2),
        customdata=monthly_trend.compliance,
        hovertemplate="<b>%{x}</b> · Compliance: %{customdata:.1f}/10  (×10 for scale)<extra></extra>"))
    add_month_vline(fig_trend, selected_month, MONTHS)
    fig_trend.update_layout(**get_dark_chart_layout(height=300, margin=dict(t=10,b=60,l=55,r=20)),
                            yaxis_title="Score (0–100)", xaxis_title="Month")
    apply_dark_axes(fig_trend)
    fig_trend.update_layout(legend=dict(orientation="h", y=-0.22, bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8",size=11)))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ── Section-wise Charts ────────────────────────────────────────────────
    section_data = (data_for_selected_month.groupby("section")
                    .agg(delivery=("teaching_delivery_curr","mean"),
                         comp=("compliance_score","mean"),
                         cca=("cca_score","mean"),
                         num_teachers=("teacher_id","nunique"))
                    .reset_index())

    chart_col_a, chart_col_b = st.columns(2)
    with chart_col_a:
        show_chart_title(f"🏫 Teaching Quality vs Admin Compliance by Section ({selected_month} {get_year_for_month(selected_month)})")
        fig_sec = go.Figure()
        fig_sec.add_trace(go.Bar(x=section_data.section, y=section_data.delivery,
            name="Teaching Score (%)", marker_color="#38bdf8",
            hovertemplate="<b>%{x}</b> · Teaching: %{y:.1f}%<extra></extra>"))
        fig_sec.add_trace(go.Bar(x=section_data.section, y=section_data.comp*10,
            name="Compliance (×10)", marker_color="#8b5cf6",
            hovertemplate="<b>%{x}</b> · Compliance: %{y:.1f} (raw ÷10)<extra></extra>"))
        fig_sec.update_layout(**get_dark_chart_layout(height=280, margin=dict(t=10,b=50,l=55,r=20)),
                              barmode="group", yaxis_range=[0,100],
                              xaxis_title="Section", yaxis_title="Score")
        apply_dark_axes(fig_sec)
        st.plotly_chart(fig_sec, use_container_width=True)

    with chart_col_b:
        show_chart_title("🔵 Admin Compliance vs CCA Participation by Section  (bubble = no. of teachers)")
        fig_sc = px.scatter(section_data, x="comp", y="cca", text="section",
                            size="num_teachers", color_discrete_sequence=["#38bdf8"])
        fig_sc.update_traces(textposition="top center",
            hovertemplate="<b>%{text}</b> · Compliance:%{x:.1f}  CCA:%{y:.1f}<extra></extra>")
        fig_sc.update_layout(**get_dark_chart_layout(height=280, margin=dict(t=10,b=50,l=65,r=20)),
                             xaxis_title="Compliance (0–10)", yaxis_title="CCA Score (0–10)")
        apply_dark_axes(fig_sc)
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── Top & Bottom 5 ────────────────────────────────────────────────────
    if can_see_top_bottom_5:
        teachers_ranked = (data_for_selected_month.groupby("teacher_name")["teaching_delivery_curr"]
                           .mean().reset_index().sort_values("teaching_delivery_curr", ascending=False))
        top_col, bottom_col = st.columns(2)

        for col, label, color, df_slice in [
            (top_col,    f"🏆 Top 5 Teachers — {selected_month}",     "#4ade80", teachers_ranked.head(5)),
            (bottom_col, "🔴 Bottom 5 Teachers — Need Support",        "#f87171", teachers_ranked.tail(5)),
        ]:
            with col:
                show_chart_title(label)
                fig_rank = go.Figure(go.Bar(
                    x=df_slice.teaching_delivery_curr, y=df_slice.teacher_name, orientation="h",
                    marker_color=color, text=df_slice.teaching_delivery_curr.map("{:.1f}%".format),
                    textposition="outside", hovertemplate="<b>%{y}</b> · %{x:.1f}%<extra></extra>"))
                fig_rank.update_layout(**get_dark_chart_layout(height=260, margin=dict(l=130,r=70,t=10,b=40)),
                                       xaxis_range=[0,115], xaxis_title="Teaching Score (%)")
                apply_dark_axes(fig_rank)
                st.plotly_chart(fig_rank, use_container_width=True)

    st.markdown("---")

    # ── Attrition Charts ──────────────────────────────────────────────────
    if can_see_attrition_charts:
        show_chart_title("⚠️ Attrition Risk Distribution")
        risk_counts = (attrition_df["risk_level"].value_counts()
                       .reindex(["High","Medium","Low","None"], fill_value=0).reset_index())
        risk_counts.columns = ["label","count"]
        risk_colors = {"High":"#f87171","Medium":"#facc15","Low":"#38bdf8","None":"#4ade80"}

        pie_col, bar_col = st.columns(2)
        with pie_col:
            fig_pie = go.Figure(go.Pie(
                labels=risk_counts.label, values=risk_counts["count"],
                marker=dict(colors=[risk_colors[l] for l in risk_counts.label]),
                hole=.45, textinfo="label+value", textfont=dict(color="#f1f5f9",size=12),
                hovertemplate="<b>%{label}</b> · %{value} teachers · %{percent}<extra></extra>"))
            fig_pie.update_layout(**get_dark_chart_layout(height=290, margin=dict(t=20,b=20,l=20,r=20)),
                                  annotations=[dict(text="Risk<br>Level",x=.5,y=.5,
                                                    font_size=12,showarrow=False,font_color="#94a3b8")])
            apply_dark_axes(fig_pie)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.caption("🔴 High = leave soon  🟡 Medium = at risk  🔵 Low = minor concern  🟢 Stable")

        with bar_col:
            exit_counts = (attrition_df[attrition_df.attrition_score > 0]["attrition_type"]
                           .value_counts().reset_index())
            exit_counts.columns = ["type","count"]
            fig_exit = go.Figure(go.Bar(x=exit_counts.type, y=exit_counts["count"],
                marker_color="#8b5cf6", text=exit_counts["count"], textposition="outside",
                textfont=dict(color="#f1f5f9",size=11),
                hovertemplate="<b>%{x}</b> · %{y} teachers<extra></extra>"))
            fig_exit.update_layout(**get_dark_chart_layout(height=290, margin=dict(t=20,b=60,l=55,r=20)),
                                   xaxis_title="Exit Type", yaxis_title="No. of Teachers",
                                   yaxis_range=[0, exit_counts["count"].max()+2])
            apply_dark_axes(fig_exit)
            st.plotly_chart(fig_exit, use_container_width=True)
            st.caption("Voluntary = teacher's choice  |  Involuntary = school decision  |  Structural = role removed")


# =====================================================
# PAGE 2 — TEACHER PROFILE
# =====================================================
elif current_page in ("👤 Teacher Profile", "👤 My Profile"):
    if is_teacher:
        st.markdown('<p class="sec-title">👤 My Performance Profile</p>', unsafe_allow_html=True)
        st.markdown(f"""<div style="background:#1e293b;border:1px solid #334155;border-left:4px solid #4ade80;
            border-radius:12px;padding:12px 18px;margin-bottom:16px;">
            <span style="font-size:12px;color:#4ade80;font-weight:700;">👩‍🏫 YOUR PROFILE &nbsp;·&nbsp;</span>
            <span style="font-size:12px;color:#94a3b8;">Viewing your personal performance data for
            <b style="color:#f1f5f9;">{selected_month} {get_year_for_month(selected_month)}</b>.</span>
        </div>""", unsafe_allow_html=True)
        selected_teacher = logged_teacher
    else:
        st.markdown('<p class="sec-title">👤 Teacher Performance Profile</p>', unsafe_allow_html=True)
        st.markdown("""<div style="background:#1e293b;border:1px solid #334155;border-left:4px solid #8b5cf6;
            border-radius:12px;padding:12px 18px;margin-bottom:16px;">
            <span style="font-size:12px;color:#a78bfa;font-weight:700;">📋 HOW TO READ THIS PAGE &nbsp;·&nbsp;</span>
            <span style="font-size:12px;color:#94a3b8;">Select a teacher below to view their full profile.</span>
        </div>""", unsafe_allow_html=True)
        selected_teacher = st.selectbox("Select Teacher", sorted(performance_df.teacher_name.unique()))

    # Fetch all data rows for selected teacher
    teacher_info_row   = teachers_df[teachers_df.teacher_name == selected_teacher].iloc[0]
    teacher_perf_month = performance_df[(performance_df.teacher_name == selected_teacher) & (performance_df.month == selected_month)]
    teacher_perf_all   = performance_df[performance_df.teacher_name == selected_teacher].copy()
    teacher_late_month = late_df[(late_df.teacher_name == selected_teacher) & (late_df.month == selected_month)]
    teacher_compliance = compliance_df[compliance_df.teacher_id == teacher_info_row.teacher_id].iloc[0]
    teacher_cca        = cca_df[cca_df.teacher_id == teacher_info_row.teacher_id].iloc[0]
    teacher_ratings    = ratings_df[ratings_df.teacher_id == teacher_info_row.teacher_id].set_index("stakeholder")["stars"]
    teacher_attrition  = attrition_df[attrition_df.teacher_id == teacher_info_row.teacher_id].iloc[0]

    if teacher_perf_month.empty:
        st.warning(f"No data for {selected_month}.")
        st.stop()

    monthly_row      = teacher_perf_month.iloc[0]
    benchmark_score  = monthly_row.teaching_delivery_bm
    actual_score     = monthly_row.teaching_delivery_curr
    compliance_score = monthly_row.compliance_score
    cca_score        = monthly_row.cca_score
    late_count       = int(teacher_late_month.late_count.values[0]) if len(teacher_late_month) else 0
    overall_score    = min(100, actual_score*.6 + compliance_score/10*25 + cca_score/10*15)
    score_vs_bench   = actual_score - benchmark_score

    # ── Top row: Late card | Overall gauge | Teacher info card ───────────
    info_col1, gauge_col, info_col2 = st.columns([1.4, 1, 1.4])

    with info_col1:
        boxes_html = "".join([
            f'<div style="width:20px;height:20px;border-radius:4px;margin:2px;display:inline-block;'
            f'background:{"#f87171" if i < late_count else "#1e293b"};border:1px solid #334155;"></div>'
            for i in range(12)])
        late_status = "✅ No issues" if late_count == 0 else "⚠️ Monitor" if late_count > 2 else "🟡 Minor"
        st.markdown(f"""
        <div class="card">
            <div class="card-title">⏰ Late Arrivals — {selected_month}</div>
            <div style="font-size:40px;font-weight:800;color:#f87171;line-height:1;">{late_count}</div>
            <div style="font-size:12px;color:#64748b;margin:6px 0 10px;">times late &nbsp;·&nbsp; <b style="color:#f1f5f9;">{late_status}</b></div>
            <div style="font-size:10px;color:#475569;margin-bottom:5px;">Monthly tracker (🔴 = late)</div>
            {boxes_html}
        </div>""", unsafe_allow_html=True)

    with gauge_col:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=round(overall_score,1),
            number={"font":{"color":"#38bdf8","size":32},"suffix":"%"},
            title={"text":"<b>Overall Score</b>","font":{"color":"#94a3b8","size":13},"align":"center"},
            gauge={"axis":{"range":[0,100],"tickcolor":"#334155","tickfont":{"color":"#64748b","size":9}},
                   "bar":{"color":"#38bdf8","thickness":.4},"bgcolor":"#0f172a","borderwidth":0,
                   "steps":[{"range":[0,40],"color":"rgba(239,68,68,.1)"},
                              {"range":[40,65],"color":"rgba(234,179,8,.1)"},
                              {"range":[65,100],"color":"rgba(34,197,94,.1)"}]}))
        fig_gauge.update_layout(**get_dark_chart_layout(height=240, margin=dict(t=60,b=10,l=30,r=30)), autosize=True)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(f"60% Teaching + 25% Compliance + 15% CCA  ·  **{get_performance_label(overall_score)}**")

    with info_col2:
        attrition_row_html = (f'<div class="info-row"><span>Attrition Risk</span><b>{get_risk_badge_html(teacher_attrition.attrition_score)}</b></div>'
                              if can_see_attrition_kpi else "")
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Teacher Info</div>
            <div class="info-row"><span>Qualification</span><b>{teacher_info_row.qualification}</b></div>
            <div class="info-row"><span>Experience (Here)</span><b>{teacher_info_row.experience_current} yrs</b></div>
            <div class="info-row"><span>Prior Experience</span><b>{teacher_info_row.experience_previous} yrs</b></div>
            <div class="info-row"><span>Section</span><b>{teacher_info_row.section}</b></div>
            <div class="info-row"><span>Subject</span><b>{teacher_info_row.subject}</b></div>
            <div class="info-row"><span>Classes / Week</span><b>{teacher_info_row.classes_per_week}</b></div>
            {attrition_row_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Middle row: Compliance | Benchmark | Actual ───────────────────────
    comp_col, bench_col, actual_col = st.columns(3)

    with comp_col:
        st.markdown('<div class="card-title">🔏 Compliance <span style="font-size:10px;color:#475569;font-weight:400;">(Year-to-date)</span></div>', unsafe_allow_html=True)
        st.progress(float(teacher_compliance.training_hours / teacher_compliance.training_max),
                    f"Training: {teacher_compliance.training_hours}/{teacher_compliance.training_max} hrs")
        sf = int(teacher_compliance.assignment_correction_stars)
        st.markdown(f"**Assignment Marking:** {'⭐'*sf}{'☆'*(5-sf)}  ({sf}/5)")
        school_avg_comp = round(data_for_selected_month["compliance_score"].mean(), 1)
        st.metric("Compliance Score", f"{compliance_score:.1f}/10",
                  delta=f"{compliance_score - school_avg_comp:.1f} vs school avg ({school_avg_comp}/10)")
        st.caption(f"Status: **{get_compliance_label(compliance_score)}**")

    with bench_col:
        st.markdown('<div class="card-title">📚 Teaching Score — Benchmark</div>', unsafe_allow_html=True)
        st.caption("Expected score based on experience & historical data")
        st.progress(float(benchmark_score / 100))
        st.metric("Expected", f"{benchmark_score:.1f}%")
        st.caption(f"Level: **{get_performance_label(benchmark_score)}**  ·  Target ≥ 70%")
        for criterion in ["Lesson Plan","Worksheet Quality","Time Management","Teaching Methods","Lesson Flow"]:
            st.caption(f"  · {criterion}")

    with actual_col:
        delta_color = "#4ade80" if score_vs_bench >= 0 else "#f87171"
        delta_arrow = "▲" if score_vs_bench >= 0 else "▼"
        st.markdown('<div class="card-title">📝 Teaching Score — Actual</div>', unsafe_allow_html=True)
        st.caption("Observed score this month from classroom evaluation")
        st.progress(float(actual_score / 100))
        st.metric("Actual", f"{actual_score:.1f}%", delta=f"{score_vs_bench:.1f}% vs benchmark")
        st.markdown(f"<span style='color:{delta_color};font-size:13px;font-weight:600;'>{delta_arrow} {abs(score_vs_bench):.1f}% {'above' if score_vs_bench >= 0 else 'below'} benchmark</span>", unsafe_allow_html=True)
        st.caption(f"Level: **{get_performance_label(actual_score)}**")

    st.markdown("---")

    # ── Bottom row: CCA | Ratings | HOD Expectations & Duties ────────────
    cca_col, ratings_col, expectations_col = st.columns(3)

    with cca_col:
        st.markdown('<div class="card-title">🎭 CCA Contribution <span style="font-size:10px;color:#475569;font-weight:400;">(Year-to-date)</span></div>', unsafe_allow_html=True)
        st.progress(float(teacher_cca.activities_completed / max(teacher_cca.activities_total,1)),
                    f"{teacher_cca.activities_completed}/{teacher_cca.activities_total} activities")
        qc = {"Excellent":"#4ade80","Good":"#38bdf8"}.get(teacher_cca.quality,"#facc15")
        st.markdown(f"Quality: <b style='color:{qc}'>{teacher_cca.quality}</b>", unsafe_allow_html=True)
        st.metric("CCA Score", f"{cca_score:.1f}/10")
        st.caption(f"Level: **{get_cca_label(cca_score)}**")

    with ratings_col:
        st.markdown('<div class="card-title">🤝 Stakeholder Ratings</div>', unsafe_allow_html=True)
        for sh in ["Head","Peer","Student","Parent"]:
            s = int(teacher_ratings.get(sh, 3))
            st.markdown(f"**{sh}** &nbsp; {'⭐'*s}{'☆'*(5-s)} **{s}/5**", unsafe_allow_html=True)

    with expectations_col:
        st.markdown('<div class="card-title">🎯 HOD Expectations</div>', unsafe_allow_html=True)
        for exp in teacher_info_row.hod_expectations:
            st.markdown(f"📌 {exp}")
        st.markdown("---")
        st.markdown('<div class="card-title" style="margin-top:6px;">🏫 School Duties</div>', unsafe_allow_html=True)
        for duty_name, duty_desc in DUTY_LIST:
            icon = "✅" if teacher_info_row.duties[duty_name] else "❌"
            st.markdown(f"{icon} **{duty_name}**")
            st.caption(f"  _{duty_desc}_")

    st.markdown("---")

    # ── Trend chart + Summary bar ─────────────────────────────────────────
    trend_col, summary_col = st.columns([1.6, 1])

    with trend_col:
        show_chart_title("📈 Individual Performance Trend — Full Academic Year 2025–26")
        teacher_perf_all["month"] = pd.Categorical(teacher_perf_all.month, categories=MONTHS, ordered=True)
        ths = teacher_perf_all.sort_values("month")
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Scatter(x=ths.month, y=ths.teaching_delivery_bm, name="Benchmark",
            mode="lines+markers", line=dict(color="#8b5cf6",width=2), marker=dict(size=5),
            hovertemplate="%{x} · Benchmark: %{y:.1f}%<extra></extra>"))
        fig_tr.add_trace(go.Scatter(x=ths.month, y=ths.teaching_delivery_curr, name="Actual",
            mode="lines+markers", line=dict(color="#38bdf8",width=2), marker=dict(size=5),
            hovertemplate="%{x} · Actual: %{y:.1f}%<extra></extra>"))
        fig_tr.add_trace(go.Scatter(x=ths.month, y=ths.compliance_score*10, name="Compliance (×10)",
            mode="lines", line=dict(color="#4ade80",width=2,dash="dot"),
            customdata=ths.compliance_score,
            hovertemplate="%{x} · Compliance: %{customdata:.1f}/10  (×10 for scale)<extra></extra>"))
        add_month_vline(fig_tr, selected_month, MONTHS)
        fig_tr.update_layout(**get_dark_chart_layout(height=270, margin=dict(t=10,b=70,l=55,r=20)),
                             yaxis_title="Score (%)", xaxis_title="Month")
        apply_dark_axes(fig_tr)
        fig_tr.update_layout(legend=dict(orientation="h",y=-0.32,bgcolor="rgba(0,0,0,0)",font=dict(color="#94a3b8",size=11)))
        st.plotly_chart(fig_tr, use_container_width=True)

    with summary_col:
        show_chart_title("📊 Score Summary — Normalized to 0–100")
        norm_comp = (compliance_score / 10) * 100
        norm_cca  = (cca_score / 10) * 100
        summary_df = pd.DataFrame({
            "Metric": ["Benchmark\n(Teaching)","Actual\n(Teaching)","Compliance\n(Normalized)","CCA\n(Normalized)"],
            "Score":  [benchmark_score, actual_score, norm_comp, norm_cca],
            "Raw":    [f"{benchmark_score:.1f}%", f"{actual_score:.1f}%", f"{compliance_score:.1f}/10", f"{cca_score:.1f}/10"],
            "Rating": [get_performance_label(benchmark_score), get_performance_label(actual_score),
                       get_compliance_label(compliance_score), get_cca_label(cca_score)],
        })
        fig_sum = px.bar(summary_df, x="Metric", y="Score", color="Score", text="Raw",
                         color_continuous_scale=["#f87171","#facc15","#38bdf8","#4ade80"],
                         range_color=[0,100], custom_data=["Rating","Raw"])
        fig_sum.update_traces(texttemplate="%{customdata[1]}", textposition="outside",
            textfont=dict(color="#f1f5f9"),
            hovertemplate="<b>%{x}</b><br>Normalized: %{y:.1f}/100<br>Raw: %{customdata[1]}<br>Rating: %{customdata[0]}<extra></extra>")
        fig_sum.update_layout(**get_dark_chart_layout(height=300, margin=dict(t=20,b=20,l=55,r=20)),
                              showlegend=False, coloraxis_showscale=False,
                              yaxis_range=[0,120], yaxis_title="Score (normalized 0–100)")
        apply_dark_axes(fig_sum)
        st.plotly_chart(fig_sum, use_container_width=True)
        st.caption("All metrics converted to 0–100 scale for fair comparison. Raw values shown on bars.")

    # ── Download button ────────────────────────────────────────────────────
    if can_download_reports:
        report_bytes = generate_pdf_report(selected_teacher, teacher_info_row.section,
                                           teacher_info_row.subject, selected_month,
                                           benchmark_score, actual_score, compliance_score,
                                           cca_score, overall_score, teacher_attrition.risk_level, late_count)
        is_pdf = isinstance(report_bytes, bytes) and report_bytes[:4] == b'%PDF'
        btn_label = ("⬇  Download My Report" if is_teacher else "⬇  Download Teacher Report") + (" (PDF)" if is_pdf else " (TXT)")
        st.download_button(btn_label, report_bytes,
                           f"report_{teacher_info_row.teacher_id}_{selected_month}.{'pdf' if is_pdf else 'txt'}",
                           "application/pdf" if is_pdf else "text/plain")
        if not is_pdf:
            st.caption("💡 Install `reportlab` (`pip install reportlab`) for PDF output.")


# =====================================================
# PAGE 3 — LATE COUNT & ATTRITION
# =====================================================
elif current_page == "⏰Late count & Attrition":
    st.markdown('<p class="sec-title">⏰ Teacher Punctuality & Retention Risk</p>', unsafe_allow_html=True)
    st.caption(f"Late arrival patterns · Teacher attrition & retention risk  ·  {selected_month} {get_year_for_month(selected_month)}")

    st.markdown("""
    <div style="background:#1e293b;border:1px solid #334155;border-left:4px solid #facc15;
                border-radius:12px;padding:12px 18px;margin:10px 0 16px;">
        <span style="font-size:12px;color:#facc15;font-weight:700;">📌 WHAT THIS PAGE SHOWS &nbsp;·&nbsp;</span>
        <span style="font-size:12px;color:#94a3b8;">
            <b style="color:#cbd5e1;">Left panel:</b> Individual and school-wide late arrival patterns. &nbsp;|&nbsp;
            <b style="color:#cbd5e1;">Right panel:</b> Attrition risk scores (0 = Stable → 3 = High Risk).
            <b style="color:#facc15;">Annual snapshot</b> — scores do not change by month.
        </span>
    </div>""", unsafe_allow_html=True)

    if is_office or is_external:
        st.markdown(f'<div style="background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.25);border-left:4px solid #8b5cf6;border-radius:10px;padding:10px 16px;margin-bottom:16px;font-size:12px;color:#a78bfa;">🔒 You are logged in as <b>{sub_role}</b>. Attrition risk data is restricted to myN Admin, Principal / VP, and HOD only.</div>', unsafe_allow_html=True)

    st.markdown("---")

    late_col, attrition_col = st.columns([1, 1.6])

    with late_col:
        # ── Individual teacher late history ────────────────────────────────
        show_chart_title("⏰ Individual Teacher — Late Arrival History")
        sel_late_teacher = st.selectbox("Select Teacher", sorted(late_df.teacher_name.unique()), key="lt")
        tlh = late_df[late_df.teacher_name == sel_late_teacher].copy()
        tlh["month"] = pd.Categorical(tlh.month, categories=MONTHS, ordered=True)
        tlh = tlh.sort_values("month")

        tl1, tl2 = st.columns(2)
        tl1.metric("Total Lates (Year)", tlh["late_count"].sum())
        tl2.metric("Worst Month", tlh.loc[tlh["late_count"].idxmax(), "month"])

        dot_colors = ["#f87171" if v>=3 else "#facc15" if v==2 else "#38bdf8" for v in tlh.late_count]
        fig_late = go.Figure(go.Scatter(x=tlh.month, y=tlh.late_count, mode="lines+markers",
            line=dict(color="#38bdf8",width=2), marker=dict(size=11, color=dot_colors),
            fill="tozeroy", fillcolor="rgba(56,189,248,.07)",
            hovertemplate="<b>%{x}</b> · %{y} late(s)<extra></extra>"))
        add_month_vline(fig_late, selected_month, MONTHS)
        fig_late.update_layout(**get_dark_chart_layout(height=280, margin=dict(t=10,b=50,l=55,r=20)),
                               xaxis_title="Month", yaxis_title="Late Count", yaxis_dtick=1)
        apply_dark_axes(fig_late)
        st.plotly_chart(fig_late, use_container_width=True)
        st.caption("🔴 ≥3  🟡 =2  🔵 0–1")

        st.markdown("---")

        # ── School-wide late count per month ──────────────────────────────
        show_chart_title("🏫 School-wide Late Count — All Teachers per Month")
        school_late = (late_df.groupby("month")["late_count"].sum().reindex(MONTHS).reset_index())
        school_late.columns = ["month","count"]
        avg_l = school_late["count"].mean()
        bar_colors = ["#f87171" if v>avg_l*1.3 else "#facc15" if v>avg_l else "#38bdf8" for v in school_late["count"]]
        fig_sl = go.Figure()
        fig_sl.add_trace(go.Bar(x=school_late.month, y=school_late["count"], marker_color=bar_colors,
            text=school_late["count"], textposition="outside", textfont=dict(color="#f1f5f9",size=9),
            hovertemplate="<b>%{x}</b> · %{y} total late arrivals<extra></extra>"))
        fig_sl.add_hline(y=avg_l, line_dash="dot", line_color="#94a3b8", line_width=1,
                         annotation_text=f"  avg {avg_l:.0f}", annotation_font_color="#94a3b8")
        add_month_vline(fig_sl, selected_month, MONTHS)
        fig_sl.update_layout(**get_dark_chart_layout(height=250, margin=dict(t=10,b=50,l=55,r=20)),
                             xaxis_title="Month", yaxis_title="Total Late Count",
                             yaxis_range=[0, school_late["count"].max()+10])
        apply_dark_axes(fig_sl)
        st.plotly_chart(fig_sl, use_container_width=True)
        st.caption("🔴 >130% avg  🟡 >avg  🔵 normal")

    with attrition_col:
        if can_see_attrition_table:
            show_chart_title("⚠️ Attrition Risk — Annual Snapshot")
            st.markdown("""<div style="background:#0f172a;border:1px solid #334155;border-left:3px solid #facc15;
                border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:11px;color:#64748b;">
                📌 <b style="color:#facc15;">Annual Snapshot</b> — Scores based on full-year HR observations; do not change by month.
            </div>""", unsafe_allow_html=True)
            st.caption("Score: 0 = Stable · 1 = Low · 2 = Medium · 3 = High (act now)")

            r1, r2, r3, r4 = st.columns(4)
            r1.metric("🔴 High",   len(attrition_df[attrition_df.attrition_score == 3]))
            r2.metric("🟡 Medium", len(attrition_df[attrition_df.attrition_score == 2]))
            r3.metric("🔵 Low",    len(attrition_df[attrition_df.attrition_score == 1]))
            r4.metric("🟢 Stable", len(attrition_df[attrition_df.attrition_score == 0]))

            exit_filter = st.selectbox("Filter by exit type",
                ["All","Voluntary","Involuntary","Retirement","Structural","None"])
            disp = attrition_df.copy()
            if exit_filter != "All":
                disp = disp[disp.attrition_type == exit_filter]
            disp = disp.sort_values("attrition_score", ascending=False)
            ds = disp[["teacher_name","attrition_score","risk_level","attrition_type","attrition_explanation"]].copy()
            ds.columns = ["Teacher","Score","Risk Level","Exit Type","Reason"]

            def color_row_by_risk(row):
                bg = {3:"rgba(239,68,68,.14)", 2:"rgba(234,179,8,.14)", 1:"rgba(56,189,248,.08)"}.get(row["Score"],"")
                return [f"background-color:{bg}" if bg else "" for _ in row]

            st.dataframe(ds.style.apply(color_row_by_risk, axis=1), height=460, use_container_width=True)
            st.caption("🔴 High (3) · 🟡 Medium (2) · 🔵 Low (1) · White = Stable (0)")
            st.download_button("⬇  Download Attrition Report (CSV)",
                               disp.to_csv(index=False), "attrition_report.csv", "text/csv")
        else:
            st.markdown("""
            <div style="height:400px;display:flex;flex-direction:column;align-items:center;
                        justify-content:center;background:#0f172a;border:1px dashed #334155;
                        border-radius:14px;text-align:center;padding:30px;">
                <div style="font-size:48px;margin-bottom:16px;">🔒</div>
                <div style="font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:8px;">Attrition Data Restricted</div>
                <div style="font-size:13px;color:#64748b;max-width:300px;line-height:1.6;">
                    Attrition risk scores are only visible to
                    <b style="color:#38bdf8;">myN Admin</b>,
                    <b style="color:#38bdf8;">Principal / Vice Principal</b>, and
                    <b style="color:#38bdf8;">HOD</b>.<br><br>
                    Contact your school administrator for access.
                </div>
            </div>""", unsafe_allow_html=True)