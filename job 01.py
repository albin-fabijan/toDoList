import tkinter as tk
from tkinter import simpledialog
import json
import csv
import tkinter.messagebox as messagebox

class Task:
    def __init__(self, title, description, due_date, priority=0, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

class TaskManager:
    def __init__(self, master):
        self.master = master
        self.tasks = []

    def Task (self, title, description, due_date, priority=0, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def add_task(self, title, description, due_date, priority=0):
        new_task = Task(title, description, due_date, priority)
        self.tasks.append(new_task)

    def remove_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return True
        return False

    def show_tasks(self):
        return self.tasks

    def save_tasks(self, filename="save.json"):
        tasks_data = []
        for task in self.tasks:
            task_data = {
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'priority': task.priority,
                'completed': task.completed
            }
            tasks_data.append(task_data)
        with open(filename, 'w') as file:
            json.dump(tasks_data, file, indent=4)

    def load_tasks(self, filename="save.json"):
        with open(filename, 'r') as file:
            tasks_data = json.load(file)

        self.tasks = []
        for task_data in tasks_data:
            task = Task(
                task_data['title'],
                task_data['description'],
                task_data['due_date'],
                task_data['priority'],
                task_data['completed']
            )
            self.tasks.append(task)

    def del_tasks(self, filename="save.json"):
        tasks_data = []
        with open(filename, 'w') as file:
            json.dump(tasks_data, file, indent=4)

    def filter_show_tasks(self, min_priority=0, max_priority=float('inf')):
        filtered_tasks = [task for task in self.tasks if min_priority <= task.priority <= max_priority]
        return filtered_tasks

    def export_tasks_to_csv(self, filename="tasks.csv"):
        fieldnames = ['title', 'description', 'due_date', 'priority', 'completed']
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    'title': task.title,
                    'description': task.description,
                    'due_date': task.due_date,
                    'priority': task.priority,
                    'completed': task.completed
                })
        print("Fichier exporté avec succès")

    def display_interface(self):
        self.master.title("Task Manager")

        def add_task():
            title = simpledialog.askstring("Titre de la tâche", "Entrez le titre de la tâche:")
            description = simpledialog.askstring("Description de la tâche", "Entrez la description de la tâche:")
            due_date = simpledialog.askstring("Date d'échéance", "Entrez la date d'échéance (YYYY-MM-DD):")
            priority = int(simpledialog.askstring("Priorité de la tâche", "Entrez la priorité de la tâche (0 à l'infini):"))
            self.add_task(title, description, due_date, priority)
            messagebox.showinfo("Confirmation", "Tâche ajoutée avec succès.")

        def remove_task():
            title = simpledialog.askstring("Titre de la tâche", "Entrez le titre de la tâche à supprimer:")
            if self.remove_task(title):
                messagebox.showinfo("Confirmation", "Tâche supprimée avec succès.")
            else:
                messagebox.showerror("Erreur", "Tâche non trouvée.")

        def show_tasks():
            tasks = self.show_tasks()

            tasks_window = tk.Toplevel(self.master)
            tasks_window.title("Tâches")

            tasks_frame = tk.Frame(tasks_window)
            tasks_frame.pack()

            for idx, task in enumerate(tasks):
                tk.Label(tasks_frame, text=f"Titre : {task.title}").grid(row=idx, column=0, sticky="w")
                tk.Label(tasks_frame, text=f"Description : {task.description}").grid(row=idx, column=1, sticky="w")
                tk.Label(tasks_frame, text=f"Date d'échéance : {task.due_date}").grid(row=idx, column=2, sticky="w")
                tk.Label(tasks_frame, text=f"Priorité : {task.priority}").grid(row=idx, column=3, sticky="w")


        def save_tasks():
            self.save_tasks()
            messagebox.showinfo("Confirmation", "Tâches sauvegardées avec succès.")

        def load_tasks():
            self.load_tasks()
            messagebox.showinfo("Confirmation", "Tâches chargées avec succès.")

        def del_tasks():
            self.del_tasks()
            messagebox.showinfo("Confirmation", "Tâches supprimées.")

        def filter_show_tasks():
            min_priority = int(simpledialog.askstring("Priorité minimale", "Entrez la priorité minimale:"))
            max_priority = int(simpledialog.askstring("Priorité maximale", "Entrez la priorité maximale:"))
            filtered_tasks = self.filter_show_tasks(min_priority, max_priority)

            filtered_tasks_window = tk.Toplevel(self.master)
            filtered_tasks_window.title("Tâches filtrées par priorité")

            filtered_tasks_frame = tk.Frame(filtered_tasks_window)
            filtered_tasks_frame.pack()

            for idx, task in enumerate(filtered_tasks):
                tk.Label(filtered_tasks_frame, text=f"Titre : {task.title}").grid(row=idx, column=0, sticky="w")
                tk.Label(filtered_tasks_frame, text=f"Description : {task.description}").grid(row=idx, column=1, sticky="w")
                tk.Label(filtered_tasks_frame, text=f"Date d'échéance : {task.due_date}").grid(row=idx, column=2, sticky="w")
                tk.Label(filtered_tasks_frame, text=f"Priorité : {task.priority}").grid(row=idx, column=3, sticky="w")


        def export_tasks():
            self.export_tasks_to_csv()
            messagebox.showinfo("Confirmation", "Tâches exportées avec succès.")

        menu_frame = tk.Frame(self.master)
        menu_frame.pack()

        tk.Button(menu_frame, text="Ajouter une tâche", command=add_task).pack()
        tk.Button(menu_frame, text="Supprimer une tâche", command=remove_task).pack()
        tk.Button(menu_frame, text="Afficher les tâches", command=show_tasks).pack()
        tk.Button(menu_frame, text="Sauvegarder les tâches", command=save_tasks).pack()
        tk.Button(menu_frame, text="Charger les tâches depuis la sauvegarde", command=load_tasks).pack()
        tk.Button(menu_frame, text="Effacer l’intégralité des tâches enregistrées", command=del_tasks).pack()
        tk.Button(menu_frame, text="Afficher les tâches filtrées par priorité", command=filter_show_tasks).pack()
        tk.Button(menu_frame, text="Exporter sous format CSV", command=export_tasks).pack()
        tk.Button(menu_frame, text="Quitter", command=self.master.destroy).pack()


def main():
    root = tk.Tk()
    app = TaskManager(root)
    app.display_interface()
    root.mainloop()


if __name__ == "__main__":
    main()
