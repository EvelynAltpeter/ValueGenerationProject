/**
 * Candidate Authentication & Registration
 * R-UX-01: Clear, simple sign-up flow
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

function CandidateAuth() {
  const navigate = useNavigate()
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    github: '',
    educationLevel: "Bachelor's",
    graduationYear: 2025
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSignUp(e) {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_BASE}/api/candidates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      })

      if (!res.ok) {
        throw new Error('Registration failed')
      }

      const data = await res.json()
      
      // Store candidate ID in localStorage
      localStorage.setItem('candidateId', data.data.candidateId)
      localStorage.setItem('candidateName', profile.name)
      
      // Navigate to dashboard
      navigate('/candidate/dashboard')
    } catch (err) {
      setError('Unable to create profile. Please check your connection and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="main-content">
      <div style={{ maxWidth: '500px', margin: '0 auto' }}>
        <div className="hero" style={{ padding: '32px 0' }}>
          <h2>Create Your Profile</h2>
          <p>Start your journey to standardized technical certification</p>
        </div>

        {error && (
          <div className="status-message status-error">{error}</div>
        )}

        <div className="card">
          <form onSubmit={handleSignUp}>
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input
                className="form-input"
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                placeholder="Jane Doe"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                className="form-input"
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                placeholder="jane@example.com"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">GitHub Profile (Optional)</label>
              <input
                className="form-input"
                type="text"
                value={profile.github}
                onChange={(e) => setProfile({ ...profile, github: e.target.value })}
                placeholder="github.com/janedoe"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Education Level</label>
              <select
                className="form-select"
                value={profile.educationLevel}
                onChange={(e) => setProfile({ ...profile, educationLevel: e.target.value })}
              >
                <option value="Bachelor's">Bachelor's Degree</option>
                <option value="Master's">Master's Degree</option>
                <option value="Bootcamp">Coding Bootcamp</option>
                <option value="Self-taught">Self-taught</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Graduation Year</label>
              <input
                className="form-input"
                type="number"
                value={profile.graduationYear}
                onChange={(e) => setProfile({ ...profile, graduationYear: parseInt(e.target.value) })}
                min="2020"
                max="2030"
              />
            </div>

            <div className="btn-group">
              <button 
                type="submit" 
                className="btn btn-large" 
                disabled={loading || !profile.name || !profile.email}
                style={{ width: '100%' }}
              >
                {loading ? 'Creating Profile...' : 'Create Profile & Continue'}
              </button>
            </div>
          </form>
        </div>

        <p className="text-center text-muted" style={{ marginTop: '24px', fontSize: '15px' }}>
          Already have a profile? Enter your email above to continue.
        </p>
      </div>
    </main>
  )
}

export default CandidateAuth

