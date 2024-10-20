import tkinter as tk
from tkinter import ttk
import mysql.connector

# Conexión a la base de datos MySQL
def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Cambia por la IP del servidor o 'localhost' si es local
            user="root",        # Usuario de MySQL
            password="",        # Contraseña de MySQL
            database="BYFA_CONTROL"  # Nombre de la base de datos
        )
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        exit()
#Cambiar ventana de registros 

# Función para cargar los usuarios en la tabla
def cargar_usuarios(cursor, tree):
    try:
        cursor.execute("SELECT Nombre ,Usuario,Contrasena, Cargo, Fecha FROM usuarios")
        usuarios = cursor.fetchall()
        
        # Limpiar la tabla antes de llenarla nuevamente
        for row in tree.get_children():
            tree.delete(row)
        
        # Insertar cada usuario en la tabla
        for usuario in usuarios:
            tree.insert("", "end", values=usuario)
    except mysql.connector.Error as err:
        print(f"Error al consultar la base de datos: {err}")

# Función para cerrar sesión
def cerrar_sesion(root):
    root.destroy()  # Cierra la ventana principal y termina la aplicación

# Función principal para mostrar el Dashboard
def main():
    # Conectar a la base de datos
    conn, cursor = conectar_db()
    

    
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Bienvenida")
    root.geometry("800x600")
    root.configure(bg="#E6E6FA")  
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
# Si deseas permitir que la ventana salga del modo de pantalla completa con la tecla "Esc"
#ventana.bind("<Escape>", lambda event: ventana.attributes("-fullscreen", False))

    # Etiqueta de bienvenida
    label_bienvenida = tk.Label(root, text="¡Bienvenido al sistema!", font=("Arial", 18), bg="#E6E6FA", fg="#333")
    label_bienvenida.pack(pady=20)

    # Crear el contenedor para la tabla
    frame_tabla = tk.Frame(root)
    frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    # Definir las columnas de la tabla
    tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Usuario", "Contraseña","Cargo", "Fecha de Registro"), show="headings", height=8)
    tree.pack(fill=tk.BOTH, expand=True)

    # Configurar los encabezados de la tabla
    tree.heading("Nombre", text="Nombre")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Cargo",text="Cargo")
    tree.heading("Contraseña", text="Contraseña")
    tree.heading("Fecha de Registro", text="Fecha de Registro")
    

    # Ajustar el ancho de las columnas
    tree.column("Nombre", anchor="center", width=250, stretch=tk.YES)
    tree.column("Usuario", anchor="center", width=250, stretch=tk.YES)
    tree.column("Contraseña", anchor="center", width=200, stretch=tk.YES)
    tree.column("Cargo", anchor="center", width=250, stretch=tk.YES)
    tree.column("Fecha de Registro", anchor="center", width=200, stretch=tk.YES)
    tree.column("#0", anchor="center", width=200, stretch=tk.YES)

    # Botón para cerrar sesión
    btn_cerrar_sesion = tk.Button(root, text="Cerrar Sesión", command=lambda: cerrar_sesion(root), font=("Arial", 14), bg="#FF6347", fg="#FFFFFF")
    btn_cerrar_sesion.pack(pady=20)

    # Cargar los usuarios automáticamente al iniciar
    cargar_usuarios(cursor, tree)

    # Iniciar el loop principal de Tkinter
    root.mainloop()

    # Cerrar la conexión a la base de datos al cerrar el programa
    conn.close()

# Asegurarte de que este archivo solo se ejecute si es el principal
if __name__ == "__main__":
    main()
