import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to validate entries
def validar_entrada(entry):
    try:
        return float(entry.get())
    except ValueError:
        return None

# Calculation functions
def calcular_flujo_calor(k, A, T1, T2, L):
    return abs((k * A * (T1 - T2)) / L)

def calcular_conductividad(Q, A, T1, T2, L):
    return abs((Q * L) / (A * (T1 - T2)))

def calcular_area(Q, k, T1, T2, L):
    return abs((Q * L) / (k * (T1 - T2)))

def calcular_temperatura_inicial(Q, k, A, T2, L):
    return abs((Q * L) / (k * A) + T2)

def calcular_temperatura_final(Q, k, A, T1, L):
    return abs(T1 - (Q * L) / (k * A))

def calcular_espesor(Q, k, A, T1, T2):
    return abs((Q * A) / (k * (T1 - T2)))

def calcular():
    try:
        Q = validar_entrada(entry_Q)
        A = validar_entrada(entry_A)
        T1 = validar_entrada(entry_T1)
        T2 = validar_entrada(entry_T2)
        L = validar_entrada(entry_L)
        k = validar_entrada(entry_k)

        # Check if time is included
        if var_tiempo.get():
            tiempo = validar_entrada(entry_tiempo)
            unidad_tiempo = combo_tiempo.get()
            if unidad_tiempo == "Minutos":
                tiempo *= 60  # Convert minutes to seconds
            elif unidad_tiempo == "Horas":
                tiempo *= 3600  # Convert hours to seconds
        else:
            tiempo = 1  # Default to 1 second if not selected

        variable = combo_variable.get()
        explicacion = ""

        # Calculations based on selected variable
        if variable == "Flujo de calor (Q)":
            resultado = calcular_flujo_calor(k, A, T1, T2, L) * tiempo
            unidad = "W" if not var_tiempo.get() else "J"
            formula = r"$Q = \frac{k \cdot A \cdot (T1 - T2)}{L} \cdot t$"
            explicacion = generar_explicacion_flujo_calor(k, A, T1, T2, L, tiempo, resultado, unidad, formula)

        elif variable == "Conductividad térmica (k)":
            resultado = calcular_conductividad(Q, A, T1, T2, L)
            unidad = "W/m·K"
            formula = r"$k = \frac{Q \cdot L}{A \cdot (T1 - T2)}$"
            explicacion = generar_explicacion_conductividad(Q, A, T1, T2, L, resultado, unidad, formula)

        elif variable == "Área de la superficie (A)":
            resultado = calcular_area(Q, k, T1, T2, L) * tiempo
            unidad = "m²"
            formula = r"$A = \frac{Q \cdot L}{k \cdot (T1 - T2)}$"
            explicacion = generar_explicacion_area(Q, k, T1, T2, L, tiempo, resultado, unidad, formula)

        elif variable == "Temperatura inicial (T1)":
            resultado = calcular_temperatura_inicial(Q, k, A, T2, L)
            unidad = "K"
            formula = r"$T1 = \frac{Q \cdot L}{k \cdot A} + T2$"
            explicacion = generar_explicacion_temperatura_inicial(Q, k, A, T2, L, resultado, unidad, formula)

        elif variable == "Temperatura final (T2)":
            resultado = calcular_temperatura_final(Q, k, A, T1, L)
            unidad = "K"
            formula = r"$T2 = T1 - \frac{Q \cdot L}{k \cdot A}$"
            explicacion = generar_explicacion_temperatura_final(Q, k, A, T1, L, resultado, unidad, formula)

        elif variable == "Espesor del material (L)":
            resultado = calcular_espesor(Q, k, A, T1, T2) * tiempo
            unidad = "m"
            formula = r"$L = \frac{Q \cdot A}{k \cdot (T1 - T2)}$"
            explicacion = generar_explicacion_espesor(Q, k, A, T1, T2, resultado, unidad, formula)

        # Display results and explanations
        label_resultado.config(text=f"{variable}: {resultado:.2f} {unidad}")
        label_explicacion.config(text=explicacion)

        # Update log with input and output values
        actualizar_log(variable, Q, k, A, T1, T2, L, resultado, unidad)

    except ValueError:
        continuar = messagebox.askyesno("Error", "Se ha producido un error. ¿Desea continuar con la operación?")
        if continuar:
            label_resultado.config(text="")
            label_explicacion.config(text="")
        else:
            return

