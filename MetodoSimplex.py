import tkinter as tk
from tkinter import messagebox
import numpy as np
from scipy.optimize import linprog

class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Simplex")

        # Etiquetas y campos de entrada para el número de variables y restricciones
        tk.Label(root, text="Número de variables:").grid(row=0, column=0)
        tk.Label(root, text="Número de restricciones:").grid(row=1, column=0)
        tk.Label(root, text="Tipo de optimización:").grid(row=2, column=0)

        self.num_vars_entry = tk.Entry(root)
        self.num_vars_entry.grid(row=0, column=1)
        self.num_restrictions_entry = tk.Entry(root)
        self.num_restrictions_entry.grid(row=1, column=1)

        self.optimization_type = tk.StringVar(root)
        self.optimization_type.set("Maximizar")
        tk.OptionMenu(root, self.optimization_type, "Maximizar", "Minimizar").grid(row=2, column=1)

        tk.Button(root, text="Siguiente", command=self.create_input_fields).grid(row=3, columnspan=2)

        self.entries = []
        self.coeff_entries = []
        self.constraint_entries = []
        self.solve_button = None  # Botón Resolver
        self.function_label = None  # Etiqueta "Coeficientes de la función objetivo"
        self.restriction_label = None  # Etiqueta "Restricciones"

    def create_input_fields(self):
        if self.solve_button is not None:
            self.solve_button.destroy()  # Eliminar el botón Resolver si ya existe

        try:
            self.num_vars = int(self.num_vars_entry.get())
            self.num_restrictions = int(self.num_restrictions_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")
            return

        if self.function_label is not None:
            self.function_label.destroy()  # Eliminar la etiqueta "Coeficientes de la función objetivo" si ya existe
            self.function_label = None

        if self.restriction_label is not None:
            self.restriction_label.destroy()  # Eliminar la etiqueta "Restricciones" si ya existe
            self.restriction_label = None

        tk.Label(self.root, text="Coeficientes de la función objetivo:").grid(row=4, columnspan=2)
        self.coeff_entries = []
        for i in range(self.num_vars):
            entry = tk.Entry(self.root)
            entry.grid(row=5, column=i)
            self.coeff_entries.append(entry)

        tk.Label(self.root, text="Restricciones:").grid(row=6, columnspan=2)
        self.constraint_entries = []
        for i in range(self.num_restrictions):
            row_entries = []
            for j in range(self.num_vars):
                entry = tk.Entry(self.root)
                entry.grid(row=7+i, column=j)
                row_entries.append(entry)
            self.constraint_entries.append(row_entries)
            entry = tk.Entry(self.root)
            entry.grid(row=7+i, column=self.num_vars)
            row_entries.append(entry)

        self.solve_button = tk.Button(self.root, text="Resolver", command=self.solve)
        self.solve_button.grid(row=8+self.num_restrictions, columnspan=2)
        tk.Button(self.root, text="Limpiar", command=self.clear_fields).grid(row=9+self.num_restrictions, columnspan=2)

    def clear_fields(self):
        # Limpiar campos de entrada y reiniciar estado de la aplicación
        self.num_vars_entry.delete(0, tk.END)
        self.num_restrictions_entry.delete(0, tk.END)
        self.optimization_type.set("Maximizar")

        if self.function_label is not None:
            self.function_label.destroy()  # Eliminar la etiqueta "Coeficientes de la función objetivo" si existe
            self.function_label = None

        for entry in self.coeff_entries:
            entry.destroy()
        self.coeff_entries.clear()

        if self.restriction_label is not None:
            self.restriction_label.destroy()  # Eliminar la etiqueta "Restricciones" si existe
            self.restriction_label = None

        for row_entries in self.constraint_entries:
            for entry in row_entries:
                entry.destroy()
        self.constraint_entries.clear()

        if self.solve_button is not None:
            self.solve_button.destroy()  # Eliminar el botón Resolver si existe

    def solve(self):
        try:
            c = np.array([float(entry.get()) for entry in self.coeff_entries])
            A = np.array([[float(entry.get()) for entry in row[:-1]] for row in self.constraint_entries])
            b = np.array([float(row[-1].get()) for row in self.constraint_entries])
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos en las matrices.")
            return

        if self.optimization_type.get() == "Minimizar":
            res = linprog(c, A_ub=A, b_ub=b)
            if res.success:
                valor_optimo = res.fun  # Valor óptimo devuelto por linprog
                messagebox.showinfo("Solución", f"Solución óptima: {res.x}\nValor óptimo: {valor_optimo}")
            else:
                messagebox.showerror("Error", "El problema no tiene solución óptima acotada.")
        else:
            res = linprog(-c, A_ub=A, b_ub=b)
            if res.success:
                valor_optimo = -res.fun  # Valor óptimo devuelto por linprog
                messagebox.showinfo("Solución", f"Solución óptima: {res.x}\nValor óptimo: {valor_optimo}")
            else:
                messagebox.showerror("Error", "El problema no tiene solución óptima acotada.")

root = tk.Tk()
app = SimplexApp(root)
root.mainloop()
