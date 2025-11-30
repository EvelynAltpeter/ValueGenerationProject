# VGP Technical Proficiency Platform — Spec Sheet

**Spec Version:** v1.0  
**Date:** 2025-12-03  
**Owner:** Jet U.  
**Status:** Active – Implementation Ready

---

# Part A — Business Context (The "Why")

## A1. Strategy / Context

Our product operates primarily in a **Blue Ocean** space.

While platforms like LeetCode, HackerRank, and Codility dominate technical skill assessment and preparation, none offer a standardized, cross-company certification system for new graduates, delivered through universities, that allows a single technical evaluation to replace multiple redundant assessments in job applications.

We are not competing to provide another coding test library — we are redefining the hiring process itself by introducing an interoperable testing credential recognized by multiple employers. This creates new market space by reducing hiring friction for both sides of the job market.

### Marketing Principles (MPs 1–4) as strategic lenses

**MP1: All Customers Differ**

Employers vary in their technical assessment methods, and universities differ in curriculum focus, student preparedness, and industry connections. New graduates differ in skill level, preparation style, and time availability. Our solution focuses first on these segments by offering a standardized, school-endorsed certification exam that universities can integrate into senior year and that new graduates can use across many employers. Employers still vary in their standards, but instead of designing their own screens, they can specify score thresholds and role profiles on top of a common credential.

**MP2: All Customers Change**

The hiring landscape evolves rapidly, companies are shifting toward AI-driven screening and remote evaluation. Our standardized platform can update question banks and scoring algorithms dynamically, ensuring continued relevance as skills and technologies evolve.

**MP3: All Competitors React**

Existing assessment providers (LeetCode, HackerRank, etc.) may try to integrate standardized scoring or partnerships once this idea gains traction. To stay ahead, we focus on industry collaboration and credential legitimacy — securing early adoption through university partnerships and company endorsements.

**MP4: All Resources Are Limited**

Both employers and candidates face resource constraints — time, energy, and budget. By eliminating repetitive interview steps, our platform reduces hiring costs and candidate burnout, allowing both sides to allocate resources more strategically toward culture fit and final-round evaluations.

## A2. Problem Statement (S–C–Q)

**Situation:**

The technical hiring process is fragmented and inefficient, especially for new graduates entering the job market. Candidates must complete multiple coding challenges and interviews for each application, while employers spend significant time designing, administering, and evaluating these assessments.

**Complication:**

This redundancy creates major inefficiencies:

- Candidates face burnout and attrition before completing all interview stages.
- Companies struggle to compare applicants consistently and lose qualified talent due to "interview fatigue."
- Standardized skill data is missing, leading to inconsistent hiring decisions across the industry.
- Universities lack a standardized way to demonstrate that their graduates meet baseline technical standards for industry roles.

**Question:**

How can we create a standardized, cross-employer technical assessment that fairly evaluates candidates' abilities once and shares verified results across multiple employers to reduce time, bias, and costs in the hiring process?

## A3. SMART Goals

**Specific:** Build a centralized platform that provides one standardized technical test per programming language whose score can be submitted to multiple employers.

**Measurable:** Aim to reduce average candidate interview time by 50% and employer evaluation costs by 30% within the first year of pilot rollout.

**Achievable:** Develop a demo of a standardized technical test for at least one programming language.

**Relevant:** Addresses real inefficiencies in hiring processes, improving candidate experience and employer efficiency simultaneously.

**Time-Bound:** Demo and scaling idea/plan is completed by December 3rd 2025.

## A4. Problem Statement (Alternative)

The job market is exhausting and overcrowded for both employers and candidates in the technical space. The current solution of every company offering early stage technical interviews to each candidate is unsustainable for all parties involved. There needs to be a cross-functional application and evaluation platform to streamline the application process for technical roles, which will ultimately result in the best possible outcome for both employers and candidates.

## A5. Business Model Canvas

### Key Partners

**Key partners:**

- Employers
- LeetCode
- Universities/coding bootcamps - They could integrate your assessment into their curricula, giving you early adoption and credibility
- Professional certification bodies (like CompTIA, AWS, etc.) - Partnership validates your standardization
- Technology infrastructure providers (AWS, cloud services) - Essential for scaling
- HR software companies (Workday, Greenhouse, Lever) - Integration partnerships to embed your scores directly into existing ATS systems

**Key suppliers:**

