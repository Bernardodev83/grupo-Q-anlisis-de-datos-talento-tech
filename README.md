# 🌿 EcoAnalytics Pro: Inteligencia Ambiental Industrial
### Análisis de Microdatos del DANE (EAS) | 2019 - 2023

## 📌 Descripción del Proyecto
Este sistema de **Inteligencia de Datos** permite visualizar y analizar el desempeño ambiental del sector industrial en Colombia. Utilizando los microdatos de la Encuesta Ambiental Industrial (EAS) del DANE, la herramienta transforma filas de datos complejos en indicadores visuales para la toma de decisiones estratégicas.

El proyecto nace de la necesidad de entender cómo la eficiencia en el uso de recursos (Agua y Energía) impacta la sostenibilidad y cómo factores externos, como la pandemia del COVID-19, alteraron la dinámica productiva del país.

---

## 🚀 Funcionalidades Principales

### 1. ⚡ Eficiencia Energética y 💧 Consumo de Agua
- **Visualización Dinámica:** Uso de indicadores tipo "Velocímetro" (Gauges) para medir el desempeño por año.
- **Filtros Inteligentes:** Capacidad de comparar la inversión ambiental frente al consumo real de recursos.

### 2. 🦠 Análisis de Impacto COVID-19
- **Geolocalización:** Mapa de calor que muestra la intensidad de la pandemia en diferentes regiones de Colombia.
- **Correlación Industrial:** Gráficos que comparan las curvas de contagio con la caída/recuperación de la inversión ambiental.

### 3. 💡 Hallazgos y Estrategia
- **Diagnósticos Automáticos:** El sistema genera reportes basados en los datos (Estabilidad, Crisis o Recuperación).
- **Hoja de Ruta:** Sugerencias técnicas y gerenciales para mejorar la sostenibilidad.

---

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.x
- **Framework Web:** Streamlit
- **Procesamiento de Datos:** Pandas & NumPy
- **Visualización:** Plotly (Gráficos interactivos)
- **Gestión de Datos:** Excel (OpenPyXL) y CSV

---

## 📁 Estructura del Repositorio
- `app.py`: Archivo principal y menú de navegación.
- `pages/`: Módulos individuales para cada indicador ambiental.
- `datos/procesados/`: Archivos `.csv` optimizados y limpios (2019-2023).
- `requirements.txt`: Lista de dependencias necesarias para la ejecución.

---

## 👤 Autor
**Bernardo** - *Desarrollador y Analista de Datos*
- GitHub: [@Bernardodev83](https://github.com/Bernardodev83)

---

## 📝 Notas de Versión
*V1.0.0 - Implementación de filtros dinámicos, corrección de rutas de archivos `_final.csv` y optimización de visualizaciones Plotly.*