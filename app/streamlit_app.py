import html
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

import streamlit as st

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.hybrid import hybrid_search
from src.search.matching import match_jobs, explain_matches, candidate_skills
from src.generate.cv_suggestions import suggest_improvements
from src.generate.learning_plan import make_plan, check_plan, remove_links
from src.generate.resume_rewrite import rewrite_resume, check_rewrite, build_docx
from src.mentor.rag_chain import ask_mentor
from src.safety.guardrails import mask_pii

st.set_page_config(page_title="SmartHire", page_icon="💼", layout="wide")

LEVELS = ["Student or fresher", "I have work experience"]
DOCX_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

for key, default in {"profile": None, "jobs": [], "tips": "", "plan": None,
                     "rewrite": None, "chat": []}.items():
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


def friendly(e):
    msg = str(e)
    if any(w in msg.lower() for w in ("limit", "busy", "unavailable", "429", "503", "exhausted")):
        return "The AI service is busy, or the free daily limit is used up. Please try again in a few minutes."
    return msg


def get_matches(profile):
    student = st.session_state.get("level_choice", LEVELS[0]) == LEVELS[0]
    jobs = match_jobs(profile, search_fn=hybrid_search, level_boost=student)
    return explain_matches(profile, jobs)


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
            jobs = get_matches(profile)
        st.session_state.profile = profile
        st.session_state.jobs = jobs
        st.session_state.tips = ""
        st.session_state.plan = None
        st.session_state.rewrite = None
        st.success("Done! Open the tabs on the right.")
    except Exception as e:
        st.error(f"Something went wrong: {friendly(e)}")
    finally:
        os.remove(path)


with st.sidebar:
    st.title("💼 SmartHire")
    st.caption("Upload your resume to find jobs, get resume tips, a 30-day plan, a tailored "
               "resume and a career mentor.")
    uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    st.radio("Your level", LEVELS, key="level_choice",
             help="Students see Fresher and Junior jobs first. After changing this, click "
                  "'Update jobs for this role' on the Profile tab.")
    if st.button("Analyze my resume", type="primary", disabled=uploaded is None):
        analyze(uploaded)
    st.info("Your email and phone number are hidden before anything is sent to the AI model.")
    with st.expander("About and limits"):
        st.markdown(
            "- Jobs come from a list of 5,000 tech job postings, not live websites.\n"
            "- The mentor answers only from our career notes and that job list.\n"
            "- AI can make mistakes. Check every tip, plan and rewrite against your real experience.")

(tab_profile, tab_jobs, tab_tips,
 tab_plan, tab_resume, tab_mentor) = st.tabs(
    ["Profile", "Jobs", "Resume Tips", "30-Day Plan", "Tailored Resume", "Career Mentor"])

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
                    st.session_state.jobs = get_matches(p)
                    st.session_state.tips = ""
                    st.session_state.plan = None
                    st.session_state.rewrite = None
                    st.success("Jobs updated. Open the Jobs tab.")
                except Exception as e:
                    st.error(f"Something went wrong: {friendly(e)}")

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
        st.caption("Jobs are found by meaning and by exact words, then ranked by your level and by "
                   "how many of the required skills you already have.")
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
                    st.error(f"Something went wrong: {friendly(e)}")
        tips = st.session_state.tips
        if tips:
            for h in ("MISSING SKILLS", "WEAK POINTS", "REWRITTEN SUMMARY"):
                tips = tips.replace(h, f"### {h.title()}")
            st.markdown(tips)
            st.warning("These are suggestions. Check each one against your real experience "
                       "and never add skills you do not have.")

