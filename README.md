# 🌍 EcoAnalytics Pro: Inteligencia Ambiental para la Industria Colombiana

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Data Source](https://img.shields.io/badge/Fuente-DANE%20Colombia-orange)

## 🎯 Intención del Proyecto
En un contexto de crisis climática global, la transparencia en el uso de recursos industriales es vital. **EcoAnalytics Pro** nace con el propósito de **democratizar el acceso a los microdatos del DANE**, transformando tablas complejas de la Encuesta Anual de Servicios (EAS) en visualizaciones estratégicas.

La intención principal es permitir que analistas, estudiantes y entidades gubernamentales puedan:
1. **Identificar ineficiencias:** Detectar qué sectores económicos presentan un consumo energético desproporcionado.
2. **Medir el compromiso real:** Evaluar si el crecimiento económico de las empresas va de la mano con una inversión real en gestión ambiental.
3. **Facilitar la Auditoría Social:** Proveer una herramienta de código abierto para que cualquier ciudadano pueda auditar el desempeño ambiental industrial de los últimos 5 años (2019-2023).

---

## 🚀 Funcionalidades Clave

* **⚡ Dashboard de Eficiencia:** Análisis dinámico de consumo en kWh, permitiendo comparar el impacto entre más de 50 sectores económicos.
* **🚀 Índice de Desempeño Ambiental (ICA):** Un indicador sintético que mide la "salud ambiental" de la industria. No solo vemos cuánto gastan, sino qué tan eficiente es su inversión en protección del entorno.
* **🗺️ Mapeo de Proporcionalidad (Treemaps):** Visualización jerárquica para entender de un vistazo qué industrias dominan la matriz de consumo energético nacional.
* **📅 Motor de Consulta Histórica:** Arquitectura capaz de procesar y filtrar bases de datos masivas por año de manera instantánea.

---

## 🛠️ Arquitectura Técnica
El proyecto sigue un patrón de diseño **modular**, separando la lógica de conexión, el procesamiento de datos y la interfaz de usuario:

* **Frontend:** Streamlit para una experiencia de usuario (UX) fluida y reactiva.
* **Procesamiento:** Pandas para la limpieza y normalización de microdatos heterogéneos del DANE.
* **Gráficos:** Plotly (Gauge, Bar & Treemaps) para visualizaciones interactivas de alto impacto.

---

## 📊 Metodología del Indicador ICA
Para este proyecto, el **Puntaje ICA (pts)** se define como la *Tasa de Intensidad Ambiental (TIA)*. 
> **Fórmula:** `(Inversión en Gestión Ambiental / Gastos Totales) * Factor de Normalización`

Esta métrica permite nivelar sectores con presupuestos muy diferentes y evaluar su esfuerzo relativo en sostenibilidad en una escala de **0 a 100 puntos**.

---

## 📂 Estructura de Archivos
```text
├── Inicio.py                # Dashboard principal y bienvenida
├── requirements.txt         # Librerías necesarias (Pandas, Plotly, etc.)
├── data/                    # Microdatos originales y procesados (CSV/XLSX)
├── pages/                   # Módulos especializados de análisis
│   └── 03_⚡_Eficiencia_Energetica.py  # Motor de análisis energético e ICA
└── utils/                   # Utilidades de conexión y limpieza

---



