import { useState, useEffect } from 'react'

export function useGeolocation() {
  const [location, setLocation] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const requestLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser')
      return
    }

    setLoading(true)
    setError(null)

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords
        let address = `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`

        // Try reverse geocoding
        try {
          const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`
          )
          const data = await res.json()
          if (data.display_name) {
            address = data.display_name
          }
        } catch {
          // Keep coordinate-based address
        }

        setLocation({ lat: latitude, lng: longitude, address })
        setLoading(false)
      },
      (err) => {
        setError(err.message || 'Failed to get location')
        setLoading(false)
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
    )
  }

  const setManualLocation = (address, lat, lng) => {
    setLocation({ lat, lng, address })
    setError(null)
  }

  return { location, error, loading, requestLocation, setManualLocation }
}
