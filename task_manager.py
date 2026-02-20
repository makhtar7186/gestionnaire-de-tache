import json
import os
import logging
logging.basicConfig(
    filename="./logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    # 🔹 Charger les tâches depuis le fichier
    def load_tasks(self):
        if not os.path.exists(self.filename):
            logging.info("No tasks file found. Creating new task list.")
            return []

        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            logging.error("JSON file corrupted. Starting with empty list.")
            return []

    # 🔹 Sauvegarder les tâches dans le fichier
    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    # 🔹 Ajouter une tâche
    def add_task(self, title):
        task_id = len(self.tasks) + 1
        new_task = {
            "id": task_id,
            "title": title,
            "completed": False
        }
        self.tasks.append(new_task)
        self.save_tasks()
        logging.info(f"Task added: ID={task_id}, Title={title}")

    # 🔹 Marquer comme complétée
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return
        logging.warning(f"Attempt to complete non-existing task ID={task_id}")
        print("Task not found.")

    # 🔹 Récupérer toutes les tâches
    def get_tasks(self):
        return self.tasks

    # 🔹 Tâches complétées
    def get_completed_tasks(self):
        return [task for task in self.tasks if task["completed"]]

    # 🔹 Tâches en attente
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task["completed"]]

    # 🔹 Supprimer une tâche
    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return
        logging.warning(f"Attempt to delete non-existing task ID={task_id}")

        print("Task not found.")
