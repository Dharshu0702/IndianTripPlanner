import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import api from '../api/axios'
import {
  HiOutlineMapPin, HiOutlineCurrencyRupee, HiOutlineCalendarDays,
  HiOutlineBuildingOffice2, HiOutlineSparkles,
  HiOutlineChevronDown, HiOutlineMap, HiOutlineArrowRight,
} from 'react-icons/hi2'
import '../styles/results.css'

const PLAN_THEMES = {
  'Budget Plan': { color: '#059669', gradient: 'linear-gradient(135deg, #059669, #10B981)', badge: 'badge-budget', icon: '💰' },
  'Balanced Plan': { color: '#4F46E5', gradient: 'linear-gradient(135deg, #4F46E5, #7C3AED)', badge: 'badge-balanced', icon: '⚖️' },
  'Luxury Plan': { color: '#F97316', gradient: 'linear-gradient(135deg, #F97316, #EF4444)', badge: 'badge-luxury', icon: '👑' },
}

export default function TripResults() {
  const { tripId } = useParams()
  const navigate = useNavigate()
  const [trip, setTrip] = useState(null)
  const [loading, setLoading] = useState(true)
  const [expandedPlan, setExpandedPlan] = useState(null)

  useEffect(() => {
    api.get(`/trips/${tripId}`)
      .then(r => { setTrip(r.data.trip); setLoading(false) })
      .catch(() => { toast.error('Failed to load trip'); setLoading(false) })
  }, [tripId])

  const handleDownloadPDF = async (planIndex) => {
    try {
      const res = await api.get(`/pdf/trip/${tripId}/${planIndex}`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `TripPlan_${trip.destination.place}_${planIndex}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      toast.success('PDF downloaded!')
    } catch {
      toast.error('Failed to download PDF')
    }
  }

  if (loading) return <div className="spinner-overlay"><div className="spinner"></div><p className="spinner-text">Loading your plans...</p></div>
  if (!trip) return <div className="page-wrapper"><div className="container"><p>Trip not found.</p></div></div>

  const plans = trip.generated_plans || []

  return (
    <div className="page-wrapper">
      <div className="container">
        <div className="results-header animate-fadeInUp">
          <h1>Your AI-Generated <span className="gradient-text">Travel Plans</span></h1>
          <div className="trip-summary-bar">
            <span><HiOutlineMapPin /> {trip.origin_location?.address?.split(',')[0] || 'Origin'}</span>
            <HiOutlineArrowRight />
            <span className="dest-highlight">{trip.destination.place}, {trip.destination.state}</span>
            <span className="summary-divider">|</span>
            <span>{trip.distance_km?.toFixed(0)} km</span>
            <span className="summary-divider">|</span>
            <span>{trip.inputs.travelers} travelers</span>
            <span className="summary-divider">|</span>
            <span>{trip.inputs.days} days</span>
          </div>
        </div>

        <div className="plans-grid stagger-children">
          {plans.map((plan, idx) => {
            const theme = PLAN_THEMES[plan.plan_name] || PLAN_THEMES['Balanced Plan']
            const isExpanded = expandedPlan === idx
            return (
              <div key={idx} className={`plan-card glass-card animate-fadeInUp ${isExpanded ? 'expanded' : ''}`}>
                <div className="plan-card-header" style={{ background: theme.gradient }}>
                  <span className="plan-icon">{theme.icon}</span>
                  <h2>{plan.plan_name}</h2>
                  <div className="plan-total">₹{(plan.total_cost || 0).toLocaleString('en-IN')}</div>
                </div>

                <div className="plan-card-body">
                  <div className="plan-detail-row">
                    <span>🚌</span>
                    <span className="detail-label">Travel</span>
                    <span className="detail-value">{plan.travel_mode}{plan.travel_time ? ` (${plan.travel_time})` : ''} — ₹{(plan.travel_cost || 0).toLocaleString('en-IN')}</span>
                  </div>
                  <div className="plan-detail-row">
                    <HiOutlineBuildingOffice2 />
                    <span className="detail-label">Hotel</span>
                    <span className="detail-value">{plan.hotel_name} — ₹{(plan.hotel_cost_per_night || 0).toLocaleString('en-IN')}/night</span>
                  </div>
                  <div className="plan-detail-row">
                    <HiOutlineCurrencyRupee />
                    <span className="detail-label">Food</span>
                    <span className="detail-value">₹{(plan.food_cost_per_day || 0).toLocaleString('en-IN')}/day</span>
                  </div>
                  <div className="plan-detail-row">
                    <HiOutlineMapPin />
                    <span className="detail-label">Local Transport</span>
                    <span className="detail-value">₹{(plan.local_transport_per_day || 0).toLocaleString('en-IN')}/day</span>
                  </div>

                  {plan.cab_info && (
                    <div className="cab-notice">🚕 {plan.cab_info.note}</div>
                  )}

                  {plan.places_to_visit && plan.places_to_visit.length > 0 && (
                    <div className="plan-places">
                      <h4><HiOutlineMap /> Places to Visit</h4>
                      <div className="places-tags">
                        {plan.places_to_visit.map((p, i) => <span key={i} className="place-tag">{p}</span>)}
                      </div>
                    </div>
                  )}

                  <button className="expand-toggle" onClick={() => setExpandedPlan(isExpanded ? null : idx)}>
                    <HiOutlineChevronDown className={isExpanded ? 'rotated' : ''} />
                    {isExpanded ? 'Hide Itinerary' : 'Show Day-wise Itinerary'}
                  </button>

                  {isExpanded && plan.day_wise_itinerary && (
                    <div className="itinerary-section animate-fadeIn">
                      {plan.day_wise_itinerary.map((day, di) => (
                        <div key={di} className="itinerary-day">
                          <div className="day-marker">
                            <div className="day-dot"></div>
                            {di < plan.day_wise_itinerary.length - 1 && <div className="day-line"></div>}
                          </div>
                          <div className="day-content">
                            <h5><HiOutlineCalendarDays /> Day {day.day}: {day.title}</h5>
                            <ul>
                              {(day.activities || []).map((act, ai) => <li key={ai}>{act}</li>)}
                            </ul>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="plan-actions">
                    <button className="btn btn-primary" onClick={() => navigate(`/customize/${tripId}/${idx}`)}>
                      <HiOutlineSparkles /> Select & Customize
                    </button>
                    <button className="btn btn-outline btn-sm" onClick={() => handleDownloadPDF(idx)}>
                      📄 PDF
                    </button>
                    {plan.maps_link && (
                      <a href={plan.maps_link} target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-sm">
                        🗺️ Map
                      </a>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
