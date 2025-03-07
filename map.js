// Inisialisasi peta
const map = L.map('map').setView([-6.9175, 107.6191], 13);

// Tambahkan layer peta dasar
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Definisikan warna berdasarkan tipe jalan
const roadColors = {
    'motorway': '#e892a2',
    'trunk': '#f58445',
    'primary': '#fcd6a4',
    'secondary': '#f7fabf',
    'tertiary': '#b6d4d3',
    'residential': '#ffffff',
    'unclassified': '#ffffff',
    'service': '#ffffff'
};

// Definisikan ketebalan garis berdasarkan tipe jalan
const roadWeights = {
    'motorway': 5,
    'trunk': 4,
    'primary': 3,
    'secondary': 2.5,
    'tertiary': 2,
    'residential': 1.5,
    'unclassified': 1,
    'service': 1
};

// Fungsi untuk mendapatkan style jalan
function getRoadStyle(feature) {
    const highway = feature.properties.highway || 'unclassified';
    return {
        color: roadColors[highway] || '#ffffff',
        weight: roadWeights[highway] || 1,
        opacity: 0.8
    };
}

// Tambahkan data jalan ke peta
L.geoJSON(roadsData, {
    style: getRoadStyle,
    onEachFeature: function(feature, layer) {
        const name = feature.properties.name || 'Unnamed Road';
        const highway = feature.properties.highway || 'unclassified';
        layer.bindPopup(`<b>${name}</b><br>Type: ${highway}`);
    }
}).addTo(map);

// Tambahkan legenda
const legend = L.control({position: 'bottomright'});

legend.onAdd = function(map) {
    const div = L.DomUtil.create('div', 'info legend');
    div.style.backgroundColor = 'white';
    div.style.padding = '10px';
    div.style.border = '2px solid grey';
    div.style.borderRadius = '5px';
    
    div.innerHTML = '<b>Tipe Jalan:</b><br>';
    
    const types = [
        ['Motorway', 'motorway'],
        ['Trunk', 'trunk'],
        ['Primary', 'primary'],
        ['Secondary', 'secondary'],
        ['Tertiary', 'tertiary'],
        ['Others', 'residential']
    ];
    
    for (const [label, type] of types) {
        div.innerHTML += 
            `<i style="background: ${roadColors[type]}; 
                      display: inline-block;
                      width: 18px;
                      height: 2px;
                      margin: 3px 7px 0 0;"></i>${label}<br>`;
    }
    
    return div;
};

legend.addTo(map);
