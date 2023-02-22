# Pasos para levantar proyecto back

# Base de datos
La base de datos esta con sqlite, se encuentra en el archivo accounts.sql, no es necesario hacer nada para activarla

# Crear entorno virtual
El back esta realizado con python 3.9 y flask por lo que para correrlo sera necesario crear un entorno virtual, en la terminal de command prompt o powershell lo puedes crear con el comando: python -m venv env

# Activar entorno virtual
Activa el entorno virtual con el siguiente comando: .\env\Scripts\activate

# Instalar dependencias
Ahora toca instalar las dependencias del proyecto, lo puedes realizar con el comando: pip install requirements.txt

# Correr el proyecto
Una vez hecho todo lo anterior, ejecuta el siguiente comando para que el proyecto empiece a funcionar: flask run -p 5001