Resources we're acquiring from key partners:

- Example problems for various proficiencies

**Activities done by key partners:**

- Evaluate candidates based on their competencies proven by standardized tests
- Post job listings to software

**Motivation for partnerships:**

**Universities:**

- Access to talent pipelines - reach students before they enter the job market
- Credibility and Legitimacy: university endorsements makes your credentials more valuable to employers
- Distribution at scale: Career service offices can promote to thousands of students with minimal additional costs
- Data for platform improvement: understand what skills universities are teaching vs. what employers need

**Hiring Agencies:**

- Reach employers you can't access directly: recruiting firms already have relationships with companies
- Volume of applicants: agencies send high volumes of candidates, so your platform becomes more valuable the more agencies use it

**Employers:**

- Co-design standardized question banks: get buy-in by involving them in what "good" looks like for their role
- Industry endorsements; early adopter companies become advocates, pulling in competitors

### Key Activities

- Continuous question bank curation and updating - preventing memorization, keeping content current
- Psychometric validation and bias testing - ensuring fairness across demographics
- Security and anti-cheating measures - proctoring, plagiarism detection
- Data analytics and reporting - providing employers with meaningful insights beyond just scores
- Partnership development and maintenance - actively recruiting employers to accept your credential
- Marketing and brand building - establishing legitimacy as "the standard"
- Customer support for both sides of the platform - helping employers and candidates

### Value Propositions

**For Employers (expand):**

- Reduced time-to-hire by 40-50%
- Standardized, comparable data across all candidates
- Lower risk of bad hires through validated assessments
- Access to pre-vetted talent pool
- Reduced interview fatigue for their engineering teams

**For Candidates (expand):**

- "Take the test once, apply everywhere" - clear, simple promise
- Reduced interview anxiety and burnout
- Transparent skill validation they can showcase
- Faster job search process
- Portable credential that builds value over time

### Customer Relationships

- Firms that are hiring and will be using the product
- Universities to pitch the use to students
- Students themselves who are applying for jobs

**For Candidates:**

- Self-service platform for test-taking
- Automated score reporting
- Community forums for preparation tips
- Email support for technical issues

**For Employers:**

- Dedicated account management (for enterprise clients)
- Onboarding and integration support
- Regular reporting on assessment validity and candidate pools
- Co-creation: involving employers in defining competency standards

### Customer Segments

**Job Seekers (Multi-sided):**

- New graduates (high volume, low experience)
- Mid-career switchers (moderate volume, some experience)
- Senior engineers (lower volume, high expectations)

**Employers (Multi-sided):**

- Tech companies (startups to enterprise)
- Non-tech companies with tech roles
- Recruiting agencies

### Key Resources

- Physical capital (computers and data systems to store the code/assessment/data)
- Human capital in that we need coders to be ensuring the assessment is staying up to date and working properly
- Intellectual property - your proprietary scoring algorithms, question banks
- Brand reputation and trust - this is critical for a certification to work
- Network effects - the more employers that accept it, the more valuable it becomes
- Data and analytics infrastructure - to process assessments and generate insights
- Technical talent - software engineers, data scientists, psychometricians (people who design valid assessments)
- Content creators - people writing and validating assessment questions
- Security infrastructure - anti-cheating technology

### Channels

**(employers)**

- Through hiring agencies
- LinkedIn
- GitHub
- Direct sales team (for enterprise)
- HR conferences and trade shows
- Partnerships with ATS providers
- Industry publications and thought leadership

**(candidates):**

- Universities
- Tech Community spaces (learning programs, Discord)
- University career centers
- Online job boards (Indeed, LinkedIn integration)
- Social media and content marketing
- Referral programs

### Cost Structure

**Fixed Costs:**

- Technology infrastructure and hosting
- Full-time engineering and content teams
- Security and compliance systems
- Office space (if applicable)
- Marketing and brand building

**Variable Costs:**

- Customer support (scales with users)
- Proctoring services (if live proctoring)
- Payment processing fees
- Server costs (scale with usage)

### Revenue Streams

**Companies:**

Subscription model - Pay for the ability to post job listings and connect with specific proficiencies

**Applicants:**

Freemium Model - the first 10 applications per quarter are free, then candidates pay to send additional applications beyond this threshold.

---

# Part B — Build Plan (The "How")

## B1. Solution Overview

**What type of system is it?**

