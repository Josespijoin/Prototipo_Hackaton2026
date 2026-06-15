# app.py - YAKU DIGITAL API CON PANEL DE CONTROL INTEGRADO
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap, MarkerCluster, MiniMap
import json
from models import (
    df_proyectos, indicadores_piura, capitales,
    brecha_por_provincia, COLOR_MAP
)

# ============================================
# CREAR LA APLICACIÓN
# ============================================
app = Flask(__name__)
CORS(app)

# Crear proyectos_js para los filtros del dashboard
proyectos_js = df_proyectos[['tipo', 'estado', 'provincia', 'beneficiarios']].to_dict('records')

# ============================================
# ENDPOINTS DE LA API
# ============================================

@app.route('/')
def home():
    return jsonify({
        "nombre": "YAKU DIGITAL API",
        "version": "1.0.0",
        "descripcion": "Plataforma Digital de Monitoreo Hídrico - Piura",
        "total_proyectos": len(df_proyectos),
        "endpoints": {
            "GET /api/estadisticas": "Estadísticas generales",
            "GET /api/proyectos": "Lista de proyectos",
            "GET /api/proyectos/<cui>": "Detalle de proyecto",
            "GET /api/indicadores": "Indicadores ENAPRES 2024",
            "GET /api/provincias": "Datos por provincia",
            "GET /api/estados": "Resumen por estado",
            "GET /api/mapa": "Datos geoespaciales",
            "GET /api/filtros": "Valores para filtros",
            "GET /dashboard": "Dashboard visual"
        }
    })

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    stats = {
        "total_proyectos": len(df_proyectos),
        "paralizados": int(len(df_proyectos[df_proyectos['estado'] == "PARALIZADO"])),
        "suspendidos": int(len(df_proyectos[df_proyectos['estado'] == "SUSPENDIDO"])),
        "por_cerrar": int(len(df_proyectos[df_proyectos['estado'] == "POR CERRAR"])),
        "beneficiarios": int(df_proyectos['beneficiarios'].sum()),
        "inversion_total": float(df_proyectos['monto_inversion'].sum()),
        "inversion_paralizada": float(df_proyectos[df_proyectos['estado'] == "PARALIZADO"]['monto_inversion'].sum()),
        "brechas": indicadores_piura,
        "fecha_actualizacion": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(stats)

@app.route('/api/proyectos', methods=['GET'])
def get_proyectos():
    estado = request.args.get('estado')
    provincia = request.args.get('provincia')
    tipo = request.args.get('tipo')
   
    df_filtrado = df_proyectos.copy()
   
    if estado:
        df_filtrado = df_filtrado[df_filtrado['estado'] == estado.upper()]
    if provincia:
        df_filtrado = df_filtrado[df_filtrado['provincia'] == provincia.upper()]
    if tipo:
        df_filtrado = df_filtrado[df_filtrado['tipo'] == tipo.upper()]
   
    return jsonify({
        "total": len(df_filtrado),
        "proyectos": df_filtrado.to_dict('records')
    })

@app.route('/api/proyectos/<cui>', methods=['GET'])
def get_proyecto_by_cui(cui):
    proyecto = df_proyectos[df_proyectos['CUI'] == cui]
    if len(proyecto) == 0:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    return jsonify(proyecto.to_dict('records')[0])

@app.route('/api/indicadores', methods=['GET'])
def get_indicadores():
    return jsonify(indicadores_piura)

@app.route('/api/provincias', methods=['GET'])
def get_provincias():
    provincias_data = []
    for provincia, coords in capitales.items():
        if provincia in brecha_por_provincia:
            provincias_data.append({
                "nombre": provincia,
                "latitud": coords[0],
                "longitud": coords[1],
                "brecha_agua": brecha_por_provincia[provincia]["brecha_agua"],
                "brecha_alcantarillado": brecha_por_provincia[provincia]["brecha_alcantarillado"],
                "beneficiarios_afectados": brecha_por_provincia[provincia]["beneficiarios_afectados"]
            })
    return jsonify(provincias_data)

@app.route('/api/estados', methods=['GET'])
def get_estados_resumen():
    estados_resumen = []
    for estado in df_proyectos['estado'].unique():
        proyectos_estado = df_proyectos[df_proyectos['estado'] == estado]
        estados_resumen.append({
            "estado": estado,
            "color": COLOR_MAP.get(estado, "#95a5a6"),
            "cantidad": len(proyectos_estado),
            "monto_inversion": float(proyectos_estado['monto_inversion'].sum()),
            "beneficiarios": int(proyectos_estado['beneficiarios'].sum()),
            "avance_promedio": float(proyectos_estado['avance_fisico'].mean())
        })
    return jsonify(estados_resumen)

@app.route('/api/mapa', methods=['GET'])
def get_mapa_data():
    proyectos_mapa = df_proyectos[['nombre', 'latitud', 'longitud', 'estado', 'monto_inversion']].to_dict('records')
    provincias_mapa = []
    for provincia, coords in capitales.items():
        if provincia in brecha_por_provincia:
            provincias_mapa.append({
                "nombre": provincia,
                "latitud": coords[0],
                "longitud": coords[1],
                "brecha_agua": brecha_por_provincia[provincia]["brecha_agua"]
            })
    return jsonify({"proyectos": proyectos_mapa, "provincias": provincias_mapa})

@app.route('/api/filtros', methods=['GET'])
def get_filtros_disponibles():
    return jsonify({
        "estados": sorted(df_proyectos['estado'].unique().tolist()),
        "provincias": sorted(df_proyectos['provincia'].unique().tolist()),
        "tipos": sorted(df_proyectos['tipo'].unique().tolist()),
        "subsectores": sorted(df_proyectos['subsector'].unique().tolist())
    })

@app.route('/dashboard')
def dashboard():
    """Dashboard visual con mapa interactivo y panel de control estilo YAKU DIGITAL"""
   
    # Crear el mapa base
    mapa = folium.Map(
        location=[-5.1945, -80.6328],
        zoom_start=8.5,
        tiles="CartoDB Voyager",
        control_scale=True
    )
   
    # Capa Satelital
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri | World Imagery',
        name='Imagen Satelital',
        control=True
    ).add_to(mapa)
   
    # Capa Calles
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Mapa Calles',
        control=True
    ).add_to(mapa)
   
    # Círculos de brecha por provincia
    for provincia, coords in capitales.items():
        if provincia in brecha_por_provincia:
            brecha = brecha_por_provincia[provincia]["brecha_agua"]
            color = "#e74c3c" if brecha >= 25 else "#f39c12"
            radio = 8 + (brecha / 25) * 15
            folium.CircleMarker(
                location=coords,
                radius=radio,
                color=color,
                fill=True,
                fill_opacity=0.3,
                popup=f"<b>{provincia}</b><br>Brecha agua: {brecha}%<br>Brecha alcantarillado: {brecha_por_provincia[provincia]['brecha_alcantarillado']}%"
            ).add_to(mapa)
   
    # Marcadores de proyectos con colores
    marker_cluster = MarkerCluster(name="Proyectos de Saneamiento").add_to(mapa)
   
    for _, proyecto in df_proyectos.iterrows():
        color = COLOR_MAP.get(proyecto['estado'], "#95a5a6")
       
        popup_html = f"""
        <div style="font-family: Arial; width: 320px;">
            <h4 style="color: #1a5276; margin-bottom: 5px;">{proyecto['nombre'][:60]}...</h4>
            <hr style="margin: 5px 0;">
            <table style="width: 100%; font-size: 12px;">
                <tr><td><strong>CUI:</strong></td><td>{proyecto['CUI']}</td></tr>
                <tr><td><strong>Distrito/Provincia:</strong></td><td>{proyecto['distrito']} / {proyecto['provincia']}</td></tr>
                <tr><td><strong>Estado:</strong></td><td><span style="background:{color}; color:white; padding:2px 8px; border-radius:10px;">{proyecto['estado']}</span></td></tr>
                <tr><td><strong>Causa:</strong></td><td>{proyecto['causa'][:50]}</td></tr>
                <tr><td><strong>Avance Físico:</strong></td><td>{proyecto['avance_fisico']}%</td></tr>
                <tr><td><strong>Monto:</strong></td><td>S/ {proyecto['monto_inversion']:,.0f}</td></tr>
                <tr><td><strong>Beneficiarios:</strong></td><td>{proyecto['beneficiarios']:,}</td></tr>
                <tr><td><strong>Tipo:</strong></td><td>{proyecto['tipo']} / {proyecto['subsector']}</td></tr>
            </table>
        </div>
        """
       
        folium.Marker(
            location=[proyecto['latitud'], proyecto['longitud']],
            popup=folium.Popup(popup_html, max_width=350),
            tooltip=f"{proyecto['nombre'][:40]} - {proyecto['estado']}",
            icon=folium.DivIcon(
                html=f'<div style="background-color: {color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 3px rgba(0,0,0,0.5);"></div>'
            )
        ).add_to(marker_cluster)
   
    # Mapa de calor de inversión
    heat_data = [[p['latitud'], p['longitud'], min(p['monto_inversion'] / 10000000, 1.0)]
                 for _, p in df_proyectos.iterrows()]
    HeatMap(heat_data, name="Mapa de Calor (Inversión)", radius=15, blur=10).add_to(mapa)
   
    # Controles del mapa
    folium.LayerControl(position="topright", collapsed=False).add_to(mapa)
    MiniMap(toggle_display=True, position="bottomleft").add_to(mapa)
    plugins.MeasureControl(position="topleft").add_to(mapa)
    plugins.Fullscreen(position="topright").add_to(mapa)
   
    # Generar opciones para filtros
    tipos_proyecto = sorted(df_proyectos['tipo'].unique())
    estados_proyecto = sorted(df_proyectos['estado'].unique())
    provincias_lista = sorted(df_proyectos['provincia'].unique())
   
    tipos_options = ''.join([f'<option value="{t}">💧 {t}</option>' for t in tipos_proyecto])
    estados_options = ''.join([f'<option value="{e}"><span style="color:{COLOR_MAP[e]}">●</span> {e}</option>' for e in estados_proyecto])
    provincias_options = ''.join([f'<option value="{p}">📍 {p}</option>' for p in provincias_lista])
   
    # Calcular estadísticas para el panel
    total_proyectos = len(df_proyectos)
    total_paralizados = len(df_proyectos[df_proyectos['estado'] == "PARALIZADO"])
    total_suspendidos = len(df_proyectos[df_proyectos['estado'] == "SUSPENDIDO"])
    total_por_cerrar = len(df_proyectos[df_proyectos['estado'] == "POR CERRAR"])
    monto_total = df_proyectos['monto_inversion'].sum()
    beneficiarios_total = df_proyectos['beneficiarios'].sum()
    inversion_paralizada = df_proyectos[df_proyectos['estado'] == "PARALIZADO"]['monto_inversion'].sum()
   
    # Panel de control HTML
    panel_html = f'''
    <div id="yaku-panel" style="position: fixed; bottom: 20px; left: 20px; width: 380px; max-height: 85vh; overflow-y: auto; background: linear-gradient(135deg, #1a2a3a 0%, #0f1a24 100%); color: #e8f0f8; border-radius: 16px; z-index: 9999; padding: 18px; font-family: 'Segoe UI', 'Roboto', Arial, sans-serif; font-size: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); border: 1px solid rgba(46, 204, 113, 0.3); backdrop-filter: blur(4px);">
       
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; border-bottom: 2px solid #2ecc71; padding-bottom: 10px;">
            <span style="font-size: 18px; font-weight: 700; background: linear-gradient(135deg, #2ecc71, #27ae60); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">💧 YAKU DIGITAL</span>
            <span style="font-size: 10px; color: #7f8c8d;">Plataforma Digital de Monitoreo Hídrico | ENAPRES 2024 | Piura</span>
        </div>
       
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
            <select id="filtro_tipo" style="background: #2c3e50; color: #ecf0f1; border: 1px solid #3d566e; border-radius: 20px; padding: 6px 12px; font-size: 11px; flex: 1; cursor: pointer;">
                <option value="todos">📋 Todos los tipos</option>
                {tipos_options}
            </select>
            <select id="filtro_estado" style="background: #2c3e50; color: #ecf0f1; border: 1px solid #3d566e; border-radius: 20px; padding: 6px 12px; font-size: 11px; flex: 1; cursor: pointer;">
                <option value="todos">📊 Todos los estados</option>
                {estados_options}
            </select>
            <select id="filtro_provincia" style="background: #2c3e50; color: #ecf0f1; border: 1px solid #3d566e; border-radius: 20px; padding: 6px 12px; font-size: 11px; flex: 1; cursor: pointer;">
                <option value="todos">📍 Todas las provincias</option>
                {provincias_options}
            </select>
        </div>
       
        <div style="font-size: 10px; color: #2ecc71; text-align: center; margin-bottom: 10px;">🔄 Filtros actualizan mapa y estadísticas en tiempo real</div>
       
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 12px 0;">
            <div style="background: rgba(44, 62, 80, 0.6); border-radius: 12px; padding: 8px 10px; text-align: center;">
                <div style="font-size: 20px; font-weight: 700;" id="stat_total">{total_proyectos}</div>
                <div style="font-size: 10px; color: #bdc3c7;">🏗️ Total proyectos</div>
            </div>
            <div style="background: rgba(44, 62, 80, 0.6); border-radius: 12px; padding: 8px 10px; text-align: center;">
                <div style="font-size: 20px; font-weight: 700; color: #f1c40f;" id="stat_por_cerrar">{total_por_cerrar}</div>
                <div style="font-size: 10px; color: #bdc3c7;">🟡 Por cerrar</div>
            </div>
            <div style="background: rgba(44, 62, 80, 0.6); border-radius: 12px; padding: 8px 10px; text-align: center;">
                <div style="font-size: 20px; font-weight: 700; color: #e74c3c;" id="stat_paralizados">{total_paralizados}</div>
                <div style="font-size: 10px; color: #bdc3c7;">🔴 Paralizados</div>
            </div>
            <div style="background: rgba(44, 62, 80, 0.6); border-radius: 12px; padding: 8px 10px; text-align: center;">
                <div style="font-size: 20px; font-weight: 700; color: #f39c12;" id="stat_suspendidos">{total_suspendidos}</div>
                <div style="font-size: 10px; color: #bdc3c7;">🟠 Suspendidos</div>
            </div>
        </div>
       
        <div style="display: flex; justify-content: space-between; margin: 8px 0;">
            <span>👥 Beneficiarios directos:</span>
            <span><b id="stat_beneficiarios">{beneficiarios_total:,.0f}</b></span>
        </div>
       
        <div style="display: flex; justify-content: space-between; margin: 8px 0;">
            <span>💰 Inversión total:</span>
            <span><b>S/ {monto_total/1e6:.1f}M</b></span>
        </div>
       
        <div style="display: flex; justify-content: space-between; margin: 8px 0;">
            <span>⚠️ Inversión paralizada:</span>
            <span><b style="color:#ff6b6b;">S/ {inversion_paralizada/1e6:.1f}M</b></span>
        </div>
       
        <hr style="border-color: #2c3e50; margin: 12px 0;">
       
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>🚰 Brecha agua potable</span>
                <span><b>{indicadores_piura['brecha_agua_porcentaje']}%</b> sin acceso</span>
            </div>
            <div style="background: #2c3e50; height: 8px; border-radius: 4px; margin-top: 4px;">
                <div style="width: {indicadores_piura['brecha_agua_porcentaje']}%; background: #e74c3c; height: 8px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 9px; color: #95a5a6;">{indicadores_piura['brecha_agua_miles']:,.0f} personas</div>
        </div>
       
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>🚽 Brecha alcantarillado</span>
                <span><b>{indicadores_piura['brecha_alcantarillado_porcentaje']}%</b> sin acceso</span>
            </div>
            <div style="background: #2c3e50; height: 8px; border-radius: 4px; margin-top: 4px;">
                <div style="width: {indicadores_piura['brecha_alcantarillado_porcentaje']}%; background: #c0392b; height: 8px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 9px; color: #95a5a6;">{indicadores_piura['brecha_alcantarillado_miles']:,.0f} personas</div>
        </div>
       
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>💧 Agua segura (cloro ≥0.5mg/L)</span>
                <span><b>{indicadores_piura['agua_segura_porcentaje']}%</b> <span style="background:#e74c3c; padding:2px 6px; border-radius:10px; font-size:9px;">Muy bajo</span></span>
            </div>
            <div style="background: #2c3e50; height: 8px; border-radius: 4px; margin-top: 4px;">
                <div style="width: {indicadores_piura['agua_segura_porcentaje']}%; background: #e67e22; height: 8px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 9px;">Estándar nacional: >95%</div>
        </div>
       
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between;">
                <span>🧼 Prácticas adecuadas en uso de agua</span>
                <span><b>{indicadores_piura['practicas_adecuadas_agua']}%</b></span>
            </div>
            <div style="background: #2c3e50; height: 8px; border-radius: 4px; margin-top: 4px;">
                <div style="width: {indicadores_piura['practicas_adecuadas_agua']}%; background: #3498db; height: 8px; border-radius: 4px;"></div>
            </div>
        </div>
       
        <div style="background: rgba(0,0,0,0.3); border-radius: 12px; padding: 10px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>💰 Pago O&M rural:</span>
                <span><b>S/ {indicadores_piura['pago_mensual_operacion']}</b></span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span>📞 Hogares que pagan:</span>
                <span><b>{indicadores_piura['pago_voluntario_porcentaje']}%</b></span>
            </div>
        </div>
       
        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin: 10px 0; padding: 8px 0; border-top: 1px solid #2c3e50; border-bottom: 1px solid #2c3e50;">
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #e74c3c; border-radius: 50%; margin-right: 4px;"></span> Paralizado</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #f39c12; border-radius: 50%; margin-right: 4px;"></span> Suspendido</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #f1c40f; border-radius: 50%; margin-right: 4px;"></span> Por cerrar</div>
        </div>
       
        <div style="font-size: 9px; text-align: center; color: #7f8c8d; margin-top: 12px; padding-top: 8px; border-top: 1px solid #2c3e50;">
            Fuente: ENAPRES 2024 (INEI) | Proyecto: PISU / MVCS<br>
            Hackatón Transformagob 2026 - YAKU DIGITAL
        </div>
    </div>
   
    <script>
        var proyectosData = {json.dumps(proyectos_js)};
       
        function aplicarFiltros() {{
            var tipoFiltro = document.getElementById('filtro_tipo').value;
            var estadoFiltro = document.getElementById('filtro_estado').value;
            var provinciaFiltro = document.getElementById('filtro_provincia').value;
           
            var filtrados = proyectosData.filter(function(p) {{
                if (tipoFiltro !== 'todos' && p.tipo !== tipoFiltro) return false;
                if (estadoFiltro !== 'todos' && p.estado !== estadoFiltro) return false;
                if (provinciaFiltro !== 'todos' && p.provincia !== provinciaFiltro) return false;
                return true;
            }});
           
            document.getElementById('stat_total').innerText = filtrados.length;
            document.getElementById('stat_por_cerrar').innerText = filtrados.filter(p => p.estado === 'POR CERRAR').length;
            document.getElementById('stat_paralizados').innerText = filtrados.filter(p => p.estado === 'PARALIZADO').length;
            document.getElementById('stat_suspendidos').innerText = filtrados.filter(p => p.estado === 'SUSPENDIDO').length;
            document.getElementById('stat_beneficiarios').innerText = filtrados.reduce((s,p) => s + p.beneficiarios, 0).toLocaleString();
           
            var markers = document.querySelectorAll('.leaflet-marker-icon');
            for(var i = 0; i < markers.length; i++) {{
                if (i < filtrados.length) {{
                    markers[i].style.display = '';
                }} else {{
                    markers[i].style.display = 'none';
                }}
            }}
        }}
       
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(function() {{
                var markers = document.querySelectorAll('.leaflet-marker-icon');
            }}, 500);
           
            document.getElementById('filtro_tipo').addEventListener('change', aplicarFiltros);
            document.getElementById('filtro_estado').addEventListener('change', aplicarFiltros);
            document.getElementById('filtro_provincia').addEventListener('change', aplicarFiltros);
        }});
    </script>
    '''
   
    # Agregar el panel al mapa
    mapa.get_root().html.add_child(folium.Element(panel_html))
   
    return mapa._repr_html_()

# ============================================
# EJECUTAR LA API
# ============================================
if __name__ == '__main__':
    print("=" * 60)
    print("💧 YAKU DIGITAL API - Plataforma de Monitoreo Hídrico")
    print("=" * 60)
    print(f"\n📊 Proyectos cargados: {len(df_proyectos)}")
    print("\n📡 Endpoints disponibles:")
    print("   GET  /                 - Información de la API")
    print("   GET  /api/estadisticas - Estadísticas generales")
    print("   GET  /api/proyectos    - Lista de proyectos")
    print("   GET  /api/proyectos/<cui> - Detalle de proyecto")
    print("   GET  /api/indicadores  - Indicadores ENAPRES 2024")
    print("   GET  /api/provincias   - Datos por provincia")
    print("   GET  /api/estados      - Resumen por estado")
    print("   GET  /api/mapa         - Datos geoespaciales")
    print("   GET  /api/filtros      - Valores para filtros")
    print("   GET  /dashboard        - Dashboard visual")
    print("\n" + "=" * 60)
    print("🚀 Servidor iniciado en http://localhost:5000")
    print("🌐 Dashboard: http://localhost:5000/dashboard")
    print("=" * 60)
   
    app.run(debug=True, host='0.0.0.0', port=5000)