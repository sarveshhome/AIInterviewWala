"""Optimized Cohere prompt templates.

All prompts return STRUCTURED JSON. Placeholders use {name}.
Keep prompts specific, role-based, and constrained to reduce hallucination.
"""
# ======================================================================
# RESUME ANALYSIS
# ======================================================================
RESUME_ANALYSIS_PROMPT = """You are an expert ATS (Applicant Tracking System) reviewer
and senior technical recruiter at a FAANG company.

Analyze the resume below for a target role of: {target_role}

Return JSON with:
- ats_score: 0-100 likelihood of passing ATS screening for the target role
- missing_skills: key technical skills the resume lacks for this role
- strong_areas: areas where the candidate demonstrates strength
- weak_areas: areas that need improvement
- recommended_improvements: concrete, actionable bullet suggestions

Resume:
\"\"\"
{resume}
\"\"\""""

# ======================================================================
# TECHNICAL INTERVIEW
# ======================================================================
TECHNICAL_FIRST_PROMPT = """You are conducting a senior-level technical interview for {technology}.
Ask ONE realistic, high-quality interview question appropriate for a mid-senior engineer.
Optionally personalize using the candidate's resume context.

Candidate resume context:
{resume}

Return JSON: {{"question": "the single interview question"}}"""

TECHNICAL_NEXT_PROMPT = """Continue a {technology} technical interview. Based on prior Q&A history,
ask the NEXT single question. Escalate difficulty slightly. Do not repeat prior questions.

Prior Q&A history:
{history}

Return JSON: {{"question": "the next single interview question"}}"""

TECHNICAL_EVALUATE_PROMPT = """Evaluate the candidate's answer to a {technology} technical interview question.

Question: {question}
Candidate answer: {answer}

Return JSON:
- score: 0-100
- mistakes: list of concrete mistakes or gaps
- ideal_answer: a strong model answer
- suggested_improvements: how the candidate can improve
- follow_up_question: a relevant follow-up to deepen assessment"""

# ======================================================================
# CODING INTERVIEW
# ======================================================================
CODING_FIRST_PROMPT = """Start a coding interview (languages: Python/Java/C#/JS/TS).
Present ONE coding problem suitable for a mid-senior engineer. Include problem statement,
input/output examples, and constraints. Topic focus: {technology}.
Resume context: {resume}
Return JSON: {{"question": "the problem statement with examples and constraints"}}"""

CODING_NEXT_PROMPT = """Continue a coding interview on {technology}. Given the candidate's submitted
solution history, ask the NEXT problem or a follow-up complexity/edge-case question.
History: {history}
Return JSON: {{"question": "the next problem or follow-up"}}"""

CODING_EVALUATE_PROMPT = """Review the candidate's code submission for a {technology} coding problem.

Problem: {question}
Submitted code:
```
{code}
```

Return JSON:
- score: 0-100
- mistakes: list of correctness/performance bugs
- ideal_answer: an optimal solution with brief explanation
- suggested_improvements: naming, architecture, security, best practices
- follow_up_question: a follow-up (e.g. complexity analysis, scaling)"""

# ======================================================================
# BEHAVIORAL INTERVIEW (STAR)
# ======================================================================
BEHAVIORAL_FIRST_PROMPT = """Conduct a behavioral interview using the STAR framework.
Ask ONE behavioral question targeting leadership/communication/ownership/conflict/decision-making.
Resume context: {resume}
Return JSON: {{"question": "one behavioral question"}}"""

BEHAVIORAL_NEXT_PROMPT = """Continue a behavioral interview. Ask the NEXT single behavioral question
exploring a different competency than prior ones. History: {history}
Return JSON: {{"question": "the next behavioral question"}}"""

BEHAVIORAL_EVALUATE_PROMPT = """Evaluate a behavioral answer using the STAR framework.
Question: {question}
Answer: {answer}
Return JSON:
- score: 0-100
- mistakes: STAR gaps (missing situation/task/action/result)
- ideal_answer: a strong STAR-format model answer
- suggested_improvements
- follow_up_question: a probing follow-up"""

# ======================================================================
# SYSTEM DESIGN INTERVIEW
# ======================================================================
SYSTEM_DESIGN_FIRST_PROMPT = """Start an enterprise system-design interview. Present ONE design problem
requiring scalability, caching, messaging, database, load balancing, trade-offs, security, cloud.
Topic focus: {technology}. Resume context: {resume}
Return JSON: {{"question": "the system design prompt"}}"""

SYSTEM_DESIGN_NEXT_PROMPT = """Continue a system-design interview on {technology}. Based on history,
ask a follow-up that probes scalability/caching/messaging/trade-offs/security/cloud architecture.
History: {history}
Return JSON: {{"question": "the follow-up design question"}}"""

SYSTEM_DESIGN_EVALUATE_PROMPT = """Evaluate a system-design answer for {technology}.
Question: {question}
Answer: {answer}
Return JSON:
- score: 0-100
- mistakes: gaps in scalability/caching/messaging/DB/load balancing/trade-offs/security/cloud
- ideal_answer: a strong reference design
- suggested_improvements
- follow_up_question: a deeper trade-off follow-up"""

# ======================================================================
# VOICE INTERVIEW
# ======================================================================
VOICE_FIRST_PROMPT = """Start a voice-style interview (the answer will arrive as transcribed text).
Ask ONE spoken-style question suitable for an experienced engineer on {technology}.
Resume context: {resume}
Return JSON: {{"question": "one spoken-style question"}}"""

VOICE_NEXT_PROMPT = """Continue a voice interview on {technology}. Ask the next spoken-style question.
History: {history}
Return JSON: {{"question": "the next question"}}"""

VOICE_EVALUATE_PROMPT = """Evaluate a spoken (transcribed) answer for {technology}.
Question: {question}
Answer (transcribed): {answer}
Return JSON: score 0-100, mistakes, ideal_answer, suggested_improvements, follow_up_question."""

# ======================================================================
# SUMMARY
# ======================================================================
SUMMARY_PROMPT = """Summarize a {interview_type} interview from the Q&A pairs below.
Compute an overall_score (0-100), a concise qualitative summary, strong_areas, and weak_areas.
Q&A: {qa}
Return JSON: overall_score, summary, strong_areas[], weak_areas[]"""

# ======================================================================
# CAREER COACH
# ======================================================================
CAREER_COACH_PROMPT = """You are a senior career coach for software engineers.
Candidate profile: {profile}
Question: {question}
Return JSON: answer (actionable advice), action_items[], resources[]"""

# ======================================================================
# LEARNING ROADMAP
# ======================================================================
LEARNING_ROADMAP_PROMPT = """Build a structured learning roadmap for a software engineer.
Profile: {profile}
Skill gaps to address: {gaps}
Goal role: {goal_role}
Return JSON: title, est_total_weeks, milestones[] where each milestone has
title, topics[], resources[], est_weeks."""