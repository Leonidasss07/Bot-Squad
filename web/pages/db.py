import sqlite3
import hashlib

conn = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# Encriptar contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Crear usuario
def crear_usuario(correo, password):
    correo = correo.strip().lower()  # 👈 evita duplicados raros

    try:
        cursor.execute(
            "INSERT INTO usuarios (correo, password) VALUES (?, ?)",
            (correo, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Iniciar sesión
def iniciar_sesion(correo, password):
    correo = correo.strip().lower()

    cursor.execute(
        "SELECT * FROM usuarios WHERE correo=? AND password=?",
        (correo, hash_password(password))
    )
    return cursor.fetchone()