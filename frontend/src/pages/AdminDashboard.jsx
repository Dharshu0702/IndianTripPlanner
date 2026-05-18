import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../api/axios'
import {
  HiOutlinePresentationChartBar, HiOutlineUserGroup, HiOutlineMapPin,
  HiOutlineCheckCircle, HiOutlineXMark, HiOutlineClock,
} from 'react-icons/hi2'
import '../styles/admin.css'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(null)
  const [filter, setFilter] = useState('all')
  const [notes, setNotes] = useState({})

  useEffect(() => {
    Promise.all([
      api.get('/admin/stats'),
      api.get('/admin/bookings'),
    ])
      .then(([statsRes, bookingsRes]) => {
        setStats(statsRes.data.stats)
        setBookings(bookingsRes.data.bookings)
        setLoading(false)
      })
      .catch(() => { toast.error('Failed to load admin data'); setLoading(false) })
  }, [])

  const handleStatusUpdate = async (bookingId, status) => {
    setActionLoading(bookingId)
    try {
      await api.patch(`/admin/bookings/${bookingId}/status`, {
        status,
        admin_notes: notes[bookingId] || '',
      })
      toast.success(`Booking ${status}!`)
      // Refresh
      setBookings(bookings.map(b =>
        b.id === bookingId ? { ...b, status, admin_notes: notes[bookingId] || '' } : b
      ))
      setStats(prev => ({
        ...prev,
        pending_bookings: prev.pending_bookings - 1,
        [status === 'approved' ? 'approved_bookings' : 'rejected_bookings']:
          prev[status === 'approved' ? 'approved_bookings' : 'rejected_bookings'] + 1,
      }))
    } catch {
      toast.error('Failed to update booking')
    } finally {
      setActionLoading(null)
    }
  }

  const handleClearCache = async () => {
    if (!window.confirm('Clear AI plan cache? Users will get fresh plans next time.')) return
    try {
      await api.delete('/admin/cache/clear')
      toast.success('AI cache cleared — fresh plans will generate next trip')
    } catch {
      toast.error('Failed to clear cache')
    }
  }

  const filteredBookings = filter === 'all'
    ? bookings
    : bookings.filter(b => b.status === filter)

  if (loading) return <div className="spinner-overlay"><div className="spinner"></div></div>

  return (
    <div className="page-wrapper">
      <div className="container">
        <div className="admin-header animate-fadeInUp">
          <h1><HiOutlinePresentationChartBar /> Admin <span className="gradient-text">Dashboard</span></h1>
          <button className="btn btn-outline btn-sm" onClick={handleClearCache} title="Clear stale AI plan cache">
            🗑️ Clear AI Cache
          </button>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="stats-grid stagger-children">
            <div className="stat-card animate-fadeInUp">
              <div className="stat-value">{stats.total_users}</div>
              <div className="stat-label"><HiOutlineUserGroup /> Users</div>
            </div>
            <div className="stat-card animate-fadeInUp">
              <div className="stat-value">{stats.total_trips}</div>
              <div className="stat-label"><HiOutlineMapPin /> Trips</div>
            </div>
            <div className="stat-card animate-fadeInUp">
              <div className="stat-value">{stats.pending_bookings}</div>
              <div className="stat-label"><HiOutlineClock /> Pending</div>
            </div>
            <div className="stat-card animate-fadeInUp" style={{borderColor: 'var(--success)'}}>
              <div className="stat-value" style={{background: 'var(--gradient-success)', WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent'}}>{stats.approved_bookings}</div>
              <div className="stat-label"><HiOutlineCheckCircle /> Approved</div>
            </div>
            <div className="stat-card animate-fadeInUp" style={{borderColor: 'var(--error)'}}>
              <div className="stat-value" style={{background: 'var(--gradient-accent)', WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent'}}>{stats.rejected_bookings}</div>
              <div className="stat-label"><HiOutlineXMark /> Rejected</div>
            </div>
          </div>
        )}

        {/* Filter */}
        <div className="admin-filter animate-fadeInUp">
          {['all', 'pending', 'approved', 'rejected'].map(f => (
            <button
              key={f}
              className={`filter-btn ${filter === f ? 'active' : ''}`}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
              {f !== 'all' && <span className="filter-count">
                {bookings.filter(b => b.status === f).length}
              </span>}
            </button>
          ))}
        </div>

        {/* Bookings Table */}
        <div className="admin-bookings animate-fadeInUp">
          {filteredBookings.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📋</div>
              <h3>No {filter !== 'all' ? filter : ''} bookings</h3>
            </div>
          ) : (
            <div className="admin-table-wrapper">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Destination</th>
                    <th>Plan</th>
                    <th>Cost</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredBookings.map(b => (
                    <tr key={b.id}>
                      <td>
                        <div className="user-cell">
                          <strong>{b.user?.name || 'N/A'}</strong>
                          <small>{b.user?.email || ''}</small>
                        </div>
                      </td>
                      <td>
                        <div className="dest-cell">
                          <strong>{b.trip?.destination?.place || 'N/A'}</strong>
                          <small>{b.trip?.destination?.state || ''}</small>
                        </div>
                      </td>
                      <td>{b.selected_plan?.plan_name || 'N/A'}</td>
                      <td className="cost-cell">₹{(b.selected_plan?.total_cost || 0).toLocaleString('en-IN')}</td>
                      <td><span className={`badge badge-${b.status}`}>{b.status}</span></td>
                      <td>
                        {b.status === 'pending' ? (
                          <div className="action-cell">
                            <input
                              className="admin-notes-input"
                              placeholder="Notes (optional)"
                              value={notes[b.id] || ''}
                              onChange={(e) => setNotes({...notes, [b.id]: e.target.value})}
                            />
                            <div className="action-btns">
                              <button
                                className="btn btn-success btn-sm"
                                disabled={actionLoading === b.id}
                                onClick={() => handleStatusUpdate(b.id, 'approved')}
                              >
                                {actionLoading === b.id ? '...' : '✅ Approve'}
                              </button>
                              <button
                                className="btn btn-danger btn-sm"
                                disabled={actionLoading === b.id}
                                onClick={() => handleStatusUpdate(b.id, 'rejected')}
                              >
                                {actionLoading === b.id ? '...' : '❌ Reject'}
                              </button>
                            </div>
                          </div>
                        ) : (
                          <span className="action-done">—</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
