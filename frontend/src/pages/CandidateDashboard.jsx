/**
 * Candidate Dashboard - Test Taking & Score Viewing
 * R-UX-01: Clear instructions, timer visibility, submission state
 * R-REP-01: Display strengths and weaknesses in score reports
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

function CandidateDashboard() {
  const navigate = useNavigate()
  const [candidateId, setCandidateId] = useState(null)
  const [candidateName, setCandidateName] = useState('')
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
    const storedId = localStorage.getItem('candidateId')
    const storedName = localStorage.getItem('candidateName')
    
    if (!storedId) {
      navigate('/candidate')
    } else {
      setCandidateId(storedId)
      setCandidateName(storedName || 'Candidate')
    }
  }, [navigate])

  async function startTrack(trackId) {
    setLoading(true)
    setStatusMsg(`Starting ${trackId} session...`)
    setError('')
    
    try {
      const res = await fetch(`${API_BASE}/api/candidates/${candidateId}/tracks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trackId }),
      })
      
      const data = await res.json()
      const sessionInfo = { id: data.data.sessionId, expiresAt: data.data.expiresAt }
      setSession(sessionInfo)
      setReport(null)
      setStatusMsg('Session started! Loading first question...')
      await fetchQuestion(sessionInfo.id)
    } catch (err) {
      setError('Unable to start session. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  async function fetchQuestion(sessionId = session?.id) {
    if (!sessionId) return
    setLoading(true)
    setError('')
    
    try {
      const res = await fetch(`${API_BASE}/api/tests/${sessionId}/next`)
      
      if (!res.ok) {
        // No more questions - this is normal at the end of a test
        setStatusMsg('All questions completed. Calculating score...')
        await submitSession()
        return
      }
      
      const data = await res.json()
      
      if (!data.data || !data.data.question) {
        setStatusMsg('All questions completed. Calculating score...')
        await submitSession()
        return
      }
      
      setQuestionBlock(data.data)
      
      if (data.data.question.options?.length) {
        setAnswer(data.data.question.options[0])
      }
      
      setStatusMsg('')
    } catch (err) {
      // If we can't fetch more questions, try to submit the session
      if (session) {
        setStatusMsg('All questions completed. Calculating score...')
        await submitSession()
      } else {
        setError('Unable to fetch question. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  async function submitResponse() {
    if (!session || !questionBlock) return
    
    const isCoding = questionBlock.question.questionType === 'coding'
    setLoading(true)
    setError('')
    
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
      
      setAnswer('')
      setCode('')
      
      // Try to fetch next question
      try {
        const nextRes = await fetch(`${API_BASE}/api/tests/${session.id}/next`)
        if (nextRes.ok) {
          const nextData = await nextRes.json()
          setQuestionBlock(nextData.data)
          setStatusMsg('Responses Recorded!')
        } else {
          // No more questions - automatically submit the test
          setStatusMsg('All responses recorded! Calculating score...')
          await submitSession()
        }
      } catch (nextErr) {
        // No more questions - automatically submit the test
        setStatusMsg('All responses recorded! Calculating score...')
        await submitSession()
      }
    } catch (err) {
      setError('Submission failed. Please retry.')
      setStatusMsg('')
    } finally {
      setLoading(false)
    }
  }

  async function submitSession() {
    if (!session) return
    setLoading(true)
    setError('')
    
    // Only show scoring message if not already shown
    if (!statusMsg.includes('Calculating')) {
      setStatusMsg('Scoring your test...')
    }
    
    try {
      const res = await fetch(`${API_BASE}/api/tests/${session.id}/submit`, {
        method: 'POST',
      })
      
      if (!res.ok) {
        throw new Error('Failed to submit test')
      }
      
      const data = await res.json()
      
      if (!data.data) {
        throw new Error('Invalid response from server')
      }
      
      setReport(data.data)
      setQuestionBlock(null)
      setSession(null)
      setStatusMsg(`✅ Test Complete! Your score: ${data.data.overallScore}/100 (${data.data.percentile}th percentile)`)
    } catch (err) {
      setError('Unable to finalize test. Please try again.')
      setStatusMsg('')
    } finally {
      setLoading(false)
    }
  }

  async function fetchMatches() {
    try {
      const res = await fetch(`${API_BASE}/api/candidates/${candidateId}/matches`)
      const data = await res.json()
      setMatches(data.data.recommendedJobs ?? [])
    } catch (err) {
      setError('Unable to fetch matches.')
    }
  }

  async function shareWithEmployer() {
    if (!candidateId || !shareEmployerId.trim()) return
    
    try {
      await fetch(`${API_BASE}/api/candidates/${candidateId}/share`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ employerId: shareEmployerId.trim() }),
      })
      setStatusMsg(`✓ Shared with ${shareEmployerId}`)
      setShareEmployerId('')
    } catch (err) {
      setError('Unable to share with employer.')
    }
  }

  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getTimerClass = (timeRemaining) => {
    if (timeRemaining < 300) return 'timer danger'
    if (timeRemaining < 600) return 'timer warning'
    return 'timer'
  }

  function returnHome() {
    navigate('/')
  }

  function takeAnotherTest() {
    setSession(null)
    setQuestionBlock(null)
    setReport(null)
    setMatches([])
    setStatusMsg('')
    setError('')
  }

  if (!candidateId) return null

  return (
    <main className="main-content">
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>Welcome, {candidateName}</h1>
            <p className="text-muted">Your Technical Proficiency Dashboard</p>
          </div>
          <button className="btn btn-secondary btn-small" onClick={returnHome}>
            ← Home
          </button>
        </div>

        {/* Status Messages */}
        {statusMsg && (
          <div className="status-message status-success">{statusMsg}</div>
        )}
        {error && (
          <div className="status-message status-error">{error}</div>
        )}

        {/* Track Selection */}
        {!session && !report && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Select Skill Track</h3>
            </div>
            <p className="text-muted">Choose a standardized test to begin. Each session lasts 30 minutes.</p>
            
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
              gap: '16px',
              marginTop: '24px'
            }}>
              <button 
                className="btn" 
                onClick={() => startTrack('python_core_v1')}
                style={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  alignItems: 'center',
                  padding: '24px',
                  height: 'auto'
                }}
              >
                <span style={{ fontSize: '36px', marginBottom: '8px' }}>🐍</span>
                <strong>Python Core</strong>
                <span style={{ fontSize: '13px', marginTop: '4px', opacity: 0.8 }}>52 questions</span>
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={() => startTrack('sql_core_v1')}
                style={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  alignItems: 'center',
                  padding: '24px',
                  height: 'auto'
                }}
              >
                <span style={{ fontSize: '36px', marginBottom: '8px' }}>💾</span>
                <strong>SQL Core</strong>
                <span style={{ fontSize: '13px', marginTop: '4px', opacity: 0.8 }}>10 questions</span>
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={() => startTrack('javascript_core_v1')}
                style={{ 
                  display: 'flex', 
                  flexDirection: 'column', 
                  alignItems: 'center',
                  padding: '24px',
                  height: 'auto'
                }}
              >
                <span style={{ fontSize: '36px', marginBottom: '8px' }}>⚡</span>
                <strong>JavaScript Core</strong>
                <span style={{ fontSize: '13px', marginTop: '4px', opacity: 0.8 }}>31 questions</span>
              </button>
            </div>
          </div>
        )}

        {/* Test Player */}
        {session && questionBlock && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Adaptive Test</h3>
              <div className={getTimerClass(questionBlock.timeRemaining)}>
                ⏱ {formatTime(questionBlock.timeRemaining)}
              </div>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <div className="badge badge-accent">
                Difficulty: {questionBlock.band}
              </div>
            </div>

            <div style={{ 
              padding: '24px', 
              background: 'var(--color-surface)', 
              borderRadius: 'var(--radius-sm)',
              marginBottom: '24px'
            }}>
              <p style={{ color: 'var(--color-text-primary)', whiteSpace: 'pre-wrap' }}>
                {questionBlock.question.prompt}
              </p>
            </div>

            {questionBlock.question.questionType === 'mcq' ? (
              <div className="form-group">
                <label className="form-label">Your Answer</label>
                <select className="form-select" value={answer} onChange={(e) => setAnswer(e.target.value)}>
                  {questionBlock.question.options?.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
            ) : (
              <div className="form-group">
                <label className="form-label">Your Solution</label>
                <textarea
                  className="form-textarea"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Write your code solution here..."
                  rows={12}
                  style={{ fontFamily: 'SF Mono, Monaco, Inconsolata, monospace', fontSize: '14px' }}
                />
              </div>
            )}

            <div className="btn-group">
              <button className="btn" onClick={submitResponse} disabled={loading}>
                Submit Response →
              </button>
              <button className="btn btn-secondary" onClick={submitSession}>
                Finish Test
              </button>
            </div>
          </div>
        )}

        {/* Score Report - Show immediately when available */}
        {report && (
          <>
            <div className="score-display" style={{ marginTop: '24px' }}>
              <div className="score-main">{report.overallScore}</div>
              <div className="score-label">Overall Score</div>
              
              <div className="divider"></div>
              
              <div className="score-breakdown">
                <div className="score-item">
                  <span className="score-item-value">{report.subscores.algorithms}</span>
                  <span className="score-item-label">Algorithms</span>
                </div>
                <div className="score-item">
                  <span className="score-item-value">{report.subscores.data_structures}</span>
                  <span className="score-item-label">Data Structures</span>
                </div>
                <div className="score-item">
                  <span className="score-item-value">{report.subscores.code_quality}</span>
                  <span className="score-item-label">Code Quality</span>
                </div>
              </div>

              <p style={{ marginTop: '16px', fontSize: '17px', color: 'var(--color-text-secondary)' }}>
                Percentile: <strong>{report.percentile}th</strong>
              </p>
            </div>

            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Performance Analysis</h3>
              </div>

              {report.strengths && report.strengths.length > 0 && (
                <div style={{ marginBottom: '16px' }}>
                  <p style={{ fontWeight: 600, marginBottom: '8px' }}>✨ Strengths</p>
                  <div className="tag-list">
                    {report.strengths.map((strength) => (
                      <span key={strength} className="tag tag-success">{strength}</span>
                    ))}
                  </div>
                </div>
              )}

              {report.weaknesses && report.weaknesses.length > 0 && (
                <div>
                  <p style={{ fontWeight: 600, marginBottom: '8px' }}>📈 Areas for Improvement</p>
                  <div className="tag-list">
                    {report.weaknesses.map((weakness) => (
                      <span key={weakness} className="tag tag-warning">{weakness}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Share With Employers</h3>
              </div>
              <p className="text-muted">Share your score with employers to apply for jobs</p>
              
              <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
                <input
                  className="form-input"
                  value={shareEmployerId}
                  onChange={(e) => setShareEmployerId(e.target.value)}
                  placeholder="Enter Employer ID"
                  style={{ flex: 1 }}
                />
                <button className="btn" onClick={shareWithEmployer}>
                  Share
                </button>
              </div>
            </div>

            <div className="card">
              <div className="card-header">
                <h3 className="card-title">What's Next?</h3>
              </div>
              
              <div className="btn-group">
                <button className="btn" onClick={takeAnotherTest}>
                  📝 Take Another Test
                </button>
                <button className="btn btn-secondary" onClick={fetchMatches}>
                  🔍 Find Matching Jobs
                </button>
              </div>

              {matches.length > 0 && (
                <div style={{ marginTop: '24px' }}>
                  {matches.map((match) => (
                    <div key={match.jobId} style={{
                      padding: '16px',
                      background: 'var(--color-surface)',
                      borderRadius: 'var(--radius-sm)',
                      marginBottom: '12px'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <p style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>
                            {match.company}
                          </p>
                          <p className="text-muted" style={{ fontSize: '15px' }}>
                            Job ID: {match.jobId}
                          </p>
                        </div>
                        <div className="badge badge-accent">
                          {match.matchScore}% Match
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </main>
  )
}

export default CandidateDashboard

