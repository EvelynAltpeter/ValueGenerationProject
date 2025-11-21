# VGP Technical Proficiency Platform — Spec Sheet  

**Spec Version:** v0.1  
**Date:** 2025-11-21  
**Owner:** Jet U.  
**Status:** Draft – Course Project  

---

# Part A — Business Context & Problem Statement

## A1. Strategy / Context (Simplified)

Companies hiring for technical roles currently rely on fragmented, company-specific coding interviews, take-home challenges, and live technical screens. Candidates must repeat similar assessments for every application, while employers invest significant time designing, administering, and grading these tests.

The VGP Technical Proficiency Platform introduces a **standardized, cross-employer technical assessment system**. Candidates complete adaptive, language-specific exams once (e.g., C++, Python, SQL, R, JavaScript), and can share verified scores with multiple employers. Employers use these standardized scores to filter applicants, match candidates to roles, and reduce redundant interviews.

Strategically, this operates as a **Blue Ocean** play:  
- Existing platforms (LeetCode, HackerRank, Codility) focus on *practice* and *per-company* assessments.  
- VGP focuses on **interoperable certification** across employers — redefining how technical hiring is done rather than competing as another coding test library.

Marketing Principles applied:

- **MP1: All Customers Differ**  
  Employers differ in assessment standards; candidates differ in skills, preparation, and time. The platform provides **adaptive, modular tests** and flexible scoring views so both sides see what they need.

- **MP2: All Customers Change**  
  Tech stacks and hiring practices evolve. VGP uses **dynamic question banks and scoring algorithms** so the standard stays current.

- **MP3: All Competitors React**  
  Current players may respond with their own “standards.” VGP’s defense is **early institutional partnerships** (universities, bootcamps, certification bodies, HR tools) and strong **credential legitimacy**.

- **MP4: All Resources Are Limited**  
  Both candidates and employers are constrained by time, attention, and budget. VGP reduces **interview fatigue**, **time-to-hire**, and **screening costs**, freeing resources for higher-value interactions like culture-fit interviews and final-round panels.

---

## A2. Problem Statement (S–C–Q)

**Situation:**  
The technical hiring process is fragmented and inefficient. Candidates must complete multiple coding challenges and interviews for each application, while employers spend significant time designing, administering, and evaluating these assessments.

**Complication:**  
This redundancy creates major inefficiencies:  

- Candidates face burnout and attrition before completing all interview stages.  
- Companies struggle to compare applicants consistently and lose qualified talent due to “interview fatigue.”  
- Standardized skill data is missing, leading to inconsistent hiring decisions across the industry.

**Question:**  
How can we create a standardized, cross-employer technical assessment that fairly evaluates candidates’ abilities once and shares verified results across multiple employers to reduce time, bias, and costs in the hiring process?

---

## A3. SMART Goals (Project Scope)

- **Specific:**  
  Build a centralized platform that provides standardized technical tests per programming language (e.g., C++, Python, SQL, R, JavaScript) whose scores can be submitted to multiple employers.

- **Measurable:**  
  Within the first year of pilot rollout, target:  
  - 50% reduction in average candidate interview time for participating employers.  
  - 30% reduction in employer evaluation costs (time and resources).

- **Achievable:**  
  For this course project, develop a **demo** of a standardized technical test for at least one programming language, including scoring and basic employer filtering.

- **Relevant:**  
  Directly addresses hiring inefficiencies, improving both candidate experience and employer efficiency.

- **Time-Bound:**  
  Demo and scaling plan completed by **December 3, 2025**.

---

## A4. One-Line Scope

Build a standardized, adaptive technical testing platform that lets candidates **“test once, apply everywhere”** and enables employers to filter and match applicants using **verifiable proficiency scores** instead of repeating the same coding interviews.

---

## A5. Business Model Canvas (Summary)

