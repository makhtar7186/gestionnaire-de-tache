from app import TaskManagerApp
import tkinter as tk
import logging
from tkinter import messagebox


def main():
    """Fonction principale pour lancer l'application"""
    try:
        root = tk.Tk()
        app = TaskManagerApp(root)
        
        # Gérer la fermeture de la fenêtre
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Centrer la fenêtre
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Démarrer la boucle principale
        root.mainloop()
        
    except Exception as e:
        logging.error(f"Erreur lors du démarrage de l'application: {str(e)}")
        messagebox.showerror("Erreur", f"Impossible de démarrer l'application: {str(e)}")

if __name__ == "__main__":
    main()