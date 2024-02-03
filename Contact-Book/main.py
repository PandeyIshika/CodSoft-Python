import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.contacts = []

        self.create_widgets()

        self.load_contacts()

    def create_widgets(self):
        
        style = ttk.Style()
        style.configure("TButton", padding=(0, 0), font=('Helvetica', 10))
        style.configure("TLabel", font=('Helvetica', 12), background='#e6e6fa', foreground='black')
        style.configure("TEntry", font=('Helvetica', 10), fieldbackground='#e6e6fa')
        style.configure("Treeview", font=('Helvetica', 10), background='#e6e6fa', foreground='black')

        main_frame = ttk.Frame(self.root, style="TLabel")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Label(main_frame, text="Contact Book", padding=(5, 5), font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=4, pady=5, sticky=tk.N)
       
        labels = ["Name:", "Phone No:", "Email:", "Address:"]
        self.entries = {}  
        for i, label_text in enumerate(labels):
            ttk.Label(main_frame, text=label_text, style="TLabel").grid(row=i + 1, column=0, pady=5, padx=5, sticky=tk.W)
            self.entries[label_text] = ttk.Entry(main_frame, font=('Helvetica', 10), style="TEntry")
            self.entries[label_text].grid(row=i + 1, column=1, pady=5, padx=5, sticky=tk.W)

        self.search_entry = ttk.Entry(main_frame, font=('Helvetica', 10), width=50, style="TEntry")
        self.search_entry.grid(row=1, column=2, pady=5, padx=5, sticky=tk.W)
        ttk.Button(main_frame, text="Search", command=self.search_contact, width=18, style="TButton").grid(row=1, column=3, pady=5, sticky=tk.W)

        self.tree = ttk.Treeview(main_frame, columns=("Name", "Phone", "Email", "Address"), show="headings", selectmode="browse", style="Treeview")
        headers = ["Name", "Phone", "Email", "Address"]
        for header in headers:
            self.tree.heading(header, text=header.replace(" ", ""))
        column_widths = [100, 100, 150, 150]
        for header, width in zip(headers, column_widths):
            self.tree.column(header, width=width)
        self.tree.grid(row=2, column=2, columnspan=2, rowspan=7, pady=5, padx=5, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.tree.bind("<Double-1>", self.on_item_double_click)

        button_width = 25
        button_texts = ["Add", "Update", "Delete", "Refresh"]
        button_commands = [self.add_contact, self.edit_contact, self.delete_contact, self.refresh_contacts]

        for i, (text, command) in enumerate(zip(button_texts, button_commands)):
            ttk.Button(main_frame, text=text, command=command, width=button_width, style="TButton").grid(row=5 + i, column=0, columnspan=2, pady=5, padx=5)

    def add_contact(self):
        name = self.get_entry_value("Name:")
        phone = self.get_entry_value("Phone No:")
        email = self.get_entry_value("Email:")
        address = self.get_entry_value("Address:")

        if self.validate_input(name, phone, email, address):
            contact = {"Name": name, "Phone": phone, "Email": email, "Address": address}
            self.contacts.append(contact)
            self.show_info_message("Success", "Contact added successfully!")
            self.clear_entries()
            self.update_treeview()
            self.save_contacts()
        else:
            self.show_warning_message("Error", "Please enter valid contact details.")

    def edit_contact(self):
        edited_name = self.get_entry_value("Name:")
        edited_phone = self.get_entry_value("Phone No:")
        edited_email = self.get_entry_value("Email:")
        edited_address = self.get_entry_value("Address:")

        if self.validate_input(edited_name, edited_phone, edited_email, edited_address):
            selected_item = self.tree.selection()
            if selected_item:
                item_values = self.tree.item(selected_item, 'values')
                name_to_update = item_values[0]

                for contact in self.contacts:
                    if name_to_update.lower() == contact["Name"].lower():
                        contact["Name"] = edited_name
                        contact["Phone"] = edited_phone
                        contact["Email"] = edited_email
                        contact["Address"] = edited_address

                        self.show_info_message("Success", f"{contact['Name']} updated successfully!")
                        self.clear_entries()
                        self.update_treeview()
                        self.save_contacts()
                        return

                self.show_info_message("Please select a contact to edit.")
            else:
                self.show_warning_message("Error", "Please select a contact to edit.")

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            name_to_update = item_values[0]

            for contact in self.contacts:
                if name_to_update.lower() == contact["Name"].lower():
                    self.clear_entries()
                    self.set_entry_value("Name:", contact["Name"])
                    self.set_entry_value("Phone No:", contact["Phone"])
                    self.set_entry_value("Email:", contact["Email"])
                    self.set_entry_value("Address:", contact["Address"])
                    return

    def search_contact(self):
        search_name = self.search_entry.get().lower()
        found_contacts = [contact for contact in self.contacts if search_name in contact["Name"].lower()]

        if found_contacts:
            self.update_treeview(found_contacts)
        else:
            self.show_info_message("Search Contact", f"No contacts found with the name containing '{search_name}'.")

        self.search_entry.delete(0, tk.END)

    def delete_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            name_to_delete = item_values[0]

            confirmation = messagebox.askokcancel("Delete Contact", f"Do you want to delete the contact: {name_to_delete}?")
            if confirmation:
                for contact in self.contacts:
                    if name_to_delete.lower() == contact["Name"].lower():
                        self.contacts.remove(contact)
                        self.show_info_message("Success", f"{contact['Name']} deleted successfully!")
                        self.clear_entries()
                        self.update_treeview()
                        self.save_contacts()
                        return
                self.show_info_message("Delete Contact", f"No contact found with the name {name_to_delete}.")
        else:
            self.show_warning_message("Error", "Please select a contact to delete.")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def refresh_contacts(self):
        self.update_treeview(self.contacts)

    def update_treeview(self, contacts=None):
        self.tree.delete(*self.tree.get_children())
        contacts_to_display = contacts if contacts else self.contacts
        for contact in contacts_to_display:
            self.tree.insert("", "end", values=(contact["Name"], contact["Phone"], contact["Email"], contact["Address"]))

    def load_contacts(self):
        try:
            with open("Contact-Book\contacts.json", "r") as file:
                self.contacts = json.load(file)
                self.update_treeview()
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open("Contact-Book\contacts.json", "w") as file:
            json.dump(self.contacts, file, indent=2)

    def validate_input(self, name, phone, email, address):
        phone_pattern = re.compile(r'^\d{10}$')
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        name_pattern = re.compile(r'^[^\d]+$')
        address_pattern = re.compile(r'^[a-zA-Z0-9\s]+$')

        if not name_pattern.match(name):
            self.show_warning_message("Error", "Please enter a valid name.")
            return False
        if not phone_pattern.match(phone):
            self.show_warning_message("Error", "Please enter a valid phone number (10 digits only).")
            return False
        if not email_pattern.match(email):
            self.show_warning_message("Error", "Please enter a valid email address.")
            return False
        if not address_pattern.match(address):
            self.show_warning_message("Error", "Please enter a valid address.")
            return False
        return True

    def get_entry_value(self, label):
        return self.entries[label].get()

    def set_entry_value(self, label, value):
        self.entries[label].delete(0, tk.END)
        self.entries[label].insert(0, value)

    def show_info_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_warning_message(self, title, message):
        messagebox.showwarning(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