def habilitar_campos(variable):
    campos = {
        "Flujo de calor (Q)": [entry_k, entry_A, entry_T1, entry_T2, entry_L],
        "Conductividad térmica (k)": [entry_Q, entry_A, entry_T1, entry_T2, entry_L],
        "Área de la superficie (A)": [entry_Q, entry_k, entry_T1, entry_T2, entry_L],
        "Temperatura inicial (T1)": [entry_Q, entry_k, entry_A, entry_T2, entry_L],
        "Temperatura final (T2)": [entry_Q, entry_k, entry_A, entry_T1, entry_L],
        "Espesor del material (L)": [entry_Q, entry_k, entry_A, entry_T1, entry_T2],
    }

    # Disable all fields
    for entry in [entry_Q, entry_k, entry_A, entry_T1, entry_T2, entry_L]:
        entry.config(state=tk.DISABLED)

    # Enable only the necessary fields based on the selected variable
    if variable in campos:
        for entry in campos[variable]:
            entry.config(state=tk.NORMAL)
    elif variable == "=====Lista Var.========":
        # Ensure all fields remain disabled
        for entry in [entry_Q, entry_k, entry_A, entry_T1, entry_T2, entry_L]:
            entry.config(state=tk.DISABLED)

# Functions to generate explanations
def generar_explicacion_flujo_calor(k, A, T1, T2, L, tiempo, resultado, unidad, formula):
    return (
        "Para calcular el flujo de calor (Q), seguimos estos pasos:\n"
        f"1. Identificamos los valores:\n"
        f"   - Conductividad térmica (k): {k} W/m·K\n"
        f"   - Área de la superficie (A): {A} m²\n"
        f"   - Temperatura inicial (T1): {T1} K\n"
        f"   - Temperatura final (T2): {T2} K\n"
        f"   - Espesor del material (L): {L} m\n"
        f"   - Tiempo: {tiempo} s\n"
        "2. Aplicamos la fórmula:\n"
        f"   {formula}\n"
        "3. Calculamos la diferencia de temperatura:\n"
        f"   T1 - T2 = {T1} - {T2} = {T1 - T2} K\n"
        "4. Sustituimos los valores en la fórmula:\n"
        f"   Q = ({k} * {A} * ({T1} - {T2})) / {L} * {tiempo}\n"
        f"   Q = {resultado:.2f} {unidad}\n"
        "5. El resultado en joules (J) representa la energía total transferida a través del material durante el tiempo especificado.\n"
    )

def generar_explicacion_conductividad(Q, A, T1, T2, L, resultado, unidad, formula):
    return (
        "Para calcular la conductividad térmica (k), seguimos estos pasos:\n"
        f"1. Identificamos los valores:\n"
        f"   - Flujo de calor (Q): {Q} W\n"
        f"   - Área de la superficie (A): {A} m²\n"
        f"   - Temperatura inicial (T1): {T1} K\n"
        f"   - Temperatura final (T2): {T2} K\n"
        f"   - Espesor del material (L): {L} m\n"
        "2. Aplicamos la fórmula:\n"
        f"   {formula}\n"
        "3. Sustituimos los valores en la fórmula:\n"
        f"   k = ({Q} * {L}) / ({A} * ({T1} - {T2}))\n"
        f"   k = {resultado:.2f} {unidad}\n"
        "4. Este resultado indica cuán eficientemente el material conduce el calor.\n"
    )

def generar_explicacion_area(Q, k, T1, T2, L, tiempo, resultado, unidad, formula):
    return (
        "Para calcular el área de la superficie (A), seguimos estos pasos:\n"
        f"1. Identificamos los valores:\n"
        f"   - Flujo de calor (Q): {Q} W\n"
        f"   - Conductividad térmica (k): {k} W/m·K\n"
        f"   - Temperatura inicial (T1): {T1} K\n"
        f"   - Temperatura final (T2): {T2} K\n"
        f"   - Espesor del material (L): {L} m\n"
        f"   - Tiempo: {tiempo} s\n"
        "2. Aplicamos la fórmula:\n"
        f"   {formula}\n"
        "3. Sustituimos los valores en la fórmula:\n"
        f"   A = ({Q} * {L}) / ({k} * ({T1} - {T2}))\n"
        f"   A = {resultado:.2f} {unidad}\n"
        "4. Este resultado indica el área necesaria para que el flujo de calor (Q) se mantenga.\n"
    )

def generar_explicacion_temperatura_inicial(Q, k, A, T2, L, resultado, unidad, formula):
    return (
        "Para calcular la temperatura inicial (T1), seguimos estos pasos:\n"
        f"1. Identificamos los valores:\n"
        f"   - Flujo de calor (Q): {Q} W\n"
        f"   - Conductividad térmica (k): {k} W/m·K\n"
        f"   - Área de la superficie (A): {A} m²\n"
        f"   - Temperatura final (T2): {T2} K\n"
        f"   - Espesor del material (L): {L} m\n"
        "2. Aplicamos la fórmula:\n"
        f"   {formula}\n"
        "3. Sustituimos los valores en la fórmula:\n"
        f"   T1 = ({Q} * {L}) / ({k} * {A}) + {T2}\n"
        f"   T1 = {resultado:.2f} {unidad}\n"
        "4. Este resultado indica la temperatura inicial necesaria.\n"
    )

