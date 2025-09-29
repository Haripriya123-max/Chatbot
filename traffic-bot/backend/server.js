process.on("uncaughtException", (err) => {
  console.error("Uncaught Exception:", err);
});
process.on("unhandledRejection", (reason) => {
  console.error("Unhandled Rejection:", reason);
});


require('dotenv').config();
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;
const ORS_API_KEY = process.env.ORS_API_KEY;
console.log("Loaded ORS_API_KEY:", ORS_API_KEY ? "Yes" : "No");
if (!ORS_API_KEY) {
  console.error("Missing ORS_API_KEY in .env");
  process.exit(1);
}

// Simple destination extractor
function extractDestination(text) {
  const toMatch = text.match(/to\s+(.+)/i);
  if (toMatch) return toMatch[1].trim();
  return text.trim(); // fallback
}

app.post('/api/message', async (req, res) => {
  try {
    const { text, origin } = req.body;
    if (!text) return res.status(400).json({ error: 'text required' });
    if (!origin) return res.status(400).json({ error: 'origin {lat,lng} required' });

    const destText = extractDestination(text);

    // Step 1: Geocode destination using ORS
    const geocodeResp = await axios.get("https://api.openrouteservice.org/geocode/search", {
      params: {
        api_key: ORS_API_KEY,
        text: destText,
        size: 1
      }
    });

    if (!geocodeResp.data.features || geocodeResp.data.features.length === 0) {
      return res.json({ message: `Could not find destination: "${destText}"`, routes: [] });
    }

    const dest = geocodeResp.data.features[0];
    const destCoords = dest.geometry.coordinates; // [lng, lat]
    const destAddress = dest.properties.label;

    // Step 2: Request directions
    const directionsResp = await axios.post(
      "https://api.openrouteservice.org/v2/directions/driving-car",
      {
        coordinates: [
          [origin.lng, origin.lat],
          destCoords
        ]
      },
      {
        headers: {
          Authorization: ORS_API_KEY,
          "Content-Type": "application/json"
        }
      }
    );

    if (!directionsResp.data.routes || directionsResp.data.routes.length === 0) {
      return res.json({ message: `No routes found to ${destText}`, routes: [] });
    }

    // Step 3: Prepare routes data
    const routes = directionsResp.data.routes.map((route, idx) => {
      const summary = route.summary;
      const distanceKm = (summary.distance / 1000).toFixed(2) + " km";
      const durationMin = Math.round(summary.duration / 60) + " mins";
      return {
        summary: `Route ${idx + 1}`,
        distance: distanceKm,
        duration: durationMin,
        google_maps_url: `https://www.google.com/maps/dir/?api=1&origin=${origin.lat},${origin.lng}&destination=${destCoords[1]},${destCoords[0]}&travelmode=driving`
      };
    });

    return res.json({
      destination: destAddress,
      origin,
      routes
    });

  } catch (err) {
    console.error(err.message || err);
    return res.status(500).json({ error: err.message || 'server error' });
  }
});

app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));