**Key Partners**  
- Employers (tech and non-tech companies hiring technical roles)  
- LeetCode / similar platforms (potential content or distribution partnerships)  
- Universities and coding bootcamps (curriculum integration, early adoption)  
- Professional certification bodies (e.g., CompTIA, AWS) for credential validation  
- Technology infrastructure providers (e.g., AWS, cloud services)  
- HR software companies and ATS providers (Workday, Greenhouse, Lever, etc.)  

**Key Activities**  
- Continuous question bank curation and updates  
- Psychometric validation and bias testing of assessments  
- Security and anti-cheating measures (proctoring, plagiarism detection)  
- Data analytics and reporting for employers and candidates  
- Partnership development (universities, employers, cert bodies, ATS vendors)  
- Marketing and brand-building as “the standard” credential  
- Customer support for both candidates and employers  

**Key Resources**  
- Physical/technical infrastructure: servers, databases, secure code execution environments  
- Human capital: software engineers, data scientists, psychometricians, content creators  
- Intellectual property: question banks, scoring algorithms, adaptive testing logic  
- Brand reputation and trust in the certification  
- Network effects: more employers → more valuable credential → more candidates  
- Data and analytics infrastructure for performance and fairness monitoring  
- Security infrastructure for anti-cheating and identity verification  

**Value Propositions**  

_For Employers:_  
- Reduced time-to-hire by ~40–50%  
- Standardized, comparable skill data across applicants  
- Lower risk of bad hires via validated assessments  
- Access to a pre-vetted talent pool  
- Reduced interview fatigue for engineering teams  

_For Candidates:_  
- “Take the test once, apply everywhere”  
- Reduced interview anxiety and burnout  
- Transparent, portable skill validation  
- Faster job search process and better signaling of ability  
- Credential that grows in value as more employers accept it  

**Customer Relationships**  

_For Candidates:_  
- Self-service platform for registration, test-taking, and score sharing  
- Automated score dashboards and status notifications  
- Community forums / resources for preparation  
- Email/helpdesk support for technical and account issues  

_For Employers:_  
- Dedicated account management for enterprise clients  
- Onboarding and integration support (ATS + API)  
- Regular reporting on assessment performance and candidate pools  
- Co-creation of competency standards with top partners  

**Customer Segments**  

_Job Seekers:_  
- New graduates and early-career engineers  
- Mid-career switchers transitioning into tech roles  
- Senior engineers (for advanced or specialist certifications)

_Employers:_  
- Tech companies (startups → enterprise)  
- Non-tech companies with internal engineering/data teams  
- Recruiting agencies and staffing firms  

**Channels**  

_Employers:_  
- Direct sales to recruiters and HR leaders  
- Hiring agencies and recruiting firms  
- LinkedIn and GitHub outreach  
- HR conferences and trade shows  
- Partnerships with ATS providers and HR platforms  
- Industry publications and thought-leadership content  

_Candidates:_  
- Universities and bootcamps (career centers, course integration)  
- Tech communities (Discord, learning platforms)  
- Online job boards and LinkedIn integration  
- Social media and content marketing  
- Referral and ambassador programs  

**Cost Structure**  

_Fixed Costs:_  
- Technology infrastructure and secure hosting  
- Full-time engineering, data, and content teams  
- Security and compliance systems  
- Marketing/brand-building  
- (Optional) Office space  

_Variable Costs:_  
- Customer support (scales with user base)  
- Proctoring services (if live or AI-proctored)  
- Payment processing fees  
- Incremental server and compute costs  

**Revenue Streams**  

- **Employers:**  
  - Subscription or seat-based model for access to talent pool, dashboards, and integrations  
  - Premium analytics and benchmarking features  

- **Candidates:**  
  - Freemium model — base credential or limited test attempts free  
  - Paid re-takes or additional advanced tracks beyond some free quota  

---

# Part B — Build Plan (Solution Architecture & Design)

## B1. Overview