def generar_explicacion_temperatura_final(Q, k, A, T1, L, resultado, unidad, formula):
    return (
        "Para calcular la temperatura final (T2), seguimos estos pasos:\n"
        f"1. Identificamos los valores:\n"
        f"   - Flujo de calor (Q): {Q} W\n"
        f"   - Conductividad térmica (k): {k} W/m·K\n"
        f"   - Área de la superficie (A): {A} m²\n"
        f"   - Temperatura inicial (T1): {T1} K\n"
        f"   - Espesor del material (L): {L} m\n"
        "2. Aplicamos la fórmula:\n"
        f"   {formula}\n"
        "3. Sustituimos los valores en la fórmula:\n"
        f"   T2 = {T1} - ({Q} * {L}) / ({k} * {A})\n"
        f"   T2 = {resultado:.2f} {unidad}\n"
        "4. Este resultado indica la temperatura final del material.\n"
    )

def generar_explicacion_espesor(Q, k, A, T1, T2, resultado, unidad, formula):
    return (
        "Para calcular el espesor del material (L), seguimos estos pasos:\n"
        f"1. Identificamos los valores:\n"
        f"   - Flujo de calor (Q): {Q} W\n"
        f"   - Conductividad térmica (k): {k} W/m·K\n"
        f"   - Área de la superficie (A): {A} m²\n"
        f"   - Temperatura inicial (T1): {T1} K\n"
        f"   - Temperatura final (T2): {T2} K\n"
        "2. Aplicamos la fórmula:\n"
        f"   {formula}\n"
        "3. Sustituimos los valores en la fórmula:\n"
        f"   L = ({Q} * {A}) / ({k} * ({T1} - {T2}))\n"
        f"   L = {resultado:.2f} {unidad}\n"
        "4. Este resultado indica el espesor del material necesario.\n"
    )

def actualizar_log(variable, Q, k, A, T1, T2, L, resultado, unidad):
    # Add entry to the log
    log_entry = f"{variable}: {resultado:.2f} {unidad} | Q: {Q}, k: {k}, A: {A}, T1: {T1}, T2: {T2}, L: {L}"
    listbox_log.insert(tk.END, log_entry)

    # Display the graph in a new canvas
    for widget in frame_grafica.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to enable/disable time fields
def toggle_tiempo_fields(estado):
    if estado:
        entry_tiempo.config(state=tk.NORMAL)
        combo_tiempo.config(state=tk.NORMAL)
    else:
        entry_tiempo.config(state=tk.DISABLED)
        combo_tiempo.config(state=tk.DISABLED)
#==================================================================START OF UI===============================================================================#
# Create the main window
root = tk.Tk()
root.title("LEY THE Fourier")

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
    "1. Selecciona la variable que deseas calcular en el menú desplegable.\n"
    "2. Ingresa los valores requeridos en los campos correspondientes (requerde que los valores ingresados.\n"
    "tienen que cumplicar la normativa del sistema internacional ya que el programa se encargara de cambairlo a kelvin.\n"
    "3. Si deseas incluir un tiempo en el cálculo, selecciona la unidad de tiempo y proporciona el valor.\n"
    "4. Haz clic en el botón 'Calcular'.\n"
    "5. El resultado y la explicación del cálculo aparecerán a continuación.\n"
    "6. Revisa el registro de cálculos realizados en la sección de log."
)
label_instrucciones_detalle = ttk.Label(frame_content, text=instructions_text, justify=tk.LEFT)
label_instrucciones_detalle.grid(column=0, row=0, columnspan=2, padx=10, pady=5)

# Create a label frame for inputs
frame_inputs = ttk.LabelFrame(frame_content, text="Entradas")
frame_inputs.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky="ew")

# Dropdown menu
ttk.Label(frame_inputs, text="Seleccionar Variable:").grid(column=0, row=0, padx=10, pady=5, sticky=tk.E)
combo_variable = ttk.Combobox(frame_inputs, values=["=====Lista Var.========", "Flujo de calor (Q)", "Conductividad térmica (k)", "Área de la superficie (A)", "Temperatura inicial (T1)", "Temperatura final (T2)", "Espesor del material (L)"], state="readonly")
combo_variable.grid(column=1, row=0, padx=10, pady=5)
combo_variable.current(0)

