import pandas as pd
import numpy as np
import streamlit as st

MONTHS = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]

def month_year(m):
    return 2026 if m in ["Jan","Feb","Mar"] else 2025

HOD_POOL = [
    "Activity-based learning","Better assessments","Parent communication","Use of technology",
    "Improve lesson planning","Peer collaboration","Student feedback integration",
    "Timely report submission","Differentiated instruction","Professional development",
    "Class discipline","Regular student counselling"
]

DUTY_PARAMS = [
    ("Academic Board","Curriculum & board meetings"),
    ("Exam Portfolio","Managing exam papers"),
    ("Admissions","New student onboarding"),
    ("Affiliations","External board coordination"),
]

@st.cache_data
def generate_data():
    """
    Generates all synthetic datasets for the myNalanda dashboard.

    Returns:
        tdf    - Teacher master profiles (20 rows)
        pdf    - Monthly performance scores (240 rows = 20 teachers x 12 months)
        ldf    - Monthly late arrival counts (240 rows)
        adf    - Annual attrition risk scores (20 rows)
        cdf    - Compliance data: training hours + marking stars (20 rows)
        ccadf  - CCA participation data (20 rows)
        aldf   - Stakeholder ratings from Head/Peer/Student/Parent (80 rows)
    """
    np.random.seed(42)

    first = ["Linda","James","Emily","Robert","Sarah","David","Jessica","Kevin","Patricia","Matthew",
             "Rajesh","Priya","Amit","Sunita","Vikram","Neha","Ravi","Pooja","Arjun","Meena"]
    last  = ["Martinez","Wilson","Johnson","Brown","Taylor","Garcia","Adams","Young","Turner","Evans",
             "Sharma","Verma","Singh","Patel","Gupta","Joshi","Mehta","Rao","Kumar","Shah"]
    subjects = ["Mathematics","Science","English","Social Studies","Computer Science",
                "Physics","Chemistry","Biology","Art","Physical Education"]
    sections = ["Sec A","Sec B","Sec C","Sec D","Sec E"]
    quals    = ["M.Ed","B.Ed","M.Sc B.Ed","MA B.Ed","Ph.D"]

    # ── Teacher Master Table ─────────────────────────────────────────────────
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

    # ── Monthly Performance Scores ───────────────────────────────────────────
    # Columns: teacher_id, teacher_name, subject, section, month, month_num,
    #          teaching_delivery_bm, teaching_delivery_curr, compliance_score, cca_score
    perf = []
    for _, t in tdf.iterrows():
        bd = np.random.uniform(52, 88)   # base teaching delivery per teacher
        bc = np.random.uniform(4.5, 9)   # base compliance
        ba = np.random.uniform(4.5, 9)   # base CCA

        for mi, m in enumerate(MONTHS):
            # Benchmark: fixed with small noise only (not a rising trend)
            bm_val  = round(min(100, max(35, bd + np.random.uniform(-3, 3))), 1)
            # Actual: seasonal sine boost peaking mid-year (Sep-Nov)
            curr_val = round(min(100, max(35, bd + np.random.uniform(-8, 8) + 2.0 * np.sin(np.pi * mi / 11))), 1)
            # Compliance: gentle positive trend across the year
            comp_val = round(min(10, max(2, bc + np.random.uniform(-0.8, 0.8) + mi * 0.04)), 1)
            # CCA: gentle positive trend across the year
            cca_val  = round(min(10, max(2, ba + np.random.uniform(-0.8, 0.8) + mi * 0.03)), 1)

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

    # ── Late Arrivals ────────────────────────────────────────────────────────
    # May = 0 (summer break). All other months: Poisson-distributed count.
    late = []
    for _, t in tdf.iterrows():
        for mi, m in enumerate(MONTHS):
            late.append({
                "teacher_id":   t.teacher_id,
                "teacher_name": t.teacher_name,
                "month":        m,
                "month_num":    mi + 1,
                "late_count":   0 if m == "May" else max(0, int(np.random.poisson(1.5))),
            })
    ldf = pd.DataFrame(late)

    # ── Attrition Risk ───────────────────────────────────────────────────────
    # Annual snapshot — does NOT vary by month.
    # Score: 0=Stable, 1=Low, 2=Medium, 3=High
    # Retirement only valid when total experience >= 25 years
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
            exit_type = (np.random.choice(["Voluntary","Involuntary","Retirement","Structural"])
                         if total_exp >= 25
                         else np.random.choice(["Voluntary","Involuntary","Structural"]))
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

    # ── Compliance Data ──────────────────────────────────────────────────────
    # training_hours: 8–49 out of 50 max | assignment_correction_stars: 1–5
    cdf = pd.DataFrame([{
        "teacher_id":                  t.teacher_id,
        "training_hours":              int(np.random.randint(8, 50)),
        "training_max":                50,
        "assignment_correction_stars": int(np.random.randint(1, 6)),
    } for _, t in tdf.iterrows()])

    # ── CCA Data ─────────────────────────────────────────────────────────────
    # activities_completed always < activities_total (gap guaranteed by ranges)
    ccadf = pd.DataFrame([{
        "teacher_id":          t.teacher_id,
        "activities_completed": int(np.random.randint(3, 9)),   # max 8
        "activities_total":     int(np.random.randint(10, 15)), # min 10
        "quality":              np.random.choice(["Excellent","Good","Needs Improvement"]),
    } for _, t in tdf.iterrows()])

    # ── Stakeholder Ratings ──────────────────────────────────────────────────
    # 4 stakeholders x 20 teachers = 80 rows | stars: 1–5
    aldf = pd.DataFrame([{
        "teacher_id":  t.teacher_id,
        "stakeholder": sh,
        "stars":       int(np.random.randint(1, 6)),
    } for _, t in tdf.iterrows() for sh in ["Head","Peer","Student","Parent"]])

    return tdf, pdf, ldf, adf, cdf, ccadf, aldf
