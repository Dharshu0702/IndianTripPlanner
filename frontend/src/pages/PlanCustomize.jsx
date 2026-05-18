import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import api from '../api/axios'
import {
  HiOutlineBuildingOffice2, HiOutlineMapPin,
  HiOutlineCheckCircle, HiOutlineTrash,
  HiOutlinePlus, HiOutlineArrowPath,
} from 'react-icons/hi2'
import HotelSelector from '../components/HotelSelector'
import '../styles/customize.css'

const TRANSPORT_OPTIONS = [
  { value: 'bus', label: 'Bus' },
  { value: 'cab', label: 'Cab' },
  { value: 'train', label: 'Train (Sleeper)' },
  { value: 'train_ac', label: 'Train (AC)' },
  { value: 'flight', label: 'Flight' },
]

// Maps plan name to the trip_type the cost engine expects
const PLAN_TO_TRIP_TYPE = {
  'Budget Plan': 'Budget',
  'Balanced Plan': 'Family',
  'Luxury Plan': 'Luxury',
}

export default function PlanCustomize() {
  const { tripId, planIndex } = useParams()
  const navigate = useNavigate()
  const [trip, setTrip] = useState(null)
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  // Customization state
  const [transport, setTransport] = useState('')
  const [hotelName, setHotelName] = useState('')
  const [selectedHotel, setSelectedHotel] = useState(null)
  const [places, setPlaces] = useState([])
  const [newPlace, setNewPlace] = useState('')
  const [recalcCost, setRecalcCost] = useState(null)

  useEffect(() => {
    api.get(`/trips/${tripId}`)
      .then(r => {
        const t = r.data.trip
        setTrip(t)
        const p = t.generated_plans?.[parseInt(planIndex)]
        if (p) {
          setPlan(p)
          setTransport(p.cost_breakdown?.transport_mode_key || 'bus')
          setHotelName(p.hotel_name || '')
          setPlaces(p.places_to_visit || [])
        }
        setLoading(false)
      })
      .catch(() => { toast.error('Failed to load trip'); setLoading(false) })
  }, [tripId, planIndex])

  // When hotel is selected → update hotel name and auto-recalculate
  const handleHotelSelect = async (hotel) => {
    // Deselect if same hotel clicked
    if (selectedHotel?.id === hotel.id) {
      setSelectedHotel(null)
      setHotelName(plan.hotel_name || '')
      return
    }
    setSelectedHotel(hotel)
    setHotelName(hotel.name)
    toast.success(`Hotel selected: ${hotel.name}`)

    // Auto-recalculate with new hotel price
    if (!trip) return
    try {
      const res = await api.post('/trips/recalculate', {
        distance_km: trip.distance_km,
        days: trip.inputs.days,
        travelers: trip.inputs.travelers,
        trip_type: PLAN_TO_TRIP_TYPE[plan.plan_name] || trip.inputs.trip_type,
        transport_mode: transport,
        num_places: places.length,
      })
      const costData = res.data.cost_breakdown
      // Override hotel cost with selected hotel's actual price
      const hotelTotal = hotel.price_per_night * trip.inputs.days
      const newTotal = Math.round(
        costData.travel_cost + hotelTotal + costData.food_total + costData.local_transport_total + (costData.activity_total || 0)
      )
      setRecalcCost({
        ...costData,
        hotel_cost_per_night: hotel.price_per_night,
        hotel_total: hotelTotal,
        total_cost: newTotal,
      })
    } catch {
      // Recalculate manually if API fails
      const baseCost = plan.cost_breakdown || {}
      const hotelTotal = hotel.price_per_night * trip.inputs.days
      const foodTotal = (baseCost.food_total || 0)
      const localTotal = (baseCost.local_transport_total || 0)
      const travelCost = (baseCost.travel_cost || 0)
      setRecalcCost({
        ...baseCost,
        hotel_cost_per_night: hotel.price_per_night,
        hotel_total: hotelTotal,
        total_cost: Math.round(travelCost + hotelTotal + foodTotal + localTotal),
      })
    }
  }

  const handleRecalculate = async () => {
    if (!trip) return
    try {
      const res = await api.post('/trips/recalculate', {
        distance_km: trip.distance_km,
        days: trip.inputs.days,
        travelers: trip.inputs.travelers,
        trip_type: PLAN_TO_TRIP_TYPE[plan.plan_name] || trip.inputs.trip_type,
        transport_mode: transport,
        num_places: places.length,
      })
      const costData = res.data.cost_breakdown
      if (selectedHotel) {
        const hotelTotal = selectedHotel.price_per_night * trip.inputs.days
        const newTotal = Math.round(
          costData.travel_cost + hotelTotal + costData.food_total + costData.local_transport_total + (costData.activity_total || 0)
        )
        setRecalcCost({
          ...costData,
          hotel_cost_per_night: selectedHotel.price_per_night,
          hotel_total: hotelTotal,
          total_cost: newTotal,
        })
      } else {
        setRecalcCost(costData)
      }
      toast.success('Cost recalculated!')
    } catch {
      toast.error('Failed to recalculate')
    }
  }

  const addPlace = () => {
    if (newPlace.trim() && !places.includes(newPlace.trim())) {
      setPlaces([...places, newPlace.trim()])
      setNewPlace('')
    }
  }

  const removePlace = (idx) => setPlaces(places.filter((_, i) => i !== idx))

  const handleBooking = async () => {
    setSubmitting(true)
    try {
      const finalCost = recalcCost || plan.cost_breakdown || {}
      const customizedPlan = {
        ...plan,
        travel_mode: TRANSPORT_OPTIONS.find(o => o.value === transport)?.label || plan.travel_mode,
        hotel_name: hotelName,
        hotel_cost_per_night: selectedHotel?.price_per_night || finalCost.hotel_cost_per_night || plan.hotel_cost_per_night,
        places_to_visit: places,
        total_cost: finalCost.total_cost || plan.total_cost,
        selected_hotel_details: selectedHotel || null,
      }
      if (recalcCost) {
        customizedPlan.travel_cost = recalcCost.travel_cost
        customizedPlan.food_cost_per_day = recalcCost.food_per_person_per_day * trip.inputs.travelers
        customizedPlan.local_transport_per_day = recalcCost.local_transport_per_day
      }

      await api.post('/bookings', {
        trip_id: tripId,
        selected_plan: customizedPlan,
        customizations: {
          transport_changed: transport !== (plan.cost_breakdown?.transport_mode_key || ''),
          hotel_changed: hotelName !== plan.hotel_name,
          hotel_selected: !!selectedHotel,
          places_modified: JSON.stringify(places) !== JSON.stringify(plan.places_to_visit),
        },
      })
      toast.success('Booking request submitted! 🎉')
      navigate('/bookings')
    } catch (err) {
      toast.error(err.response?.data?.error || 'Booking failed')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="spinner-overlay"><div className="spinner"></div></div>
  if (!plan) return <div className="page-wrapper"><div className="container"><p>Plan not found.</p></div></div>

  const displayCost = recalcCost || plan.cost_breakdown || {}
  const days = trip.inputs.days

  return (
    <div className="page-wrapper">
      <div className="container">
        <div className="customize-header animate-fadeInUp">
          <h1>Customize Your <span className="gradient-text">Plan</span></h1>
          <p>{plan.plan_name} — {trip.destination.place}, {trip.destination.state}</p>
        </div>

        <div className="customize-grid">
          {/* Left: Customization Form */}
          <div className="customize-form glass-card animate-fadeInUp">
            <h3>✏️ Customize Options</h3>

            <div className="form-group">
              <label className="form-label">🚌 Transport Mode</label>
              <select className="form-select" value={transport} onChange={(e) => setTransport(e.target.value)}>
                {TRANSPORT_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label"><HiOutlineBuildingOffice2 /> Hotel Name</label>
              <input
                className="form-input"
                value={hotelName}
                onChange={(e) => setHotelName(e.target.value)}
                placeholder="Enter preferred hotel or select below"
              />
            </div>

            {/* Hotel Selector */}
            <HotelSelector
              destination={trip.destination.place}
              planName={plan.plan_name}
              selectedHotel={selectedHotel}
              onHotelSelect={handleHotelSelect}
              days={days}
            />

            <div className="form-group" style={{ marginTop: 20 }}>
              <label className="form-label"><HiOutlineMapPin /> Places to Visit</label>
              <div className="places-list">
                {places.map((p, i) => (
                  <div key={i} className="place-item">
                    <span>{p}</span>
                    <button className="remove-place" onClick={() => removePlace(i)}><HiOutlineTrash /></button>
                  </div>
                ))}
              </div>
              <div className="add-place-row">
                <input
                  className="form-input"
                  value={newPlace}
                  onChange={(e) => setNewPlace(e.target.value)}
                  placeholder="Add a place"
                  onKeyDown={(e) => e.key === 'Enter' && addPlace()}
                />
                <button className="btn btn-outline btn-sm" onClick={addPlace}><HiOutlinePlus /> Add</button>
              </div>
            </div>

            <button className="btn btn-accent btn-block" onClick={handleRecalculate}>
              <HiOutlineArrowPath /> Recalculate Cost
            </button>
          </div>

          {/* Right: Cost Summary */}
          <div className="cost-summary glass-card animate-slideIn">
            <h3>💰 Cost Summary</h3>
            <div className="cost-rows">
              <div className="cost-row">
                <span>Travel (Round Trip)</span>
                <span>₹{(displayCost.travel_cost || plan.travel_cost || 0).toLocaleString('en-IN')}</span>
              </div>
              <div className={`cost-row ${selectedHotel ? 'cost-row-highlight' : ''}`}>
                <span>
                  Hotel ({days} nights)
                  {selectedHotel && <span style={{ fontSize: '0.75rem', color: 'var(--primary-light)', marginLeft: 6 }}>★ {selectedHotel.rating}</span>}
                </span>
                <span>₹{(displayCost.hotel_total || (plan.hotel_cost_per_night || 0) * days).toLocaleString('en-IN')}</span>
              </div>
              <div className="cost-row">
                <span>Food ({days} days)</span>
                <span>₹{(displayCost.food_total || (plan.food_cost_per_day || 0) * days).toLocaleString('en-IN')}</span>
              </div>
              <div className="cost-row">
                <span>Local Transport</span>
                <span>₹{(displayCost.local_transport_total || (plan.local_transport_per_day || 0) * days).toLocaleString('en-IN')}</span>
              </div>
              {(displayCost.activity_total > 0 || places.length > 0) && (
                <div className="cost-row">
                  <span>Activities ({places.length} places)</span>
                  <span>₹{(displayCost.activity_total || 0).toLocaleString('en-IN')}</span>
                </div>
              )}
              <div className="cost-row total">
                <span>Grand Total</span>
                <span>₹{(displayCost.total_cost || plan.total_cost || 0).toLocaleString('en-IN')}</span>
              </div>
            </div>

            {selectedHotel && (
              <div className="selected-hotel-summary">
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 4 }}>Selected Hotel</div>
                <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{selectedHotel.name}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{selectedHotel.location}</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--primary-light)', marginTop: 4 }}>
                  ₹{selectedHotel.price_per_night?.toLocaleString('en-IN')}/night × {days} nights
                </div>
              </div>
            )}

            {displayCost.cab_info && (
              <div className="cab-notice" style={{ marginTop: '12px' }}>🚕 {displayCost.cab_info.note}</div>
            )}

            <button
              className="btn btn-success btn-block btn-lg"
              onClick={handleBooking}
              disabled={submitting}
              style={{ marginTop: '24px' }}
            >
              {submitting ? <span className="btn-spinner"></span> : <><HiOutlineCheckCircle /> Confirm Booking</>}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
