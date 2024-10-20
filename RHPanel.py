import tkinter as tk
from tkinter import messagebox
import GenerarQR  # Asegúrate de que este módulo contiene la función abrir_ventana_qr()

def abrir_QR():
    GenerarQR.abrir_ventana_qr(root)  # Llama a la función del módulo GenerarQR

def main():
    global root  # Hacer que root sea global para usarlo en otras funciones
    root = tk.Tk()  # Crear la ventana principal
    root.title("Panel de Recursos Humanos")

    # Etiqueta para el título
    label_titulo = tk.Label(root, text="Bienvenido al Panel de Recursos Humanos", font=("Arial", 18), bg="#E6E6FA", fg="#333")
    label_titulo.pack(pady=20)

    # Botón para abrir la ventana de generación de QR
    btn_abrir_qr = tk.Button(root, text="Abrir Generador de Código QR", command=abrir_QR, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
    btn_abrir_qr.pack(pady=20)

    # Botón para volver al inicio de sesión
    btn_volver = tk.Button(root, text="Volver al Inicio de Sesión", command=root.destroy, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
    btn_volver.pack(pady=20)

    # Iniciar el bucle de la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()  # Solo se ejecuta cuando se llama directamente