The system is a **standardized adaptive technical testing platform** for software job applicants.  

- **Type of system:** Multi-sided platform combining a **testing engine**, **AI-assisted grading**, and a **role-matching/filtering module**.  
- **Core function:** Replace repeated, employer-specific technical assessments with a **unified exam per skill track**, whose verified scores can be shared across multiple applications.  
- **Supported human/business task:**  
  - Supports recruiters and hiring managers in screening and ranking candidates.  
  - Supports candidates by reducing repeated tests and providing a portable credential.

High-level architecture:

- Frontend: Candidate and employer dashboards (web app).  
- Backend: API for registration, test delivery, scoring, analytics, and matching.  
- AI Components:  
  - Question generation and variation (LLM + RAG over question bank).  
  - Code grading and feedback models.  
  - Matching and recommendation logic for candidates ↔ roles.

---

## B2. Inputs Required from User or Data Sources

### 1. User Profile (Candidate)

- **Input Name:** Candidate Profile  
- **Description:** Basic information to create an account, verify identity, and link scores across applications.  
- **Source:** Manual user entry (sign-up form); optional OAuth (e.g., GitHub, Google).  
- **Example Value:**  
  ```json
  {
    "name": "Evelyn",
    "email": "evelyn@example.com",
    "github": "https://github.com/evelyn",
    "educationLevel": "BS Computer Science",
    "graduationYear": 2026
  }
  ```

---

### 2. Skill Selection

- **Input Name:** Selected Skill Track  
- **Description:** The programming language or technical track the candidate wants to be assessed on (e.g., C++, Python, SQL, R, JavaScript).  
- **Source:** Manual user entry/selection from a dropdown or checklist.  
- **Example Value:**  
  ```json
  {
    "trackId": "python_core_v1",
    "language": "Python",
    "level": "Intermediate"
  }
  ```

---

### 3. Test Response

- **Input Name:** Candidate Answers  
- **Description:** Code submissions, multiple-choice answers, or short-form responses provided during the exam.  
- **Source:** User submits code via in-browser editor or selects answers.  
- **Example Value:**  
  ```json
  {
    "questionId": "py-213",
    "responseType": "code",
    "code": "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target-n], i]\n        seen[n] = i"
  }
  ```

---

### 4. Employer Job Requirements

- **Input Name:** Job Proficiency Requirements  
- **Description:** Skills, experience level, and minimum score thresholds required for a given role.  
- **Source:** Employer dashboard (manual entry) or ATS integration/API.  
- **Example Value:**  
  ```json
  {
    "jobId": "backend-dev-123",
    "requiredTracks": ["python_core_v1", "sql_core_v1"],
    "minScores": {
      "python_core_v1": 75,
      "sql_core_v1": 70
    },
    "preferredExperienceYears": 2
  }
  ```

---

### 5. Item Bank / Test Database

- **Input Name:** Standardized Tests Bank  
- **Description:** Continuously updated, validated question sets per language and skill area (e.g., algorithms, data structures, SQL queries).  
- **Source:** Internal database, expert-created content, and partner contributions (e.g., universities, industry experts).  
- **Example Value:**  
  ```json
  {
    "questionId": "sql-045",
    "trackId": "sql_core_v1",
    "prompt": "Write a query to find users who have never placed an order.",
    "difficulty": 0.6,
    "tags": ["joins", "subquery"],
    "referenceSolution": "SELECT u.* FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE o.id IS NULL;"
  }
  ```

---

### 6. Historical Scoring & Adaptive Difficulty Data

- **Input Name:** Adaptive Difficulty Data  
- **Description:** Past performance data used to estimate question difficulty and calibrate adaptive testing (e.g., IRT-like parameters).  
- **Source:** System-generated from previous test-takers and ongoing analytics.  
- **Example Value:**  
  ```json
  {
    "questionId": "py-213",
    "averageScore": 0.72,
    "discrimination": 1.1,
    "difficultyEstimate": 0.68,
    "attempts": 1450
  }
  ```

