import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class TimeTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Time Tracker")
        
        self.project_label = tk.Label(master, text="Project Name:")
        self.project_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.project_entry = tk.Entry(master)
        self.project_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.task_label = tk.Label(master, text="Task Name:")
        self.task_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.task_entry = tk.Entry(master)
        self.task_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.timer_label = tk.Label(master, text="00:00:00")
        self.timer_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.grid(row=3, column=0, padx=5, pady=5)
        
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=3, column=1, padx=5, pady=5)
        
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_timer)
        self.clear_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        self.running = False
        self.start_time = None
        self.elapsed_time = timedelta()
        self.update_timer()
        
    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.DISABLED)
            self.update_timer()
    
    def stop_timer(self):
        if self.running:
            self.running = False
            end_time = datetime.now()
            self.elapsed_time += end_time - self.start_time
            self.start_time = None
            project_name = self.project_entry.get()
            task_name = self.task_entry.get()
            self.save_to_pdf(project_name, task_name, self.elapsed_time)
            self.project_entry.delete(0, tk.END)
            self.task_entry.delete(0, tk.END)
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.NORMAL)
            self.elapsed_time = timedelta()
            self.timer_label.config(text="00:00:00")
    
    def update_timer(self):
        if self.running:
            elapsed = datetime.now() - self.start_time
            self.timer_label.config(text=str(elapsed).split(".")[0])
            self.timer_label.after(1000, self.update_timer)
    
    #add data to pdf file after stop the timer.

    def save_to_pdf(self, project, task, elapsed_time): 
        pdf_filename = "time_tracker_log.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        
        try:
            with open(pdf_filename, "rb") as f:
                pdf_data = f.read()
                c.drawString(100, 750 - len(pdf_data) * 0.015, "Date: " + datetime.now().strftime('%Y-%m-%d'))
                c.drawString(100, 730 - len(pdf_data) * 0.015, "Project Name: " + project)
                c.drawString(100, 710 - len(pdf_data) * 0.015, "Task Name: " + task)
                c.drawString(100, 690 - len(pdf_data) * 0.015, "Time Tracked: " + str(elapsed_time))
        except FileNotFoundError:
            c.drawString(100, 750, "Date: " + datetime.now().strftime('%Y-%m-%d'))
            c.drawString(100, 730, "Project Name: " + project)
            c.drawString(100, 710, "Task Name: " + task)
            c.drawString(100, 690, "Time Tracked: " + str(elapsed_time))
        
        c.save()
    
    def clear_timer(self):
        self.project_entry.delete(0, tk.END)
        self.task_entry.delete(0, tk.END)
        self.timer_label.config(text="00:00:00")
        if self.running:
            self.running = False
            self.start_time = None
            self.elapsed_time = timedelta()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.NORMAL)
    
def main():
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
