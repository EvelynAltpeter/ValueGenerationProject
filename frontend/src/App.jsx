import { useEffect, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

function App() {
  return (
    <main className="app-shell">
      <header>
        <h1>VGP Technical Proficiency Platform</h1>
        <p className="subtitle">
          Standardized adaptive testing demo — candidates test once, employers filter with clarity.
        </p>
      </header>
      <div className="grid">
        <CandidateFlow />
        <EmployerFlow />
      </div>
    </main>
  )
}

function CandidateFlow() {
  const [profile, setProfile] = useState({ name: '', email: '' })
  const [candidate, setCandidate] = useState(null)
  const [session, setSession] = useState(null)
  const [questionBlock, setQuestionBlock] = useState(null)
  const [answer, setAnswer] = useState('')
  const [code, setCode] = useState('')
  const [report, setReport] = useState(null)
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [statusMsg, setStatusMsg] = useState('')
  const [shareEmployerId, setShareEmployerId] = useState('')

  useEffect(() => {
    setError('')
  }, [profile.name, profile.email])

  async function registerCandidate() {
    setLoading(true)
    setStatusMsg('Creating candidate profile...')
    try {
      const res = await fetch(`${API_BASE}/api/candidates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      })
      const data = await res.json()
      setCandidate({ id: data.data.candidateId })
      setStatusMsg('Profile created. Next, choose your track.')
    } catch (err) {
      setError('Unable to create candidate. Check backend is running.')
    } finally {
      setLoading(false)
    }
  }

  async function startTrack(trackId) {
    if (!candidate) return
    setLoading(true)
    setStatusMsg(`Opening ${trackId} session...`)
    try {
      const res = await fetch(`${API_BASE}/api/candidates/${candidate.id}/tracks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trackId }),
      })
      const data = await res.json()
      const sessionInfo = { id: data.data.sessionId, expiresAt: data.data.expiresAt }
      setSession(sessionInfo)
      setReport(null)
      await fetchQuestion(sessionInfo.id)
    } catch (err) {
      setError('Unable to start session.')
    } finally {
      setLoading(false)
    }
  }

  async function fetchQuestion(sessionId = session?.id) {
    if (!sessionId) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/api/tests/${sessionId}/next`)
      const data = await res.json()
      setQuestionBlock(data.data)
      if (data.data.question.options?.length) {
        setAnswer(data.data.question.options[0])
      }
      setStatusMsg('Question loaded. Stay focused and watch the timer!')
    } catch (err) {
      setError('Unable to fetch next question.')
    } finally {
      setLoading(false)
    }
  }

  async function submitResponse() {
    if (!session || !questionBlock) return
    const isCoding = questionBlock.question.questionType === 'coding'
    setLoading(true)
    try {
      await fetch(`${API_BASE}/api/tests/${session.id}/responses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          questionId: questionBlock.question.questionId,
          responseType: isCoding ? 'coding' : 'mcq',
          answer: isCoding ? null : answer,
          code: isCoding ? code : null,
          timeTakenSeconds: 45,
          copiedCharacters: 0,
        }),
      })
      setStatusMsg('Response recorded. Loading next question...')
      setAnswer('')
      setCode('')
      await fetchQuestion()
    } catch (err) {
      setError('Submission failed. Please retry.')
    } finally {
      setLoading(false)
    }
  }

  async function submitSession() {
    if (!session) return
    setLoading(true)
    setStatusMsg('Scoring your attempt...')
    try {
      const res = await fetch(`${API_BASE}/api/tests/${session.id}/submit`, {
        method: 'POST',
      })
      const data = await res.json()
      setReport(data.data)
      setQuestionBlock(null)
      setStatusMsg('Score ready! Share with employers or view recommended roles.')
    } catch (err) {
      setError('Unable to finalize test.')
    } finally {
      setLoading(false)
    }
  }

  async function fetchMatches() {
    if (!candidate) return
    const res = await fetch(`${API_BASE}/api/candidates/${candidate.id}/matches`)
    const data = await res.json()
    setMatches(data.data.recommendedJobs ?? [])
  }

  async function shareWithEmployer() {
    if (!candidate || !shareEmployerId) return
    await fetch(`${API_BASE}/api/candidates/${candidate.id}/share`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ employerId: shareEmployerId }),
    })
    setStatusMsg(`Shared score access with ${shareEmployerId}.`)
    setShareEmployerId('')
  }

  return (
    <section className="panel">
      <h2>Candidate Experience</h2>
      <p className="hint">
        R-UX-01: Instructions, timer, and submission state are always visible. Finish within 30 minutes.
      </p>

      {!candidate && (
        <div className="card">
          <h3>Step 1 · Sign Up</h3>
          <label>
            Name
            <input value={profile.name} onChange={(e) => setProfile({ ...profile, name: e.target.value })} />
          </label>
          <label>
            Email
            <input value={profile.email} onChange={(e) => setProfile({ ...profile, email: e.target.value })} />
          </label>
          <button disabled={!profile.name || !profile.email || loading} onClick={registerCandidate}>
            Create Profile
          </button>
        </div>
      )}

      {candidate && !session && (
        <div className="card">
          <h3>Step 2 · Choose Track</h3>
          <p>Select a skill track to open a timed adaptive session.</p>
          <button onClick={() => startTrack('python_core_v1')}>Start Python Core</button>
        </div>
      )}

      {session && questionBlock && (
        <div className="card">
          <h3>Step 3 · Test Player</h3>
          <div className="timer">Time remaining: {questionBlock.timeRemaining}s</div>
          <p className="prompt">{questionBlock.question.prompt}</p>
          {questionBlock.question.questionType === 'mcq' ? (
            <select value={answer} onChange={(e) => setAnswer(e.target.value)}>
              {questionBlock.question.options?.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          ) : (
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Write your solution here"
              rows={6}
            />
          )}
          <div className="actions">
            <button onClick={submitResponse} disabled={loading}>
              Submit Response
            </button>
            <button className="ghost" onClick={submitSession}>
              Finish & Score
            </button>
          </div>
        </div>
      )}

      {session && !questionBlock && !report && (
        <p className="hint">No more questions queued. Submit to receive your score.</p>
      )}

      {report && (
        <div className="card">
          <h3>Score Report · {report.trackId}</h3>
          <p className="score">{report.overallScore}</p>
          <div className="subscores">
            <span>Algorithms: {report.subscores.algorithms}</span>
            <span>Data Structures: {report.subscores.data_structures}</span>
            <span>Code Quality: {report.subscores.code_quality}</span>
          </div>
          <p>Percentile: {report.percentile}</p>
          <button onClick={fetchMatches}>View Recommended Roles</button>
          {matches.length > 0 && (
            <ul>
              {matches.map((match) => (
                <li key={match.jobId}>
                  {match.company} — Job {match.jobId} · Match {match.matchScore}%
                </li>
              ))}
            </ul>
          )}
          <div className="share-actions">
            <input
              value={shareEmployerId}
              onChange={(e) => setShareEmployerId(e.target.value)}
              placeholder="Employer ID to share"
            />
            <button onClick={shareWithEmployer}>Share Access</button>
          </div>
        </div>
      )}

      {loading && <p className="status">Processing...</p>}
      {statusMsg && <p className="status">{statusMsg}</p>}
      {error && <p className="error">{error}</p>}
    </section>
  )
}

