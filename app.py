import tkinter as tk
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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
    
    def save_to_pdf(self, project, task, elapsed_time):
        pdf_filename = "time_tracker_log.pdf"
        styles = getSampleStyleSheet()
        
        try:
            existing_entries = []
            with open(pdf_filename, "rb") as f:
                existing_entries = f.readlines()
            
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            story = []
            
            story.append(Paragraph("Time Tracker Log", styles['Title']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
            story.append(Paragraph(f"Project Name: {project}", styles['Normal']))
            story.append(Paragraph(f"Task Name: {task}", styles['Normal']))
            story.append(Paragraph(f"Time Tracked: {str(elapsed_time)}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            for entry in existing_entries:
                try:
                    story.append(Paragraph(entry.decode("utf-8").strip(), styles['Normal']))
                    story.append(Spacer(1, 12))
                except UnicodeDecodeError:
                    pass
            
            doc.build(story)
        except FileNotFoundError:
            pass
    
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
