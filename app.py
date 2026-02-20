import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from task_manager import TaskManager
import logging

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Tâches")
        self.root.geometry("800x600")
        
        # Initialiser le gestionnaire de tâches
        self.task_manager = TaskManager()
        
        # Variables
        self.current_filter = tk.StringVar(value="all")
        
        # Configurer l'interface
        self.setup_ui()
        
        # Charger les tâches
        self.refresh_task_list()
        
    def setup_ui(self):
        """Configure tous les éléments de l'interface"""
        
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Gestionnaire de Tâches", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Frame pour l'ajout de tâche
        add_frame = ttk.Frame(main_frame)
        add_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.task_entry = ttk.Entry(add_frame, width=50)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        add_btn = ttk.Button(add_frame, text="Ajouter Tâche", 
                            command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame pour les filtres
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(filter_frame, text="Filtrer:").pack(side=tk.LEFT, padx=5)
        
        filters = [("Toutes", "all"), ("En cours", "pending"), ("Terminées", "completed")]
        for text, value in filters:
            ttk.Radiobutton(filter_frame, text=text, value=value, 
                           variable=self.current_filter,
                           command=self.refresh_task_list).pack(side=tk.LEFT, padx=5)
        
        # Treeview pour afficher les tâches
        columns = ('ID', 'Titre', 'Statut', 'Actions')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Définir les en-têtes
        self.tree.heading('ID', text='ID')
        self.tree.heading('Titre', text='Titre')
        self.tree.heading('Statut', text='Statut')
        self.tree.heading('Actions', text='Actions')
        
        # Définir les largeurs des colonnes
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Titre', width=400)
        self.tree.column('Statut', width=100, anchor='center')
        self.tree.column('Actions', width=150, anchor='center')
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement du treeview et de la scrollbar
        self.tree.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        
        # Frame pour les actions sur les tâches
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        complete_btn = ttk.Button(action_frame, text="Marquer comme terminée", 
                                 command=self.complete_task)
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(action_frame, text="Supprimer", 
                               command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(action_frame, text="Actualiser", 
                                command=self.refresh_task_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Label pour les statistiques
        self.stats_label = ttk.Label(main_frame, text="", font=('Arial', 10))
        self.stats_label.grid(row=5, column=0, columnspan=3, pady=5)
        
    def add_task(self):
        """Ajoute une nouvelle tâche"""
        task_title = self.task_entry.get().strip()
        if task_title:
            try:
                self.task_manager.add_task(task_title)
                self.task_entry.delete(0, tk.END)
                self.refresh_task_list()
                logging.info(f"Tâche ajoutée via interface: {task_title}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter la tâche: {str(e)}")
        else:
            messagebox.showwarning("Attention", "Veuillez entrer un titre pour la tâche")
    
    def complete_task(self):
        """Marque la tâche sélectionnée comme terminée"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche")
            return
        
        # Récupérer l'ID de la tâche sélectionnée
        item = self.tree.item(selected[0])
        task_id = item['values'][0]
        
        try:
            self.task_manager.complete_task(task_id)
            self.refresh_task_list()
            logging.info(f"Tâche {task_id} marquée comme terminée via interface")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de marquer la tâche: {str(e)}")
    
    def delete_task(self):
        """Supprime la tâche sélectionnée"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche")
            return
        
        # Confirmation
        if not messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette tâche ?"):
            return
        
        # Récupérer l'ID de la tâche sélectionnée
        item = self.tree.item(selected[0])
        task_id = item['values'][0]
        
        try:
            self.task_manager.delete_task(task_id)
            self.refresh_task_list()
            logging.info(f"Tâche {task_id} supprimée via interface")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer la tâche: {str(e)}")
    
    def refresh_task_list(self):
        """Rafraîchit la liste des tâches selon le filtre sélectionné"""
        # Effacer la liste actuelle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Récupérer les tâches selon le filtre
        filter_type = self.current_filter.get()
        
        if filter_type == "all":
            tasks = self.task_manager.get_tasks()
        elif filter_type == "pending":
            tasks = self.task_manager.get_pending_tasks()
        else:  # completed
            tasks = self.task_manager.get_completed_tasks()
        
        # Ajouter les tâches au treeview
        for task in tasks:
            status = "✓ Terminée" if task['completed'] else "○ En cours"
            
            # Déterminer la couleur selon le statut
            if task['completed']:
                tag = 'completed'
            else:
                tag = 'pending'
            
            self.tree.insert('', tk.END, values=(
                task['id'],
                task['title'],
                status,
                "..."  # Placeholder pour la colonne actions
            ), tags=(tag,))
        
        # Configurer les couleurs
        self.tree.tag_configure('completed', foreground='green')
        self.tree.tag_configure('pending', foreground='blue')
        
        # Mettre à jour les statistiques
        self.update_stats()
    
    def update_stats(self):
        """Met à jour les statistiques affichées"""
        all_tasks = self.task_manager.get_tasks()
        completed = self.task_manager.get_completed_tasks()
        pending = self.task_manager.get_pending_tasks()
        
        total = len(all_tasks)
        completed_count = len(completed)
        pending_count = len(pending)
        
        stats_text = f"Total: {total} tâches | En cours: {pending_count} | Terminées: {completed_count}"
        
        if total > 0:
            completion_rate = (completed_count / total) * 100
            stats_text += f" | Taux d'achèvement: {completion_rate:.1f}%"
        
        self.stats_label.config(text=stats_text)
    
    def on_closing(self):
        """Gère la fermeture de l'application"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            logging.info("Application fermée")
            self.root.destroy()

