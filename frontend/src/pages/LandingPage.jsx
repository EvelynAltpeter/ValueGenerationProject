/**
 * Landing Page - Role Selection
 * Apple-style hero with clear role distinction
 */

import { useNavigate } from 'react-router-dom'

function LandingPage() {
  const navigate = useNavigate()

  return (
    <main className="main-content">
      <div className="hero">
        <h1>Technical Testing, Simplified</h1>
        <p>
          A standardized, adaptive testing platform that allows candidates to test once 
          and apply everywhere. Employers get verified proficiency scores with transparent 
          matching criteria.
        </p>
      </div>

      <div className="role-selection">
        <div className="role-card" onClick={() => navigate('/candidate')}>
          <div className="role-icon">🎓</div>
          <h3>I'm a Candidate</h3>
          <p>Take one standardized test, share your verified score with multiple employers, and get matched with relevant opportunities.</p>
        </div>

        <div className="role-card" onClick={() => navigate('/employer')}>
          <div className="role-icon">🏢</div>
          <h3>I'm an Employer</h3>
          <p>Access pre-screened candidates with standardized proficiency scores, set your requirements, and filter efficiently.</p>
        </div>
      </div>

      <div style={{ marginTop: '64px', textAlign: 'center' }}>
        <div className="card" style={{ maxWidth: '700px', margin: '0 auto' }}>
          <h3>How It Works</h3>
          <div style={{ textAlign: 'left', marginTop: '24px' }}>
            <p><strong>For Candidates:</strong> Create a profile, select your skill track (Python, SQL, JavaScript), take an adaptive test, and receive a comprehensive score report with strengths and areas for improvement.</p>
            <p><strong>For Employers:</strong> Create job requirements with minimum score thresholds, review eligible candidates who have shared their scores with you, and access transparent match explanations.</p>
          </div>
        </div>
      </div>
    </main>
  )
}

export default LandingPage

