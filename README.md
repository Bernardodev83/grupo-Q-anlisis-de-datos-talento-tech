# 🌿 EcoAnalytics Pro: Inteligencia Ambiental con Datos del DANE

**EcoAnalytics Pro** es una plataforma de análisis de datos (Business Intelligence) diseñada para visualizar y simular el impacto ambiental de la industria en Colombia. Utiliza microdatos oficiales del **DANE** para ofrecer una visión clara sobre el consumo de recursos y la inversión en protección ambiental.

---

## 🚀 Características Principales

* **Dashboard Híbrido:** Visualización de inversión ambiental con soporte para base de datos en la nube (Aiven/MySQL) y respaldo local (CSV).
* **Análisis Hídrico y Energético:** Seguimiento detallado del consumo de agua y energía mediante gráficos de burbujas, treemaps y velocímetros de eficiencia (ICA).
* **Módulo COVID-19:** Cruce de datos históricos con el impacto de la pandemia mediante análisis de archivos Excel y mapas de dispersión geográfica.
* **Simulador de Impacto:** Herramienta interactiva para proyectar ahorros económicos y ecológicos basados en promedios reales de la industria.
* **Arquitectura Modular:** Código organizado en componentes, servicios de conexión y reportes independientes para facilitar el mantenimiento.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14
* **Framework Web:** Streamlit
* **Visualización:** Plotly Express & Graph Objects
* **Base de Datos:** MySQL (Aiven Cloud)
* **ORM/Conectores:** SQLAlchemy & MySQL-Connector
* **Procesamiento:** Pandas & OpenPyXL

---

## 📂 Estructura del Proyecto

```text
.
├── app.py                # Punto de entrada de la aplicación
├── data/                 # Archivos CSV procesados y Excel originales
├── pages/                # Módulos de la interfaz (01 al 06)
├── scripts/              # Herramientas de carga de datos (db_uploader.py)
├── utils/                # Lógica de conexión y funciones compartidas
├── requirements.txt      # Dependencias del sistema
└── .env                  # Variables de entorno (No incluido en el repo)


Gemini ha dicho
¡Excelente, Bernardo! El requirements.txt ya es el primer paso para que tu app viva en la nube. Mientras esa terminal sigue procesando los datos del 2020 (que son bastantes), vamos a crear el README.md.

Este archivo es la "portada" de tu repositorio en GitHub. Un buen README hace que tu proyecto pase de verse como un ejercicio de clase a un producto de ingeniería de datos profesional.

Crea un archivo llamado README.md en la raíz de tu proyecto y pega esto:

Markdown
# 🌿 EcoAnalytics Pro: Inteligencia Ambiental con Datos del DANE

**EcoAnalytics Pro** es una plataforma de análisis de datos (Business Intelligence) diseñada para visualizar y simular el impacto ambiental de la industria en Colombia. Utiliza microdatos oficiales del **DANE** para ofrecer una visión clara sobre el consumo de recursos y la inversión en protección ambiental.

---

## 🚀 Características Principales

* **Dashboard Híbrido:** Visualización de inversión ambiental con soporte para base de datos en la nube (Aiven/MySQL) y respaldo local (CSV).
* **Análisis Hídrico y Energético:** Seguimiento detallado del consumo de agua y energía mediante gráficos de burbujas, treemaps y velocímetros de eficiencia (ICA).
* **Módulo COVID-19:** Cruce de datos históricos con el impacto de la pandemia mediante análisis de archivos Excel y mapas de dispersión geográfica.
* **Simulador de Impacto:** Herramienta interactiva para proyectar ahorros económicos y ecológicos basados en promedios reales de la industria.
* **Arquitectura Modular:** Código organizado en componentes, servicios de conexión y reportes independientes para facilitar el mantenimiento.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14
* **Framework Web:** Streamlit
* **Visualización:** Plotly Express & Graph Objects
* **Base de Datos:** MySQL (Aiven Cloud)
* **ORM/Conectores:** SQLAlchemy & MySQL-Connector
* **Procesamiento:** Pandas & OpenPyXL

---

## 📂 Estructura del Proyecto

```text
.
├── app.py                # Punto de entrada de la aplicación
├── data/                 # Archivos CSV procesados y Excel originales
├── pages/                # Módulos de la interfaz (01 al 06)
├── scripts/              # Herramientas de carga de datos (db_uploader.py)
├── utils/                # Lógica de conexión y funciones compartidas
├── requirements.txt      # Dependencias del sistema
└── .env                  # Variables de entorno (No incluido en el repo)




⚙️ Instalación y Uso
Clonar el repositorio:
--------------////////////////------------------
Bash
git clone [https://github.com/tu-usuario/ecoanalytics-pro.git](https://github.com/tu-usuario/ecoanalytics-pro.git)
Instalar dependencias:

Bash
pip install -r requirements.txt
Configurar variables de entorno:
Crea un archivo .env con tus credenciales de Aiven (Host, User, Password, Port, DB_Name).

Ejecutar la aplicación:

Bash
streamlit run app.py
👤 Autor
Bernardo (Bernardodev83) Desarrollador y Analista de Datos en formación.