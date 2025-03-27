import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StampingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Stamping Machine")
        # Set a minimum window size for a 3.5-inch display
        self.minsize(320, 240)
        self.geometry("800x600")  # Default size for a professional dashboard; resizable.
        
        # Apply a theme and styling for a professional look
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Helvetica", 10), padding=5)
        self.style.configure("TButton", font=("Helvetica", 10), padding=5)
        self.style.configure("Header.TLabel", font=("Helvetica", 12, "bold"), padding=8)
        
        # Machine state variables
        self.is_running = False
        self.paper_count = 0
        self.stamp_history = []  # list of (timestamp, paper_count)
        self.sensor_threshold = 50  # simulated sensor calibration value
        self.hardware_temp = 25.0   # simulated hardware temperature

        self.create_widgets()
        self.update_sensor_status()
        self.update_hardware_feedback()
    
    def create_widgets(self):
        # --- Header Section ---
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        ttk.Label(header_frame, text="Auto Stamping Machine Dashboard", style="Header.TLabel").grid(row=0, column=0)

        # --- Status Section ---
        status_frame = ttk.LabelFrame(self, text="Status", padding=10)
        status_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.machine_status_label = ttk.Label(status_frame, text="Machine: Stopped", foreground="red")
        self.machine_status_label.grid(row=0, column=0, sticky="w")
        self.sensor_status_label = ttk.Label(status_frame, text="Paper: Unknown")
        self.sensor_status_label.grid(row=0, column=1, sticky="w", padx=10)
        self.error_alert_label = ttk.Label(status_frame, text="", foreground="red")
        self.error_alert_label.grid(row=1, column=0, columnspan=2, sticky="w")
        self.hardware_feedback_label = ttk.Label(status_frame, text="Temp: 25°C")
        self.hardware_feedback_label.grid(row=0, column=2, sticky="e", padx=10)
        
        # --- Control Section ---
        control_frame = ttk.LabelFrame(self, text="Controls", padding=10)
        control_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        ttk.Label(control_frame, text="Set Speed (pps):").grid(row=0, column=0, sticky="w")
        self.speed_var = tk.DoubleVar(value=60)
        self.speed_slider = ttk.Scale(control_frame, from_=1, to=60, variable=self.speed_var, command=self.update_speed_label)
        self.speed_slider.grid(row=0, column=1, sticky="ew", padx=5)
        self.current_speed_label = ttk.Label(control_frame, text="Current Speed: 60 pps")
        self.current_speed_label.grid(row=0, column=2, sticky="w", padx=5)
        self.start_stop_btn = ttk.Button(control_frame, text="Start", command=self.toggle_machine)
        self.start_stop_btn.grid(row=1, column=0, padx=5, pady=5)
        self.emergency_stop_btn = ttk.Button(control_frame, text="Emergency Stop", command=self.emergency_stop)
        self.emergency_stop_btn.grid(row=1, column=1, padx=5, pady=5)
        self.reset_btn = ttk.Button(control_frame, text="Reset Counter", command=self.reset_counter)
        self.reset_btn.grid(row=1, column=2, padx=5, pady=5)
        self.calibration_btn = ttk.Button(control_frame, text="Calibrate Sensor", command=self.open_calibration_window)
        self.calibration_btn.grid(row=1, column=3, padx=5, pady=5)
        self.paper_count_label = ttk.Label(control_frame, text="Papers Stamped: 0")
        self.paper_count_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # --- Graph Section ---
        graph_frame = ttk.LabelFrame(self, text="Stamping History", padding=10)
        graph_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=10, pady=5)
        self.figure = Figure(figsize=(5,3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Stamping History")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Papers Stamped")
        self.line, = self.ax.plot([], [], 'b-o', label="Stamped Count")
        self.ax.legend()
        self.ax.tick_params(axis='x', rotation=45)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # --- Log Section ---
        log_frame = ttk.LabelFrame(self, text="System Log", padding=10)
        log_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        self.log_text = tk.Text(log_frame, height=8, font=("Helvetica", 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log("System initialized.")

        # Configure grid weights for responsiveness
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def update_speed_label(self, event=None):
        speed = int(self.speed_var.get())
        self.current_speed_label.config(text=f"Current Speed: {speed} pps")
    
    def toggle_machine(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.machine_status_label.config(text="Machine: Running", foreground="green")
            self.start_stop_btn.config(text="Stop")
            self.log("Machine started.")
            self.stamp_paper()  # Begin stamping process
        else:
            self.machine_status_label.config(text="Machine: Stopped", foreground="red")
            self.start_stop_btn.config(text="Start")
            self.log("Machine stopped.")
    
    def emergency_stop(self):
        self.is_running = False
        self.machine_status_label.config(text="Machine: Emergency Stopped", foreground="red")
        self.start_stop_btn.config(text="Start")
        self.log("EMERGENCY STOP activated!")
        messagebox.showwarning("Emergency Stop", "The machine has been emergency stopped!")
    
    def reset_counter(self):
        self.paper_count = 0
        self.paper_count_label.config(text="Papers Stamped: 0")
        self.log("Paper counter reset.")
        self.stamp_history = []
        self.update_graph()
    
    def stamp_paper(self):
        if self.is_running:
            self.paper_count += 1
            self.paper_count_label.config(text=f"Papers Stamped: {self.paper_count}")
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.log(f"{timestamp} - Paper stamped. Count: {self.paper_count}")
            self.stamp_history.append((timestamp, self.paper_count))
            self.update_graph()
            # Calculate interval in milliseconds based on speed (papers per second)
            interval = int(1000 / self.speed_var.get())
            self.after(interval, self.stamp_paper)
    
    def update_sensor_status(self):
        # Simulate a laser sensor reading; replace with actual sensor integration.
        sensor_active = random.choice([True, False])
        if sensor_active:
            self.sensor_status_label.config(text="Paper: Detected", foreground="green")
            self.error_alert_label.config(text="")  # Clear error
        else:
            self.sensor_status_label.config(text="Paper: Empty", foreground="red")
            self.error_alert_label.config(text="Error: Paper missing!")
        self.after(2000, self.update_sensor_status)
    
    def update_hardware_feedback(self):
        # Simulate hardware feedback (e.g., temperature) – replace with real data as needed.
        self.hardware_temp = 20 + random.random() * 10  # between 20 and 30°C
        self.hardware_feedback_label.config(text=f"Temp: {self.hardware_temp:.1f}°C")
        self.after(3000, self.update_hardware_feedback)
    
    def update_graph(self):
        if self.stamp_history:
            times = [t for t, _ in self.stamp_history]
            counts = [c for _, c in self.stamp_history]
            self.ax.clear()
            self.ax.plot(times, counts, 'b-o', label="Stamped Count")
            self.ax.set_title("Stamping History")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Papers Stamped")
            self.ax.legend()
            self.ax.tick_params(axis='x', rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()
    
    def open_calibration_window(self):
        calib_win = tk.Toplevel(self)
        calib_win.title("Sensor Calibration")
        calib_win.geometry("300x150")
        
        ttk.Label(calib_win, text="Set Sensor Threshold:", font=("Helvetica", 10)).pack(pady=10)
        threshold_var = tk.IntVar(value=self.sensor_threshold)
        slider = ttk.Scale(calib_win, from_=0, to=100, variable=threshold_var)
        slider.pack(pady=5)
        
        def apply_calibration():
            self.sensor_threshold = threshold_var.get()
            self.log(f"Sensor threshold calibrated to {self.sensor_threshold}")
            calib_win.destroy()
        
        ttk.Button(calib_win, text="Apply", command=apply_calibration).pack(pady=10)
    
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{timestamp} {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

if __name__ == "__main__":
    app = StampingMachineApp()
    app.mainloop()
