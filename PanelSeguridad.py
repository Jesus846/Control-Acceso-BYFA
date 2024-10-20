import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

# Variables globales para el control del escaneo, la cámara y último QR leído
last_data = None
escaner_activo = False
cap = None  # Variable global para la cámara

# Función para escanear código QR usando la cámara
def escanear_qr():
    global escaner_activo, last_data, cap
    escaner_activo = True  # Activar el escaneo
    cap = cv2.VideoCapture(0)  # Iniciar la cámara

    # Función interna para capturar frame a frame
    def capturar_frame():
        global last_data, escaner_activo

        if escaner_activo:  # Continuar capturando solo si el escáner está activo
            ret, frame = cap.read()
            if not ret:
                print("No se puede acceder a la cámara.")
                return

            # Convertir el frame a escala de grises
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Decodificar cualquier QR que esté en el frame
            decoded_objs = decode(gray_frame)

            for obj in decoded_objs:
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array([(point.x, point.y) for point in points], np.int32)
                    pts = pts.reshape((-1, 1, 2))  # Convertir a forma aceptada por polylines
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

                # Extraer datos del QR
                qr_data = obj.data.decode("utf-8")

                # Si es un nuevo QR, lo mostramos en la tabla
                if qr_data != last_data:
                    print(f"Datos escaneados: {qr_data}")
                    
                    # Separar los datos del QR (Nombre, Área, Sueldo Diario)
                    data_parts = qr_data.split(',')
                    if len(data_parts) == 3:
                        nombre, area, sueldo = data_parts
                        # Insertar los datos en la tabla
                        tree.insert("", tk.END, values=(nombre, area, sueldo))
                    else:
                        messagebox.showwarning("Formato inválido", f"El QR escaneado no contiene los datos esperados: {qr_data}")
                    
                    # Actualizar el último QR leído
                    last_data = qr_data

            # Mostrar el video en vivo con el QR detectado
            cv2.imshow("Escanear QR", frame)

            # Llamar de nuevo esta función después de 10ms
            ventana.after(10, capturar_frame)

            # Presiona 'q' para salir del bucle de OpenCV
            if cv2.waitKey(1) & 0xFF == ord('q'):
                detener_escaneo()

    capturar_frame()  # Llamar por primera vez

# Función para detener el escaneo
def detener_escaneo():
    global escaner_activo, cap
    escaner_activo = False  # Detener el escaneo
    if cap is not None:
        cap.release()  # Liberar la cámara
    cv2.destroyAllWindows()  # Cerrar la ventana de OpenCV

# Función para iniciar el escaneo desde el botón
def iniciar_escaneo():
    escanear_qr()

# Crear la ventana principal
def main():
    global ventana, tree  # Hacer las variables globales para su uso en otras funciones
    ventana = tk.Tk()
    ventana.title("Escanear QR y capturar datos")
    ventana.geometry("600x400")

    # Crear el botón para escanear QR
    btn_escanear = tk.Button(ventana, text="Escanear QR", command=iniciar_escaneo)
    btn_escanear.pack(pady=10)

    # Crear el botón para detener el escaneo
    btn_detener = tk.Button(ventana, text="Detener Escaneo", command=detener_escaneo)
    btn_detener.pack(pady=10)

    # Crear el Treeview para mostrar los datos capturados
    tree = ttk.Treeview(ventana, columns=("Nombre", "Área", "Sueldo Diario"), show="headings", height=10)
    tree.heading("Nombre", text="Nombre")
    tree.heading("Área", text="Área")
    tree.heading("Sueldo Diario", text="Sueldo Diario")

    # Empaquetar la tabla
    tree.pack(pady=20)

    # Iniciar la aplicación
    ventana.mainloop()
