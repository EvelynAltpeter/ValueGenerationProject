/**
 * Employer Dashboard - Job Management & Candidate Filtering
 * R-PRIV-01: Only shows candidates who have explicitly shared
 * R-UX-01: Score thresholds and match explanations are explicit
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

function EmployerDashboard() {
  const navigate = useNavigate()
  const [employerId, setEmployerId] = useState(null)
  const [employerName, setEmployerName] = useState('')
  const [jobConfig, setJobConfig] = useState({
    jobId: '',
    trackId: 'python_core_v1',
    minScore: 70
  })
  const [jobs, setJobs] = useState([])
  const [selectedJob, setSelectedJob] = useState(null)
  const [eligible, setEligible] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [statusMsg, setStatusMsg] = useState('')

  useEffect(() => {
    const storedId = localStorage.getItem('employerId')
    const storedName = localStorage.getItem('employerName')
    
    if (!storedId) {
      navigate('/employer')
    } else {
      setEmployerId(storedId)
      setEmployerName(storedName || 'Employer')
    }
  }, [navigate])

  async function createJob(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      const requirement = {
        jobId: jobConfig.jobId,
        employerId: employerId,
        requiredTracks: [jobConfig.trackId],
        minScores: { [jobConfig.trackId]: Number(jobConfig.minScore) },
      }
      
      await fetch(`${API_BASE}/api/employers/${employerId}/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requirement),
      })
      
      setStatusMsg('✓ Job requirements saved successfully!')
      setJobs([...jobs, requirement])
      setJobConfig({ jobId: '', trackId: 'python_core_v1', minScore: 70 })
    } catch (err) {
      setError('Unable to save job requirements.')
    } finally {
      setLoading(false)
    }
  }

  async function loadEligible(jobId) {
    setLoading(true)
    setError('')
    setSelectedJob(jobId)
    
    try {
      const res = await fetch(
        `${API_BASE}/api/employers/${employerId}/jobs/${jobId}/eligible`
      )
      const data = await res.json()
      setEligible(data.data.eligibleCandidates ?? [])
      setStatusMsg(`Found ${data.data.eligibleCandidates?.length ?? 0} eligible candidates`)
    } catch (err) {
      setError('Unable to fetch eligible candidates.')
    } finally {
      setLoading(false)
    }
  }

  function getScoreColor(score) {
    if (score >= 85) return 'var(--color-success)'
    if (score >= 70) return 'var(--color-accent)'
    return 'var(--color-warning)'
  }

  if (!employerId) return null

  return (
    <main className="main-content">
      <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ marginBottom: '32px' }}>
          <h1>{employerName}</h1>
          <p className="text-muted">Employer Dashboard</p>
          <div className="badge" style={{ marginTop: '8px' }}>
            Employer ID: {employerId}
          </div>
        </div>

        {/* Status Messages */}
        {statusMsg && (
          <div className="status-message status-success">{statusMsg}</div>
        )}
        {error && (
          <div className="status-message status-error">{error}</div>
        )}

        {/* Create Job */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Create Job Requirement</h3>
          </div>
          <p className="text-muted">
            Define skill requirements and minimum score thresholds for your open positions
          </p>

          <form onSubmit={createJob} style={{ marginTop: '24px' }}>
            <div className="form-group">
              <label className="form-label">Job ID / Title</label>
              <input
                className="form-input"
                type="text"
                value={jobConfig.jobId}
                onChange={(e) => setJobConfig({ ...jobConfig, jobId: e.target.value })}
                placeholder="e.g., backend-engineer-001"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Required Skill Track</label>
              <select
                className="form-select"
                value={jobConfig.trackId}
                onChange={(e) => setJobConfig({ ...jobConfig, trackId: e.target.value })}
              >
                <option value="python_core_v1">Python Core</option>
                <option value="sql_core_v1">SQL Core</option>
                <option value="javascript_core_v1">JavaScript Core</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">
                Minimum Score Threshold (0-100)
              </label>
              <input
                className="form-input"
                type="number"
                value={jobConfig.minScore}
                onChange={(e) => setJobConfig({ ...jobConfig, minScore: e.target.value })}
                min="0"
                max="100"
                required
              />
              <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', marginTop: '8px' }}>
                Only candidates with scores at or above this threshold will appear as eligible
              </p>
            </div>

            <button 
              type="submit" 
              className="btn" 
              disabled={loading || !jobConfig.jobId}
            >
              Create Job Requirement
            </button>
          </form>
        </div>

        {/* Job List */}
        {jobs.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Your Job Requirements</h3>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {jobs.map((job) => (
                <div
                  key={job.jobId}
                  style={{
                    padding: '16px',
                    background: 'var(--color-surface)',
                    borderRadius: 'var(--radius-sm)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}
                >
                  <div>
                    <p style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>
                      {job.jobId}
                    </p>
                    <p className="text-muted" style={{ fontSize: '15px' }}>
                      {job.requiredTracks[0]} • Min Score: {job.minScores[job.requiredTracks[0]]}
                    </p>
                  </div>
                  <button 
                    className="btn btn-secondary btn-small"
                    onClick={() => loadEligible(job.jobId)}
                  >
                    View Candidates
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Candidate Sharing Instructions */}
        <div className="card" style={{ background: 'var(--color-surface)' }}>
          <h4 style={{ marginBottom: '12px' }}>📋 How to Access Candidates</h4>
          <p style={{ fontSize: '15px', color: 'var(--color-text-secondary)' }}>
            Candidates must explicitly share their scores with you. Share your <strong>Employer ID</strong> ({employerId}) 
            with candidates so they can grant you access to their proficiency scores.
          </p>
          <p style={{ fontSize: '15px', color: 'var(--color-text-secondary)', marginTop: '12px' }}>
            This ensures <strong>R-PRIV-01 compliance</strong> – no candidate data is visible without explicit consent.
          </p>
        </div>

        {/* Eligible Candidates */}
        {selectedJob && eligible.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Eligible Candidates for {selectedJob}</h3>
            </div>

            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Candidate Name</th>
                    <th>Score</th>
                    <th>Match Quality</th>
                    <th>Details</th>
                  </tr>
                </thead>
                <tbody>
                  {eligible.map((candidate) => {
                    const score = candidate.trackScores[Object.keys(candidate.trackScores)[0]]
                    return (
                      <tr key={candidate.candidateId}>
                        <td>
                          <div>
                            <p style={{ fontWeight: 600 }}>{candidate.name}</p>
                            <p className="text-muted" style={{ fontSize: '13px' }}>
                              ID: {candidate.candidateId}
                            </p>
                          </div>
                        </td>
                        <td>
                          <span style={{ 
                            fontSize: '20px', 
                            fontWeight: 600,
                            color: getScoreColor(score)
                          }}>
                            {score}
                          </span>
                        </td>
                        <td>
                          <div className="badge badge-accent">
                            {candidate.matchScore}% Match
                          </div>
                        </td>
                        <td>
                          <p className="text-muted" style={{ fontSize: '13px' }}>
                            {candidate.matchExplanation}
                          </p>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {selectedJob && eligible.length === 0 && !loading && (
          <div className="card">
            <p className="text-center text-muted">
              No eligible candidates have shared their scores with you yet.
              <br />
              Share your Employer ID with candidates to grant access.
            </p>
          </div>
        )}
      </div>
    </main>
  )
}

export default EmployerDashboard

