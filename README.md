# 🌿 EcoAnalytics Pro: Inteligencia Ambiental Industrial (2019-2023)

**Proyecto Final - Nivel Integrador** **Bootcamp de Análisis de Datos**

---

## 👥 Equipo de Desarrollo
* **Bernardo (Bernardodev83)** - *Líder de Arquitectura y Backend*
* **compañeros 2** - *[Completar Rol]*
* **Compañero 3** - *[Completar Rol]*
* **Compañero 4** - *[Completar Rol]*
* **Compañero 5** - *[Completar Rol]*

---

## 🚀 Descripción del Proyecto
EcoAnalytics Pro es una plataforma interactiva de **Business Intelligence** diseñada para analizar la transición productiva y el impacto ambiental de la industria colombiana. Utilizando microdatos oficiales del **DANE**, el sistema permite visualizar la relación entre la inversión económica en protección ambiental y el consumo de recursos críticos (agua y energía) antes, durante y después de la pandemia por COVID-19.

### 🔗 Aplicación en Vivo
Puedes acceder al dashboard interactivo aquí:  
👉 **[https://grupo-q-anlisis-de-datos-talento-tech.streamlit.app/]**

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.14
* **Base de Datos:** MySQL / MariaDB (Hosteada en Aiven Cloud)
* **Procesamiento de Datos:** Pandas, NumPy
* **Visualización:** Plotly Express
* **Interfaz de Usuario:** Streamlit
* **Gestión de Entorno:** Python-dotenv, SQLAlchemy

---

## 📂 Estructura del Repositorio
* `Inicio.py`: Punto de entrada de la aplicación y navegación principal.
* `database_schema.sql`: **(Archivo SQL Principal)** Contiene el diseño de la tabla y consultas analíticas complejas.
* `pages/`: Módulos de análisis (Dashboard, Agua, Energía, COVID, Simulador, Hallazgos).
* `scripts/`: Herramientas de limpieza (`limpiador_maestro.py`) y carga de datos (`db_uploader.py`).
* `utils/`: Lógica de conexión resiliente a la base de datos.
* `data/`: Almacenamiento de microdatos originales y procesados (CSV).
* `requirements.txt`: Librerías necesarias para ejecutar el proyecto.

---

## 🗄️ Gestión de Base de Datos (Punto 3 del Proyecto)
El sistema utiliza una arquitectura de datos en la nube. El archivo `database_schema.sql` adjunto documenta:
1. **Estructura DDL:** Creación de tablas normalizadas.
2. **Consultas DML:** Análisis de promedios de consumo, sumatorias de inversión y rankings de eficiencia por sector económico, integrando SQL directamente con el motor de análisis de Python.

---

## ⚙️ Instalación y Uso Local
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar archivo `.env` con las credenciales de la base de datos.
4. Ejecutar la aplicación: `streamlit run app.py`

---

## 💡 Conclusiones Técnicas
Este proyecto demuestra la integración exitosa de un pipeline **ETL** completo, desde la ingesta de microdatos crudos hasta la visualización estratégica en la nube, cumpliendo con los estándares de un **Nivel Integrador** en Ciencia, Tecnología e Innovación.