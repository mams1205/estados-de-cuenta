
import smtplib


import os
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from datetime import datetime

import tkinter as tk
from tkinter import messagebox



def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def send_mail(ruta_archivo, value_sender_email, value_receiver_email, value_password):
    try:
        file_name = resource_path(f"{ruta_archivo}")
        base_file_name = os.path.basename(file_name)


        #sendmail
        # Configurar los detalles del correo electrónico
        sender_email = str(value_sender_email) #"bertha.segovia@slic-soluciones.com"
        receiver_email = str(value_receiver_email) #"pattotorres@gmail.com"
        subject = "Prueba IATI"#"Estado de Cuenta APG Química"
        body = f"""Estimado/a cliente
        Adjunto a este correo encontrará su estado de cuenta actualizado, donde se detallan las facturas pendientes de pago.
        Si tiene alguna pregunta, no dude en contactarnos.
        Le agradecemos su pronta atención a este asunto.
        Saludos cordiales"""
        password = str(value_password) #"MApdMS041816"

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        # print(sender_email, password)
        # Agregar el cuerpo del mensaje
        msg.attach(MIMEText(body, 'plain'))


        # Adjuntar el archivo CSV
        attachment = open(file_name, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {base_file_name}')
        msg.attach(part)

        # print("ennviando correo")
        # Conectar al servidor SMTP y enviar el correo electrónico
        server = smtplib.SMTP('send.one.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        
        server.sendmail(sender_email, receiver_email, text)
        server.quit()


    
    except Exception as e:
        titulo = "Error"
        mensaje = f"Error, No fue posible enviar el correo. Contactar a soporte: {str(e)}"
        messagebox.showerror(titulo, mensaje)
        print(e)

    

