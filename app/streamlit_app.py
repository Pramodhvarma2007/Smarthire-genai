import html
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

import streamlit as st

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.matching import match_jobs, explain_matches
from src.generate.cv_suggestions import suggest_improvements
from src.mentor.rag_chain import ask_mentor
from src.safety.guardrails import mask_pii

st.set_page_config(page_title="SmartHire", page_icon="💼", layout="wide")

for key, default in {"profile": None, "jobs": [], "tips": "", "chat": []}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def chips(items, kind):
    colors = {"good": ("#d1fae5", "#065f46"),
              "bad": ("#fee2e2", "#991b1b"),
              "plain": ("#e0e7ff", "#3730a3")}
    bg, fg = colors[kind]
    if not items:
        return "<span style='opacity:0.6'>None</span>"
    return " ".join(
        f"<span style='background:{bg};color:{fg};padding:2px 10px;"
        f"border-radius:12px;margin:2px;display:inline-block;"
        f"font-size:0.85em'>{html.escape(str(i))}</span>" for i in items)


def analyze(uploaded):
    suffix = os.path.splitext(uploaded.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        path = tmp.name
    try:
        with st.spinner("Reading your resume..."):
            profile = parse_resume(load_resume(path))
            if not (profile.skills or profile.experience or profile.education or profile.projects):
                raise ValueError("This file does not look like a resume. Please upload your resume.")
        with st.spinner("Finding jobs for you..."):
            jobs = explain_matches(profile, match_jobs(profile))
        st.session_state.profile = profile
        st.session_state.jobs = jobs
        st.session_state.tips = ""
        st.success("Done! Open the tabs on the right.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
    finally:
        os.remove(path)


with st.sidebar:
    st.title("💼 SmartHire")
    st.caption("Upload your resume to find jobs, get resume tips and chat with a career mentor.")
    uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    if st.button("Analyze my resume", type="primary", disabled=uploaded is None):
        analyze(uploaded)
    st.info("Your email and phone number are hidden before anything is sent to the AI model.")

tab_profile, tab_jobs, tab_tips, tab_mentor = st.tabs(
    ["Profile", "Jobs", "Resume Tips", "Career Mentor"])

# ---------------- Profile ----------------
with tab_profile:
    p = st.session_state.profile
    if p is None:
        st.info("Upload a resume in the sidebar, then click **Analyze my resume**.")
    else:
        st.header(p.name or "Your profile")
        if p.email:
            st.write(p.email)

        new_role = st.text_input("Job you want", value=p.target_role)
        if st.button("Update jobs for this role"):
            p.target_role = new_role
            with st.spinner("Finding jobs..."):
                try:
                    st.session_state.jobs = explain_matches(p, match_jobs(p))
                    st.session_state.tips = ""
                    st.success("Jobs updated. Open the Jobs tab.")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        st.subheader("Skills")
        st.markdown(chips(p.skills, "plain"), unsafe_allow_html=True)
        if p.soft_skills:
            st.markdown("**Other strengths**")
            st.markdown(chips(p.soft_skills, "plain"), unsafe_allow_html=True)

        if p.experience:
            st.subheader("Experience")
            for e in p.experience:
                st.markdown(f"**{e.role}**, {e.company} ({e.duration})")
                if e.summary:
                    st.write(e.summary)
        if p.projects:
            st.subheader("Projects")
            for pr in p.projects:
                st.markdown(f"**{pr.name}**")
                if pr.description:
                    st.write(pr.description)
                if pr.tech:
                    st.markdown(chips(pr.tech, "plain"), unsafe_allow_html=True)
        if p.education:
            st.subheader("Education")
            for ed in p.education:
                st.markdown(f"**{ed.degree}**, {ed.institution} ({ed.year})")

# ---------------- Jobs ----------------
with tab_jobs:
    jobs = st.session_state.jobs
    if not jobs:
        st.info("Analyze your resume first to see matching jobs.")
    else:
        st.caption("Jobs are ranked by how close they are to your profile and how many of the "
                   "required skills you already have.")
        for j in jobs:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                c1.subheader(f"{j['Job_Title']} at {j['Company']}")
                details = [str(j[k]) for k in ("City", "Experience_Level", "Work_Mode") if j.get(k)]
                try:
                    sal = float(j.get("Salary_LPA"))
                    if sal == sal:
                        details.append(f"{sal:.1f} LPA")
                except (TypeError, ValueError):
                    pass
                c1.caption(" · ".join(details))
                c2.metric("Skills you have", f"{j['skill_match']}%")
                st.markdown("**You have:** " + chips(j["matched"], "good"), unsafe_allow_html=True)
                st.markdown("**To learn:** " + chips(j["missing"], "bad"), unsafe_allow_html=True)
                if j["skill_match"] < 50:
                    st.caption("Partial match: you have less than half of the skills for this job.")
                if j.get("why"):
                    st.write(j["why"])

# ---------------- Resume tips ----------------
with tab_tips:
    p, jobs = st.session_state.profile, st.session_state.jobs
    if p is None or not jobs:
        st.info("Analyze your resume first.")
    else:
        options = [f"{j['Job_Title']} at {j['Company']}" for j in jobs]
        choice = st.selectbox("Improve my resume for this job", options)
        if st.button("Get resume tips"):
            j = jobs[options.index(choice)]
            job_text = (f"{j['Job_Title']} at {j['Company']}. Required skills: {j['Skills_Required']}. "
                        f"Level: {j['Experience_Level']}. Education: {j['Education_Required']}. "
                        f"Industry: {j['Industry']}.")
            with st.spinner("Writing your tips..."):
                try:
                    st.session_state.tips = suggest_improvements(p, job_text)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
        tips = st.session_state.tips
        if tips:
            for h in ("MISSING SKILLS", "WEAK POINTS", "REWRITTEN SUMMARY"):
                tips = tips.replace(h, f"### {h.title()}")
            st.markdown(tips)
            st.warning("These are suggestions. Check each one against your real experience "
                       "and never add skills you do not have.")

# ---------------- Career mentor ----------------
with tab_mentor:
    st.caption("Ask about careers, skills, resumes, interviews or the jobs in our list. "
               "Answers come only from our career notes and job list.")
    if st.button("Clear chat"):
        st.session_state.chat = []
    box = st.container()
    question = st.chat_input("Ask the career mentor...")
    if question:
        history = [{"role": m["role"], "text": mask_pii(m["text"])[0]}
                   for m in st.session_state.chat]
        with st.spinner("Thinking..."):
            try:
                r = ask_mentor(question, history)
            except Exception as e:
                r = {"answer": f"Sorry, something went wrong: {e}", "sources": []}
        st.session_state.chat.append({"role": "user", "text": question})
        st.session_state.chat.append(
            {"role": "mentor", "text": r["answer"], "sources": r["sources"]})
    with box:
        for m in st.session_state.chat:
            with st.chat_message("user" if m["role"] == "user" else "assistant"):
                st.markdown(m["text"])
                if m.get("sources"):
                    with st.expander("Where this answer came from"):
                        for s in m["sources"]:
                            kind = "career note" if s["type"] == "note" else "job"
                            st.write(f"[{s['label']}] {s['title']} ({kind})")