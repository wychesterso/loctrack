const map = L.map('map').setView([-27.497, 153.013], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

fetch('http://localhost:5000/locations')
    .then(res => res.json())
    .then(data => {
        const heatPoints = data
            .filter(loc => typeof loc.lat === 'number' && typeof loc.lng === 'number')
            .map(loc => [loc.lat, loc.lng, 1]);
        console.log("Heatmap points:", heatPoints);
        L.heatLayer(heatPoints, { radius: 25 }).addTo(map);
    })
    .catch(err => console.error('Failed to load location data: ', err));
