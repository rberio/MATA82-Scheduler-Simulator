# Scheduler Simulator, MATA82 - 2025.01

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import threading
import csv


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "[MATA82] - Simulador de Escalonador de Tarefas (Multi-Processador)")
        self.root.geometry("1920x1080")
        self.version = "v0628b10_alignfix"
        self.loaded_filename = None
        self.tasks = []
        self.colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
                       "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ab"]
        self.setup_ui()

    def setup_ui(self):
        self.name_var = tk.StringVar()
        self.c_var = tk.DoubleVar()
        self.t_var = tk.DoubleVar()
        self.d_var = tk.DoubleVar()
        self.j_var = tk.DoubleVar()
        self.sim_time_var = tk.IntVar(value=100)
        self.num_processors_var = tk.IntVar(value=1)

        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(left_frame, text="Configuração da Tarefa",
                 font=("Arial", 10, "bold")).pack(anchor='w')
        entries = [
            ("Nome da Tarefa", self.name_var),
            ("Tempo de Computação (C)", self.c_var),
            ("Período (T)", self.t_var),
            ("Deadline (D)", self.d_var),
            ("Jitter (J) (opcional)", self.j_var)
        ]
        for lbl, var in entries:
            tk.Label(left_frame, text=lbl).pack(anchor='w')
            tk.Entry(left_frame, textvariable=var, width=30).pack(fill=tk.X)

        tk.Button(left_frame, text="Adicionar Tarefa",
                  command=self.add_task).pack(pady=5)
        tk.Button(left_frame, text="Carregar CSV",
                  command=self.load_csv).pack()
        tk.Button(left_frame, text="Limpar Tarefas",
                  command=self.clear_tasks).pack(pady=5)

        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.task_list = tk.Listbox(
            list_frame, width=30, yscrollcommand=list_scrollbar.set)
        list_scrollbar.config(command=self.task_list.yview)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="Configuração da Simulação", font=(
            "Arial", 10, "bold")).pack(anchor='w', pady=(10, 0))
        tk.Label(left_frame, text="Tempo de Simulação").pack(anchor='w')
        tk.Entry(left_frame, textvariable=self.sim_time_var).pack(fill=tk.X)

        tk.Label(left_frame, text="Número de Processadores").pack(anchor='w')
        tk.Entry(left_frame, textvariable=self.num_processors_var).pack(fill=tk.X)

        tk.Button(left_frame, text="Executar Simulação",
                  command=self.run_simulation).pack(pady=10)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.graph_canvases = []
        self.result_labels = []
        algorithms = ["RM", "EDF", "LLF"]
        for alg in algorithms:
            frame = tk.Frame(self.canvas_frame, bg='#f0f0f0')
            frame.pack(fill=tk.BOTH, expand=True, pady=2)

            title = tk.Label(frame, text=f"Simulação {alg}", font=(
                "Arial", 10, "bold"), anchor='w')
            title.pack(anchor='w')

            canvas_container = tk.Frame(frame)
            canvas_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            canvas_scrollbar_y = ttk.Scrollbar(
                canvas_container, orient=tk.VERTICAL)
            canvas_scrollbar_x = ttk.Scrollbar(
                canvas_container, orient=tk.HORIZONTAL)

            canvas = tk.Canvas(canvas_container, bg='white',
                               yscrollcommand=canvas_scrollbar_y.set,
                               xscrollcommand=canvas_scrollbar_x.set)

            canvas_scrollbar_y.config(command=canvas.yview)
            canvas_scrollbar_x.config(command=canvas.xview)

            canvas_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            canvas_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            result = tk.Label(frame, text=f"Resultados {alg}", font=(
                "Arial", 10), relief=tk.SOLID, bd=1, width=35, height=7, anchor='nw', justify='left')
            result.pack(side=tk.RIGHT, padx=10, pady=5)

            self.graph_canvases.append(canvas)
            self.result_labels.append(result)

        self.version_label = tk.Label(
            self.root, text=f"Versão: {self.version}", font=("Arial", 8), fg="orange")
        self.version_label.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-5)

    def add_task(self):
        task = (self.name_var.get(), self.c_var.get(),
                self.t_var.get(), self.d_var.get(), self.j_var.get())
        self.tasks.append(task)
        self.task_list.insert(
            tk.END, f"{task[0]}: C={task[1]} T={task[2]} D={task[3]} J={task[4]}")

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivos CSV", "*.csv")])
        if file_path:
            self.clear_tasks()
            self.loaded_filename = file_path.split("/")[-1]
            with open(file_path, newline='', encoding='utf-8') as csvfile:
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
                    self.task_list.insert(
                        tk.END, f"{task[0]}: C={task[1]} T={task[2]} D={task[3]} J={task[4]}")
            messagebox.showinfo(
                "CSV Carregado", f"Tarefas do arquivo {self.loaded_filename} carregadas com sucesso.")

    def clear_tasks(self):
        self.tasks.clear()
        self.task_list.delete(0, tk.END)

    def run_simulation(self):
        if not self.tasks:
            messagebox.showwarning(
                "Nenhuma Tarefa", "Por favor, adicione ou carregue tarefas antes de executar a simulação.")
            return

        num_solicitado = self.num_processors_var.get()
        if num_solicitado < 1:
            messagebox.showwarning(
                "Entrada Inválida", "O número de processadores deve ser no mínimo 1.")
            return

        num_fisico = os.cpu_count()
        if num_solicitado > num_fisico:
            prosseguir = messagebox.askyesno(
                "Aviso de Simulação",
                f"Você solicitou a simulação de {num_solicitado} processadores, mas sua máquina possui {num_fisico}.\n\n"
                "A simulação irá modelar um sistema hipotético e pode ficar mais lenta.\n\nDeseja continuar mesmo assim?"
            )
            if not prosseguir:
                return

        for canvas in self.graph_canvases:
            canvas.delete("all")
        threading.Thread(target=self.animate_all_schedules,
                         daemon=True).start()

    def animate_all_schedules(self):
        for alg, canvas, label in zip(["RM", "EDF", "LLF"], self.graph_canvases, self.result_labels):
            canvas.delete("all")
            self.animate_schedule(canvas, alg, label)

    def animate_schedule(self, canvas, algorithm, label):
        num_processors = self.num_processors_var.get()
        sim_time = self.sim_time_var.get()
        px_per_unit = 10
        job_queue = []

        total_canvas_width = 40 + sim_time * px_per_unit + 40
        total_canvas_height = 40 + len(self.tasks) * 25
        canvas.config(scrollregion=(
            0, 0, total_canvas_width, total_canvas_height))

        for t in range(sim_time + 1):
            x = 40 + t * px_per_unit
            canvas.create_line(x, 30, x, total_canvas_height, fill="#ccc")
            if t % 5 == 0:
                canvas.create_text(x, 20, text=str(t), font=("Arial", 7))

        task_y_positions = {}
        for i, t in enumerate(self.tasks):
            y = 40 + i * 25
            task_y_positions[t[0]] = y
            canvas.create_text(
                35, y + 10, text=t[0], font=("Arial", 8), anchor='e')

        preemptions = 0
        deadline_miss = 0
        response_times = []
        completed_jobs = []
        prev_running_jobs = set()
        time_unit = 0

        while time_unit < sim_time:
            for name, c, p, d, j in self.tasks:
                if p > 0 and (time_unit - j) >= 0 and (time_unit - j) % p == 0:
                    job_queue.append({
                        "name": name, "release": time_unit, "remaining": c,
                        "deadline": time_unit + d, "period": p, "wcet": c,
                        "start": None, "end": None
                    })

            ready = [j for j in job_queue if j["remaining"] > 0]

            if ready:
                if algorithm == "RM":
                    ready.sort(key=lambda x: x["period"])
                elif algorithm == "EDF":
                    ready.sort(key=lambda x: x["deadline"])
                elif algorithm == "LLF":
                    for j in ready:
                        j["laxity"] = j["deadline"] - \
                            time_unit - j["remaining"]
                    ready.sort(key=lambda x: x["laxity"])

                running_jobs = ready[:num_processors]
                current_running_jobs = {job['name'] for job in running_jobs}

                preempted_jobs = prev_running_jobs - current_running_jobs
                for job_name in preempted_jobs:
                    if any(j['name'] == job_name and j['remaining'] > 0 for j in job_queue):
                        preemptions += 1

                prev_running_jobs = current_running_jobs

                for job in running_jobs:
                    if job["start"] is None:
                        job["start"] = time_unit

                    y1 = task_y_positions.get(job["name"], 0)
                    x1 = 40 + time_unit * px_per_unit
                    x2 = x1 + px_per_unit
                    y2 = y1 + 20
                    task_index = self.tasks.index(
                        next(t for t in self.tasks if t[0] == job["name"]))
                    canvas.create_rectangle(
                        x1, y1, x2, y2, fill=self.colors[task_index % 10], outline='black')

                    job["remaining"] -= 1
                    if job["remaining"] <= 0:
                        job["end"] = time_unit + 1
                        response_times.append(job["end"] - job["release"])
                        completed_jobs.append(job)
                        if job['name'] in prev_running_jobs:
                            prev_running_jobs.remove(job['name'])
            else:
                prev_running_jobs.clear()

            job_queue = [j for j in job_queue if j["remaining"] > 0]

            time_unit += 1
            if len(self.tasks) > 50:
                time.sleep(0.001)
            elif len(self.tasks) > 0:
                time.sleep(0.05 / len(self.tasks))

            if len(self.tasks) < 50 or time_unit % 5 == 0:
                canvas.update()

        for job in job_queue:
            if job["deadline"] < sim_time:
                deadline_miss += 1
                y = task_y_positions.get(job["name"], 0)
                x = 40 + job["deadline"] * px_per_unit
                canvas.create_oval(x - 3, y + 10, x + 3, y + 16,
                                   fill="red", outline="red")

        utilization = round(sum(t[1]/t[2] for t in self.tasks if t[2] > 0), 2)
        avg_response = round(sum(response_times) /
                             len(response_times), 2) if response_times else 0

        result_text = (
            f"Algoritmo: {algorithm}\n"
            f"Processadores: {num_processors}\n"
            f"Utilização da CPU: {utilization} (de {num_processors}.0)\n"
            f"Preempções: {preemptions}\n"
            f"Deadlines Perdidos: {deadline_miss}\n"
            f"Tempo de Resposta Médio: {avg_response}"
        )
        color = "green" if deadline_miss == 0 else "red"
        label.config(text=result_text, fg=color)
        canvas.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