# ---------------- 30-day plan ----------------
with tab_plan:
    p, jobs = st.session_state.profile, st.session_state.jobs
    if p is None or not jobs:
        st.info("Analyze your resume first.")
    else:
        options = [f"{j['Job_Title']} at {j['Company']}" for j in jobs]
        choice = st.selectbox("Make a plan for this job", options, key="plan_job")
        hours = st.slider("Hours you can study each day", 1, 4, 2)
        if st.button("Make my 30-day plan"):
            j = jobs[options.index(choice)]
            mine = candidate_skills(p)
            with st.spinner("Writing your plan..."):
                try:
                    r = make_plan(mine, j, hours=hours)
                    r["plan"] = remove_links(r["plan"])
                    issues = check_plan(r["plan"], r["missing"]) if r["used_ai"] else []
                    if issues:
                        r = make_plan(mine, j, hours=hours, fresh=True)
                        r["plan"] = remove_links(r["plan"])
                        issues = check_plan(r["plan"], r["missing"])
                    st.session_state.plan = {"job": choice, "text": r["plan"],
                                             "issues": issues, "missing": r["missing"]}
                except Exception as e:
                    st.error(f"Something went wrong: {friendly(e)}")
        plan = st.session_state.plan
        if plan:
            st.subheader(f"Plan for: {plan['job']}")
            if plan["missing"]:
                st.markdown("**Skills to learn:** " + chips(plan["missing"], "bad"),
                            unsafe_allow_html=True)
            if plan["issues"]:
                st.warning("This plan may be incomplete: " + "; ".join(plan["issues"]))
            st.markdown(re.sub(r"(?m)^(WEEK \d+[^\n]*)", r"### \1", plan["text"]))
            st.download_button("Download plan as text", plan["text"], file_name="learning_plan.txt")
            st.caption("A plan is a guide. It does not promise a job.")

# ---------------- Tailored resume ----------------
with tab_resume:
    p, jobs = st.session_state.profile, st.session_state.jobs
    if p is None or not jobs:
        st.info("Analyze your resume first.")
    else:
        options = [f"{j['Job_Title']} at {j['Company']}" for j in jobs]
        choice = st.selectbox("Rewrite my resume for this job", options, key="rewrite_job")
        st.caption("The AI only rewrites wording. Your companies, dates, degrees and skills are "
                   "copied from your own resume.")
        if st.button("Rewrite my resume"):
            j = jobs[options.index(choice)]
            with st.spinner("Rewriting your resume..."):
                try:
                    result = rewrite_resume(p, j)
                    issues = check_rewrite(p, j, result)
                    if issues:
                        result = rewrite_resume(p, j, fresh=True)
                        issues = check_rewrite(p, j, result)
                    st.session_state.rewrite = {"job": choice, "result": result,
                                                "issues": issues, "docx": build_docx(p, result)}
                except Exception as e:
                    st.error(f"Something went wrong: {friendly(e)}")
        rw = st.session_state.rewrite
        if rw:
            res = rw["result"]
            st.subheader(f"Rewritten for: {rw['job']}")
            if rw["issues"]:
                st.error("This rewrite failed the safety checks, so no download is offered: "
                         + "; ".join(rw["issues"]) + ". Click the button to try again.")
            else:
                st.success("Safety checks passed: no new numbers and no skills you do not have.")
            st.markdown("**Summary**")
            st.write(res["summary"])
            st.markdown("**Skills**")
            st.markdown(chips(res["skills"], "plain"), unsafe_allow_html=True)
            for e, b in zip(p.experience, res["experience"]):
                st.markdown(f"**{e.role}**, {e.company}")
                for line in b:
                    st.write("• " + line)
            for pr, b in zip(p.projects, res["projects"]):
                st.markdown(f"**{pr.name}**")
                for line in b:
                    st.write("• " + line)
            if not rw["issues"]:
                name = re.sub(r"\W+", "_", rw["job"])
                st.download_button("Download as Word file", rw["docx"],
                                   file_name=f"resume_for_{name}.docx", mime=DOCX_TYPE)
            st.warning("Read every line before you send it, add your phone number, and never "
                       "keep anything that is not true.")

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
                r = {"answer": f"Sorry, something went wrong: {friendly(e)}", "sources": []}
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