from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from jwt import PyJWTError

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_muy_segura"  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="Sistema de Gestión de Pacientes")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Modelos
class MedicoBase(BaseModel):
    nombre: str
    email: EmailStr
    especialidad: str

class MedicoCreate(MedicoBase):
    password: str

class Medico(MedicoBase):
    id: int

class PacienteBase(BaseModel):
    nombre: str
    edad: int
    historialMedico: str

class Paciente(PacienteBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

# Configuración de la base de datos
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "clinica")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )

# Funciones de seguridad
def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def obtener_hash_password(password):
    return pwd_context.hash(password)

def crear_token_acceso(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def obtener_medico_actual(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM medicos WHERE email = %s", (email,))
        medico = cur.fetchone()
        if medico is None:
            raise credentials_exception
        return medico
    finally:
        cur.close()
        conn.close()

# Rutas
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("static/index.html")

@app.post("/registro", response_model=Medico)
async def registrar_medico(medico: MedicoCreate):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        hash_password = obtener_hash_password(medico.password)
        cur.execute(
            """
            INSERT INTO medicos (nombre, email, password, especialidad)
            VALUES (%s, %s, %s, %s)
            RETURNING id, nombre, email, especialidad
            """,
            (medico.nombre, medico.email, hash_password, medico.especialidad)
        )
        nuevo_medico = cur.fetchone()
        conn.commit()
        return nuevo_medico
    except psycopg2.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )
    finally:
        cur.close()
        conn.close()

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM medicos WHERE email = %s", (form_data.username,))
        medico = cur.fetchone()
        if not medico or not verificar_password(form_data.password, medico["password"]):
            raise HTTPException(
                status_code=400,
                detail="Email o contraseña incorrectos"
            )
        
        access_token = crear_token_acceso({"sub": medico["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        cur.close()
        conn.close()

@app.post("/pacientes/", response_model=Paciente)
async def crear_paciente(paciente: PacienteBase, medico: dict = Depends(obtener_medico_actual)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO pacientes (nombre, edad, historialMedico)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (paciente.nombre, paciente.edad, paciente.historialMedico)
        )
        nuevo_paciente = cur.fetchone()
        conn.commit()
        return nuevo_paciente
    finally:
        cur.close()
        conn.close()

@app.get("/pacientes/", response_model=List[Paciente])
async def obtener_pacientes(medico: dict = Depends(obtener_medico_actual)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM pacientes")
        pacientes = cur.fetchall()
        return pacientes
    finally:
        cur.close()
        conn.close()

@app.get("/pacientes/{id_paciente}", response_model=Paciente)
async def obtener_paciente(id_paciente: int, medico: dict = Depends(obtener_medico_actual)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM pacientes WHERE id = %s", (id_paciente,))
        paciente = cur.fetchone()
        if paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return paciente
    finally:
        cur.close()
        conn.close()

@app.delete("/pacientes/{id_paciente}")
async def eliminar_paciente(id_paciente: int, medico: dict = Depends(obtener_medico_actual)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM pacientes WHERE id = %s RETURNING id", (id_paciente,))
        eliminado = cur.fetchone()
        if eliminado is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        conn.commit()
        return {"mensaje": "Paciente eliminado correctamente"}
    finally:
        cur.close()
        conn.close()