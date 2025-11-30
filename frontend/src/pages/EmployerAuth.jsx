/**
 * Employer Authentication & Registration
 * R-UX-01: Clear, simple sign-up flow for employers
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

function EmployerAuth() {
  const navigate = useNavigate()
  const [companyName, setCompanyName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSignUp(e) {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_BASE}/api/employers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: companyName }),
      })

      if (!res.ok) {
        throw new Error('Registration failed')
      }

      const data = await res.json()
      
      // Store employer ID in localStorage
      localStorage.setItem('employerId', data.data.employerId)
      localStorage.setItem('employerName', companyName)
      
      // Navigate to dashboard
      navigate('/employer/dashboard')
    } catch (err) {
      setError('Unable to create employer account. Please check your connection and try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="main-content">
      <div style={{ maxWidth: '500px', margin: '0 auto' }}>
        <div className="hero" style={{ padding: '32px 0' }}>
          <h2>Create Employer Account</h2>
          <p>Get access to pre-screened technical talent</p>
        </div>

        {error && (
          <div className="status-message status-error">{error}</div>
        )}

        <div className="card">
          <form onSubmit={handleSignUp}>
            <div className="form-group">
              <label className="form-label">Company Name</label>
              <input
                className="form-input"
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="Acme Corp"
                required
              />
            </div>

            <div style={{ 
              padding: '16px', 
              background: 'var(--color-surface)', 
              borderRadius: 'var(--radius-sm)',
              marginBottom: '24px'
            }}>
              <p style={{ fontSize: '15px', color: 'var(--color-text-secondary)' }}>
                <strong>What you'll get:</strong>
              </p>
              <ul style={{ marginTop: '12px', paddingLeft: '24px', color: 'var(--color-text-secondary)', fontSize: '15px' }}>
                <li>Access to verified technical proficiency scores</li>
                <li>Ability to set custom score thresholds</li>
                <li>Filter candidates by skill track and requirements</li>
                <li>Transparent matching criteria and explanations</li>
              </ul>
            </div>

            <div className="btn-group">
              <button 
                type="submit" 
                className="btn btn-large" 
                disabled={loading || !companyName.trim()}
                style={{ width: '100%' }}
              >
                {loading ? 'Creating Account...' : 'Create Account & Continue'}
              </button>
            </div>
          </form>
        </div>

        <p className="text-center text-muted" style={{ marginTop: '24px', fontSize: '15px' }}>
          Already have an account? Enter your company name above to continue.
        </p>
      </div>
    </main>
  )
}

export default EmployerAuth

