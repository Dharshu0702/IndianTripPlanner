import { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../api/axios'
import {
  HiOutlineMapPin, HiOutlineCalendarDays,
  HiOutlineArrowDownTray, HiOutlineClock,
} from 'react-icons/hi2'
import '../styles/bookings.css'

export default function MyBookings() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/bookings/my-bookings')
      .then(r => { setBookings(r.data.bookings); setLoading(false) })
      .catch(() => { toast.error('Failed to load bookings'); setLoading(false) })
  }, [])

  const handleDownloadPDF = async (bookingId) => {
    try {
      const res = await api.get(`/pdf/booking/${bookingId}`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `Booking_${bookingId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      toast.success('PDF downloaded!')
    } catch {
      toast.error('Failed to download PDF')
    }
  }

  if (loading) return <div className="spinner-overlay"><div className="spinner"></div></div>

  return (
    <div className="page-wrapper">
      <div className="container">
        <div className="bookings-header animate-fadeInUp">
          <h1>My <span className="gradient-text">Bookings</span></h1>
          <p>Track your trip booking requests</p>
        </div>

        {bookings.length === 0 ? (
          <div className="empty-state animate-fadeIn">
            <div className="empty-icon">🧳</div>
            <h3>No bookings yet</h3>
            <p>Plan a trip and submit a booking to see it here.</p>
          </div>
        ) : (
          <div className="bookings-list stagger-children">
            {bookings.map(b => {
              const dest = b.trip?.destination || {}
              const plan = b.selected_plan || {}
              const statusClass = `badge-${b.status}`
              return (
                <div key={b.id} className="booking-card glass-card animate-fadeInUp">
                  <div className="booking-card-left">
                    <div className="booking-dest">
                      <h3><HiOutlineMapPin /> {dest.place || 'N/A'}, {dest.state || ''}</h3>
                      <span className={`badge ${statusClass}`}>{b.status}</span>
                    </div>
                    <div className="booking-meta">
                      <span><HiOutlineCalendarDays /> {b.trip?.inputs?.days || '?'} days</span>
                      <span>👥 {b.trip?.inputs?.travelers || '?'} travelers</span>
                      <span>🏷️ {plan.plan_name || 'N/A'}</span>
                    </div>
                    <div className="booking-cost">
                      <span>₹</span>
                      <span className="cost-amount">{(plan.total_cost || 0).toLocaleString('en-IN')}</span>
                    </div>
                    {b.admin_notes && (
                      <div className="admin-notes">
                        <strong>Admin:</strong> {b.admin_notes}
                      </div>
                    )}
                    <div className="booking-time">
                      <HiOutlineClock /> {new Date(b.created_at).toLocaleDateString('en-IN', { day:'numeric', month:'short', year:'numeric' })}
                    </div>
                  </div>
                  <div className="booking-card-right">
                    {b.status === 'approved' && (
                      <button className="btn btn-primary" onClick={() => handleDownloadPDF(b.id)}>
                        <HiOutlineArrowDownTray /> Download PDF
                      </button>
                    )}
                    {b.status === 'pending' && <p className="pending-note">⏳ Awaiting admin approval</p>}
                    {b.status === 'rejected' && <p className="rejected-note">❌ Booking was rejected</p>}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
