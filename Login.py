import tkinter as tk
from tkinter import messagebox
import mysql.connector
import Dashboard  # Importa tu archivo Dashboard.py
import Registro    # Importa tu archivo Registro.py  # Importa el panel de administración
import PanelSeguridad  # Importa el panel de seguridad
import RHPanel     # Importa el panel de RH

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",  # Cambia por la IP del servidor o 'localhost' si es local
    user="root",        # Usuario de MySQL
    password="",        # Contraseña de MySQL
    database="BYFA_CONTROL"  # Nombre de la base de datos
)
cursor = conn.cursor()

def centrar_ventana(ventana, ancho, alto):
    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Calcular la posición x e y para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    # Establecer la geometría de la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Función para verificar las credenciales del usuario e iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    if usuario and contrasena:
        # Verificar si el usuario existe y la contraseña es correcta
        cursor.execute("SELECT * FROM usuarios WHERE Usuario = %s AND Contrasena = %s", (usuario, contrasena))
        resultado = cursor.fetchone()
        
        if resultado:
            # Extraer el cargo del usuario
            cargo = resultado[4]  # Asumiendo que el cargo está en la tercera columna

            # Si la autenticación es correcta, redirigir a la página principal según el cargo
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario}!")
            root.destroy()  # Cierra la ventana actual de inicio de sesión
            
            # Redirigir según el cargo
            if cargo == "Admin":
                Dashboard.main()  # Llama a la función main() de Dashboard.py
            elif cargo == "Seguridad":
                PanelSeguridad.main()  # Llama a la función main() de SeguridadPanel.py
            elif cargo == "Recursos Humanos":
                RHPanel.main()  # Llama a la función main() de RHPanel.py
            else:
                messagebox.showwarning("Error", "Cargo no reconocido.")
        else:
            messagebox.showwarning("Error", "Usuario o contraseña incorrectos. Inténtalo de nuevo.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

# Función para abrir la ventana de registro desde Registro.py
def abrir_registro():
    Registro.abrir_ventana_registro()  # Suponiendo que en el archivo Registro.py tienes una función para abrir la ventana de registro

# Crear la ventana principal de inicio de sesión
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("600x400")
root.configure(bg="#E6E6FA")  # Color de fondo lavanda

centrar_ventana(root, 600, 400)

# Etiqueta y campo de entrada para el nombre de usuario
label_usuario = tk.Label(root, text="Nombre de usuario:", font=("Arial", 14), bg="#E6E6FA", fg="#333")
label_usuario.pack(pady=10)
entry_usuario = tk.Entry(root, font=("Arial", 14), width=30, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="groove")
entry_usuario.pack(pady=10)

# Etiqueta y campo de entrada para la contraseña
label_contrasena = tk.Label(root, text="Contraseña:", font=("Arial", 14), bg="#E6E6FA", fg="#333")
label_contrasena.pack(pady=10)
entry_contrasena = tk.Entry(root, show="*", font=("Arial", 14), width=30, bg="#FFFFFF", fg="#000000", borderwidth=2, relief="groove")
entry_contrasena.pack(pady=10)

# Botón para iniciar sesión
btn_iniciar_sesion = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
btn_iniciar_sesion.pack(pady=20)

# Botón para abrir la ventana de registro
btn_registrar = tk.Button(root, text="Registrar usuario", command=abrir_registro, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
btn_registrar.pack(pady=20)

# Iniciar el loop principal de Tkinter
root.mainloop()

# Cerrar la conexión a la base de datos al cerrar el programa
conn.close()
