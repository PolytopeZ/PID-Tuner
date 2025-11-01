import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from const import Label, Value


class SimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(Label.TITLE)
        self.init_widgets()

    def init_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        # System parameters
        # First order => G(s) = K / (Ts + 1)
        ttk.Label(frame, text=Label.K).grid(row=0, column=0, sticky="e")
        self.value_K = ttk.Entry(frame, width=8)
        self.value_K.insert(0, Value.K_DEFAULT)
        self.value_K.grid(row=0, column=1)

        ttk.Label(frame, text=Label.TAU).grid(row=1, column=0, sticky="e")
        self.value_tau = ttk.Entry(frame, width=8)
        self.value_tau.insert(0, Value.TAU_DEFAULT)
        self.value_tau.grid(row=1, column=1)

        ttk.Label(frame, text=Label.T_SIM).grid(row=2, column=0, sticky="e")
        self.value_t_sim = ttk.Entry(frame, width=8)
        self.value_t_sim.insert(0, Value.T_SIM_DEFAULT)
        self.value_t_sim.grid(row=2, column=1)

        ttk.Label(frame, text=Label.DT).grid(row=3, column=0, sticky="e")
        self.value_dt = ttk.Entry(frame, width=8)
        self.value_dt.insert(0, Value.DT_DEFAULT)
        self.value_dt.grid(row=3, column=1)

        # Inputs
        ttk.Label(frame, text=Label.INPUT).grid(row=4, column=0, sticky="e")
        self.input_type = ttk.Combobox(
            frame, values=[Label.STEP, Label.RAMP], width=10, state="readonly")
        self.input_type.current(0)
        self.input_type.grid(row=4, column=1)
        self.input_type.bind("<<ComboboxSelected>>", self.update_input_fields)

        self.inputs_params_frame = ttk.Frame(frame)
        self.inputs_params_frame.grid(row=5, column=0, columnspan=2, pady=5)
        self.create_input_fields()

        # Button
        btn_run = ttk.Button(frame, text=Label.SIMULATE,
                             command=self.run_sim)
        btn_run.grid(row=6, column=0, columnspan=2, pady=5)

        # Graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=7, padx=10, pady=5)

    def create_input_fields(self):
        for widget in self.inputs_params_frame.winfo_children():
            widget.destroy()

        if self.input_type.get() == Label.STEP:
            ttk.Label(self.inputs_params_frame, text=Label.AMP).grid(
                row=0, column=0, sticky="e")
            self.value_amp = ttk.Entry(self.inputs_params_frame, width=7)
            self.value_amp.insert(0, 1.0)
            self.value_amp.grid(row=0, column=1)

        elif self.input_type.get() == Label.RAMP:
            ttk.Label(self.inputs_params_frame, text=Label.SLOPE).grid(
                row=0, column=0, sticky="e")
            self.value_slope = ttk.Entry(self.inputs_params_frame, width=7)
            self.value_slope.insert(0, 1.0)
            self.value_slope.grid(row=0, column=1)

    def update_input_fields(self, event=None):
        self.create_input_fields()

    def generate_input(self, t):
        if self.input_type.get() == Label.STEP:
            amp = float(self.value_amp.get())
            return amp * np.ones_like(t)
        elif self.input_type.get() == Label.RAMP:
            slope = float(self.value_slope.get())
            return slope * t

    def simulate_first_order(self, K, tau, t, u):
        y = np.zeros_like(t)
        dt = t[1] - t[0]

        for i in range(1, len(t)):
            dy = (-y[i-1] + K * u[i]) / tau * dt
            y[i] = y[i-1] + dy

        return y

    def run_sim(self):
        K = float(self.value_K.get())
        tau = float(self.value_tau.get())
        t_sim = float(self.value_t_sim.get())
        dt = float(self.value_dt.get())

        t = np.arange(0, t_sim + dt, dt)
        u = self.generate_input(t)
        y = self.simulate_first_order(K, tau, t, u)

        self.ax.clear()
        self.ax.plot(t, u, label=Label.INPUT_PLOT)
        self.ax.plot(t, y, label=Label.OUTPUT_PLOT)
        self.ax.set_xlabel(Label.X_AXIS)
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimulatorApp(root)

    def on_close():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
