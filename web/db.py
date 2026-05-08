import sqlite3
import hashlib
import os
import random
import time

print("DB path:", os.path.abspath("usuarios.db"))

conn = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tabla 
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    codigo_recuperacion TEXT,
    codigo_expira INTEGER
)
""")
conn.commit()

try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN codigo_recuperacion TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN codigo_expira INTEGER")
except:
    pass

conn.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Crear usuario
def crear_usuario(correo, password):
    correo = correo.strip().lower()

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

# Recuperacón de contraseña
def guardar_codigo_recuperacion(correo):
    correo = correo.strip().lower()
    codigo = str(random.randint(100000, 999999))
    expiracion = int(time.time()) + 600  # 10 min

    cursor.execute(
        """
        UPDATE usuarios
        SET codigo_recuperacion = ?, codigo_expira = ?
        WHERE correo = ?
        """,
        (codigo, expiracion, correo)
    )
    conn.commit()

    if cursor.rowcount > 0:
        return codigo
    return None


def verificar_codigo(correo, codigo):
    correo = correo.strip().lower()

    cursor.execute(
        """
        SELECT codigo_recuperacion, codigo_expira
        FROM usuarios
        WHERE correo = ?
        """,
        (correo,)
    )

    resultado = cursor.fetchone()

    if not resultado:
        return False

    codigo_db, expira = resultado

    if not codigo_db or not expira:
        return False

    return codigo_db == codigo and int(time.time()) <= expira


def cambiar_password(correo, nueva_password):
    correo = correo.strip().lower()

    cursor.execute(
        """
        UPDATE usuarios
        SET password = ?, codigo_recuperacion = NULL, codigo_expira = NULL
        WHERE correo = ?
        """,
        (hash_password(nueva_password), correo)
    )

    conn.commit()
    return cursor.rowcount > 0
print("FUNCIONES CARGADAS OK")