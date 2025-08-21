
# 📌 API de Gestión de Tareas

API RESTful construida con **FastAPI** y **PostgreSQL** para la gestión de usuarios, tareas y categorías.  
Este backend está diseñado para interactuar con un frontend en **React + Vite**.  

La arquitectura sigue el **patrón Repository**, lo que facilita la separación de la lógica de negocio y la capa de acceso a datos, mejorando la mantenibilidad y escalabilidad del proyecto.

---

## 🚀 Tecnologías utilizadas
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel / SQLAlchemy](https://sqlmodel.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Uvicorn](https://www.uvicorn.org/)

---

## ⚙️ Instalación y ejecución local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/RocioDure12/Basic_Api.git
   cd Basic_Api

2. **Crea y activa un entorno virtual:**
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

3. **Instala dependencias:**
    pip install -r requirements.txt

4. **Crea un archivo .env con tu configuración:**
    DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/app_db
    SECRET_KEY=tu_secret_key

5. **Inicia el servidor:**
    uvicorn app.main:app --reload

### 🔐 Seguridad y Autenticación

- ✅ **OAuth2 con Password Flow** – Genera tokens seguros.  
- ✅ **JWT con Cookies HTTPOnly** – Protege contra ataques XSS (adaptación de OAuth2 de FastAPI para lectura desde cookies).  
- ✅ **Cookies seguras** (`HttpOnly`, `Secure`) – Reducen riesgos de robo de sesión.  
- ✅ **Gestión de roles** (admin / user) – Permisos diferenciados.  
- ✅ **Verificación por email** – Previene spam y cuentas falsas.  


    
📖 Documentación

La documentación interactiva de la API está disponible en:

-Swagger UI → http://localhost:8000/docs

-ReDoc → http://localhost:8000/redoc

🔗 URLs de la aplicación

    -API Producción: https://taskplanner-api.onrender.com/

    -Frontend Producción: https://task-planner-wajw.onrender.com

    -API Local: http://localhost:8000

    -Frontend Local: http://localhost:5173

📂 Arquitectura

    La aplicación sigue el patrón Repository, que separa la lógica de negocio de la persistencia de datos.
    Esto facilita el mantenimiento, pruebas unitarias y escalabilidad del sistema.


✨ Notas finales

    -Todas las respuestas siguen el formato JSON.

    -Backend y frontend están completamente integrados.

    -No es un simple CRUD: incluye autenticación robusta, verificación de usuarios y control de roles.


