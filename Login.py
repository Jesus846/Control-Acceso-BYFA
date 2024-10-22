import tkinter as tk
from tkinter import messagebox
import mysql.connector
import Dashboard  
import Registro     
import PanelSeguridad  
import RHPanel     

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

def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    if usuario and contrasena:
        cursor.execute("SELECT * FROM usuarios WHERE Usuario = %s AND Contrasena = %s", (usuario, contrasena))
        resultado = cursor.fetchone()
        
        if resultado:
            cargo = resultado[4]  

            messagebox.showinfo("Éxito", f"Bienvenido, {usuario}!")
            root.destroy()  
            
            if cargo == "Admin":
                Dashboard.main()  
            elif cargo == "Seguridad":
                PanelSeguridad.main()  
            elif cargo == "Recursos Humanos":
                RHPanel.main()  
            else:
                messagebox.showwarning("Error", "Cargo no reconocido.")
        else:
            messagebox.showwarning("Error", "Usuario o contraseña incorrectos. Inténtalo de nuevo.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

def abrir_registro():
    Registro.abrir_ventana_registro()  

def on_closing():
    if messagebox.askokcancel("Salir", "¿Quieres salir?"):
        conn.close()  
        root.destroy()

root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("600x400")
root.configure(bg="#E6E6FA")  

centrar_ventana(root, 600, 400)

label_usuario = tk.Label(root, text="Nombre de usuario:", font=("Arial", 14), bg="#E6E6FA", fg="#333")
label_usuario.pack(pady=10)
entry_usuario = tk.Entry(root, font=("Arial", 14), width=30, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="groove")
entry_usuario.pack(pady=10)

label_contrasena = tk.Label(root, text="Contraseña:", font=("Arial", 14), bg="#E6E6FA", fg="#333")
label_contrasena.pack(pady=10)
entry_contrasena = tk.Entry(root, show="*", font=("Arial", 14), width=30, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="groove")
entry_contrasena.pack(pady=10)

btn_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
btn_iniciar_sesion.pack(pady=20)

btn_registrar = tk.Button(root, text="Registrar usuario", command=abrir_registro, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
btn_registrar.pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_closing)  
root.mainloop()