---

### 7. Employer & Candidate Behavioral Data (Optional for Matching)

- **Input Name:** Engagement & Outcome Data  
- **Description:** Interview outcomes, offer acceptance, and performance feedback used to improve matching and scoring weights.  
- **Source:** Employer feedback forms; ATS webhooks; manual updates.  
- **Example Value:**  
  ```json
  {
    "candidateId": "cand-987",
    "jobId": "backend-dev-123",
    "stageReached": "offer_accepted",
    "performanceReviewAfter6Months": "meets_expectations"
  }
  ```

---

## B3. Outputs Produced by the System

### 1. Candidate Score Report

- **Output Name:** CandidateScoreReport  
- **Format:** JSON object; rendered as a dashboard for candidates.  
- **Who sees it:** Candidate (primary), employers via shared links or API.  
- **Example:**  
  ```json
  {
    "candidateId": "cand-987",
    "trackId": "python_core_v1",
    "overallScore": 82,
    "subscores": {
      "algorithms": 88,
      "data_structures": 79,
      "code_quality": 80
    },
    "percentile": 76,
    "completedAt": "2025-11-20T15:30:00Z"
  }
  ```

---

### 2. Employer Filtered Candidate List

- **Output Name:** EligibleCandidateList  
- **Format:** JSON list returned to employer UI or ATS.  
- **Who sees it:** Employers / recruiters.  
- **Example:**  
  ```json
  {
    "jobId": "backend-dev-123",
    "eligibleCandidates": [
      {
        "candidateId": "cand-987",
        "name": "Evelyn",
        "trackScores": {
          "python_core_v1": 82,
          "sql_core_v1": 78
        },
        "matchScore": 91
      }
    ]
  }
  ```

---

### 3. Role Recommendations for Candidate

- **Output Name:** RoleMatchList  
- **Format:** JSON list of suggested roles and match scores.  
- **Who sees it:** Candidate dashboard.  
- **Example:**  
  ```json
  {
    "candidateId": "cand-987",
    "recommendedJobs": [
      {
        "jobId": "backend-dev-123",
        "company": "TechNova",
        "matchScore": 91
      }
    ]
  }
  ```

---

### 4. Analytics & Fairness Reports

- **Output Name:** AssessmentAnalytics  
- **Format:** Aggregated metrics and fairness checks (dashboard + JSON export).  
- **Who sees it:** Internal admins; optionally employer admins.  

---

## B4. Core Logic / System Modules

1. **Registration & Authentication Module**  
   - Create candidate and employer accounts; manage identity verification.  

2. **Skill Track & Test Selection Module**  
   - Candidate selects track(s); system confirms eligibility and available test windows.  

3. **Test Assembly & Delivery Module**  
   - Use Item Bank + Adaptive Difficulty Data to assemble a test:  
     - Mix of multiple-choice and coding tasks.  
     - Adaptive selection adjusting difficulty based on ongoing performance.  
   - Deliver questions in secure browser environment with timing.

4. **Proctoring & Security Module**  
   - Monitor for cheating (e.g., copy-paste patterns, suspicious tab switching, webcam/AI proctor if in scope).  
   - Enforce time limits and detect anomalies.

5. **Grading & Scoring Module (AI + Rules)**  
   - Auto-grade multiple-choice items via answer key.  
   - For coding tasks, run submissions against test cases, record:  
     - Correctness (test case pass rate)  
     - Time and space performance (efficiency)  
     - Possible plagiarism/“collusion-like” patterns  
   - Combine into overall scores and subscores with standardized scaling.

6. **Standardization & Normalization Module**  
   - Normalize scores across test variants and cohorts.  
   - Compute percentiles and confidence intervals.

7. **Reporting & Credential Module**  
   - Generate Candidate Score Reports.  
   - Allow candidates to share score links or tokens with employers.  

