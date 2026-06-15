Para ejecutar el proyecto en Visual Studio Code, se debe abrir una terminal y seguir los pasos mostrados:

1. Crear entorno virtual: python -m venv venv
2. Activar entorno virtual: venv\Scripts\actívate (Windows) y source venv/bin/actívate (Linux/Mac)
3. Instalar dependencias: pip install -r requirements.txt y pip install flask flask-cors pandas folium
4. Ejecutar la API: python app.py
   
Se mostrarán diversos Endpoints, a los cuales se pueden acceder desde el puerto 5000, que contienen información sobre los proyectos y el mapa georreferenciado de estos (dashboard).
