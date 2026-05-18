import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Signup from './pages/Signup'
import TripPlanner from './pages/TripPlanner'
import TripResults from './pages/TripResults'
import PlanCustomize from './pages/PlanCustomize'
import MyBookings from './pages/MyBookings'
import AdminDashboard from './pages/AdminDashboard'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="spinner-overlay"><div className="spinner"></div></div>
  if (!user) return <Navigate to="/login" replace />
  return children
}

function AdminRoute({ children }) {
  const { user, isAdmin, loading } = useAuth()
  if (loading) return <div className="spinner-overlay"><div className="spinner"></div></div>
  if (!user) return <Navigate to="/login" replace />
  if (!isAdmin) return <Navigate to="/planner" replace />
  return children
}

function GuestRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="spinner-overlay"><div className="spinner"></div></div>
  if (user) return <Navigate to="/planner" replace />
  return children
}

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/planner" replace />} />
        <Route path="/login" element={<GuestRoute><Login /></GuestRoute>} />
        <Route path="/signup" element={<GuestRoute><Signup /></GuestRoute>} />
        <Route path="/planner" element={<ProtectedRoute><TripPlanner /></ProtectedRoute>} />
        <Route path="/results/:tripId" element={<ProtectedRoute><TripResults /></ProtectedRoute>} />
        <Route path="/customize/:tripId/:planIndex" element={<ProtectedRoute><PlanCustomize /></ProtectedRoute>} />
        <Route path="/bookings" element={<ProtectedRoute><MyBookings /></ProtectedRoute>} />
        <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
        <Route path="*" element={<Navigate to="/planner" replace />} />
      </Routes>
    </>
  )
}