8. **Role Matching & Filtering Module**  
   - Read Job Proficiency Requirements.  
   - Filter candidates meeting minimum thresholds.  
   - Compute job-candidate match scores and rank lists.

9. **Analytics & Fairness Monitoring Module**  
   - Track outcome distributions and bias indicators across demographics (where legally collected).  
   - Flag problematic questions or scoring patterns.

10. **Administration & Content Management Module**  
    - Author, review, and retire questions.  
    - Manage track definitions and difficulty calibrations.

11. **Logging & Trace Module**  
    - Log key events (test starts, submissions, scoring, rule changes).  
    - Maintain a **project trace** for prompts, rules, and test results (for build/debug).

---

## B5. Design & Behavior Rules (Rule IDs)

- **R-PRIV-01 (Privacy):**  
  The system must store and expose candidate data only to the candidate and explicitly authorized employers, in compliance with relevant privacy policies.

- **R-SEC-01 (Security & Anti-Cheating):**  
  The system must enforce time limits, prevent trivial cheating where possible, and log suspicious behavior for review.

- **R-SCORE-01 (Scoring Consistency):**  
  The same raw performance should always map to the same standardized score within a given test version.

- **R-FAIR-01 (Fairness & Bias):**  
  Assessments must be periodically tested for bias; flagged questions must be reviewed and, if necessary, removed or re-weighted.

- **R-UX-01 (Candidate Clarity):**  
  The candidate interface must clearly display time remaining, question instructions, and submission status.

- **R-UX-02 (Employer Clarity):**  
  Employer-facing dashboards must clearly display scores, thresholds, and filtering criteria (no “black box” match scores without summary explanations).

- **R-PERF-01 (Performance):**  
  Test pages and score retrieval should respond within 2 seconds under normal load.

- **R-TRACE-01 (Trace Logging):**  
  Automatically log every user prompt, system response, rule update, and test result in a project trace file for future reference and debugging.

---

## B6. Schemas (Authoritative)

- **Input Schemas:**  
  Defined in **B2** (Candidate Profile, Selected Skill Track, Candidate Answers, Job Proficiency Requirements, Item Bank, Adaptive Difficulty Data).  

- **Output Schemas:**  
  Defined in **B3** (CandidateScoreReport, EligibleCandidateList, RoleMatchList, AssessmentAnalytics).

These JSON-like schemas are the source of truth for API contracts between frontend, backend, and AI modules.

---

## B7. Mini Input/Output Example

**Simplest Useful Request – Candidate Taking a Python Test & Employer Filtering**

1. Candidate registers and selects the Python track:

   ```json
   {
     "candidateProfile": {
       "name": "Evelyn",
       "email": "evelyn@example.com"
     },
     "selectedTrack": {
       "trackId": "python_core_v1"
     }
   }
   ```

2. Candidate completes test; system scores and generates:

   ```json
   {
     "candidateId": "cand-987",
     "trackId": "python_core_v1",
     "overallScore": 82,
     "subscores": {
       "algorithms": 88,
       "data_structures": 79
     }
   }
   ```

3. Employer sets requirements and retrieves eligible candidates:

   **Input (Employer Requirements):**  
   ```json
   {
     "jobId": "backend-dev-123",
     "requiredTracks": ["python_core_v1"],
     "minScores": {
       "python_core_v1": 75
     }
   }
   ```

   **Output (Filtered Result):**  
   ```json
   {
     "jobId": "backend-dev-123",
     "eligibleCandidates": [
       {
         "candidateId": "cand-987",
         "name": "Evelyn",
         "trackScores": {
           "python_core_v1": 82
         },
         "matchScore": 90
       }
     ]
   }
   ```

---

## B8. Metrics (Simplified, Aligned with SMART)