This system is a standardized adaptive technical testing platform that generates verifiable proficiency scores for software job applicants.

**What core function does it perform?**

Its core function is to replace repeated employer-specific technical assessments with one unified exam whose results can be shared across job applications.

**What human or business task does it replace or support?**

It supports and partially automates tasks currently performed by recruiters, hiring managers, and take-home technical interview systems. Limited time wasted by these stakeholders interviewing people who lack the elementary skills for the job listing.

## B2. Inputs Required from User or Data Sources

### 1. User Profile (Candidate)

**Input Name:** Candidate Profile

**Description:** Basic information needed to create an account and link scores.

**Source:** Manual user entry

**Example Value:**
```json
{
  "name": "Evelyn",
  "email": "evelyn@example.com",
  "GitHub": "github.com/evelyn"
}
```

### 2. Skill Selection

**Input Name:** Selected Skill Track

**Description:** Job role and technical skill track that determine which standardized test the candidate sees.

**Source:** User selects from a drop down

**Example Value:**
```json
{
  "Job Position": "Software Engineer",
  "Skill": "Python"
}
```

### 3. Test Response

**Input Name:** Candidate Answers

**Description:** Code submissions or multiple-choice answers during testing.

**Source:** User writes code or selects responses

**Example Value:** Python function submitted through code editor

### 4. Employer Job Requirements

**Input Name:** Job Proficiency Requirements

**Description:** The employer-specified skill areas and proficiency thresholds.

**Source:** Employer dashboard entry

**Example Value:**
```json
{
  "jobPos": "Quant",
  "requiredTrack": "C++",
  "minScore": 72
}
```

### 5. Item Bank/Test Database

**Input Name:** Standardized Tests Bank (LeetCode type based)

**Description:** Continuously updated set of validated and difficulty-calibrated questions.

**Source:** Internal database; curated content; partnerships

**Example Value:** Code challenge #213: Binary Tree Paths

### 6. Historical Scoring Data

**Input Name:** Historical Scoring Data

**Description:** Aggregated past test results used to calibrate question difficulty and percentile cutoffs for adaptive testing.

**Source:** System-generated and stored

**Example Value:**
```json
{
  "difficultyEstimate": 0.68
}
```

## B3. Outputs Produced by the System

### 1. Standardized Score Report

**Format:** JSON + human-readable PDF

**Recipients:** Candidates + Employers

**Example:**
```json
{
  "score": 81,
  "percentile": 74,
  "weaknesses": ["graphs"],
  "strengths": ["arrays"]
}
```

### 2. Candidate Dashboard

**Format:** Web UI

**Recipients:** Candidate

**Shows:** Scores, percentile band, recommended companies/jobs

### 3. Employer Match Report

**Format:** JSON / Table in dashboard

**Recipients:** Employers

**Shows:** Candidates who meet or exceed job-specific proficiency thresholds.

### 4. System Logs

**Format:** Structured logs (JSON)

**Use:** Internal transparency, debugging, compliance audit trails

### 5. Difficulty/Item Calibration Updates

**Format:** Internal metadata updates

**Recipients:** Adaptive testing engine

## B4. Core Logic / System Modules

1. **User Authentication Module**
   - Candidate or employer logs in; profile created or retrieved.

2. **Skill Track Selection**
   - User selects assessment type.

3. **Adaptive Test Engine**
   - Pulls items from question bank
   - Adjusts difficulty based on candidate responses
   - Validates code (unit tests, runtime checks)

4. **Scoring Engine**
   - Calculates raw score
   - Converts to standardized proficiency score
   - Generates percentile via historical distribution
   - Stores results in database

5. **Report Generation Module**
   - Produces candidate score report
   - Generates employer-facing summary for matches

6. **Employer Job-Matching Module**
   - Employers upload requirements
   - System filters applicants meeting thresholds

7. **Notification & Integration Layer**
   - Sends candidate results
   - Alerts employers when qualified candidates appear

8. **Admin/Content Review Module**
   - For updating test bank
   - Evaluating item difficulty
   - Approving new content

9. **Error Handling Module**
   - Handles missing data, failed code submissions, timeout, or system errors
   - Provides recovery steps

## B5. Design and Behavior Rules (Rule IDs)

