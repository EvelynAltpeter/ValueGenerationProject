/**
 * VGP Platform - Apple-Style Minimalist UI
 * R-UX-01: Clear, intuitive navigation with separate flows for candidates and employers
 */

import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import LandingPage from './pages/LandingPage'
import CandidateAuth from './pages/CandidateAuth'
import CandidateDashboard from './pages/CandidateDashboard'
import EmployerAuth from './pages/EmployerAuth'
import EmployerDashboard from './pages/EmployerDashboard'

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <nav className="navbar">
          <div className="navbar-content">
            <Link to="/" className="logo">
              VGP Platform
            </Link>
            <div className="nav-links">
              <Link to="/candidate" className="nav-link">For Candidates</Link>
              <Link to="/employer" className="nav-link">For Employers</Link>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/candidate" element={<CandidateAuth />} />
          <Route path="/candidate/dashboard" element={<CandidateDashboard />} />
          <Route path="/employer" element={<EmployerAuth />} />
          <Route path="/employer/dashboard" element={<EmployerDashboard />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
