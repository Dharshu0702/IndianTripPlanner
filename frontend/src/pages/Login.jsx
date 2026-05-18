import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { toast } from 'react-toastify'
import { HiOutlineEnvelope, HiOutlineLockClosed, HiOutlineEye, HiOutlineEyeSlash } from 'react-icons/hi2'
import '../styles/auth.css'

export default function Login() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email || !password) return toast.error('Please fill all fields')
    setLoading(true)
    try {
      await login(email, password)
      toast.success('Welcome back! 🎉')
    } catch (err) {
      toast.error(err.response?.data?.error || 'Login failed')
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
          <div className="auth-logo">✈️</div>
          <h1>Welcome Back</h1>
          <p>Sign in to India Smart Trip Planner</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
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
                id="login-email"
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
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                id="login-password"
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

          <button type="submit" className="btn btn-primary btn-block btn-lg" disabled={loading} id="login-submit">
            {loading ? <span className="btn-spinner"></span> : 'Sign In'}
          </button>
        </form>

        <div className="auth-footer">
          <p>Don't have an account? <Link to="/signup">Create one</Link></p>
        </div>
      </div>
    </div>
  )
}