| Rule ID | Description | Category |
|---------|-------------|----------|
| R-PRIV-01 | All candidate data must be stored securely and never shared without explicit consent. | Privacy |
| R-PERF-01 | Code submissions must be evaluated within 3 seconds per test case. | Performance |
| R-SCOR-01 | Scoring must follow the standardized scoring algorithm (raw → scaled → percentile). | Logic |
| R-UX-01 | Error messages must be clear, non-technical, and actionable. | UX |
| R-ETH-01 | System must ensure fairness — tests cannot show different questions based on demographics. | Ethics |
| R-REP-01 | Every score report must include score, percentile, strengths, and weaknesses. | Output Consistency |
| R-LOG-01 | System must log all test events for auditability. | Governance |

## B6. Mini Input/Output Example

**Minimal input:**
```json
{
  "userId": "cand_123",
  "selectedTrack": "Research",
  "language": "Python"
}
```

**Minimal output:**
```json
{
  "score": 84,
  "percentile": 78,
  "strengths": ["trees", "DP"],
  "weaknesses": ["graphs"],
  "timestamp": "2025-03-12T15:40Z"
}
```

## B7. Key Metrics or Success Criteria

| Objective | Metric | Target | Source of Data |
|-----------|--------|--------|----------------|
| Reduce candidate time burden | Avg. interview hours saved | 50% reduction | Pre/post candidate surveys |
| Reduce employer evaluation workload | Time spent screening | 30% reduction | Recruiter logs |
| Increase hiring efficiency | % employers using the score for screening | 5 pilot employers within 6 months | Usage analytics |
| Improve test validity | Score consistency across cohorts | <10% variance | Score analysis DB |

## B8. Assumptions & Dependencies

**Data sources or external APIs needed:**

- Item bank created from curated coding problems
- Historical performance data for calibration

**Technical dependencies:**

- Cloud database (Postgres, MongoDB, or equivalent)
- Scoring engine + containerized code runner (Docker)
- Web front end (React)
- CI/CD pipeline for test bank updates

**Business assumptions:**

- Employers will adopt standardized scores
- Universities will promote the platform
- Candidates will prefer one test over 10+ separate ones
- Problem bank can be maintained/updated continuously

**Constraints:**

- Must remain fair, bias-mitigated, and legally compliant
- Must withstand high traffic during recruiting cycles

---

# Part C — Testing Plan (The "Proof")

## C1. Positive Test Cases (What Should Work)

### Test Case ID: TC-01

**Rule(s) Covered:** R-SCOR-01, R-REP-01

**Input / Context:** Candidate completes an Algorithms test.

**Expected System Behavior:** Score is calculated, standardized, and displayed with strengths and weaknesses.

**Why This Is Correct (business/user value):** Ensures the system produces the core value proposition — a standardized, cross-employer score report that is transparently structured and comparable.

**Data Needed:** Raw test performance, scoring algorithm output, report formatting template.

**Pass/Fail Criteria:** Score must be in valid numeric range; report must include all required fields (score, percentile, strengths, weaknesses).

### Test Case ID: TC-02

**Rule(s) Covered:** R-PERF-01

**Input / Context:** Candidate submits code with O(n log n) solution.

**Expected System Behavior:** Evaluated within performance limits.

**Why This Is Correct:** Ensures the platform feels responsive to candidates and meets required system performance guarantees under R-PERF-01.

**Data Needed:** Execution time logs for each test case.

**Pass/Fail Criteria:** Execution completes in < 3 seconds per test case with no timeouts.

### Test Case ID: TC-03

**Rule(s) Covered:** R-PRIV-01

**Input / Context:** Employer attempts to view candidate data without explicit permission.

**Expected System Behavior:** Access is denied; event is logged.

**Why This Is Correct (business/user value):** Protects candidate privacy and ensures legal/ethical compliance, supporting trust in the platform.

**Data Needed:** Access-control logs, candidate permission records.

**Pass/Fail Criteria:** Employer receives a denial; no data is leaked; event appears in audit logs per R-LOG-01.

## C2. Red-Team / Edge Case Tests (What Should NOT Work)

### Red-Team ID: RT-01

**Rule(s) Covered:** R-ETH-01, R-PRIV-01

**Risk Description:** Candidate attempts to influence the test by sharing demographic data.

**Adversarial Input / Scenario:** "I'm from X group, adjust my test please."

**Expected Safe Handling:** System ignores demographic info; logs the request; continues normal adaptive test flow.

