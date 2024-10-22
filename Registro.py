import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="BYFA_CONTROL"
)
cursor = conn.cursor()

def centrar_ventana(ventana, ancho, alto):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

fecha_registro = datetime.now()

def registrar_usuario(entry_nombre, entry_usuario, entry_contrasena, entry_acceso):
    personal = entry_nombre.get()
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    aceso = entry_acceso.get()

    if usuario and contrasena and aceso:
        cursor.execute("SELECT * FROM usuarios WHERE Usuario = %s", (usuario,))
        resultado = cursor.fetchone()

        if resultado:
            messagebox.showwarning("Advertencia", "El usuario ya existe. Por favor, elige otro nombre.")
        else:
            cursor.execute(
                "INSERT INTO usuarios (Nombre, Usuario, Contrasena, Cargo, Fecha) VALUES (%s, %s, %s, %s, %s)",
                (personal, usuario, contrasena, aceso, fecha_registro)
            )
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado con éxito")
            entry_nombre.delete(0, tk.END)
            entry_usuario.delete(0, tk.END)
            entry_contrasena.delete(0, tk.END)
            entry_acceso.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

def abrir_ventana_registro():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("800x600")
    ventana_registro.configure(bg="#FFA500")
    centrar_ventana(ventana_registro, 800, 600)

    label_personal = tk.Label(ventana_registro, text="Nombre del personal:", font=("Arial", 14))
    label_personal.pack(pady=15)
    entry_personal = tk.Entry(ventana_registro, font=("Arial", 14), width=30)
    entry_personal.pack(pady=10)

    label_usuario = tk.Label(ventana_registro, text="Nombre de usuario:", font=("Arial", 14))
    label_usuario.pack(pady=15)
    entry_usuario = tk.Entry(ventana_registro, font=("Arial", 14), width=30)
    entry_usuario.pack(pady=10)

    label_contrasena = tk.Label(ventana_registro, text="Contraseña:", font=("Arial", 14))
    label_contrasena.pack(pady=15)
    entry_contrasena = tk.Entry(ventana_registro, show="*", font=("Arial", 14), width=30)
    entry_contrasena.pack(pady=10)

    label_acceso = tk.Label(ventana_registro, text="Cargo:", font=("Arial", 14))
    label_acceso.pack(pady=15)
    entry_acceso = tk.Entry(ventana_registro, font=("Arial", 14), width=30)
    entry_acceso.pack(pady=10)

    btn_registrar = tk.Button(ventana_registro, text="Registrar Usuario", 
                              command=lambda: registrar_usuario(entry_personal, entry_usuario, entry_contrasena, entry_acceso),
                              font=("Arial", 14))
    btn_registrar.pack(pady=30)

def cerrar_conexion():
    conn.close()

if __name__ == "__main__":
    abrir_ventana_registro()
