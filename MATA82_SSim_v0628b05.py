# Scheduler Simulator v0628b05
# Build date: 06/28

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import threading
import csv

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("[MATA82] - Task Scheduler Simulator")
        self.root.geometry("1920x1080")
        self.version = "v0628b05"
        self.loaded_filename = None
        self.tasks = []
        self.colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ab"]
        self.setup_ui()

    def setup_ui(self):
        self.name_var = tk.StringVar()
        self.c_var = tk.DoubleVar()
        self.t_var = tk.DoubleVar()
        self.d_var = tk.DoubleVar()
        self.j_var = tk.DoubleVar()
        self.sim_time_var = tk.IntVar(value=100)

        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(left_frame, text="Task Configuration", font=("Arial", 10, "bold")).pack(anchor='w')
        entries = [
            ("Task Name", self.name_var),
            ("Computation Time", self.c_var),
            ("Period", self.t_var),
            ("Deadline", self.d_var),
            ("Jitter (optional)", self.j_var)
        ]
        for lbl, var in entries:
            tk.Label(left_frame, text=lbl).pack(anchor='w')
            tk.Entry(left_frame, textvariable=var, width=30).pack(fill=tk.X)

        tk.Button(left_frame, text="Add Task", command=self.add_task).pack(pady=5)
        tk.Button(left_frame, text="Load CSV", command=self.load_csv).pack()
        tk.Button(left_frame, text="Clear Tasks", command=self.clear_tasks).pack(pady=5)

        self.task_list = tk.Listbox(left_frame, height=10, width=30)
        self.task_list.pack(fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="Simulation Configuration", font=("Arial", 10, "bold")).pack(anchor='w', pady=(10, 0))
        tk.Label(left_frame, text="Simulation Time").pack(anchor='w')
        tk.Entry(left_frame, textvariable=self.sim_time_var).pack(fill=tk.X)
        tk.Button(left_frame, text="Run Simulation", command=self.run_simulation).pack(pady=10)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.graph_canvases = []
        self.result_labels = []
        algorithms = ["RM", "EDF", "LLF"]
        for alg in algorithms:
            frame = tk.Frame(self.canvas_frame, bg='#f0f0f0')
            frame.pack(fill=tk.BOTH, expand=True, pady=2)

            title = tk.Label(frame, text=f"{alg} Simulation", font=("Arial", 10, "bold"), anchor='w')
            title.pack(anchor='w')
            canvas = tk.Canvas(frame, height=250, bg='white')
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            result = tk.Label(frame, text=f"{alg} Results", font=("Arial", 10), relief=tk.SOLID, bd=1, width=35, height=6, anchor='nw', justify='left')
            result.pack(side=tk.RIGHT, padx=10, pady=5)

            self.graph_canvases.append(canvas)
            self.result_labels.append(result)

        self.version_label = tk.Label(self.root, text=f"Version: {self.version}", font=("Arial", 8), fg="orange")
        self.version_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-5)

    def add_task(self):
        task = (self.name_var.get(), self.c_var.get(), self.t_var.get(), self.d_var.get(), self.j_var.get())
        self.tasks.append(task)
        self.task_list.insert(tk.END, f"{task[0]}: C={task[1]} T={task[2]} D={task[3]} J={task[4]}")

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.clear_tasks()
            self.loaded_filename = file_path.split("/")[-1]
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    task = (
                        row["Name"],
                        float(row["Computation Time"]),
                        float(row["Period"]),
                        float(row["Deadline"]),
                        float(row.get("Jitter", 0.0))
                    )
                    self.tasks.append(task)
                    self.task_list.insert(tk.END, f"{task[0]}: C={task[1]} T={task[2]} D={task[3]} J={task[4]}")
            messagebox.showinfo("CSV Loaded", f"Tasks from {self.loaded_filename} loaded successfully.")

    def clear_tasks(self):
        self.tasks.clear()
        self.task_list.delete(0, tk.END)

    def run_simulation(self):
        if not self.tasks:
            messagebox.showwarning("No Tasks", "Please add or load tasks before running the simulation.")
            return
        for canvas in self.graph_canvases:
            canvas.delete("all")
        threading.Thread(target=self.animate_all_schedules, daemon=True).start()

    def animate_all_schedules(self):
        for alg, canvas, label in zip(["RM", "EDF", "LLF"], self.graph_canvases, self.result_labels):
            self.animate_schedule(canvas, alg, label)

    def animate_schedule(self, canvas, algorithm, label):
        time_unit = 0
        sim_time = self.sim_time_var.get()
        px_per_unit = 10
        job_queue = []
        schedule = []
        for name, c, p, d, j in self.tasks:
            release = j
            while release < sim_time:
                schedule.append({
                    "name": name,
                    "release": release,
                    "remaining": c,
                    "deadline": release + d,
                    "period": p,
                    "wcet": c,
                    "start": None,
                    "end": None
                })
                release += p
        schedule.sort(key=lambda x: x["release"])

        for t in range(sim_time):
            canvas.create_line(40 + t * px_per_unit, 30, 40 + t * px_per_unit, 30 + len(self.tasks) * 20, fill="#ccc")
            if t % 5 == 0:
                canvas.create_text(40 + t * px_per_unit, 20, text=str(t), font=("Arial", 7))

        for i, t in enumerate(self.tasks):
            y = 40 + i * 20
            canvas.create_text(25, y + 5, text=t[0], font=("Arial", 8))

        preemptions = 0
        deadline_miss = 0
        response_times = []
        prev_job = None

        while time_unit < sim_time:
            for job in schedule:
                if job["release"] == time_unit:
                    job_queue.append(job)

            ready = [j for j in job_queue if j["release"] <= time_unit and j["remaining"] > 0]
            job = None
            if ready:
                if algorithm == "RM":
                    ready.sort(key=lambda x: x["period"])
                elif algorithm == "EDF":
                    ready.sort(key=lambda x: x["deadline"])
                elif algorithm == "LLF":
                    for j in ready:
                        j["laxity"] = j["deadline"] - time_unit - j["remaining"]
                    ready.sort(key=lambda x: x["laxity"])
                job = ready[0]

                if prev_job and prev_job != job:
                    preemptions += 1
                prev_job = job

                if job["start"] is None:
                    job["start"] = time_unit
                idx = next(i for i, t in enumerate(self.tasks) if t[0] == job["name"])
                x1 = 40 + time_unit * px_per_unit
                x2 = 40 + (time_unit + 1) * px_per_unit
                y1 = 40 + idx * 20
                y2 = y1 + px_per_unit
                canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors[idx % 10], outline='black')
                job["remaining"] -= 1
                if job["remaining"] == 0:
                    job["end"] = time_unit + 1
                    rt = job["end"] - job["release"]
                    response_times.append(rt)

            time_unit += 1
            time.sleep(0.005)
            canvas.update()

        for job in schedule:
            if job["remaining"] > 0 and job["deadline"] <= sim_time:
                deadline_miss += 1
                idx = next(i for i, t in enumerate(self.tasks) if t[0] == job["name"])
                x = 40 + job["deadline"] * px_per_unit
                y = 40 + idx * 20
                canvas.create_oval(x-3, y+7, x+3, y+13, fill="red")

        utilization = round(sum(t[1]/t[2] for t in self.tasks), 2)
        avg_response = round(sum(response_times)/len(response_times), 2) if response_times else 0
        result_text = (
            f"Algorithm: {algorithm}\n"
            f"CPU Utilization: {utilization}\n"
            f"Preemptions: {preemptions}\n"
            f"Missed Deadlines: {deadline_miss}\n"
            f"Average Response Time: {avg_response}"
        )
        color = "green" if deadline_miss == 0 else "red"
        label.config(text=result_text, fg=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