- **Objective:** Reduce candidate interview burden.  
  - **Metric:** Average interview hours per candidate (for participating employers).  
  - **Target:** 50% reduction vs. baseline.  
  - **Source of Data:** Employer-reported interview stages and durations, platform analytics.

- **Objective:** Reduce employer screening cost.  
  - **Metric:** Average engineering hours spent on early-stage technical interviews.  
  - **Target:** 30% reduction in first year of pilot.  
  - **Source of Data:** Employer time-tracking / survey + platform usage logs.

- **Objective:** Ensure fairness and consistency.  
  - **Metric:** Variance in scores across demographic subgroups controlling for experience.  
  - **Target:** No statistically significant unfair outcome patterns; <5% of questions flagged as problematic at any time.  
  - **Source of Data:** AssessmentAnalytics and fairness reports.

---

## B9. Assumptions & Dependencies

- **Data Sources / External APIs:**  
  - Identity verification (optional).  
  - ATS integrations (e.g., via REST APIs).  
  - Cloud compute for secure code execution.  
  - Optional LLM APIs or locally hosted models for grading and question generation.

- **Technical Dependencies:**  
  - Backend framework (e.g., FastAPI or Express).  
  - Frontend framework (React or similar).  
  - Database for user data, test results, and item bank.  
  - Secure code execution sandbox for running candidate code.  
  - Logging infrastructure for trace and analytics.

- **Business Assumptions:**  
  - Employers are willing to adopt standardized scores and adjust hiring workflows.  
  - Universities/bootcamps will integrate assessments into curricula.  
  - Candidates will trust and invest effort in a third-party credential.  
  - There is sustained stakeholder support to maintain content, fairness, and security.

---

# Part C — Testing Plan

List below references the rules from **B5**.

## C1. Positive Test Cases (What Should Work)

### Test Case ID: TC-01 — Successful Candidate Test & Score Generation

- **Rule(s) Covered:** R-UX-01, R-SCORE-01, R-PERF-01, R-TRACE-01  
- **Input / Context:**  
  - Candidate “Evelyn” selects `python_core_v1`, completes all required questions within the time limit, and submits responses.  
- **Expected System Behavior:**  
  - Test interface loads quickly and clearly shows instructions and timer.  
  - System executes code, grades answers, produces a consistent standardized score, and returns a CandidateScoreReport within 2 seconds of submission.  
  - Event is logged in trace file.  
- **Why This Is Correct (business/user value):**  
  - Demonstrates the core value: a smooth, reliable test experience and standardized score for employers.  
- **Data Needed:**  
  - Sample Python questions, scoring rules, and candidate responses.  
- **Pass/Fail Criteria:**  
  - PASS if response time <2 seconds, score is computed, report is saved, and trace entry exists.

---

### Test Case ID: TC-02 — Employer Filtering for a Role

- **Rule(s) Covered:** R-UX-02, R-SCORE-01, R-PERF-01, R-TRACE-01  
- **Input / Context:**  
  - Employer posts `backend-dev-123` requiring `python_core_v1 >= 75`.  
  - Candidate with score 82 exists in database.  
- **Expected System Behavior:**  
  - Employer dashboard displays a list of eligible candidates including “Evelyn” with clear listing of her scores and match score.  
  - Response is rendered or returned via API in <2 seconds.  
  - Filtering logic is recorded in trace.  
- **Why This Is Correct:**  
  - Delivers tangible value to employers by eliminating manual score checking.  
- **Data Needed:**  
  - Stored candidate scores, job requirement config.  
- **Pass/Fail Criteria:**  
  - PASS if “Evelyn” appears in eligible list and lower-scoring candidates are excluded.

---

### Test Case ID: TC-03 — Adaptive Question Selection

- **Rule(s) Covered:** R-SCORE-01, R-FAIR-01, R-TRACE-01  
- **Input / Context:**  
  - Candidate starts Python test; initial questions are moderate difficulty.  
  - Candidate answers correctly; system should gradually increase difficulty.  
