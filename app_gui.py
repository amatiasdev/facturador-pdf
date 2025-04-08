import os
from tkinter import Tk, Label, Entry, Button, messagebox
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Ruta de carpetas
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

# Cargar plantilla HTML con Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template('invoice_template.html')

def generar_factura():
    cliente = entry_cliente.get().strip()
    concepto = entry_concepto.get().strip()
    monto = entry_monto.get().strip()
    fecha = entry_fecha.get().strip() or datetime.now().strftime('%Y-%m-%d')

    if not cliente or not concepto or not monto:
        messagebox.showerror("Error", "Todos los campos excepto fecha son obligatorios.")
        return

    try:
        monto = float(monto)
    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número.")
        return

    html_renderizado = template.render(
        cliente=cliente,
        concepto=concepto,
        monto=f"${monto:.2f}",
        fecha=fecha
    )

    nombre_archivo = f"{cliente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)

    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(html_renderizado)

    messagebox.showinfo("Éxito", f"Factura generada:\n{ruta_archivo}")

# GUI con Tkinter
root = Tk()
root.title("Facturador PDF")

Label(root, text="Cliente:").grid(row=0, column=0, sticky='e')
Label(root, text="Concepto:").grid(row=1, column=0, sticky='e')
Label(root, text="Monto:").grid(row=2, column=0, sticky='e')
Label(root, text="Fecha (opcional):").grid(row=3, column=0, sticky='e')

entry_cliente = Entry(root, width=30)
entry_concepto = Entry(root, width=30)
entry_monto = Entry(root, width=30)
entry_fecha = Entry(root, width=30)

entry_cliente.grid(row=0, column=1, padx=10, pady=5)
entry_concepto.grid(row=1, column=1, padx=10, pady=5)
entry_monto.grid(row=2, column=1, padx=10, pady=5)
entry_fecha.grid(row=3, column=1, padx=10, pady=5)

btn_generar = Button(root, text="Generar HTML", command=generar_factura)
btn_generar.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
