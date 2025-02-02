import tkinter as tk
from tkinter import ttk
import math

# Create the main window
root = tk.Tk()
root.title("Calculadora de Enfriamiento de Newton")

# Create a frame for the scrollbar
frame_main = tk.Frame(root)
frame_main.pack(fill=tk.BOTH, expand=True)

# Create a canvas for scrolling
canvas = tk.Canvas(frame_main)
canvas.grid(row=0, column=0, sticky="nsew")

# Create vertical scrollbar
v_scrollbar = tk.Scrollbar(frame_main, orient="vertical", command=canvas.yview)
v_scrollbar.grid(row=0, column=1, sticky="ns")

# Create horizontal scrollbar
h_scrollbar = tk.Scrollbar(frame_main, orient="horizontal", command=canvas.xview)
h_scrollbar.grid(row=1, column=0, sticky="ew")

# Configure the canvas
canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Create a frame inside the canvas
frame_content = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_content, anchor="nw")

# Adjust the canvas to make the scrollbar overlap
canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

# Ensure the horizontal scrollbar works with the width of the content
frame_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Configure grid weights to ensure proper resizing
frame_main.grid_rowconfigure(0, weight=1)
frame_main.grid_columnconfigure(0, weight=1)

# Instructions text
instructions_text = (
    "1. Ingresa los valores correspondientes en los campos habilitados.\n"
    "2. Haz clic en el botón 'Calcular'.\n"
    "3. El resultado y la explicación del cálculo aparecerán a continuación.\n"
    "4. Revisa el registro de cálculos realizados en la sección de log."
)
label_instrucciones_detalle = ttk.Label(frame_content, text=instructions_text, justify=tk.LEFT)
label_instrucciones_detalle.grid(column=0, row=0, columnspan=2, padx=10, pady=5)

# Create a label frame for inputs
frame_inputs = ttk.LabelFrame(frame_content, text="Entradas")
frame_inputs.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky="ew")

# Create and place input fields
ttk.Label(frame_inputs, text="Temperatura inicial (T1):").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
entry_T1 = ttk.Entry(frame_inputs)
entry_T1.grid(column=1, row=1, padx=5, pady=2)

ttk.Label(frame_inputs, text="Temperatura ambiente (Ta):").grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
entry_Ta = ttk.Entry(frame_inputs)
entry_Ta.grid(column=1, row=2, padx=5, pady=2)

ttk.Label(frame_inputs, text="Constante de enfriamiento (h):").grid(column=0, row=3, padx=5, pady=5, sticky=tk.E)
entry_h = ttk.Entry(frame_inputs)
entry_h.grid(column=1, row=3, padx=5, pady=2)

ttk.Label(frame_inputs, text="Tiempo (t en minutos):").grid(column=0, row=4, padx=5, pady=5, sticky=tk.E)
entry_t = ttk.Entry(frame_inputs)
entry_t.grid(column=1, row=4, padx=5, pady=2)

# Create and place the calculate button
boton_calcular = ttk.Button(frame_content, text="Calcular", command=lambda: calcular())
boton_calcular.grid(column=0, row=5, columnspan=2, pady=10)

# Create and place labels to show results and explanations
label_resultado = ttk.Label(frame_content, text="", font=("Arial", 12, "bold"))
label_resultado.grid(column=0, row=6, columnspan=2, padx=10, pady=5)

label_explicacion = ttk.Label(frame_content, text="", justify=tk.LEFT)
label_explicacion.grid(column=0, row=7, columnspan=2, padx=10, pady=5)

# Create and place the log of calculations
frame_log = ttk.LabelFrame(frame_content, text="Log de Cálculos")
frame_log.grid(column=0, row=8, columnspan=2, padx=10, pady=5, sticky="ew")
listbox_log = tk.Listbox(frame_log, width=70, height=10)
listbox_log.pack(padx=10, pady=5)

# Function to calculate temperature based on Newton's Law of Cooling
def calcular():
    T1 = float(entry_T1.get())
    Ta = float(entry_Ta.get())
    h = float(entry_h.get())
    time = float(entry_t.get())

    # Calculate temperature after time using Newton's Law of Cooling
    T = Ta + (T1 - Ta) * math.exp(-h * time / 60)  # Convert time to hours
    label_resultado.config(text=f"Temperatura después de {time} minutos: {T:.2f} °C")
    label_explicacion.config(text=f"La temperatura del objeto después de {time} minutos es aproximadamente {T:.2f} °C.\n"
                                  f"1. Identificamos los valores:\n"
                                  f"   - Temperatura inicial (T1): {T1} °C\n"
                                  f"   - Temperatura ambiente (Ta): {Ta} °C\n"
                                  f"   - Constante de enfriamiento (h): {h}\n"
                                  f"   - Tiempo (t): {time} minutos\n"
                                  f"2. Aplicamos la fórmula:\n"
                                  f"   T(t) = Ta + (T1 - Ta) * e^(-h * t / 60)\n"
                                  f"3. Calculamos el exponente:\n"
                                  f"   -h * t / 60 = -{h} * {time} / 60 = {-h * time / 60}\n"
                                  f"4. Calculamos el valor de e elevado al exponente:\n"
                                  f"   e^{{-h * t / 60}} = e^{{{-h * time / 60}}} ≈ {math.exp(-h * time / 60):.4f}\n"
                                  f"5. Sustituimos este valor en la fórmula:\n"
                                  f"   T(t) = {Ta} + ({T1} - {Ta}) * {math.exp(-h * time / 60):.4f}\n"
                                  f"6. Realizamos la multiplicación y sumamos a la temperatura ambiente:\n"
                                  f"   T(t) = {T:.2f} °C\n"
                                  f"7. El resultado es la temperatura del objeto después del tiempo especificado.\n")
    log_entry = f"T1: {T1} °C, Ta: {Ta} °C, h: {h}, Tiempo: {time} min => Resultado: {T:.2f} °C"
    listbox_log.insert(tk.END, log_entry)

# Run the main loop
root.mainloop()