function EmployerFlow() {
  const [name, setName] = useState('')
  const [employer, setEmployer] = useState(null)
  const [jobConfig, setJobConfig] = useState({ jobId: 'backend-dev-123', trackId: 'python_core_v1', minScore: 75 })
  const [eligible, setEligible] = useState([])
  const [status, setStatus] = useState('')

  async function createEmployer() {
    const res = await fetch(`${API_BASE}/api/employers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    })
    const data = await res.json()
    setEmployer({ id: data.data.employerId, name })
    setStatus(`Employer ${name} ready. Configure a role next.`)
  }

  async function saveJob() {
    if (!employer) return
    const requirement = {
      jobId: jobConfig.jobId,
      employerId: employer.id,
      requiredTracks: [jobConfig.trackId],
      minScores: { [jobConfig.trackId]: Number(jobConfig.minScore) },
    }
    await fetch(`${API_BASE}/api/employers/${employer.id}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requirement),
    })
    setStatus('Job thresholds saved. Ask candidates to share scores.')
  }

  async function loadEligible() {
    if (!employer) return
    const res = await fetch(
      `${API_BASE}/api/employers/${employer.id}/jobs/${jobConfig.jobId}/eligible`,
    )
    const data = await res.json()
    setEligible(data.data.eligibleCandidates ?? [])
    setStatus(`Found ${data.data.eligibleCandidates?.length ?? 0} eligible candidates.`)
  }

  return (
    <section className="panel">
      <h2>Employer Console</h2>
      <p className="hint">R-UX-02: Score thresholds and match explanations are explicit.</p>

      {!employer && (
        <div className="card">
          <h3>Step 1 · Create Employer</h3>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Team name" />
          <button disabled={!name} onClick={createEmployer}>
            Generate Employer ID
          </button>
        </div>
      )}

      {employer && (
        <>
          <div className="badge">Employer ID: {employer.id}</div>
          <div className="card">
            <h3>Step 2 · Define Job Filter</h3>
            <label>
              Job ID
              <input
                value={jobConfig.jobId}
                onChange={(e) => setJobConfig({ ...jobConfig, jobId: e.target.value })}
              />
            </label>
            <label>
              Track
              <select
                value={jobConfig.trackId}
                onChange={(e) => setJobConfig({ ...jobConfig, trackId: e.target.value })}
              >
                <option value="python_core_v1">Python Core</option>
              </select>
            </label>
            <label>
              Minimum Score
              <input
                type="number"
                value={jobConfig.minScore}
                onChange={(e) => setJobConfig({ ...jobConfig, minScore: e.target.value })}
              />
            </label>
            <button onClick={saveJob}>Save Requirements</button>
          </div>

          <div className="card">
            <h3>Step 3 · Filter Candidates</h3>
            <p>
              Ask candidates to call <code>/share</code> with employer ID <strong>{employer.id}</strong>.
            </p>
            <button onClick={loadEligible}>Run Filter</button>
            {eligible.length > 0 && (
              <table>
                <thead>
                  <tr>
                    <th>Candidate</th>
                    <th>Python Score</th>
                    <th>Match</th>
                    <th>Explanation</th>
                  </tr>
                </thead>
                <tbody>
                  {eligible.map((item) => (
                    <tr key={item.candidateId}>
                      <td>{item.name}</td>
                      <td>{item.trackScores.python_core_v1}</td>
                      <td>{item.matchScore}%</td>
                      <td>{item.matchExplanation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
      {status && <p className="status">{status}</p>}
    </section>
  )
}

export default App
