// ========================================
// SISTEMA DE RUTAS MINEDU
// ========================================

class TransportRouteSystem {
    constructor() {
        this.map = null;
        this.routingControl = null;
        this.data = [];
        this.currentRegime = 'sierra';
        this.markers = [];
        this.init();
    }

    init() {
        this.initMap();
        this.setupEventListeners();
        this.showWelcomeMessage();
    }

    initMap() {
        // Inicializar mapa centrado en Perú
        this.map = L.map('map').setView([-9.19, -75.0152], 6);

        // Añadir capa de OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Añadir control de escala
        L.control.scale({ imperial: false, metric: true }).addTo(this.map);
    }

    showWelcomeMessage() {
        const popup = L.popup()
            .setLatLng([-9.19, -75.0152])
            .setContent('<b>Sistema de Rutas MINEDU</b><br>Carga tu archivo Excel para comenzar')
            .openOn(this.map);
    }

    setupEventListeners() {
        // Selector de régimen
        document.querySelectorAll('.regime-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.regime-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentRegime = e.target.dataset.regime;
                this.filterDataByRegime();
            });
        });

        // Upload de archivo
        const fileInput = document.getElementById('excelFile');
        const uploadArea = document.getElementById('fileUploadArea');

        uploadArea.addEventListener('click', () => fileInput.click());

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.background = '#f0f4ff';
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.background = '';
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.background = '';
            const file = e.dataTransfer.files[0];
            if (file) {
                this.handleFileUpload(file);
            }
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleFileUpload(file);
            }
        });

        // Botón calcular ruta
        document.getElementById('calculateRoute').addEventListener('click', () => {
            this.calculateRoute();
        });

        // Botón exportar
        document.getElementById('exportRoute').addEventListener('click', () => {
            this.exportRoute();
        });

        // Cambios en selectores
        document.getElementById('unidadEje').addEventListener('change', () => {
            this.updateMap();
        });

        document.getElementById('unidadAbsorbida').addEventListener('change', () => {
            this.updateMap();
        });
    }

    handleFileUpload(file) {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                
                // Leer la primera hoja
                const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                const jsonData = XLSX.utils.sheet_to_json(firstSheet);
                
                this.processExcelData(jsonData);
                this.showAlert('success', `✅ Archivo cargado: ${jsonData.length} registros encontrados`);
            } catch (error) {
                this.showAlert('error', '❌ Error al leer el archivo: ' + error.message);
            }
        };

        reader.readAsArrayBuffer(file);
    }

    processExcelData(jsonData) {
        // Procesar y normalizar datos
        this.data = jsonData.map((row, index) => {
            // Detectar columnas de coordenadas (pueden tener diferentes nombres)
            const latColNames = ['latitud', 'lat', 'latitude', 'lat_eje', 'latitud_eje', 'lat_absorbida', 'latitud_absorbida'];
            const lonColNames = ['longitud', 'lon', 'longitude', 'long', 'lng', 'lon_eje', 'longitud_eje', 'lon_absorbida', 'longitud_absorbida'];
            
            const getCoordValue = (row, possibleNames) => {
                for (let name of possibleNames) {
                    const key = Object.keys(row).find(k => k.toLowerCase().includes(name));
                    if (key && row[key]) return parseFloat(row[key]);
                }
                return null;
            };

            return {
                id: index,
                ...row,
                // Intentar extraer coordenadas EJE
                lat_eje: getCoordValue(row, latColNames.filter(n => n.includes('eje'))),
                lon_eje: getCoordValue(row, lonColNames.filter(n => n.includes('eje'))),
                // Intentar extraer coordenadas Absorbida
                lat_absorbida: getCoordValue(row, latColNames.filter(n => n.includes('absorbida'))),
                lon_absorbida: getCoordValue(row, lonColNames.filter(n => n.includes('absorbida'))),
                regime: row.regimen || row.régimen || row.regime || 'sierra'
            };
        });

        // Mostrar preview
        this.showDataPreview();
        
        // Poblar selectores
        this.populateSelectors();
        
        // Habilitar botón de cálculo
        document.getElementById('calculateRoute').disabled = false;

        // Mostrar algunas ubicaciones en el mapa
        this.showAllLocations();
    }

    showDataPreview() {
        const preview = document.getElementById('fileInfo');
        preview.style.display = 'block';
        
        const sampleData = this.data.slice(0, 3);
        let html = '<strong>📋 Vista previa:</strong><br>';
        html += `<small>Total de registros: ${this.data.length}</small><br><br>`;
        
        sampleData.forEach((item, idx) => {
            html += `<div style="margin-bottom: 8px; padding: 5px; background: white; border-radius: 4px;">`;
            html += `<strong>${idx + 1}.</strong> ${Object.keys(item).slice(0, 3).map(key => 
                `${key}: ${item[key]}`
            ).join(', ')}...`;
            html += `</div>`;
        });
        
        preview.innerHTML = html;
    }

    populateSelectors() {
        const ejeSelect = document.getElementById('unidadEje');
        const absorbidaSelect = document.getElementById('unidadAbsorbida');
        
        // Limpiar selectores
        ejeSelect.innerHTML = '<option value="">Seleccionar unidad EJE...</option>';
        absorbidaSelect.innerHTML = '<option value="">Seleccionar unidad absorbida...</option>';
        
        // Identificar columnas de nombres
        const nameColumns = Object.keys(this.data[0] || {}).filter(key => 
            key.toLowerCase().includes('nombre') || 
            key.toLowerCase().includes('unidad') ||
            key.toLowerCase().includes('ie') ||
            key.toLowerCase().includes('colegio')
        );
        
        const nameCol = nameColumns[0] || Object.keys(this.data[0] || {})[0];
        
        this.data.forEach((item, idx) => {
            const name = item[nameCol] || `Unidad ${idx + 1}`;
            const option = new Option(`${name}`, idx);
            
            if (item.lat_eje && item.lon_eje) {
                ejeSelect.add(option.cloneNode(true));
            }
            if (item.lat_absorbida && item.lon_absorbida) {
                absorbidaSelect.add(option.cloneNode(true));
            }
        });
    }

    filterDataByRegime() {
        // Filtrar datos por régimen seleccionado
        this.populateSelectors();
        this.showAllLocations();
    }

    showAllLocations() {
        // Limpiar marcadores anteriores
        this.markers.forEach(marker => this.map.removeLayer(marker));
        this.markers = [];

        // Iconos personalizados
        const ejeIcon = L.divIcon({
            html: '<div style="background: #2a5298; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">E</div>',
            className: '',
            iconSize: [30, 30]
        });

        const absorbidaIcon = L.divIcon({
            html: '<div style="background: #764ba2; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">A</div>',
            className: '',
            iconSize: [25, 25]
        });

        const bounds = [];

        this.data.forEach((item, idx) => {
            // Marcador para unidad EJE
            if (item.lat_eje && item.lon_eje) {
                const marker = L.marker([item.lat_eje, item.lon_eje], { icon: ejeIcon })
                    .bindPopup(`<b>🏫 Unidad EJE</b><br>${this.getItemName(item, idx)}`)
                    .addTo(this.map);
                this.markers.push(marker);
                bounds.push([item.lat_eje, item.lon_eje]);
            }

            // Marcador para unidad Absorbida
            if (item.lat_absorbida && item.lon_absorbida) {
                const marker = L.marker([item.lat_absorbida, item.lon_absorbida], { icon: absorbidaIcon })
                    .bindPopup(`<b>🏫 Unidad Absorbida</b><br>${this.getItemName(item, idx)}`)
                    .addTo(this.map);
                this.markers.push(marker);
                bounds.push([item.lat_absorbida, item.lon_absorbida]);
            }
        });

        // Ajustar vista del mapa
        if (bounds.length > 0) {
            this.map.fitBounds(bounds, { padding: [50, 50] });
        }
    }

    getItemName(item, idx) {
        const nameColumns = Object.keys(item).filter(key => 
            key.toLowerCase().includes('nombre') || 
            key.toLowerCase().includes('unidad') ||
            key.toLowerCase().includes('ie')
        );
        return item[nameColumns[0]] || `Unidad ${idx + 1}`;
    }

    updateMap() {
        const ejeIdx = document.getElementById('unidadEje').value;
        const absorbidaIdx = document.getElementById('unidadAbsorbida').value;

        if (ejeIdx && absorbidaIdx) {
            const eje = this.data[ejeIdx];
            const absorbida = this.data[absorbidaIdx];

            if (eje.lat_eje && eje.lon_eje && absorbida.lat_absorbida && absorbida.lon_absorbida) {
                // Centrar mapa en ambos puntos
                const bounds = [
                    [eje.lat_eje, eje.lon_eje],
                    [absorbida.lat_absorbida, absorbida.lon_absorbida]
                ];
                this.map.fitBounds(bounds, { padding: [50, 50] });
            }
        }
    }

    async calculateRoute() {
        const ejeIdx = document.getElementById('unidadEje').value;
        const absorbidaIdx = document.getElementById('unidadAbsorbida').value;
        const transportType = document.getElementById('transportType').value;

        if (!ejeIdx || !absorbidaIdx) {
            this.showAlert('error', '⚠️ Por favor selecciona ambas unidades');
            return;
        }

        const eje = this.data[ejeIdx];
        const absorbida = this.data[absorbidaIdx];

        if (!eje.lat_eje || !eje.lon_eje || !absorbida.lat_absorbida || !absorbida.lon_absorbida) {
            this.showAlert('error', '⚠️ Las coordenadas no están disponibles para las unidades seleccionadas');
            return;
        }

        // Mostrar loading
        document.getElementById('loadingIndicator').classList.add('active');

        try {
            // Limpiar ruta anterior
            if (this.routingControl) {
                this.map.removeControl(this.routingControl);
            }

            const startPoint = L.latLng(eje.lat_eje, eje.lon_eje);
            const endPoint = L.latLng(absorbida.lat_absorbida, absorbida.lon_absorbida);

            // Configurar perfil de ruta según tipo de transporte
            let profile = 'driving'; // default
            if (transportType === 'foot') profile = 'walking';
            if (transportType === 'boat') profile = 'driving'; // Para fluvial usamos driving como aproximación

            // Crear control de ruta
            this.routingControl = L.Routing.control({
                waypoints: [startPoint, endPoint],
                router: L.Routing.osrmv1({
                    serviceUrl: 'https://router.project-osrm.org/route/v1',
                    profile: profile
                }),
                lineOptions: {
                    styles: [
                        { color: '#2a5298', weight: 8, opacity: 0.6 },
                        { color: '#667eea', weight: 5, opacity: 0.9 }
                    ]
                },
                showAlternatives: false,
                addWaypoints: false,
                routeWhileDragging: false,
                fitSelectedRoutes: true,
                show: false, // Ocultar panel de instrucciones
                createMarker: (i, waypoint, n) => {
                    const icon = L.divIcon({
                        html: `<div style="background: ${i === 0 ? '#2a5298' : '#764ba2'}; color: white; border-radius: 50%; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 3px solid white; box-shadow: 0 3px 10px rgba(0,0,0,0.4); font-size: 16px;">${i === 0 ? 'O' : 'D'}</div>`,
                        className: '',
                        iconSize: [35, 35]
                    });
                    return L.marker(waypoint.latLng, { icon: icon });
                }
            }).addTo(this.map);

            // Esperar a que se calcule la ruta
            this.routingControl.on('routesfound', (e) => {
                const route = e.routes[0];
                this.displayRouteResults(route, eje, absorbida, transportType);
                document.getElementById('loadingIndicator').classList.remove('active');
            });

            this.routingControl.on('routingerror', (e) => {
                this.showAlert('error', '❌ Error al calcular la ruta. Intenta con otro tipo de transporte.');
                document.getElementById('loadingIndicator').classList.remove('active');
            });

        } catch (error) {
            this.showAlert('error', '❌ Error: ' + error.message);
            document.getElementById('loadingIndicator').classList.remove('active');
        }
    }

    displayRouteResults(route, eje, absorbida, transportType) {
        const distanceKm = (route.summary.totalDistance / 1000).toFixed(2);
        const timeMinutes = Math.round(route.summary.totalTime / 60);
        const hours = Math.floor(timeMinutes / 60);
        const minutes = timeMinutes % 60;

        // Actualizar stats
        document.getElementById('distanceValue').textContent = `${distanceKm} km`;
        document.getElementById('timeValue').textContent = hours > 0 
            ? `${hours}h ${minutes}m` 
            : `${minutes}m`;

        // Información detallada
        const transportNames = {
            'car': '🚗 Terrestre',
            'foot': '🚶 A pie',
            'boat': '⛵ Fluvial'
        };

        const routeDetails = document.getElementById('routeDetails');
        routeDetails.innerHTML = `
            <h4>Detalles de la Ruta</h4>
            <p><strong>Origen:</strong> ${this.getItemName(eje, 0)}</p>
            <p><strong>Destino:</strong> ${this.getItemName(absorbida, 0)}</p>
            <p><strong>Tipo:</strong> ${transportNames[transportType]}</p>
            <p><strong>Vía:</strong> ${this.getRouteType(route)}</p>
            <p><strong>Coordenadas Origen:</strong> ${eje.lat_eje}, ${eje.lon_eje}</p>
            <p><strong>Coordenadas Destino:</strong> ${absorbida.lat_absorbida}, ${absorbida.lon_absorbida}</p>
        `;

        // Mostrar sección de resultados
        document.getElementById('resultsSection').style.display = 'block';

        // Guardar última ruta calculada
        this.lastRoute = {
            route,
            eje,
            absorbida,
            transportType,
            distanceKm,
            timeMinutes
        };
    }

    getRouteType(route) {
        // Analizar el tipo de vía basado en las instrucciones
        const instructions = route.instructions || [];
        const roadTypes = new Set();
        
        instructions.forEach(inst => {
            if (inst.road) roadTypes.add(inst.road);
        });

        if (roadTypes.size === 0) return 'Ruta calculada';
        if (roadTypes.size <= 2) return Array.from(roadTypes).join(', ');
        return `${roadTypes.size} vías diferentes`;
    }

    exportRoute() {
        if (!this.lastRoute) {
            this.showAlert('error', '⚠️ No hay ruta calculada para exportar');
            return;
        }

        const exportData = {
            fecha_calculo: new Date().toISOString(),
            regimen: this.currentRegime,
            origen: {
                nombre: this.getItemName(this.lastRoute.eje, 0),
                latitud: this.lastRoute.eje.lat_eje,
                longitud: this.lastRoute.eje.lon_eje
            },
            destino: {
                nombre: this.getItemName(this.lastRoute.absorbida, 0),
                latitud: this.lastRoute.absorbida.lat_absorbida,
                longitud: this.lastRoute.absorbida.lon_absorbida
            },
            transporte: this.lastRoute.transportType,
            distancia_km: this.lastRoute.distanceKm,
            tiempo_minutos: this.lastRoute.timeMinutes,
            geometria: this.lastRoute.route.coordinates
        };

        // Crear y descargar JSON
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `ruta_${this.currentRegime}_${Date.now()}.json`;
        link.click();

        this.showAlert('success', '✅ Ruta exportada correctamente');
    }

    showAlert(type, message) {
        // Crear alerta temporal
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        
        const sidebar = document.querySelector('.sidebar');
        sidebar.insertBefore(alert, sidebar.firstChild);

        setTimeout(() => alert.remove(), 5000);
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.routeSystem = new TransportRouteSystem();
});
