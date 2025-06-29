const map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

fetch('http://localhost:5000/locations')
    .then(res => res.json())
    .then(data => {
        const heatPoints = data.map(loc => [loc.latitude, loc.longitude, 1]);
        L.heatLayer(heatPoints, { radius: 25 }).addTo(map);
    })
    .catch(err => console.error('Failed to load location data: ', err));
