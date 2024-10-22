import tkinter as tk
import GenerarQR

def abrir_QR():
    GenerarQR.abrir_ventana_qr(root)

def main():
    global root
    root = tk.Tk()
    root.title("Panel de Recursos Humanos")

    label_titulo = tk.Label(root, text="Bienvenido al Panel de Recursos Humanos", font=("Arial", 18), bg="#E6E6FA", fg="#333")
    label_titulo.pack(pady=20)

    btn_abrir_qr = tk.Button(root, text="Abrir Generador de Código QR", command=abrir_QR, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
    btn_abrir_qr.pack(pady=20)

    btn_volver = tk.Button(root, text="Volver al Inicio de Sesión", command=root.destroy, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", relief="raised", padx=10, pady=5)
    btn_volver.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