- **Expected System Behavior:**  
  - Next questions pulled from higher difficulty band using Adaptive Difficulty Data.  
  - Final score reflects difficulty profile and raw performance.  
  - Adaptation decisions logged in trace for debugging.  
- **Why This Is Correct:**  
  - Ensures efficient and fair assessment of ability without overly long tests.  
- **Data Needed:**  
  - Difficulty metadata for item bank, candidate response stream.  
- **Pass/Fail Criteria:**  
  - PASS if successive questions show increased difficulty when candidate performs well, and final score matches expected calibration.

---

## C2. Red-Team / Edge Case Tests (What Should NOT Work)

### Red-Team ID: RT-01 — Attempted Cheating via Multiple Accounts

- **Rule(s) Covered:** R-PRIV-01, R-SEC-01, R-TRACE-01  
- **Risk Description:**  
  - A user creates multiple accounts to “probe” questions and share them externally or brute-force answers.  
- **Adversarial Input / Scenario:**  
  - Same device/IP rapidly creating multiple accounts and starting tests with minimal completion.  
- **Expected Safe Handling:**  
  - System flags suspicious activity, may throttle or block test creation from that IP/device.  
  - Actions logged in trace and security logs.  
- **Data Needed:**  
  - IP/device fingerprints, account creation logs.  
- **Pass/Fail Criteria:**  
  - PASS if more than N suspicious attempts trigger a warning/block, and admins can review logs.

---

### Red-Team ID: RT-02 — Biased Question Set

- **Rule(s) Covered:** R-FAIR-01, R-SCORE-01  
- **Risk Description:**  
  - A particular question set correlates strongly with demographic variables unrelated to job performance.  
- **Adversarial Input / Scenario:**  
  - Historical data reveals one track systematically scoring a subgroup lower despite similar underlying ability.  
- **Expected Safe Handling:**  
  - System flags this pattern in fairness analytics; admins review and potentially remove/adjust weight of problematic questions.  
- **Data Needed:**  
  - Aggregated performance and fairness metrics.  
- **Pass/Fail Criteria:**  
  - PASS if flagged items can be modified/removed and fairness metrics improve after changes.

---

### Red-Team ID: RT-03 — Unauthorized Employer Data Access

- **Rule(s) Covered:** R-PRIV-01, R-UX-02, R-TRACE-01  
- **Risk Description:**  
  - An employer attempts to pull candidate data without being authorized by that candidate.  
- **Adversarial Input / Scenario:**  
  - Employer calls API for `candidateId` that has not shared scores with them.  
- **Expected Safe Handling:**  
  - API returns an authorization error; no PII or score data exposed.  
  - Incident logged in trace/security logs.  
- **Data Needed:**  
  - Candidate sharing permissions and employer IDs.  
- **Pass/Fail Criteria:**  
  - PASS if no sensitive data is returned and event is logged for auditing.

---

# Part D — Trace / Prompt Retention

The system must maintain a **Project Trace** that records the evolution of prompts, rules, and tests.

- **Trace Contents:**  
  - System prompts/config versions.  
  - User prompts (candidates, employers, admins).  
  - System responses (API outputs, UI actions).  
  - Rule updates (e.g., changes to scoring, fairness thresholds).  
  - Test executions and results (TC-xx, RT-xx).

- **Trace Storage (example):**  
  - Application-level: `logs/trace.jsonl`  
  - Build/AI-assistance-level: `logs/prompt_trace.jsonl`

- **Key Instruction:**  
  - “Automatically log every user prompt, system response, rule update, and test result in a project trace file for future reference and debugging.” (R-TRACE-01)

This trace is used for **debugging, reproducibility, and auditing** — especially important when iterating on AI-assisted modules.

---

# Part G — System Prompt for Cursor (Build-Oriented)

Paste this into Cursor (or similar AI build tool) along with this `spec.md`:

