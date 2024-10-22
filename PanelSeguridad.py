import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

last_data = None
escaner_activo = False
cap = None  
qr_registros = {}

def escanear_qr(escanear_salida=False):
    global escaner_activo, last_data, cap
    escaner_activo = True 
    cap = cv2.VideoCapture(0)  

    def capturar_frame():
        global last_data, escaner_activo

        if escaner_activo:  
            ret, frame = cap.read()
            if not ret:
                print("No se puede acceder a la cámara.")
                return

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objs = decode(gray_frame)

            for obj in decoded_objs:
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array([(point.x, point.y) for point in points], np.int32)
                    pts = pts.reshape((-1, 1, 2))  
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

                qr_data = obj.data.decode("utf-8")

                if qr_data != last_data:
                    print(f"Datos escaneados: {qr_data}")
                    
                    data_parts = qr_data.split(',')
                    
                    if len(data_parts) == 3:
                        nombre, area = data_parts[0], data_parts[1]  
                    elif len(data_parts) == 2:
                        nombre, area = data_parts  
                    else:
                        messagebox.showwarning("Formato inválido", f"El QR escaneado no contiene los datos esperados: {qr_data}")
                        return

                    if escanear_salida:
                        if qr_data in qr_registros:
                            hora_salida = datetime.now().strftime("%H:%M:%S")
                            qr_registros[qr_data]["Hora de Salida"] = hora_salida

                            for item in tree.get_children():
                                item_values = tree.item(item, "values")
                                if item_values[0] == nombre and item_values[1] == area:
                                    tree.set(item, column="Hora de Salida", value=hora_salida)
                                    break
                            
                            messagebox.showinfo("Salida registrada", f"Hora de salida registrada para {nombre}")
                        else:
                            messagebox.showwarning("No registrado", "Este QR no ha sido registrado previamente para una entrada.")
                    else:
                        if qr_data not in qr_registros:
                            hora_entrada = datetime.now().strftime("%H:%M:%S")
                            fecha_registro = datetime.now().strftime("%Y-%m-%d")
                            observaciones = simpledialog.askstring("Observaciones", f"Ingrese observaciones para {nombre}:")

                            qr_registros[qr_data] = {
                                "Nombre": nombre,
                                "Área": area,
                                "Hora de Entrada": hora_entrada,
                                "Hora de Salida": "",
                                "Fecha de Registro": fecha_registro,
                                "Observaciones": observaciones or ""
                            }

                            tree.insert("", tk.END, values=(nombre, area, hora_entrada, "", fecha_registro, observaciones))
                        else:
                            messagebox.showinfo("QR repetido", "Este QR ya ha sido registrado anteriormente.")
                    
                    last_data = qr_data

            cv2.imshow("Escanear QR", frame)
            ventana.after(10, capturar_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                detener_escaneo()

    capturar_frame()

def detener_escaneo():
    global escaner_activo, cap
    escaner_activo = False  
    if cap is not None:
        cap.release()  
    cv2.destroyAllWindows()

def iniciar_escaneo():
    escanear_qr(escanear_salida=False)

def iniciar_escaneo_salida():
    escanear_qr(escanear_salida=True)

def main():
    global ventana, tree  
    ventana = tk.Tk()
    ventana.title("Escanear QR y capturar datos")
    ventana.geometry("800x500")

    btn_escanear = tk.Button(ventana, text="Escanear Entrada", command=iniciar_escaneo)
    btn_escanear.pack(pady=10)

    btn_escanear_salida = tk.Button(ventana, text="Escanear Salida", command=iniciar_escaneo_salida)
    btn_escanear_salida.pack(pady=10)

    btn_detener = tk.Button(ventana, text="Detener Escaneo", command=detener_escaneo)
    btn_detener.pack(pady=10)

    tree = ttk.Treeview(ventana, columns=("Nombre", "Área", "Hora de Entrada", "Hora de Salida", "Fecha de Registro", "Observaciones"), show="headings", height=10)
    tree.heading("Nombre", text="Nombre")
    tree.heading("Área", text="Área")
    tree.heading("Hora de Entrada", text="Hora de Entrada")
    tree.heading("Hora de Salida", text="Hora de Salida")
    tree.heading("Fecha de Registro", text="Fecha de Registro")
    tree.heading("Observaciones", text="Observaciones")

    tree.pack(pady=20)

    ventana.mainloop()

main()

