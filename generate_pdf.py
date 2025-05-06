from fpdf import FPDF, Align
from datetime import datetime
# import locale
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


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        # Aquí puedes agregar un encabezado si lo necesitas
        # self.cell(0, 10, "APG Química SA de CV", ln=True, align="C")

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "I", 10)
        # Aquí puedes agregar un pie de página si lo necesitas
        # self.cell(0, 10, f"Página {self.page_no()}", align="C")

def generate_pdf(cve_cliente,cliente, data_factura, folder_path):
    # Crear PDF
    pdf = PDF('P', 'mm', 'Letter')
    pdf.set_margins(20,25,20)
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    # Establecer fuente
    pdf.set_font("Arial", size=10)

    # Configurar la fecha
    meses_en_espanol = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    fecha = datetime.today()
    day = fecha.strftime('%d')
    month = fecha.strftime('%B')
    
    month_2 = fecha.strftime('%m')
    month = meses_en_espanol[int(month_2) - 1]
    year = fecha.strftime('%Y')

    # Agregar el logo
    pdf.image(resource_path("img/logo_login_screen.jpg"), x=20, y=5, w=50)

    # Agregar la fecha alineada a la derecha
    pdf.text(120, 55, f"Santiago de Querétaro, a {day} de {month} del {year}.")
    # Agregar un salto de línea
    # pdf.ln(5)  

    # Agregar destinatario personalizado
    # cliente = "XXXXXX"
    pdf.set_font("Arial", "B", 10)
    pdf.text(20, 75, f"Estimado/a cliente {cliente}")

    # Agregar más contenido (si es necesario)
    # pdf.ln(5)  # Espacio después del destinatario

    # Agregar cuerpo del mensaje
    texto = """Con motivo de nuestra mejora continua y apegándonos a nuestras políticas de funcionamiento, la familia de APG Química le informa que al día de hoy usted cuenta con los siguientes documentos vencidos:"""

    # Definir las cabeceras de la tabla
    cabecera = ['Factura', 'Importe', 'Fecha Factura', 'Fecha de\nVencimiento', 'Días de Retraso']

    
    # Calcular el ancho de las columnas
    ancho_pagina = 210 - 20 * 2  # Ancho de la página (210 mm) menos márgenes izquierdo y derecho (20 mm cada uno)
    ancho_columnas = [ancho_pagina / len(cabecera)] * len(cabecera)  # Distribuir el ancho de la tabla entre las columnas

    # Agregar primer párrafo
    pdf.set_font("Arial", size=10)
    # Mover el cursor a la posición (19, 80)
    pdf.set_xy(19, 80)
    pdf.multi_cell(0, 8, texto)
    pdf.ln(5)  # Espacio entre párrafos

    # Agregar cabecera de la tabla
    pdf.set_font("Arial", 'B', 10)
    for i in range(len(cabecera)):
        pdf.cell(ancho_columnas[i], 8, cabecera[i], border='B', align='C')
    pdf.ln()  # Salto de línea después de la cabecera

    # Agregar data_factura en la tabla
    pdf.set_font("Arial", size=8)
    for fila in data_factura:
        for i in range(len(fila)):
            pdf.cell(ancho_columnas[i], 8, str(fila[i]), border='B', align='C')
        pdf.ln()  # Salto de línea después de cada fila
    pdf.set_font("Arial", size=10)

    # Segundo párrafo
    pdf.ln()
    texto2 = """Por favor, revise los detalles adjuntos y agradecemos pueda realizar el pago a la brevedad o en su caso nos indique la fecha de pago programada. Le recordamos nuestras cuentas bancarias a las cuales pueda realizar su pago."""
    pdf.multi_cell(0, 8, texto2)
    pdf.ln(5)

    # Agregar el logo
    pdf.image(resource_path("img/cuentas_banco.png"), x=20, y=170, w=180)

    pdf.set_xy(19, 185)
    # Tercer párrafo
    texto3 = """Finalmente, le recordamos que, como parte de nuestras políticas de calidad y crédito a clientes, le invitamos a cuidar su línea de crédito, evitar caer en moras y afectar su calificación en su evaluación. Agradecemos su comprensión y colaboración."""
    pdf.multi_cell(0, 8, texto3)
    pdf.ln(5)  # Espacio extra antes de la firma

    # Firma
    pdf.set_font("Arial", "B", 10)
    pdf.text(19, 220, "Atentamente")
    # pdf.ln(5)
    pdf.text(19, 227, "L.C. Juana Elizabeth Moreno Zambrano")
    pdf.text(19, 234, "Crédito y cobranza")
    pdf.text(19, 241, "APG Química SA de CV")

    pdf.set_fill_color(128, 144, 176)  # Azul
    pdf.rect(0,250,218,30, round_corners = False, style = "F")

    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial", size = 10)
    text1 = 'Ezequiel Montes # 401, Localidad El Carmen. El Marqués, Qro.'
    text2 = 'TEL. / Fax   (442)  218 17 00'
    # pdf.text(65,268, '(442) 221 6466, (442) 221 6467, (442) 221 5255')
    text3 = 'Email:    creditoycobranza@apgquimica.com.mx  cp.carlosluna@apgquimica.com.mx '

    page_width = pdf.w
    #calcular posiciones
    x1 = (page_width - pdf.get_string_width(text1)) / 2
    x2 = (page_width - pdf.get_string_width(text2)) / 2
    x3 = (page_width - pdf.get_string_width(text3)) / 2

    #centrar textos
    pdf.text(x1, 263, text1)
    pdf.text(x2, 268, text2)
    pdf.text(x3, 273, text3)

    # pdf.ln(5)



    # # Guardar PDF
    pdf.output(f"{folder_path}/EC_{str(cliente)}-{cve_cliente}_{year}{month_2}{day}.pdf")
    print("PDF generado exitosamente.")