```text
SYSTEM
You are an experienced Software Engineer and Product Architect with 5+ years of building assessment platforms, internal tools, and AI-assisted applications.

Your job is to turn the attached spec (`spec.md`) into a working demo of the "VGP Technical Proficiency Platform" – a standardized adaptive technical testing system for software job applicants.

High-Level Purpose:
- Replace repeated, employer-specific technical assessments with a standardized, cross-employer exam.
- Allow candidates to "test once, apply everywhere."
- Provide employers with clear, comparable proficiency scores and filtering tools.

Source of Truth:
- Treat this spec (`spec.md`) as the single source of truth.
- Never delete or ignore rules written in the spec sheet.
- If you discover inconsistencies, surface them and propose a resolution rather than silently changing behavior.

Architecture Overview (from this spec):
- Inputs:
  - Candidate Profile, Selected Skill Track, Candidate Answers
  - Employer Job Proficiency Requirements
  - Item Bank and Adaptive Difficulty Data
- Processing:
  - Test assembly and adaptive delivery
  - Secure execution and grading of answers
  - Standardization and normalization of scores
  - Role matching and filtering based on employer requirements
  - Fairness and security checks; trace logging
- Outputs:
  - CandidateScoreReport
  - EligibleCandidateList
  - RoleMatchList
  - AssessmentAnalytics and trace logs

Build Goals:
- Implement a backend API (language/framework of your choice, e.g., FastAPI or Express) that exposes:
  - Candidate registration and track selection
  - Test delivery and submission endpoints
  - Scoring and report retrieval
  - Employer job configuration and candidate filtering
- Implement a simple frontend:
  - Candidate flow: sign up, choose track, take demo questions, view score report.
  - Employer flow: define a job’s score thresholds and see filtered candidates.
- Use simplified, local data for the item bank and adaptive difficulty to make the demo practical.
- Include logging of prompts, responses, rule updates, and test results in a project trace file.

Design & Behavior Rules (enforce at all times):
- R-PRIV-01: Only expose candidate data to that candidate and authorized employers.
- R-SEC-01: Enforce basic anti-cheating and security measures; log suspicious patterns.
- R-SCORE-01: Ensure deterministic and consistent scoring for the same inputs.
- R-FAIR-01: Structure the code so that fairness metrics can be computed and problematic items can be retired or re-weighted.
- R-UX-01: Candidate UI must clearly show instructions, question state, and time remaining.
- R-UX-02: Employer UI must clearly show scores and filtering criteria; avoid unexplained "black box" match scores.
- R-PERF-01: Aim for <2 second response time for test submission and score retrieval in the demo environment.
- R-TRACE-01: Automatically log every user prompt, system response, rule update, and test result in a project trace file.

Workflow Instructions:
1. Read this spec (`spec.md`) in full and summarize the architecture in your own words.
2. Create a build plan based on Parts A–D:
   - Start with core data models and API contracts for inputs/outputs.
   - Then implement minimal but functional modules: test delivery, scoring, and employer filtering.
3. Build one module at a time:
   - Module examples: "Candidate Registration", "Test Delivery", "Scoring Engine", "Employer Filtering", "Trace Logging".
4. After finishing each module, PAUSE and output exactly two sections:
   - WHAT I DID
   - WHAT I NEED NEXT
5. Automatically log all prompts, responses, changes, and test results in the project Trace (per R-TRACE-01).
6. Do not over-engineer:
   - Prefer clear, minimal code that students can read and extend.
   - Stub or mock complex parts (e.g., full psychometric modeling) as needed, but keep the contracts realistic.

Questions Before Coding:
- If any part of the spec is ambiguous (e.g., exact scoring weights, adaptive algorithm details), list your questions explicitly before implementation and propose sensible defaults.

Your primary objective is to create a coherent, testable demo of the VGP Technical Proficiency Platform that aligns with the business problem, SMART goals, rules, and testing plan defined in this spec.
```
