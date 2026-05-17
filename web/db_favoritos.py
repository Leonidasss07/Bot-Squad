import sqlite3
import os

DB_PATH = "data/favoritos.db"

def _conectar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def crear_tablas():
    conn = _conectar()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS canciones_favoritas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            nombre TEXT NOT NULL,
            artista TEXT,
            imagen_url TEXT,
            url TEXT,
            audio_url TEXT,
            reproducciones TEXT,
            genero TEXT,
            fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(usuario, nombre, artista)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS artistas_favoritos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            nombre TEXT NOT NULL,
            imagen_url TEXT,
            url TEXT,
            oyentes TEXT,
            fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(usuario, nombre)
        )
    """)

    conn.commit()
    conn.close()


# Canciones

def agregar_cancion_favorita(usuario, nombre, artista="", imagen_url="",
                              url="", audio_url="", reproducciones="", genero=""):
    crear_tablas()
    conn = _conectar()
    try:
        conn.execute("""
            INSERT OR IGNORE INTO canciones_favoritas
            (usuario, nombre, artista, imagen_url, url, audio_url, reproducciones, genero)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (usuario, nombre, artista, imagen_url, url, audio_url, str(reproducciones), genero))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def eliminar_cancion_favorita(usuario, nombre, artista=""):
    crear_tablas()
    conn = _conectar()
    conn.execute(
        "DELETE FROM canciones_favoritas WHERE usuario=? AND nombre=? AND artista=?",
        (usuario, nombre, artista)
    )
    conn.commit()
    conn.close()


def obtener_canciones_favoritas(usuario):
    crear_tablas()
    conn = _conectar()
    rows = conn.execute(
        "SELECT * FROM canciones_favoritas WHERE usuario=? ORDER BY fecha_agregado DESC",
        (usuario,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def es_cancion_favorita(usuario, nombre, artista=""):
    crear_tablas()
    conn = _conectar()
    row = conn.execute(
        "SELECT 1 FROM canciones_favoritas WHERE usuario=? AND nombre=? AND artista=?",
        (usuario, nombre, artista)
    ).fetchone()
    conn.close()
    return row is not None


# Artistas

def agregar_artista_favorito(usuario, nombre, imagen_url="", url="", oyentes=""):
    crear_tablas()
    conn = _conectar()
    try:
        conn.execute("""
            INSERT OR IGNORE INTO artistas_favoritos
            (usuario, nombre, imagen_url, url, oyentes)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario, nombre, imagen_url, url, str(oyentes)))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def eliminar_artista_favorito(usuario, nombre):
    crear_tablas()
    conn = _conectar()
    conn.execute(
        "DELETE FROM artistas_favoritos WHERE usuario=? AND nombre=?",
        (usuario, nombre)
    )
    conn.commit()
    conn.close()


def obtener_artistas_favoritos(usuario):
    crear_tablas()
    conn = _conectar()
    rows = conn.execute(
        "SELECT * FROM artistas_favoritos WHERE usuario=? ORDER BY fecha_agregado DESC",
        (usuario,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def es_artista_favorito(usuario, nombre):
    crear_tablas()
    conn = _conectar()
    row = conn.execute(
        "SELECT 1 FROM artistas_favoritos WHERE usuario=? AND nombre=?",
        (usuario, nombre)
    ).fetchone()
    conn.close()
    return row is not None