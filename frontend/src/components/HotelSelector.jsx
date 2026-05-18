import { useState, useEffect } from 'react'
import { HiOutlineMapPin, HiOutlineStar, HiOutlineArrowTopRightOnSquare, HiOutlineCheckCircle, HiOutlineXMark } from 'react-icons/hi2'
import api from '../api/axios'
import '../styles/hotels.css'

/* ── Modal ── */
function HotelModal({ hotel, onClose, onSelect, isSelected }) {
  if (!hotel) return null
  return (
    <div className="hotel-modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="hotel-modal">
        <img
          src={hotel.image}
          alt={hotel.name}
          className="hotel-modal-img"
          onError={(e) => { e.target.replaceWith(Object.assign(document.createElement('div'), { className: 'hotel-card-img-placeholder', style: 'height:220px;border-radius:20px 20px 0 0', textContent: '🏨' })) }}
        />
        <div className="hotel-modal-body">
          <div className="hotel-modal-header">
            <div className="hotel-modal-name">{hotel.name}</div>
            <button className="hotel-modal-close" onClick={onClose}>✕</button>
          </div>
          <div className="hotel-modal-location"><HiOutlineMapPin /> {hotel.location}</div>
          <div className="hotel-modal-stats">
            <div className="hotel-stat-box">
              <div className="hotel-stat-value">₹{hotel.price_per_night?.toLocaleString('en-IN')}</div>
              <div className="hotel-stat-label">per night</div>
            </div>
            <div className="hotel-stat-box">
              <div className="hotel-stat-value" style={{ color: '#f59e0b' }}>⭐ {hotel.rating}</div>
              <div className="hotel-stat-label">rating / 5</div>
            </div>
          </div>
          <div className="hotel-modal-actions">
            <button
              className={`btn ${isSelected ? 'btn-outline' : 'btn-primary'}`}
              onClick={() => { onSelect(hotel); onClose() }}
            >
              {isSelected ? <><HiOutlineXMark /> Deselect</> : <><HiOutlineCheckCircle /> Select Hotel</>}
            </button>
            <a href={hotel.website} target="_blank" rel="noopener noreferrer" className="btn-website">
              Visit Website <HiOutlineArrowTopRightOnSquare />
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

/* ── Card ── */
function HotelCard({ hotel, isSelected, onSelect, onInfo }) {
  return (
    <div className={`hotel-card ${isSelected ? 'selected' : ''}`} onClick={() => onSelect(hotel)}>
      {isSelected && <div className="hotel-selected-badge">✓</div>}
      <button className="hotel-info-btn" title="View details"
        onClick={(e) => { e.stopPropagation(); onInfo(hotel) }}>ℹ</button>
      <img src={hotel.image} alt={hotel.name} className="hotel-card-img"
        onError={(e) => { e.target.style.display = 'none' }} />
      <div className="hotel-card-body">
        <div className="hotel-card-name">{hotel.name}</div>
        <div className="hotel-card-location"><HiOutlineMapPin style={{ flexShrink: 0 }} />{hotel.location}</div>
        <div className="hotel-card-footer">
          <div className="hotel-card-price">₹{hotel.price_per_night?.toLocaleString('en-IN')} <span>/night</span></div>
          <div className="hotel-card-rating">⭐ {hotel.rating}</div>
        </div>
      </div>
    </div>
  )
}

/* ── Main Selector ── */
export default function HotelSelector({ destination, planName, selectedHotel, onHotelSelect, days }) {
  const [hotels, setHotels] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalHotel, setModalHotel] = useState(null)

  useEffect(() => {
    if (!destination || !planName) return
    setLoading(true)
    api.get('/hotels', { params: { destination, plan: planName } })
      .then(r => setHotels(r.data.hotels || []))
      .catch(() => setHotels([]))
      .finally(() => setLoading(false))
  }, [destination, planName])

  const totalHotelCost = selectedHotel ? selectedHotel.price_per_night * (days || 1) : null

  return (
    <div className="hotel-section">
      <div className="hotel-section-title">
        <HiOutlineStar />
        Choose Your Hotel
        {selectedHotel && (
          <span style={{ marginLeft: 'auto', fontSize: '0.8rem', color: 'var(--primary-light)', fontWeight: 500 }}>
            ✓ {selectedHotel.name}
          </span>
        )}
      </div>

      {loading && <div className="hotels-loading">🔍 Loading hotel options...</div>}

      {!loading && hotels.length > 0 && (
        <div className="hotels-grid">
          {hotels.map(hotel => (
            <HotelCard
              key={hotel.id}
              hotel={hotel}
              isSelected={selectedHotel?.id === hotel.id}
              onSelect={onHotelSelect}
              onInfo={setModalHotel}
            />
          ))}
        </div>
      )}

      {!loading && hotels.length === 0 && (
        <div className="hotels-loading">No hotels found for this destination.</div>
      )}

      {selectedHotel && days && (
        <div style={{
          marginTop: 12, padding: '10px 14px',
          background: 'rgba(79,70,229,0.1)', borderRadius: 10,
          border: '1px solid rgba(79,70,229,0.3)',
          fontSize: '0.85rem', color: 'var(--text-secondary)'
        }}>
          🏨 <strong>{selectedHotel.name}</strong> —
          ₹{selectedHotel.price_per_night?.toLocaleString('en-IN')}/night × {days} nights =&nbsp;
          <strong style={{ color: 'var(--primary-light)' }}>₹{totalHotelCost?.toLocaleString('en-IN')}</strong>
        </div>
      )}

      {modalHotel && (
        <HotelModal
          hotel={modalHotel}
          onClose={() => setModalHotel(null)}
          onSelect={onHotelSelect}
          isSelected={selectedHotel?.id === modalHotel.id}
        />
      )}
    </div>
  )
}
