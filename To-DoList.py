import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        self.master.geometry("325x380")

        style = ttk.Style()
        style.theme_use("winnative")

        self.tasks = []
        self.task_counter = 0  

        ttk.Label(self.master, text="Your To-Do List", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)

        self.task_entry = ttk.Entry(self.master, width=50)
        self.task_entry.grid(row=1, column=0, columnspan=3, pady=10)

        self.add_task_button = ttk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.exit_button = ttk.Button(self.master, text="Exit", command=self.master.destroy)
        self.exit_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        self.tasks_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, height=10, width=50)
        self.tasks_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.update_button = ttk.Button(self.master, text="Update Task", command=self.update_task)
        self.update_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.delete_button = ttk.Button(self.master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        self.mark_completed_button = ttk.Button(self.master, text="Mark Completed", command=self.mark_completed)
        self.mark_completed_button.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

        self.update_tasks_listbox()

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False, "order": self.task_counter})
            self.task_counter += 1
            self.task_entry.delete(0, tk.END)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Empty Task", "Please enter a task.")

    def update_task(self):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            original_task_text = selected_task["text"]
            new_task_text = simpledialog.askstring("Update Task", f"Update task '{original_task_text}':")
            if new_task_text:
                selected_task["text"] = new_task_text
                self.update_tasks_listbox()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to update.")

    def delete_task(self):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to delete.")

    def mark_completed(self):
        selected_text = self.tasks_listbox.get(self.tasks_listbox.curselection())
        for task in self.tasks:
            if task["text"] == selected_text:
                task["completed"] = not task.get("completed", False)
                self.update_tasks_listbox()
                break
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to mark as completed.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)

        sorted_tasks = sorted(self.tasks, key=lambda x: (x.get("completed", False), x.get("order", 0)))

        for task in sorted_tasks:
            if task.get("completed", False):
                self.tasks_listbox.insert(tk.END, f"✓ {task['text']}")
            else:
                self.tasks_listbox.insert(tk.END, task['text'])

if __name__ == "__main__":
    root = tk.Tk()

    app = TodoApp(root)
    root.mainloop()