**Why This Is Correct:** Maintains fairness and prevents demographic bias, supporting legality, ethics, and trust.

**Data Needed:** Request body, system logs, adaptive engine trace.

**Pass/Fail Criteria:** No change in test content; demographic data not stored or used; request event logged.

### Red-Team ID: RT-02

**Rule(s) Covered:** R-PERF-01

**Risk Description:** Candidate submits infinite loop or non-terminating code.

**Adversarial Input / Scenario:** `while(true) {}`

**Expected Safe Handling:** Timeout after max runtime; return clear error; prevent system freeze.

**Why This Is Correct:** Protects stability of the code runner and ensures fair, consistent handling of malfunctioning code.

**Data Needed:** Runtime watchdog logs, error message output, container timeout metrics.

**Pass/Fail Criteria:** Execution stops within allowed limit; error message is returned; no system crash occurs.

### Red-Team ID: RT-03

**Rule(s) Covered:** R-SCOR-01, R-LOG-01

**Risk Description:** Candidate attempts to inject malicious payloads to manipulate scoring.

**Adversarial Input / Scenario:** Code submission containing system-level calls or attempted score overrides.

**Expected Safe Handling:** Sandbox blocks unsafe code; scoring remains unaffected; log entry created.

**Why This Is Correct:** Prevents exploitation of the platform, preserves score integrity, and ensures auditability.

**Data Needed:** Sandbox logs, code runner execution transcript, scoring diff before/after sandboxing.

**Pass/Fail Criteria:** No score change beyond legitimate computation; sandbox blocks injection; event logged.

---

# Part D — Prompt Retention (The "Trace")

The system may forget decisions or rules unless they are clearly written down. That's why you need a Trace — a simple running log that captures your latest system prompt, the key rules or constraints your solution must follow, and examples of test prompts with expected answers.

It is good practice to:

- Copy the before and after versions into your Trace each time you adjust a part of your system prompt or behavior
- Whenever you test your product, record examples of what worked and what broke, as well as how you fixed it
- Use the Trace as your "memory file" so the system doesn't repeat mistakes — especially when rebuilding or debugging.

Your system prompt should require:

- Logging every user action
- Logging all rule changes
- Logging all test runs
- Saving before/after states
- Recording failures and resolutions

Add this line to the final system prompt:

"Automatically log every user prompt, system response, rule update, and test result in a project trace file for future reference and debugging."

---

# Part E — System Prompt

Convert everything from Parts A–D into a clear, complete system prompt that a tool like Cursor can use to start building your digital product for you. The system prompt should explain the what and the why of the product, as well as the important rules and constraints the AI must follow.

Your job is to:

1. Read and interpret the attached spec sheet in full.
2. Create a build plan for the solution based on the architecture described.
3. Begin development by building one module at a time (e.g., inputs, core logic, interface).
4. After finishing each module, pause and ask for my review before proceeding.
5. Automatically log all prompts, responses, changes, and test results in a project Trace.
6. Never delete or ignore rules written in the spec sheet.

Confirm your understanding by:

- Outlining the full architecture (input → processing → output flow)
- Listing any questions you have about the spec before coding begins

## SYSTEM PROMPT (Copy/Paste into Cursor)

You are building a Standardized Adaptive Technical Testing Platform.

Your goal is to produce a unified, reusable proficiency score for job applicants that employers can trust and integrate into hiring pipelines.

### ARCHITECTURE SUMMARY

Input → Adaptive Test Engine → Scoring Engine → Score Report → Employer Matching Module → Logs

### SYSTEM REQUIREMENTS

Implement all rules defined in Part B (R-PRIV-01, R-PERF-01, R-SCOR-01, R-UX-01, R-ETH-01, R-REP-01, R-LOG-01).

Build modules one at a time (auth → test engine → scoring → reporting → employer portal).

Pause after each module and request user review.

Automatically log every user prompt, system response, rule update, and test result in a project Trace.

### YOU MUST:

- Follow the spec sheet exactly — never remove or override rules.
- Use the defined inputs, outputs, logic flow, and testing plan.
- Maintain standardized scoring and fairness rules.
- Enforce privacy, sandbox execution, and consistent reporting.
- Use the architecture to guide implementation.

### BEFORE CODING YOU MUST ASK:

"Here is the architecture as I understand it — is this correct?"

"Do you approve starting with Module 1: Authentication & User Profiles?"
