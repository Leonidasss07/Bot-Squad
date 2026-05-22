import smtplib
import streamlit as st


from email.message import EmailMessage
from email.headerregistry import Address

EMAIL_EMISOR = st.secrets["EMAIL_EMISOR"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

def enviar_codigo(destinatario, codigo):
    mensaje = EmailMessage()
    mensaje["Subject"] = "Codigo Nova Music"
    mensaje["From"] = EMAIL_EMISOR
    mensaje["To"] = destinatario

    cuerpo = f"""
Hola,

Tu codigo para restablecer tu password es:

{codigo}

Este codigo expira en 10 minutos.

Nova Music
"""

    mensaje.set_content(cuerpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_EMISOR, EMAIL_PASSWORD)
        smtp.send_message(mensaje)