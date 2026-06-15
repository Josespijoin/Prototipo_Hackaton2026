# models.py
import pandas as pd
from datetime import datetime

# ============================================
# DATOS DE PROYECTOS
# ============================================

proyectos_data = [
    {
        "CUI": "2307711",
        "nombre": "AMPLIACIÓN Y MEJORAMIENTO DE SERVICIOS DE AGUA POTABLE Y ALCANTARILLADO - PARACHIQUE",
        "distrito": "SECHURA",
        "provincia": "SECHURA",
        "estado": "PARALIZADO",
        "causa": "Discrepancias, controversias y arbitraje",
        "avance_fisico": 46.7,
        "monto_inversion": 60404253.47,
        "beneficiarios": 25965,
        "fecha_paralizacion": "2022-05-28",
        "latitud": -5.5576,
        "longitud": -80.8222,
        "tipo": "AGUA POTABLE",
        "subsector": "URBANO"
    },
    {
        "CUI": "2030755",
        "nombre": "AMPLIACIÓN Y MEJORAMIENTO DE SISTEMAS DE AGUA POTABLE - LA ARENA",
        "distrito": "LA ARENA",
        "provincia": "PIURA",
        "estado": "PARALIZADO",
        "causa": "Incumplimiento de contrato",
        "avance_fisico": 77.76,
        "monto_inversion": 22726345.75,
        "beneficiarios": 17656,
        "fecha_paralizacion": "2011-04-18",
        "latitud": -5.1945,
        "longitud": -80.6328,
        "tipo": "AGUA POTABLE",
        "subsector": "URBANO"
    },
    {
        "CUI": "2056438",
        "nombre": "AMPLIACIÓN DEL SISTEMA DE AGUA POTABLE - UPIS LUIS ANTONIO EGUIGUREN",
        "distrito": "PIURA",
        "provincia": "PIURA",
        "estado": "PARALIZADO",
        "causa": "Deficiencia en el expediente técnico",
        "avance_fisico": 84.14,
        "monto_inversion": 26864446.49,
        "beneficiarios": 9895,
        "fecha_paralizacion": "2014-10-21",
        "latitud": -5.2000,
        "longitud": -80.6300,
        "tipo": "AGUA POTABLE",
        "subsector": "URBANO"
    },
    {
        "CUI": "2090577",
        "nombre": "AMPLIACIÓN Y REHABILITACIÓN DE SISTEMAS DE AGUA POTABLE - TAMBOGRANDE",
        "distrito": "TAMBO GRANDE",
        "provincia": "PIURA",
        "estado": "PARALIZADO",
        "causa": "Deficiencia administrativa de la UE",
        "avance_fisico": 100.0,
        "monto_inversion": 58302488.20,
        "beneficiarios": 30036,
        "fecha_paralizacion": "2016-05-23",
        "latitud": -4.9333,
        "longitud": -80.3500,
        "tipo": "AGUA POTABLE",
        "subsector": "URBANO"
    },
    {
        "CUI": "2376184",
        "nombre": "MEJORAMIENTO DE CALIDAD DE AGUA POTABLE - PTAP SULLANA",
        "distrito": "SULLANA",
        "provincia": "SULLANA",
        "estado": "PARALIZADO",
        "causa": "Resolución de Contrato",
        "avance_fisico": 18.91,
        "monto_inversion": 242928460.00,
        "beneficiarios": 243621,
        "fecha_paralizacion": "2024-10-05",
        "latitud": -4.9039,
        "longitud": -80.6853,
        "tipo": "AGUA POTABLE",
        "subsector": "URBANO"
    },
    {
        "CUI": "2148113",
        "nombre": "MEJORAMIENTO DEL COLECTOR SAN MIGUEL",
        "distrito": "BELLAVISTA",
        "provincia": "SULLANA",
        "estado": "POR CERRAR",
        "causa": "Paralizada - Permanente",
        "avance_fisico": 97.0,
        "monto_inversion": 18764626.74,
        "beneficiarios": 73089,
        "fecha_paralizacion": "2014-12-31",
        "latitud": -4.9000,
        "longitud": -80.6800,
        "tipo": "ALCANTARILLADO",
        "subsector": "URBANO"
    },
    {
        "CUI": "2056440",
        "nombre": "MEJORAMIENTO Y AMPLIACIÓN DE AGUA POTABLE - QUERECOTILLO",
        "distrito": "QUERECOTILLO",
        "provincia": "SULLANA",
        "estado": "PARALIZADO",
        "causa": "Deficiencia en el expediente técnico",
        "avance_fisico": 97.0,
        "monto_inversion": 39758247.66,
        "beneficiarios": 13477,
        "fecha_paralizacion": "2015-09-26",
        "latitud": -4.8333,
        "longitud": -80.4500,
        "tipo": "AGUA POTABLE",
        "subsector": "RURAL"
    },
    {
        "CUI": "2436071",
        "nombre": "REHABILITACIÓN DE AGUA POTABLE - LOCALIDAD PROGRESO KM 65",
        "distrito": "HUARMACA",
        "provincia": "HUANCABAMBA",
        "estado": "SUSPENDIDO",
        "causa": "Residentes declinaron firma de contratos",
        "avance_fisico": 76.47,
        "monto_inversion": 279696.88,
        "beneficiarios": 176,
        "fecha_paralizacion": "2019-12-03",
        "latitud": -5.2383,
        "longitud": -79.4500,
        "tipo": "AGUA POTABLE",
        "subsector": "RURAL"
    },
    {
        "CUI": "2436074",
        "nombre": "REHABILITACIÓN DE AGUA POTABLE - LOCALIDAD HUALAPAMPA",
        "distrito": "HUARMACA",
        "provincia": "HUANCABAMBA",
        "estado": "SUSPENDIDO",
        "causa": "Residentes declinaron firma de contratos",
        "avance_fisico": 65.37,
        "monto_inversion": 493314.41,
        "beneficiarios": 368,
        "fecha_paralizacion": "2019-12-03",
        "latitud": -5.2400,
        "longitud": -79.4550,
        "tipo": "AGUA POTABLE",
        "subsector": "RURAL"
    },
    {
        "CUI": "2436483",
        "nombre": "REHABILITACIÓN DE AGUA POTABLE - LOCALIDAD SAN ISIDRO",
        "distrito": "FRIAS",
        "provincia": "AYABACA",
        "estado": "SUSPENDIDO",
        "causa": "Residente con rendición observada",
        "avance_fisico": 71.58,
        "monto_inversion": 101827.07,
        "beneficiarios": 107,
        "fecha_paralizacion": "2020-01-06",
        "latitud": -4.6500,
        "longitud": -79.7167,
        "tipo": "AGUA POTABLE",
        "subsector": "RURAL"
    },
    {
        "CUI": "CI44403",
        "nombre": "CREACIÓN DEL SERVICIO DE AGUA POTABLE - URB. LOMAS DE PIURA",
        "distrito": "CURA MORI",
        "provincia": "PIURA",
        "estado": "PARALIZADO",
        "causa": "Paralizado en preinversión",
        "avance_fisico": 0.0,
        "monto_inversion": 55206700.00,
        "beneficiarios": 9255,
        "fecha_paralizacion": "2020-01-01",
        "latitud": -5.1667,
        "longitud": -80.6000,
        "tipo": "AGUA POTABLE",
        "subsector": "URBANO"
    }
]

