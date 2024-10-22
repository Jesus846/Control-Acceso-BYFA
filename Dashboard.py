import tkinter as tk
from tkinter import ttk
import mysql.connector

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",        
            password="",        
            database="BYFA_CONTROL"  
        )
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        exit()

def cargar_usuarios(cursor, tree):
    try:
        cursor.execute("SELECT Nombre ,Usuario,Contrasena, Cargo, Fecha FROM usuarios")
        usuarios = cursor.fetchall()
        
        for row in tree.get_children():
            tree.delete(row)
        
        for usuario in usuarios:
            tree.insert("", "end", values=usuario)
    except mysql.connector.Error as err:
        print(f"Error al consultar la base de datos: {err}")

def cerrar_sesion(root):
    root.destroy()

def main():
    conn, cursor = conectar_db()
    
    root = tk.Tk()
    root.title("Bienvenida")
    root.geometry("800x600")
    root.configure(bg="#E6E6FA")  
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

    label_bienvenida = tk.Label(root, text="¡Bienvenido al sistema!", font=("Arial", 18), bg="#E6E6FA", fg="#333")
    label_bienvenida.pack(pady=20)

    frame_tabla = tk.Frame(root)
    frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame_tabla, columns=("Nombre", "Usuario", "Contraseña","Cargo", "Fecha de Registro"), show="headings", height=8)
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("Nombre", text="Nombre")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Cargo", text="Cargo")
    tree.heading("Contraseña", text="Contraseña")
    tree.heading("Fecha de Registro", text="Fecha de Registro")
    
    tree.column("Nombre", anchor="center", width=250, stretch=tk.YES)
    tree.column("Usuario", anchor="center", width=250, stretch=tk.YES)
    tree.column("Contraseña", anchor="center", width=200, stretch=tk.YES)
    tree.column("Cargo", anchor="center", width=250, stretch=tk.YES)
    tree.column("Fecha de Registro", anchor="center", width=200, stretch=tk.YES)
    tree.column("#0", anchor="center", width=200, stretch=tk.YES)

    btn_cerrar_sesion = tk.Button(root, text="Cerrar Sesión", command=lambda: cerrar_sesion(root), font=("Arial", 14), bg="#FF6347", fg="#FFFFFF")
    btn_cerrar_sesion.pack(pady=20)

    cargar_usuarios(cursor, tree)

    root.mainloop()

    conn.close()

if __name__ == "__main__":
    main()
