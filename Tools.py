import numpy as np
from joblib import load
import tkinter as tk
from tkinter import ttk

loaded_model = load('trained_model.joblib')

def predict_emission():
    new_numbers = float(numbers_entry.get())
    new_power_per_unit = float(power_per_unit_entry.get())

    new_sample = np.array([[new_numbers, new_power_per_unit]])
    prediction = loaded_model.predict(new_sample)

    result_label.config(text=f"The estimated emission value is: {prediction[0]:.2f} Ton")

root = tk.Tk()
root.title("Emission Estimation")

ttk.Label(root, text="Numbers:").grid(column=0, row=0, padx=10, pady=10)
numbers_entry = ttk.Entry(root)
numbers_entry.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Power per unit:").grid(column=0, row=1, padx=10, pady=10)
power_per_unit_entry = ttk.Entry(root)
power_per_unit_entry.grid(column=1, row=1, padx=10, pady=10)

predict_button = ttk.Button(root, text="Estimate", command=predict_emission)
predict_button.grid(column=0, row=2, columnspan=2, pady=20)

result_label = ttk.Label(root, text="")
result_label.grid(column=0, row=3, columnspan=2, pady=10)

root.mainloop()
