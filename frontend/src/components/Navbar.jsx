import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { HiOutlineMap, HiOutlineBookOpen, HiOutlineShieldCheck, HiOutlineArrowRightOnRectangle, HiOutlineUser } from 'react-icons/hi2'
import './Navbar.css'

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!user) return null

  return (
    <nav className="navbar">
      <div className="navbar-inner container">
        <Link to="/planner" className="navbar-brand">
          <span className="brand-icon">✈️</span>
          <span className="brand-text">
            <span className="brand-highlight">India</span> Smart Trip
          </span>
        </Link>

        <div className="navbar-links">
          <Link
            to="/planner"
            className={`nav-link ${location.pathname === '/planner' ? 'active' : ''}`}
          >
            <HiOutlineMap /> Plan Trip
          </Link>
          <Link
            to="/bookings"
            className={`nav-link ${location.pathname === '/bookings' ? 'active' : ''}`}
          >
            <HiOutlineBookOpen /> My Bookings
          </Link>
          {isAdmin && (
            <Link
              to="/admin"
              className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}
            >
              <HiOutlineShieldCheck /> Admin
            </Link>
          )}
        </div>

        <div className="navbar-user">
          <div className="user-badge">
            <HiOutlineUser />
            <span>{user.name}</span>
            {isAdmin && <span className="role-badge">Admin</span>}
          </div>
          <button onClick={handleLogout} className="logout-btn" title="Logout">
            <HiOutlineArrowRightOnRectangle />
          </button>
        </div>
      </div>
    </nav>
  )
}
