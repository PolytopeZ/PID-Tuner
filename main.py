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
        self.init_input_frame()
        self.init_system_frame()
        self.init_controller_frame()
        self.init_graph_frame()
        self.init_button()

    def init_input_frame(self):
        # ==== Input settings ====
        frame_input = ttk.Frame(self.root, padding=10)
        frame_input.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame_input, text=Label.INPUT).grid(
            row=0, column=0, sticky="e")
        self.input_type = ttk.Combobox(
            frame_input, values=[Label.STEP, Label.RAMP], width=10, state="readonly")
        self.input_type.current(0)
        self.input_type.grid(row=0, column=1)
        self.input_type.bind("<<ComboboxSelected>>", self.update_input_fields)

        self.inputs_params_frame = ttk.Frame(frame_input)
        self.inputs_params_frame.grid(row=1, column=0, columnspan=2, pady=5)
        self.create_input_fields()

    def init_system_frame(self):
        # ==== System settings ====
        # First order => G(s) = K / (Ts + 1)
        frame_system = ttk.Frame(self.root, padding=10)
        frame_system.grid(row=0, column=1, sticky="nsew")

        ttk.Label(frame_system, text=Label.K).grid(
            row=0, column=0, sticky="e")
        self.value_K = ttk.Entry(frame_system, width=8)
        self.value_K.insert(0, Value.K_DEFAULT)
        self.value_K.grid(row=0, column=1)

        ttk.Label(frame_system, text=Label.TAU).grid(
            row=1, column=0, sticky="e")
        self.value_tau = ttk.Entry(frame_system, width=8)
        self.value_tau.insert(0, Value.TAU_DEFAULT)
        self.value_tau.grid(row=1, column=1)

        ttk.Label(frame_system, text=Label.T_SIM).grid(
            row=2, column=0, sticky="e")
        self.value_t_sim = ttk.Entry(frame_system, width=8)
        self.value_t_sim.insert(0, Value.T_SIM_DEFAULT)
        self.value_t_sim.grid(row=2, column=1)

        ttk.Label(frame_system, text=Label.DT).grid(
            row=3, column=0, sticky="e")
        self.value_dt = ttk.Entry(frame_system, width=8)
        self.value_dt.insert(0, Value.DT_DEFAULT)
        self.value_dt.grid(row=3, column=1)

    def init_controller_frame(self):
        # ==== Controller settings ====
        frame_controller = ttk.Frame(self.root, padding=10)
        frame_controller.grid(row=0, column=2, sticky="nsew")

        # Controller selection
        ttk.Label(frame_controller, text=Label.CONTROLLER).grid(
            row=0, column=0, sticky="e")
        self.controller_type = ttk.Combobox(
            frame_controller,
            values=[Label.NONE, Label.P, Label.PI, Label.PID],
            width=10,
            state="readonly"
        )
        self.controller_type.current(0)
        self.controller_type.grid(row=0, column=1)
        self.controller_type.bind(
            "<<ComboboxSelected>>", self.update_controller_fields)

        self.controller_params_frame = ttk.Frame(frame_controller)
        self.controller_params_frame.grid(
            row=1, column=0, columnspan=2, pady=5)
        self.create_controller_fields()

    def init_graph_frame(self):
        # ==== Graph visu ====
        frame_graph = ttk.Frame(self.root, padding=10)
        frame_graph.grid(row=0, column=3, sticky="nsew")

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graph)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, pady=10)

    def init_button(self):
        # ==== Button ====
        btn_run = ttk.Button(self.root, text=Label.SIMULATE,
                             command=self.run_sim)
        btn_run.grid(row=1, column=0, columnspan=3, pady=7)

    def create_input_fields(self):
        # Dynamics fields depending on which input is selected
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

    def create_controller_fields(self):
        for widget in self.controller_params_frame.winfo_children():
            widget.destroy()

        c = self.controller_type.get()
        row = 0

        if c in [Label.P, Label.PI, Label.PID]:
            ttk.Label(self.controller_params_frame, text=Label.KP).grid(
                row=row, column=0, sticky="e")
            self.value_kp = ttk.Entry(self.controller_params_frame, width=8)
            self.value_kp.insert(0, Value.P_DEFAULT)
            self.value_kp.grid(row=row, column=1)
            row += 1

        if c in [Label.PI, Label.PID]:
            ttk.Label(self.controller_params_frame, text=Label.KI).grid(
                row=row, column=0, sticky="e")
            self.value_ki = ttk.Entry(self.controller_params_frame, width=8)
            self.value_ki.insert(0, Value.I_DEFAULT)
            self.value_ki.grid(row=row, column=1)
            row += 1

        if c == Label.PID:
            ttk.Label(self.controller_params_frame, text=Label.KD).grid(
                row=row, column=0, sticky="e")
            self.value_kd = ttk.Entry(self.controller_params_frame, width=8)
            self.value_kd.insert(0, Value.D_DEFAULT)
            self.value_kd.grid(row=row, column=1)

    def update_controller_fields(self, event=None):
        self.create_controller_fields()

    # Generate input depending on if it's a step, ramp ..
    def generate_input(self, t):
        if self.input_type.get() == Label.STEP:
            amp = float(self.value_amp.get())
            return amp * np.ones_like(t)
        elif self.input_type.get() == Label.RAMP:
            slope = float(self.value_slope.get())
            return slope * t

    # Compute 1st order function
    def simulate_first_order(self, K, tau, t, u, controller, kp=0, ki=0, kd=0):
        y = np.zeros_like(t)
        integral = 0.0
        dt = t[1] - t[0]
        e_prev = 0.0

        for i in range(1, len(t)):
            e = u[i] - y[i-1]

            u_c = 0.0
            if controller == Label.NONE:
                u_c = u[i]
            else:
                if controller in ["P", "PI", "PID"]:
                    u_c += kp * e
                if controller in ["PI", "PID"]:
                    integral += e * dt
                    u_c += ki * integral
                if controller == "PID":
                    deriv = (e - e_prev) / dt
                    u_c += kd * deriv

            dy = (-y[i-1] + K * u_c) / tau * dt
            y[i] = y[i-1] + dy
            e_prev = e

        return y

    # Get settings, generate everything and plot
    def run_sim(self):
        K = float(self.value_K.get())
        tau = float(self.value_tau.get())
        t_sim = float(self.value_t_sim.get())
        dt = float(self.value_dt.get())

        controller = self.controller_type.get()
        kp = float(self.value_kp.get()) if controller in [
            Label.P, Label.PI, Label.PID] else 0
        ki = float(self.value_ki.get()) if controller in [
            Label.PI, Label.PID] else 0
        kd = float(self.value_kd.get()) if controller in [
            Label.PID] else 0

        t = np.arange(0, t_sim + dt, dt)
        u = self.generate_input(t)
        y = self.simulate_first_order(K, tau, t, u, controller, kp, ki, kd)

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
