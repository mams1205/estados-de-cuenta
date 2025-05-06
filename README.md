# 💳 Automatización de Estados de Cuenta - Cartera Vencida

Este repositorio contiene un programa en **Python** que consulta una base de datos **SQL** para identificar clientes con **facturas vencidas** o **saldo negativo**, agrupa las facturas por cliente, genera un **estado de cuenta en PDF** y lo envía automáticamente por correo electrónico.

## ⚙️ Tecnologías y Librerías Utilizadas

- **Python**
- **tkinter**: Interfaz gráfica para seleccionar parámetros o ejecutar el proceso manualmente.
- **pandas**: Manipulación de datos.
- **numpy**: Estructuración y cálculos de datos numéricos.
- **pyodbc**: Conexión a la base de datos SQL.
- **fpdf**: Para la generación de archivos PDF.
- **smtplib / email**: Envío automático de correos electrónicos con los estados de cuenta.

## 📌 Funcionalidades

- 🗃️ **Consulta SQL automatizada**  
  Extrae información de la base de datos sobre facturas vencidas y saldos pendientes por cliente.

- 📄 **Generación de estados de cuenta en PDF**  
  Agrupa todas las facturas vencidas de un mismo cliente y forma un documento PDF con su resumen detallado.

- ✉️ **Envío automático por correo electrónico**  
  Envía los archivos PDF a los correos electrónicos registrados de los clientes con cartera vencida.

- 🖥️ **Interfaz de usuario con tkinter**  
  Permite ejecutar el proceso de forma manual con opciones de filtrado y visualización previa.