# Create and place input fields
ttk.Label(frame_inputs, text="Flujo de calor (Q):").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
entry_Q = ttk.Entry(frame_inputs)
entry_Q.grid(column=1, row=1, padx=5, pady=2)
entry_Q.config(state=tk.DISABLED)  # Disable initially

ttk.Label(frame_inputs, text="Conductividad térmica (k):").grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
entry_k = ttk.Entry(frame_inputs)
entry_k.grid(column=1, row=2, padx=5, pady=2)
entry_k.config(state=tk.DISABLED)  # Disable initially

ttk.Label(frame_inputs, text="Área de la superficie (A):").grid(column=0, row=3, padx=10, pady=5, sticky=tk.E)
entry_A = ttk.Entry(frame_inputs)
entry_A.grid(column=1, row=3, padx=10, pady=5)
entry_A.config(state=tk.DISABLED)  # Disable initially

ttk.Label(frame_inputs, text="Temperatura inicial (T1):").grid(column=0, row=4, padx=10, pady=5, sticky=tk.E)
entry_T1 = ttk.Entry(frame_inputs)
entry_T1.grid(column=1, row=4, padx=10, pady=5)
entry_T1.config(state=tk.DISABLED)  # Disable initially

ttk.Label(frame_inputs, text="Temperatura final (T2):").grid(column=0, row=5, padx=10, pady=5, sticky=tk.E)
entry_T2 = ttk.Entry(frame_inputs)
entry_T2.grid(column=1, row=5, padx=10, pady=5)
entry_T2.config(state=tk.DISABLED)  # Disable initially

ttk.Label(frame_inputs, text="Espesor del material (L):").grid(column=0, row=6, padx=10, pady=5, sticky=tk.E)
entry_L = ttk.Entry(frame_inputs)
entry_L.grid(column=1, row=6, padx=10, pady=5)
entry_L.config(state=tk.DISABLED)  # Disable initially

# Create a label frame for time selection
frame_tiempo = ttk.LabelFrame(frame_content, text="Tiempo")
frame_tiempo.grid(column=0, row=7, columnspan=2, padx=10, pady=5, sticky="ew")

var_tiempo = tk.BooleanVar(value=False)  # Set checkbox as unchecked by default
checkbox_tiempo = ttk.Checkbutton(frame_tiempo, text="Incluir tiempo en el cálculo", variable=var_tiempo, command=lambda: toggle_tiempo_fields(var_tiempo.get()))
checkbox_tiempo.grid(column=0, row=0, columnspan=2, pady=5)

ttk.Label(frame_tiempo, text="Tiempo:").grid(column=0, row=1, padx=10, pady=5, sticky=tk.E)
entry_tiempo = ttk.Entry(frame_tiempo)
entry_tiempo.grid(column=1, row=1, padx=10, pady=5)

ttk.Label(frame_tiempo, text="Unidad de tiempo:").grid(column=0, row=2, padx=10, pady=5, sticky=tk.E)
combo_tiempo = ttk.Combobox(frame_tiempo, values=["Segundos", "Minutos", "Horas"], state="readonly")
combo_tiempo.grid(column=1, row=2, padx=10, pady=5)
combo_tiempo.current(0)  # Default to seconds

# Create and place the calculate button
boton_calcular = ttk.Button(frame_content, text="Calcular", command=calcular)
boton_calcular.grid(column=0, row=8, columnspan=2, pady=10)

# Create and place labels to show results and explanations
label_resultado = ttk.Label(frame_content, text="", font=("Arial", 12, "bold"))
label_resultado.grid(column=0, row=9, columnspan=2, padx=10, pady=5)

label_explicacion = ttk.Label(frame_content, text="", justify=tk.LEFT)
label_explicacion.grid(column=0, row=10, columnspan=2, padx=10, pady=5)

# Create and place the log of calculations
frame_log = ttk.LabelFrame(frame_content, text="Log de Cálculos")
frame_log.grid(column=0, row=11, columnspan=2, padx=10, pady=5, sticky="ew")
listbox_log = tk.Listbox(frame_log, width=70, height=10)
listbox_log.pack(padx=10, pady=5)

# Create and place the frame for displaying the formula
frame_formula = ttk.LabelFrame(frame_content, text="Fórmula")
frame_formula.grid(column=0, row=12, columnspan=2, padx=10, pady=5, sticky="ew")

# Initialize the state of the time fields
toggle_tiempo_fields(var_tiempo.get())

# Configure event to enable/disable fields when selecting variable
combo_variable.bind("<<ComboboxSelected>>", lambda event: habilitar_campos(combo_variable.get()))

# Update scroll region
def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


# Run the main loop
root.mainloop()
