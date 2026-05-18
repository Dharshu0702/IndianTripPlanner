import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { toast } from 'react-toastify'
import { HiOutlineUser, HiOutlineEnvelope, HiOutlineLockClosed, HiOutlineEye, HiOutlineEyeSlash } from 'react-icons/hi2'
import '../styles/auth.css'

export default function Signup() {
  const { signup } = useAuth()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name || !email || !password) return toast.error('Please fill all fields')
    if (password.length < 6) return toast.error('Password must be at least 6 characters')
    setLoading(true)
    try {
      await signup(name, email, password)
      toast.success('Account created! 🎉')
    } catch (err) {
      toast.error(err.response?.data?.error || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-bg-decoration">
        <div className="deco-circle deco-1"></div>
        <div className="deco-circle deco-2"></div>
        <div className="deco-circle deco-3"></div>
      </div>

      <div className="auth-card glass-card animate-scaleIn">
        <div className="auth-header">
          <div className="auth-logo">🌏</div>
          <h1>Create Account</h1>
          <p>Start planning your dream trip across India</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <div className="input-icon-wrapper">
              <HiOutlineUser className="input-icon" />
              <input
                type="text"
                className="form-input"
                placeholder="Your full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                id="signup-name"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Email</label>
            <div className="input-icon-wrapper">
              <HiOutlineEnvelope className="input-icon" />
              <input
                type="email"
                className="form-input"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                id="signup-email"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div className="input-icon-wrapper">
              <HiOutlineLockClosed className="input-icon" />
              <input
                type={showPass ? 'text' : 'password'}
                className="form-input"
                placeholder="Min 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                id="signup-password"
              />
              <button
                type="button"
                className="input-toggle"
                onClick={() => setShowPass(!showPass)}
              >
                {showPass ? <HiOutlineEyeSlash /> : <HiOutlineEye />}
              </button>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-block btn-lg" disabled={loading} id="signup-submit">
            {loading ? <span className="btn-spinner"></span> : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account? <Link to="/login">Sign in</Link></p>
        </div>
      </div>
    </div>
  )
}
