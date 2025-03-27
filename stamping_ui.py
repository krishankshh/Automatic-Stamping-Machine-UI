import tkinter as tk
from tkinter import Label, Button
import random  # Simulating sensor input (Replace with real sensor input)
import time

# Function to update sensor status
def update_sensor_status():
    """Simulates sensor detecting paper presence (Replace with real sensor logic)."""
    is_paper_present = random.choice([True, False])  # Simulating laser sensor detection
    if is_paper_present:
        sensor_label.config(text="Paper Status: ✅ Paper Present", fg="green")
    else:
        sensor_label.config(text="Paper Status: ❌ No Paper", fg="red")
    
    # Schedule next update in 2 seconds
    root.after(2000, update_sensor_status)

# Function to increase stamped paper count
def stamp_paper():
    """Increments the count when a paper is stamped."""
    global stamped_count
    stamped_count += 1
    count_label.config(text=f"Papers Stamped: {stamped_count}")

# Debugging output for Codespaces
print("✅ Tkinter UI is starting...")

# Create main window
root = tk.Tk()
root.title("Automatic Stamping Machine")
root.geometry("400x300")  # Window size

# Labels
sensor_label = Label(root, text="Paper Status: Checking...", font=("Arial", 14))
sensor_label.pack(pady=20)

count_label = Label(root, text="Papers Stamped: 0", font=("Arial", 14))
count_label.pack(pady=10)

# Button to stamp paper
stamp_button = Button(root, text="Stamp Paper", font=("Arial", 12), command=stamp_paper)
stamp_button.pack(pady=20)

# Initialize paper count
stamped_count = 0

# Start updating sensor status
root.after(1000, update_sensor_status)

# Debugging output for Codespaces
print("✅ Tkinter window created successfully!")

# Start UI
root.mainloop()
