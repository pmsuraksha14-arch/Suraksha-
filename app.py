from flask import Flask, render_template, request
import re

app = Flask(__name__)

SKILLS = [
    "python", "java", "c", "c++", "javascript", "html", "css", "sql",
    "machine learning", "deep learning", "artificial intelligence", "ai",
    "data science", "pandas", "numpy", "tensorflow", "pytorch",
    "flask", "django", "git", "github", "excel", "power bi",
    "communication", "leadership", "teamwork", "problem solving"
]

SECTIONS = ["education", "experience", "skills", "projects", "certifications", "summary"]

def analyze_resume(text, job_description=""):
    lower = text.lower()
    jd = job_description.lower()

    found_skills = [s for s in SKILLS if re.search(r"\b" + re.escape(s) + r"\b", lower)]
    jd_skills = [s for s in SKILLS if s in jd]
    matched = [s for s in jd_skills if s in found_skills]
    missing = [s for s in jd_skills if s not in found_skills]

    sections_found = [s.title() for s in SECTIONS if s in lower]

    score = 40
    score += min(len(found_skills) * 2, 20)
    score += min(len(sections_found) * 4, 24)
    if len(text.split()) >= 250:
        score += 8
    score = min(score, 100)

    suggestions = []
    if "summary" not in lower:
        suggestions.append("Add a short professional summary tailored to the target role.")
    if "projects" not in lower:
        suggestions.append("Add 2–3 relevant projects with technologies and measurable results.")
    if "experience" not in lower:
        suggestions.append("Add internship, work, volunteer, or practical experience where applicable.")
    if not found_skills:
        suggestions.append("Add relevant technical and soft skills using keywords from the job description.")
    if len(text.split()) < 250:
        suggestions.append("Add more relevant details while keeping the resume concise.")
    if not suggestions:
        suggestions.append("Keep your resume tailored to each job and quantify achievements where possible.")

    return {
        "score": score,
        "skills": found_skills,
        "sections": sections_found,
        "matched": matched,
        "missing": missing,
        "suggestions": suggestions
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    resume_text = ""
    job_description = ""

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "")
        job_description = request.form.get("job_description", "")
        result = analyze_resume(resume_text, job_description)

    return render_template(
        "index.html",
        result=result,
        resume_text=resume_text,
        job_description=job_description
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