# Convertir a DataFrame
df_proyectos = pd.DataFrame(proyectos_data)

# Calcular años de retraso
def calcular_retraso(fecha_str):
    if fecha_str and fecha_str != "Por definir":
        try:
            fecha = pd.to_datetime(fecha_str)
            return round((pd.Timestamp.now() - fecha).days / 365, 1)
        except:
            return 0
    return 0

df_proyectos['anos_retraso'] = df_proyectos['fecha_paralizacion'].apply(calcular_retraso)

# ============================================
# INDICADORES DE BRECHA - PIURA (ENAPRES 2024)
# ============================================
indicadores_piura = {
    "poblacion_total": 1958.148,
    "poblacion_acceso_agua": 1604.277,
    "brecha_agua_miles": 353.871,
    "brecha_agua_porcentaje": 18.07,
    "poblacion_acceso_alcantarillado": 1211.789,
    "brecha_alcantarillado_miles": 746.359,
    "brecha_alcantarillado_porcentaje": 38.12,
    "agua_segura_porcentaje": 9.54,
    "capacitacion_agua_porcentaje": 80.66,
    "pago_mensual_operacion": 9.54,
    "practicas_adecuadas_agua": 76.81,
    "pago_voluntario_porcentaje": 81.23,
}

# Coordenadas de capitales de provincia
capitales = {
    "PIURA": [-5.1945, -80.6328],
    "SULLANA": [-4.9039, -80.6853],
    "SECHURA": [-5.5576, -80.8222],
    "HUANCABAMBA": [-5.2383, -79.4500],
    "AYABACA": [-4.6500, -79.7167],
    "PAITA": [-5.0892, -81.1144],
    "MORROPON": [-5.1864, -79.9700]
}

# Brecha por provincia
brecha_por_provincia = {
    "PIURA": {"brecha_agua": 18.5, "brecha_alcantarillado": 39.2, "beneficiarios_afectados": 89000},
    "SULLANA": {"brecha_agua": 19.2, "brecha_alcantarillado": 41.5, "beneficiarios_afectados": 156000},
    "SECHURA": {"brecha_agua": 16.8, "brecha_alcantarillado": 35.7, "beneficiarios_afectados": 42000},
    "HUANCABAMBA": {"brecha_agua": 22.5, "brecha_alcantarillado": 48.3, "beneficiarios_afectados": 35000},
    "AYABACA": {"brecha_agua": 24.1, "brecha_alcantarillado": 52.6, "beneficiarios_afectados": 28000},
    "PAITA": {"brecha_agua": 15.4, "brecha_alcantarillado": 32.1, "beneficiarios_afectados": 31000},
    "MORROPON": {"brecha_agua": 20.3, "brecha_alcantarillado": 44.8, "beneficiarios_afectados": 22000},
}

# Colores por estado
COLOR_MAP = {
    "PARALIZADO": "#e74c3c",
    "SUSPENDIDO": "#f39c12",
    "POR CERRAR": "#f1c40f",
    "EN EJECUCIÓN": "#2ecc71",
    "CONCLUIDO": "#3498db"
}