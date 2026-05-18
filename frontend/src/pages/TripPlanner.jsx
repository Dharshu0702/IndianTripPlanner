import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import { useGeolocation } from '../hooks/useGeolocation'
import api from '../api/axios'
import {
  HiOutlineMapPin, HiOutlineGlobeAlt, HiOutlineUserGroup,
  HiOutlineCalendarDays, HiOutlineCurrencyRupee, HiOutlineSparkles,
  HiOutlineArrowRight, HiOutlineArrowLeft, HiOutlineCheckCircle,
} from 'react-icons/hi2'
import '../styles/planner.css'

const TRIP_TYPES = [
  { value: 'Budget', icon: '💰', label: 'Budget', desc: 'Affordable & smart' },
  { value: 'Family', icon: '👨‍👩‍👧‍👦', label: 'Family', desc: 'Comfort & fun' },
  { value: 'Adventure', icon: '🏔️', label: 'Adventure', desc: 'Thrills & nature' },
  { value: 'Luxury', icon: '👑', label: 'Luxury', desc: 'Premium experience' },
]

export default function TripPlanner() {
  const navigate = useNavigate()
  const { location, error: geoError, loading: geoLoading, requestLocation, setManualLocation } = useGeolocation()
  const [step, setStep] = useState(1)
  const [states, setStates] = useState([])
  const [destinations, setDestinations] = useState([])
  const [manualAddress, setManualAddress] = useState('')
  const [manualLat, setManualLat] = useState('')
  const [manualLng, setManualLng] = useState('')
  const [showManual, setShowManual] = useState(false)

  // Form state
  const [selectedState, setSelectedState] = useState('')
  const [selectedDest, setSelectedDest] = useState('')
  const [travelers, setTravelers] = useState(2)
  const [days, setDays] = useState(3)
  const [budget, setBudget] = useState(50000)
  const [tripType, setTripType] = useState('Family')
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    api.get('/destinations/states').then(r => setStates(r.data.states)).catch(() => {})
  }, [])

  useEffect(() => {
    if (selectedState) {
      api.get(`/destinations/by-state/${selectedState}`)
        .then(r => setDestinations(r.data.destinations))
        .catch(() => setDestinations([]))
      setSelectedDest('')
    }
  }, [selectedState])

  const handleManualSubmit = () => {
    if (!manualAddress || !manualLat || !manualLng) {
      toast.error('Please fill all location fields')
      return
    }
    setManualLocation(manualAddress, parseFloat(manualLat), parseFloat(manualLng))
    toast.success('Location set!')
  }

  const canProceed = () => {
    switch (step) {
      case 1: return !!location
      case 2: return !!selectedState && !!selectedDest
      case 3: return travelers >= 1 && days >= 1 && budget >= 1000 && !!tripType
      default: return false
    }
  }

  const handleGenerate = async () => {
    setGenerating(true)
    try {
      const res = await api.post('/trips/generate', {
        location,
        state: selectedState,
        destination: selectedDest,
        travelers,
        days,
        budget,
        trip_type: tripType,
      })
      toast.success('Plans generated! 🎉')
      navigate(`/results/${res.data.trip.id}`)
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to generate plans')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="page-wrapper">
      <div className="container">
        <div className="planner-header animate-fadeInUp">
          <h1>Plan Your <span className="gradient-text">Dream Trip</span></h1>
          <p>AI-powered travel planning for destinations across India</p>
        </div>

        {/* Progress Steps */}
        <div className="progress-bar animate-fadeInUp">
          {[
            { num: 1, label: 'Location' },
            { num: 2, label: 'Destination' },
            { num: 3, label: 'Details' },
          ].map(({ num, label }) => (
            <div key={num} className={`progress-step ${step >= num ? 'active' : ''} ${step > num ? 'completed' : ''}`}>
              <div className="step-circle">
                {step > num ? <HiOutlineCheckCircle /> : num}
              </div>
              <span className="step-label">{label}</span>
            </div>
          ))}
        </div>

        <div className="planner-card glass-card animate-fadeInUp">
          {/* Step 1: Location */}
          {step === 1 && (
            <div className="step-content animate-fadeIn">
              <div className="step-title">
                <HiOutlineMapPin className="step-icon" />
                <div>
                  <h2>Your Current Location</h2>
                  <p>We need your location to calculate travel distance & cost</p>
                </div>
              </div>

              {location ? (
                <div className="location-result">
                  <div className="location-pin">📍</div>
                  <div className="location-info">
                    <strong>Location Detected</strong>
                    <span>{location.address}</span>
                    <span className="location-coords">
                      {location.lat.toFixed(4)}, {location.lng.toFixed(4)}
                    </span>
                  </div>
                  <HiOutlineCheckCircle className="location-check" />
                </div>
              ) : (
                <div className="location-actions">
                  <button
                    className="btn btn-primary btn-lg"
                    onClick={requestLocation}
                    disabled={geoLoading}
                  >
                    {geoLoading ? <span className="btn-spinner"></span> : <><HiOutlineMapPin /> Detect My Location</>}
                  </button>

                  {geoError && <p className="form-error">{geoError}</p>}

                  <button
                    className="btn btn-outline"
                    onClick={() => setShowManual(!showManual)}
                  >
                    Enter Manually
                  </button>

                  {showManual && (
                    <div className="manual-location animate-fadeIn">
                      <div className="form-group">
                        <label className="form-label">City / Address</label>
                        <input className="form-input" placeholder="e.g., Mumbai, Maharashtra" value={manualAddress} onChange={(e) => setManualAddress(e.target.value)} />
                      </div>
                      <div className="manual-coords">
                        <div className="form-group">
                          <label className="form-label">Latitude</label>
                          <input className="form-input" type="number" step="0.0001" placeholder="e.g., 19.0760" value={manualLat} onChange={(e) => setManualLat(e.target.value)} />
                        </div>
                        <div className="form-group">
                          <label className="form-label">Longitude</label>
                          <input className="form-input" type="number" step="0.0001" placeholder="e.g., 72.8777" value={manualLng} onChange={(e) => setManualLng(e.target.value)} />
                        </div>
                      </div>
                      <button className="btn btn-accent" onClick={handleManualSubmit}>Set Location</button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Step 2: Destination */}
          {step === 2 && (
            <div className="step-content animate-fadeIn">
              <div className="step-title">
                <HiOutlineGlobeAlt className="step-icon" />
                <div>
                  <h2>Choose Destination</h2>
                  <p>Select a state and destination in India</p>
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Select State</label>
                <select
                  className="form-select"
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  id="select-state"
                >
                  <option value="">-- Choose a state --</option>
                  {states.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              {selectedState && destinations.length > 0 && (
                <div className="dest-grid animate-fadeIn">
                  {destinations.map(d => (
                    <button
                      key={d.name}
                      className={`dest-card ${selectedDest === d.name ? 'selected' : ''}`}
                      onClick={() => setSelectedDest(d.name)}
                    >
                      <div className="dest-card-icon">🏛️</div>
                      <h3>{d.name}</h3>
                      <p>{d.description?.substring(0, 80)}...</p>
                      {d.best_time_to_visit && (
                        <span className="dest-season">🗓️ {d.best_time_to_visit}</span>
                      )}
                      {selectedDest === d.name && <div className="dest-selected-badge"><HiOutlineCheckCircle /></div>}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Step 3: Trip Details */}
          {step === 3 && (
            <div className="step-content animate-fadeIn">
              <div className="step-title">
                <HiOutlineSparkles className="step-icon" />
                <div>
                  <h2>Trip Details</h2>
                  <p>{selectedDest}, {selectedState}</p>
                </div>
              </div>

              <div className="details-grid">
                <div className="form-group">
                  <label className="form-label"><HiOutlineUserGroup /> Travelers</label>
                  <div className="stepper">
                    <button className="stepper-btn" onClick={() => setTravelers(Math.max(1, travelers - 1))}>−</button>
                    <span className="stepper-value">{travelers}</span>
                    <button className="stepper-btn" onClick={() => setTravelers(Math.min(50, travelers + 1))}>+</button>
                  </div>
                  {travelers > 4 && <p className="info-note">🚕 Multiple cabs will be arranged</p>}
                </div>

                <div className="form-group">
                  <label className="form-label"><HiOutlineCalendarDays /> Days</label>
                  <div className="stepper">
                    <button className="stepper-btn" onClick={() => setDays(Math.max(1, days - 1))}>−</button>
                    <span className="stepper-value">{days}</span>
                    <button className="stepper-btn" onClick={() => setDays(Math.min(30, days + 1))}>+</button>
                  </div>
                </div>

                <div className="form-group full-width">
                  <label className="form-label"><HiOutlineCurrencyRupee /> Budget (₹)</label>
                  <input
                    type="range"
                    min="5000"
                    max="500000"
                    step="5000"
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                    className="budget-slider"
                  />
                  <div className="budget-display">
                    <span>₹5,000</span>
                    <span className="budget-value">₹{budget.toLocaleString('en-IN')}</span>
                    <span>₹5,00,000</span>
                  </div>
                </div>

                <div className="form-group full-width">
                  <label className="form-label">Trip Type</label>
                  <div className="trip-type-grid">
                    {TRIP_TYPES.map(t => (
                      <button
                        key={t.value}
                        className={`trip-type-card ${tripType === t.value ? 'selected' : ''}`}
                        onClick={() => setTripType(t.value)}
                      >
                        <span className="tt-icon">{t.icon}</span>
                        <strong>{t.label}</strong>
                        <small>{t.desc}</small>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Navigation */}
          <div className="step-nav">
            {step > 1 && (
              <button className="btn btn-outline" onClick={() => setStep(step - 1)}>
                <HiOutlineArrowLeft /> Back
              </button>
            )}
            <div className="step-nav-spacer" />
            {step < 3 ? (
              <button
                className="btn btn-primary"
                disabled={!canProceed()}
                onClick={() => setStep(step + 1)}
              >
                Next <HiOutlineArrowRight />
              </button>
            ) : (
              <button
                className="btn btn-accent btn-lg"
                disabled={!canProceed() || generating}
                onClick={handleGenerate}
                id="generate-plans"
              >
                {generating ? (
                  <>
                    <span className="btn-spinner"></span>
                    Generating AI Plans...
                  </>
                ) : (
                  <>
                    <HiOutlineSparkles /> Generate AI Plans
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>

      {generating && (
        <div className="spinner-overlay">
          <div className="ai-generating">
            <div className="ai-orb"></div>
            <h2>AI is crafting your plans...</h2>
            <p>Analyzing {selectedDest}, calculating costs, building itinerary</p>
          </div>
        </div>
      )}
    </div>
  )
}
