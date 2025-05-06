import tkinter as tk
from tkinter import ttk
from unicodedata import numeric
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import pandas as pd
from tkinter import ttk
from tkinter import messagebox, filedialog
from mail import send_mail
from model.functions_db import consulta_detalle, data_mail, insert_data_factura, muestra_facturas, muestra_pdf, muestra_pdf_cliente, query_login, update_status_mail
from generate_pdf import generate_pdf
from tkcalendar import *
# import locale
import re
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # Create the root window
    root = tk.Tk()
    # Change the title of the window
    root.title("SLIC-IATI")
    # Add the logo
    icon_path = resource_path("img/Picture1.ico")
    root.iconbitmap(icon_path)
    # Change the size of the window
    # root.resizable(0, 0)
    root.geometry("1400x750")


    # Create the login window
    login_window = LoginWindow(root)

    # Start the Tkinter main loop
    root.mainloop()

class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # Logo
        logo_path = resource_path("img/logo_login_screen.jpg")
        logo = Image.open(logo_path)
        resized_image = logo.resize((200, 200), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_image)  # Keep a reference to avoid garbage collection
        label_image = tk.Label(self, image=self.converted_image, width=200, height=200, bg="black", fg="yellow")
        label_image.grid(row=0, column=1)

        # Login frame
        login_frame = ttk.Frame(self)
        login_frame.grid(column=1, row=1)

        # Label
        login_label = tk.Label(login_frame, text="Iniciar sesión")
        login_label.config(font=("Roboto", 30, "bold"), anchor="center")
        login_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        # User label
        user_label = tk.Label(login_frame, text="Usuario")
        user_label.config(font=("Roboto", 16, "bold"), anchor="center")
        user_label.grid(row=1, column=0, padx=10, pady=10)

        # User entry
        self.my_user = tk.StringVar()
        user_entry = tk.Entry(login_frame, textvariable=self.my_user)
        user_entry.config(width=12, font=("Roboto", 16))
        user_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Password label
        password_label = tk.Label(login_frame, text="Contraseña")
        password_label.config(font=("Roboto", 16, "bold"), anchor="center")
        password_label.grid(row=2, column=0, padx=10, pady=10)

        # Password entry
        self.my_password = tk.StringVar()
        password_entry = tk.Entry(login_frame, textvariable=self.my_password, show="*")
        password_entry.config(width=12, font=("Roboto", 16))
        password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # Login button
        login_button = ctk.CTkButton(login_frame, text="Iniciar sesión", command = self.open_new_window)
        login_button.configure(width=200, height=50, font=("Roboto", 16, "bold"), anchor="center", border_color = "black",
                               border_width = 2)
        login_button.grid(row=3, column=0, columnspan = 2, padx=10, pady=10)

    def open_new_window(self):
        try:
            # Validate the login credentials
            if query_login(self.my_user.get(), self.my_password.get()):
                # If login is successful, switch to opcioneswindow
                hide_all_frames(self.master)
                opciones_window = opcioneswindow(self.master)
                opciones_window.pack(fill="both", expand=True)
            else:
                titulo = "Inicio de sesión"
                mensaje = "Usuario o Contraseña incorrectos"
                messagebox.showerror(titulo, mensaje)

        except Exception as e:
            titulo = "Error open_new_window"
            mensaje = f"No se pudo iniciar sesión: {str(e)}"
            messagebox.showerror(titulo, mensaje)
            print(e)

class opcioneswindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure((0,1,2), weight = 1)
        self.rowconfigure((0,1,2,3), weight = 1)

        #frame for all the options
        self.opciones_frame = tk.Frame(self)
        self.opciones_frame.grid(row = 0, column = 1, padx=10, pady =10)

        self.salir_frame = tk.Frame(self)
        self.salir_frame.grid(row = 3, column = 1, padx=10, pady =10)

        self.opciones()

    def opciones(self):
        #options
        #img
        img_path = resource_path("img/facturas.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((35,35), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton
        self.button_consulta_fac = ctk.CTkButton(self.opciones_frame, 
                                                 image = self.converted_image,
                                                 text = "Consulta de Facturas",
                                                 command = self.open_consulta_fac_window 
                                                  )
        self.button_consulta_fac.configure(width = 300, height = 50,
                                            fg_color ="#3B8ED0", text_color="black", hover_color="#36719F",
                                            border_width = 2,
                                            font=("Roboto", 16, "bold"),
                                            anchor = "center",
                                            compound = tk.LEFT)
        self.button_consulta_fac.grid(row = 0, column = 0, sticky = "n" )

                #options
        #img
        img_path = resource_path("img/mail.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((35,35), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton
        self.button_consulta_fac = ctk.CTkButton(self.opciones_frame, 
                                                 image = self.converted_image,
                                                 text = "Envío Estados de Cuenta",
                                                 command = self.open_envio_fac_window
                                                  )
        self.button_consulta_fac.configure(width = 300, height = 50,
                                            fg_color ="#3B8ED0", text_color="black", hover_color="#36719F",
                                            border_width = 2,
                                            font=("Roboto", 16, "bold"),
                                            anchor = "center",
                                            compound = tk.LEFT)
        self.button_consulta_fac.grid(row = 1, column = 0, sticky = "n", pady = 10 )

    def open_consulta_fac_window(self):
        hide_all_frames(self.master)
        consulta_fac = consulta_fac_window(self.master)
        consulta_fac.pack(fill="both", expand=True)
    
    def open_envio_fac_window(self):
        hide_all_frames(self.master)
        envio_fac = envio_fac_window(self.master)
        envio_fac.pack(fill="both", expand=True)

class consulta_fac_window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure((0,1,2), weight = 1)
        self.rowconfigure((0,1,2,3), weight = 1)

        #frame for all the options
        self.opciones = tk.Frame(self)
        self.opciones.grid(row = 0, column = 0, sticky = "nw")

        self.tabla_frame = tk.Frame(self)
        self.tabla_frame.grid(row = 0, column=1, sticky="nw")

        self.bajo_frame = tk.Frame(self)
        self.bajo_frame.grid(row = 1, column=1, sticky="nw")
        
        self.campos()
        self.tabla_ctrl_facturas()

    def campos(self):

         # label
        empresa_label = tk.Label(self.opciones, text="Empresa:")
        empresa_label.config(font=("Roboto", 16, "bold"), anchor="center")
        empresa_label.grid(row=0, column=0, padx = 5, pady = 5, sticky = "nw")
        

        #combo empresa
        self.combo_empresa =  ttk.Combobox(self.opciones, values = ["4","7", "9"])
        self.combo_empresa.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "ew")
        self.combo_empresa.set("Seleccionar empresa")

         # label
        cliente_label = tk.Label(self.opciones, text="Cliente:")
        cliente_label.config(font=("Roboto", 16, "bold"), anchor="center")
        cliente_label.grid(row=1, column=0, padx = 5, pady = 5, sticky = "nw")

        # entry
        self.my_cliente = tk.StringVar()
        cliente_entry = ctk.CTkEntry(self.opciones,
                                             width=100,
                                             textvariable=self.my_cliente)
        # cliente_entry = tk.Entry(self.opciones, textvariable=self.my_cliente )
        # cliente_entry.config(width=25, font=("Roboto", 10))
        cliente_entry.grid(row=1, column=1, columnspan = 2, sticky="ew", padx = 5, pady = 10)

         #label date
        self.label_date_ini = tk.Label(self.opciones, text = "Fecha Inicial:")
        self.label_date_ini.config(font = ("Roboto", 16, "bold"), anchor = "e") #style
        self.label_date_ini.grid(row = 2, column = 0, padx = 5, pady = 10, sticky="nw") #position in the screen
           # entry calendar
        self.my_date_ini = tk.StringVar()
        self.calendar_date_ini = ctk.CTkEntry(self.opciones,
                                             width=100,
                                             placeholder_text = "YYYY-MM-DD",
                                             textvariable=self.my_date_ini)
        self.calendar_date_ini.grid(row = 2, column = 1, padx = 5, pady = 10, sticky = "ew")
         # Bind para el evento de escritura en el campo
        self.calendar_date_ini.bind("<KeyRelease>", self.format_date_ini_input)
        # self.calendar_date_ini.configure (font=("Roboto", 10))
        # self.calendar_date_ini = DateEntry(self.opciones, select_mode = "day", date_pattern = "yyyy-mm-dd", state = "readonly", date = None)
        
       
         #label date
        self.label_date_fin = tk.Label(self.opciones, text = "Fecha Final:")
        self.label_date_fin.config(font = ("Roboto", 16, "bold"), anchor = "e") #style
        self.label_date_fin.grid(row = 3, column = 0, padx = 5, pady = 10, sticky = "nw") #position in the screen
           # entry calendar
        self.my_date_fin = tk.StringVar()
        self.calendar_date_fin = ctk.CTkEntry(self.opciones,
                                             width=100,
                                             placeholder_text = "YYYY-MM-DD",
                                             textvariable=self.my_date_fin)
        self.calendar_date_fin.grid(row = 3, column = 1, padx = 5, pady = 10, sticky = "ew")
         # Bind para el evento de escritura en el campo
        self.calendar_date_fin.bind("<KeyRelease>", self.format_date_fin_input)
        # self.calendar_date_fin = DateEntry(self.opciones, select_mode = "day", date_pattern = "yyyy-mm-dd", state = "readonly", date = None)
        # self.calendar_date_fin.grid(row = 3, column = 1, padx = 5, pady = 10, sticky = "ew")
        # self.my_date_fin = tk.StringVar()
        # self.my_date_fin.set(None)

        #Boton buscar
        #img
        img_path = resource_path("img/lupa.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((20,20), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton
        self.button_buscar = ctk.CTkButton(self.opciones, 
                                                 image = self.converted_image,
                                                 text = "Buscar",
                                                 command= self.search_facturas)
        self.button_buscar.configure(width = 75, height = 25,
                                            fg_color ="#3B8ED0", text_color="black", hover_color="#36719F",
                                            border_width = 2,
                                            font=("Roboto", 16, "bold"),
                                            anchor = "center",
                                            compound = tk.LEFT)
        self.button_buscar.grid(row = 4, column =    1, sticky = "e" )

        #Boton pdf
        #img
        img_path = resource_path("img/pdf.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((35,35), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton
        self.button_pdf = ctk.CTkButton(self.bajo_frame, 
                                                 image = self.converted_image,
                                                 text = "Genera PDF",
                                                 command=self.crear_pdf)
        self.button_pdf.configure(width = 100, height = 45,
                                            fg_color ="#3B8ED0", text_color="black", hover_color="#36719F",
                                            border_width = 2,
                                            font=("Roboto", 16, "bold"),
                                            anchor = "center",
                                            compound = tk.LEFT)
        self.button_pdf.grid(row = 0, column = 0, padx = (700,0), sticky = "e")

        #Boton Salir
        #img
        img_path = resource_path("img/home.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((35,35), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton
        self.button_salir = ctk.CTkButton(self.bajo_frame, 
                                                 image = self.converted_image,
                                                 text = "Home",
                                                 command = self.open_main_window)
        self.button_salir.configure(width = 100, height = 45,
                                            fg_color ="#EC7070", text_color="black", hover_color="#B51717",
                                            border_width = 2,
                                            font=("Roboto", 16, "bold"),
                                            anchor = "center",
                                            compound = tk.LEFT)
        self.button_salir.grid(row = 2, column = 0, padx = (700,0), pady = 10, sticky = "e")

    def format_date_ini_input(self, event):
        current_text = self.calendar_date_ini.get()
        if len(current_text) == 4 and not current_text.endswith('-'):
            self.calendar_date_ini.insert(tk.END, '-')
        elif len(current_text) == 7 and not current_text.endswith('-'):
            self.calendar_date_ini.insert(tk.END, '-')
        # Limitar a 10 caracteres
        if len(current_text) >= 10:
            self.calendar_date_ini.delete(10, tk.END)
    
    def format_date_fin_input(self, event):
        current_text = self.calendar_date_fin.get()
        if len(current_text) == 4 and not current_text.endswith('-'):
            self.calendar_date_fin.insert(tk.END, '-')
        elif len(current_text) == 7 and not current_text.endswith('-'):
            self.calendar_date_fin.insert(tk.END, '-')
        # Limitar a 10 caracteres
        if len(current_text) >= 10:
            self.calendar_date_fin.delete(10, tk.END)

    def tabla_ctrl_facturas(self):
     #create table to show the entrys
        self.tabla = ttk.Treeview(self.tabla_frame,
                                  column = ("cve_cliente","cliente_name","num_fact", "fecha_factura", "fecha_venc", "importe",
                                            "saldo", "moneda", "dias_retraso", "pdf"),
                                  height = 30,
                                  show =  "headings",
                                  selectmode="extended"
                                  )
        
        # Add headings
        
        self.tabla.heading("cve_cliente", text="CVE. Cliente")
        self.tabla.heading("cliente_name", text="Cliente")
        self.tabla.heading("num_fact", text="No. Factura")
        self.tabla.heading("fecha_factura", text="Fecha Factura")
        self.tabla.heading("fecha_venc", text="Fecha Vencimiento")
        self.tabla.heading("importe", text="Importe")
        self.tabla.heading("saldo", text="Saldo")
        self.tabla.heading("moneda", text="Moneda")
        self.tabla.heading("dias_retraso", text="Días de Retraso")
        self.tabla.heading("pdf", text="PDF")

    # Configure column width
        self.tabla.column("cve_cliente", width=80)
        self.tabla.column("cliente_name", width=180)
        self.tabla.column("num_fact", width=100)
        self.tabla.column("fecha_factura", width = 100)
        self.tabla.column("fecha_venc", width = 110)
        self.tabla.column("importe", width=100) 
        self.tabla.column("saldo", width=75)
        self.tabla.column("moneda", width=75)    
        self.tabla.column("dias_retraso", width=150) 
        self.tabla.column("pdf", width=50)
    
    #etiquetas para asignar color a renglones
        self.tabla.tag_configure("rojo", background="#EC7070")   # Rojo para valores < -1
        self.tabla.tag_configure("amarillo", background="#FFEC5C")  # Amarillo para valores < 7
        self.tabla.tag_configure("verde", background="#8BE48E")  # Verde para los demás
        self.tabla.tag_configure("azul", background="#029CFF")  # azul si ya se hizo el pdf


    # Pack the treeview inside the productos tab frame
        self.tabla.grid(row = 0, column = 0, columnspan = 9, padx=5, pady=5, sticky = "ew")

        #add scrollbar
        self.scroll = ttk.Scrollbar(self.tabla_frame,
                                    orient = "vertical", 
                                    command = self.tabla.yview)
        self.scroll.grid(row = 0, column = 10, sticky = "nse")
        self.tabla.configure(yscrollcommand = self.scroll.set)
     
    def search_facturas(self):
        self.tabla.delete(*self.tabla.get_children())
        self.lista_facturas = muestra_facturas(self.combo_empresa.get(),self.my_cliente.get(), self.calendar_date_ini.get(), self.calendar_date_fin.get())
        self.lista_facturas.reverse()

        for p in self.lista_facturas:

            if p[8] <= -1 and p[6] < 0:
                tag = "rojo"
            elif p[8] <= 7:
                tag = "amarillo"
            else:
                tag = "verde"
            self.tabla.insert('', 0, text=p[0], values=(p[0:]), tags=(tag,))

    def crear_pdf(self):
        selected_item = self.tabla.selection()
        datos_select = []
        for item in selected_item:
            current_item = self.tabla.item(item)['values']
            datos_select.append(current_item)
        
        df_data = pd.DataFrame(datos_select, columns = ['cve_cliente', 'cliente', 'num_fac', 'fecha_fact', 'fecha_venc','importe', 'saldo', 'moneda','dias_retraso', 'pdf'])
        orden_columnas = ['cve_cliente', 'cliente', 'num_fac', 'importe', 'moneda', 'fecha_fact','fecha_venc','saldo', 'dias_retraso', 'pdf']
        df_data = df_data[orden_columnas]
        clientes = df_data['cve_cliente'].unique()
        pdf_value = (df_data['pdf'] == 'SI').any()
        
        if len(clientes) > 1:
            messagebox.showerror('Error', 'Solo se permite generar un estado de cuenta para un cliente. Por favor, realice otra selección.')
        # elif pdf_value == True:
        #     messagebox.showerror('Error', 'Alguna de las facturas seleccionadas ya ha sido añadida a un estado de cuenta creado previamente.')
        else:
            try:
                #folder donde se guardara el PDF
                folder_path = filedialog.askdirectory(title = "Seleccione la carpeta destino")

                #informacion para la tabla de detalle de estados de cuenta
                lista_detalle =  df_data[['num_fac', 'importe', 'fecha_venc', 'moneda']]
                lista_detalle['partida'] = range(1, len(lista_detalle)+1)
                lista_detalle = lista_detalle.values.tolist()
                # print(lista_detalle)
                

                # data para crear el pdf
                name_cliente = df_data['cliente'].iloc[0]
                cve_cliente = df_data['cve_cliente'].iloc[0]
                print(name_cliente, cve_cliente, df_data)

                #insertar informacion de estado de cuenta en base de datos
                meses_en_espanol = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                
                # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                fecha = datetime.today()
                day = fecha.strftime('%d')
                month = fecha.strftime('%m')
                # month = meses_en_espanol[int(month) - 1]
                year = fecha.strftime('%Y')
                ruta_archivo = f"{folder_path}/EC_{str(name_cliente)}-{cve_cliente}_{year}{month}{day}.pdf"
                
                insert_data_factura(name_cliente,clientes[0], len(df_data), ruta_archivo, lista_detalle, self.combo_empresa.get())
                
                df_data['importe'] = pd.to_numeric(df_data['importe'], errors='coerce')
                df_data['importe'] = df_data['importe'].apply(lambda x: f"${x:,.2f}") + ' ' + df_data["moneda"]
                df_data['dias_retraso'] = df_data['dias_retraso'].abs()

                
                df_data.drop(columns =['cve_cliente', 'cliente', 'saldo', 'pdf', 'moneda'], inplace=True)
                
                data_factura = df_data.values.tolist()
                generate_pdf(cve_cliente,name_cliente, data_factura, folder_path)

                # print(df_data)
                messagebox.showinfo('Exito', 'PDF creado con éxito')
                self.open_envio_fac_window()
            except Exception as e:
                titulo = "Error al crear PDF"
                mensaje = f"Error: {str(e)}"
                messagebox.showerror(titulo, mensaje)
                print(e)

    def open_envio_fac_window(self):
        hide_all_frames(self.master)
        envio_fac = envio_fac_window(self.master)
        envio_fac.pack(fill="both", expand=True)
    
    def open_main_window(self):
        hide_all_frames(self.master)
        opciones_window = opcioneswindow(self.master)
        opciones_window.pack(fill="both", expand=True)

class envio_fac_window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure((0,1,2,3,4,5), weight = 1)
        # self.rowconfigure((0,1,2,3), weight = 1)

        #frame for all the options
        self.opciones = tk.Frame(self)
        self.opciones.grid(row = 0, column = 0, sticky = "nw")

        self.tabla_frame = tk.Frame(self)
        self.tabla_frame.grid(row = 1, column=0, sticky="nw")

        self.botones_frame = tk.Frame(self)
        self.botones_frame.grid(row = 1, column = 5, padx = 10, pady = 10, sticky = "nw")

        self.campos()
        self.tabla_ctrl_facturas()
    
    def campos(self):
        #barra busqueda
        # entry
        self.my_entry = tk.StringVar()
        busqueda_entry = tk.Entry(self.opciones, textvariable=self.my_entry)
        busqueda_entry.config(width=50, font=("Roboto", 12))
        busqueda_entry.grid(row=0, column = 0, columnspan = 2, sticky="ew", padx = 5, pady = 10)

        #Boton buscar
        #img
        img_path = resource_path("img/lupa.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((20,20), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton
        self.button_buscar = ctk.CTkButton(self.opciones, 
                                                 image = self.converted_image,
                                                 command=self.search_facturas)
        self.button_buscar.configure(width = 25, height = 25,
                                            fg_color ="#3B8ED0", text_color="black", hover_color="#36719F",
                                            border_width = 2,
                                            text = "",
                                            font=("Roboto", 16, "bold"),
                                            anchor = "center",
                                            compound = tk.LEFT)
        self.button_buscar.grid(row = 0, column =    2, sticky = "e")

        #boton ENVIAR
        #img
        img_path = resource_path("img/mail.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((50,50), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        self.boton_enviar = ctk.CTkButton(self.botones_frame,
                                          text = "ENVIAR", image =self.converted_image,
                                          command=self.open_send_mail)
        self.boton_enviar.configure(width = 200, height = 50,
                                   border_width = 2,
                                   font = ("Roboto", 16, "bold"),
                                   compound  = tk.LEFT)
        self.boton_enviar.grid(row = 0, column = 0, padx = 10, pady = 10)

        #boton CONSULTA DETALLE
        #img
        img_path = resource_path("img/detail.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((50,50), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        self.boton_detalle = ctk.CTkButton(self.botones_frame, 
                                           text = "Consultar\n Detalle", image =self.converted_image,
                                           command=self.open_detalle)
        self.boton_detalle.configure(width = 200, height = 50,
                                   border_width = 2,
                                   font = ("Roboto", 16, "bold"),
                                   compound  = tk.LEFT)
        self.boton_detalle.grid(row = 1, column = 0, padx = 10, pady = 10)

        #boton SALIR
        #img
        img_path = resource_path("img/home.png")
        img_real = Image.open(img_path)
        resized_img = img_real.resize((50,50), Image.Resampling.LANCZOS)
        self.converted_image = ImageTk.PhotoImage(resized_img)

        #buton salir a home
        self.boton_salir = ctk.CTkButton(self.botones_frame, image = self.converted_image, text = "Home", command = self.open_main_window)
        self.boton_salir.configure(width = 200, height = 30,
                                   fg_color ="#FF5050", text_color="black", hover_color="#DD1818",
                                   border_width = 2,
                                   font = ("Roboto", 16, "bold"),
                                   compound  = tk.LEFT)
        self.boton_salir.grid(row = 4, column = 0, pady = 10)
    
    def open_main_window(self):
        hide_all_frames(self.master)
        opciones_window = opcioneswindow(self.master)
        opciones_window.pack(fill="both", expand=True)

    def tabla_ctrl_facturas(self):
     #create table to show the entrys
        self.tabla = ttk.Treeview(self.tabla_frame,
                                  column = ("id","empresa","cve_cliente","cliente_name","tot_fact", "fecha_creacion", "status", "fecha_envio", "pdf"),
                                  height = 30,
                                  show =  "headings",
                                  selectmode="extended"
                                  )
        
        # Add headings
        self.tabla.heading("id", text="ID")
        self.tabla.heading("cve_cliente", text="Cve. Cliente")
        self.tabla.heading("empresa", text="Empresa")
        self.tabla.heading("cliente_name", text="Cliente")
        self.tabla.heading("tot_fact", text="No. Facturas")
        self.tabla.heading("fecha_creacion", text="Fecha de Creación PDF")
        self.tabla.heading("status", text="Status")
        self.tabla.heading("fecha_envio", text="Fecha de Envío")
        self.tabla.heading("pdf", text="Ruta Archivo")

    # Configure column width
        self.tabla.column("id", width=50)
        self.tabla.column("empresa", width=75)
        self.tabla.column("cve_cliente", width=75)
        self.tabla.column("cliente_name", width=200)
        self.tabla.column("tot_fact", width=75)
        self.tabla.column("fecha_creacion", width = 150)
        self.tabla.column("status", width=50) 
        self.tabla.column("fecha_envio", width=100)    
        self.tabla.column("pdf", width=200)
    
    #etiquetas para asignar color a renglones
        self.tabla.tag_configure("rojo", background="#EC7070")   # Rojo para valores < -1
        # self.tabla.tag_configure("amarillo", background="#FFEC5C")  # Amarillo para valores < 7
        self.tabla.tag_configure("verde", background="#8BE48E")  # Verde para los demás


    # Pack the treeview inside the productos tab frame
        self.tabla.grid(row = 0, column = 0, columnspan = 8, padx=5, pady=5, sticky = "ew")

        #add scrollbar
        self.scroll = ttk.Scrollbar(self.tabla_frame,
                                    orient = "vertical", 
                                    command = self.tabla.yview)
        self.scroll.grid(row = 0, column = 8, sticky = "nse")
        self.tabla.configure(yscrollcommand = self.scroll.set)


        self.lista_facturas = muestra_pdf()
        # self.lista_facturas.reverse()
        
        for p in self.lista_facturas:
            if p[6] == 'C':
                tag = "rojo"
            else:
                tag = "verde"
            self.tabla.insert('', 0, text=p[0], values=(p[0:]), tags=(tag,))

    def search_facturas(self):
        self.tabla.delete(*self.tabla.get_children())
        # print(self.my_entry.get())
        self.lista_facturas = muestra_pdf_cliente(self.my_entry.get())
        # self.lista_facturas.reverse()
    
        for p in self.lista_facturas:
            if p[6] == 'C':
                tag = "rojo"
            else:
                tag = "verde"
            self.tabla.insert('', 0, text=p[0], values=(p[0:]), tags=(tag,))

    def open_detalle(self):
        try:
            selected_items = self.tabla.selection()
            items_df = []
            for item in selected_items:
                current_item = self.tabla.item(item)['values']
                items_df.append(current_item)
            items_df = pd.DataFrame(items_df, columns=["id","empresa","cve_cliente","cliente", "num_factura", "fecha_crea_pdf", "status","fecha_envio","ruta"])

            if(len(items_df)>1):
                messagebox.showerror("ERROR!", "Seleccionar solo un registro")
            else:
                id_value = items_df['id'][0]
                detalle_fac_window = detalle_factura_window(self.master, id_value)
                # detalle_fac_window.pack(fill="both", expand=True)

        except Exception as e:
            titulo = "Error"
            mensaje = f"Contactar a SLIC-IATI Error: {str(e)}"
            messagebox.showerror(titulo, mensaje)
    
    def open_send_mail(self):
        try:
            selected_items = self.tabla.selection()
            items_df = []
            for item in selected_items:
                current_item = self.tabla.item(item)['values']
                items_df.append(current_item)
            items_df = pd.DataFrame(items_df, columns=["id","empresa","cve_cliente","cliente", "num_factura", "fecha_crea_pdf", "status","fecha_envio","ruta"])

            if(len(items_df)>1):
                messagebox.showerror("ERROR!", "Seleccionar solo un registro")
            elif items_df['status'][0] == 'E':
                messagebox.showerror("ERROR!", "Registro enviado previamente")
            else:
                receiver_mail = data_mail(int(items_df["cve_cliente"][0]),int(items_df["empresa"][0]))
                ruta = items_df["ruta"][0]
                id_h = items_df["id"][0]

                # self.mail_prueba_d = ['mariosegovia1205@gmail.com'] 
                self.mail_prueba_s = "creditoycobranza@apgquimica.com.mx"
                self.my_password = 'ApGcr3d1t0'
                
                if not receiver_mail:
                    messagebox.showerror('Error', 'No es posible enviar el correo, ya que el cliente no tiene un correo de contacto asignado. Por favor, verifica la información y actualízala si es necesario.')
                else:
                    receiver_mail.append("creditoycobranza@apgquimica.com.mx")
                    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    # messagebox.showinfo('correo', 'correo enviado')
                    for mail in receiver_mail:
                        if not re.match(regex,mail):
                            messagebox.showerror('Error',f'{mail}, es un correo invalido. Por favor, verifica la información y actualízala si es necesario.')
                            break  # Exit the loop on first invalid email
                    else:
                        # If all emails are valid, send them and update the status
                        for mail in receiver_mail:
                            # print('enviado')
                            # print(mail)
                            send_mail(ruta, self.mail_prueba_s, mail, self.my_password)
                            update_status_mail(int(id_h))

                        messagebox.showinfo('Éxito', 'Correos enviados con éxito')
                self.refresh_table()


                # print(receiver_mail, ruta)
                # send_mail_window = send_mail_w(self, self, receiver_mail, ruta, id_h)

        except Exception as e:
            titulo = "Error"
            mensaje = f"Contactar a SLIC-IATI Error: {str(e)}"
            messagebox.showerror(titulo, mensaje)
            print(e)

    def refresh_table(self):

        self.tabla.delete(*self.tabla.get_children())
        self.lista_facturas = muestra_pdf()
        # self.lista_facturas.reverse()
        
        for p in self.lista_facturas:
            if p[6] == 'C':
                tag = "rojo"
            else:
                tag = "verde"
            self.tabla.insert('', 0, text=p[0], values=(p[0:]), tags=(tag,))

class detalle_factura_window(tk.Toplevel):
    def __init__(self, parent, id_value):
        super().__init__(parent)
        self.id_value = id_value  # Store the DataFrame
        self.geometry("652x404")
        self.resizable(0,0)
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        self.parent = parent

        self.title(f"Detalle de Estado de Cuenta")

        # self.campos = tk.Frame(self)
        # self.campos.grid(row = 1, column = 0, columnspan=3)

        self.tabla_frame = tk.Frame(self)
        self.tabla_frame.grid(row = 0, column = 0, sticky='w')


        self.grab_set()
        self.tabla_detalle()

    def tabla_detalle(self):
        #create table to show the entrys
        self.tabla = ttk.Treeview(self.tabla_frame,
                                  column = ("id", "partida", "num_factura", "importe", "fecha_vencimiento"),
                                  height = 15,
                                  show =  "headings"
                                  )
        # Add headings
        self.tabla.heading("id", text="ID")
        self.tabla.heading("partida", text="Partida")
        self.tabla.heading("num_factura", text="No. Factura")
        self.tabla.heading("importe", text="Importe ($)")
        self.tabla.heading("fecha_vencimiento", text="Fecha Vencimiento")

    # Configure column width
        self.tabla.column("id", width=50)
        self.tabla.column("partida", width=150)
        self.tabla.column("num_factura", width=100)
        self.tabla.column("importe", width=100)
        self.tabla.column("fecha_vencimiento", width=200) 

    
    # Pack the treeview inside the productos tab frame
        self.tabla.grid(row = 0, column = 0, columnspan = 6, padx=5, pady=5, sticky = "ew")

        #add scrollbar
        self.scroll = ttk.Scrollbar(self.tabla_frame,
                                    orient = "vertical", 
                                    command = self.tabla.yview)
        self.scroll.grid(row = 0, column = 6, sticky = "nse")
        self.tabla.configure(yscrollcommand = self.scroll.set)

        self.lista_detalle = consulta_detalle(int(self.id_value))
        self.lista_detalle.reverse()
       

        for p in self.lista_detalle:
            self.tabla.insert('', 0, text=p[0], values=(p[0:]))





def hide_all_frames(master):
    for widget in master.winfo_children():
        widget.pack_forget()

# Check if the script is being run directly by the Python interpreter
if __name__ == '__main__':
    main()
