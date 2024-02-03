import tkinter as tk
from tkinter import ttk, messagebox
import json

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        self.master.geometry("400x400")
        self.master.configure(bg="#F5F5FD") 

        style = ttk.Style()

        style.configure("TEntry", background="#F5F5FD", font=('Arial', 10))

        style.theme_use("winnative")

        ttk.Label(self.master, text="To-Do List", font=('Arial', 20, 'bold'), background="#F5F5FD", foreground="#9958c5").grid(row=0, column=0, columnspan=4, pady=10)

        self.task_entry = ttk.Entry(self.master, width=50, style="TEntry")
        self.task_entry.insert(0, "Enter your task")

        self.task_entry.bind("<FocusIn>", self.clear_placeholder)
       
        self.task_entry.bind("<FocusOut>", self.restore_placeholder)

        self.task_entry.grid(row=1, column=0, columnspan=4, pady=10, padx=20, sticky="ew")

        tk.Button(self.master, text="Add Task", command=self.add_task, bg="#b78ed8", fg="white",width=10).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self.master, text="Search", command=self.search_task, bg="#b78ed8", fg="white",width=10).grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        self.tasks_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, height=10, width=50, bg="#F5F5FD", selectbackground="#B9B9F5", font=('Arial', 10))
        self.tasks_listbox.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        tk.Button(self.master, text="Completed", command=self.mark_done, bg="#b78ed8", fg="white",width=10).grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(self.master, text="View Status", command=self.view_status, bg="#b78ed8", fg="white",width=10).grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self.master, text="Delete", command=self.delete_task, bg="#b78ed8", fg="white",width=10).grid(row=4, column=2, padx=10, pady=10, sticky="ew")
        tk.Button(self.master, text="Delete All", command=self.clear_all_tasks, bg="#b78ed8", fg="white",width=10).grid(row=4, column=3, padx=10, pady=10, sticky="ew")

        self.load_tasks()

    def clear_placeholder(self, event):
        if self.task_entry.get() == "Enter your task":
            self.task_entry.delete(0, tk.END)
            self.task_entry.configure(style="TEntry")

    def restore_placeholder(self, event):
        if self.task_entry.get() == "":
            self.task_entry.insert(0, "Enter your task")
            self.task_entry.configure(style="Custom.TEntry")

    def view_status(self):
        done_count = sum(1 for i in range(self.tasks_listbox.size()) if self.tasks_listbox.itemcget(i, "fg") == "#b78ed8")
        total_count = self.tasks_listbox.size()
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks_listbox.insert(tk.END, task)
            self.tasks_listbox.itemconfig(tk.END, fg="#9958c5") 
            self.task_entry.delete(0, tk.END)
            self.save_tasks()

    def mark_done(self):
        task_index = self.tasks_listbox.curselection()
        if task_index:
            self.tasks_listbox.itemconfig(task_index, fg="#b78ed8")  
            self.save_tasks()

    def delete_task(self):
        task_index = self.tasks_listbox.curselection()
        if task_index:
            self.tasks_listbox.delete(task_index)
            self.save_tasks()

    def clear_all_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        self.save_tasks()

    def search_task(self):
        search_text = self.task_entry.get().lower()
        self.tasks_listbox.selection_clear(0, tk.END)
        found = False
        for i in range(self.tasks_listbox.size()):
            task_text = self.tasks_listbox.get(i).lower()
            if search_text in task_text:
                self.tasks_listbox.select_set(i)
                self.tasks_listbox.activate(i)
                found = True
                break

        if not found:
            messagebox.showinfo("Task Not Found", f"No task with the name '{search_text}' found.")

        self.task_entry.delete(0, tk.END)
        self.task_entry.configure(style="Custom.TEntry")

    def load_tasks(self):

        try:
            with open("ToDo-List\Tasks.json", "r") as f:
                data = json.load(f)
                for task in data:
                    self.tasks_listbox.insert(tk.END, task["text"])
                    self.tasks_listbox.itemconfig(tk.END, fg=task["color"])
                    
        except FileNotFoundError:
            pass

    def save_tasks(self):
        data = [{"text": self.tasks_listbox.get(i), "color": self.tasks_listbox.itemcget(i, "fg")} for i in range(self.tasks_listbox.size())]
        with open("ToDo-List\Tasks.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
