import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
from datetime import datetime
import os
#created by Gemini

DB_FILE = 'customers.db'

# --- New Entry Window (Toplevel) ---
class CustomerEntryWindow(tk.Toplevel):
    """A Toplevel window for entering a new customer's data."""
    def __init__(self, parent_app):
        super().__init__(parent_app.root)
        self.parent_app = parent_app # Reference to the main app window

        self.title("Add New Customer")
        self.geometry("450x400")
        self.transient(parent_app.root) # Keep this window on top of the main app
        self.grab_set() # Modal behavior

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.configure('TLabel', font=('Helvetica', 11))
        style.configure('TEntry', font=('Helvetica', 11))
        style.configure('TButton', font=('Helvetica', 11, 'bold'))
        style.configure('TCombobox', font=('Helvetica', 11))

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")
        main_frame.columnconfigure(1, weight=1)

        # --- Input Fields ---
        self.widgets = {}
        fields = {
            "Name": "TEntry", "Birthday (MM-DD-YYYY)": "TEntry", "Email": "TEntry",
            "Phone Number (XXX-XXX-XXXX)": "TEntry", "Address": "TEntry",
            "Preferred contact method": "TCombobox"
        }
        for i, (label_text, widget_type) in enumerate(fields.items()):
            label = ttk.Label(main_frame, text=label_text)
            label.grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
            if widget_type == "TEntry":
                widget = ttk.Entry(main_frame)
            else: # TCombobox
                widget = ttk.Combobox(main_frame, values=["Email", "Phone", "Mail"], state="readonly")
                widget.set("Email")
            widget.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
            self.widgets[label_text.split(" ")[0]] = widget

        # --- Submit Button ---
        submit_button = ttk.Button(main_frame, text="Submit", command=self.submit_data)
        submit_button.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def validate_inputs(self, data):
        """Validates all user-entered data before submission."""
        for key, value in data.items():
            if not value:
                messagebox.showerror("Validation Error", f"The '{key}' field cannot be empty.", parent=self)
                return False
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data["Email"]):
            messagebox.showerror("Validation Error", "Please enter a valid email address.", parent=self)
            return False
        try:
            datetime.strptime(data["Birthday"], '%m-%d-%Y')
        except ValueError:
            messagebox.showerror("Validation Error", "Please use MM-DD-YYYY for the birthday.", parent=self)
            return False
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', data["Phone"]):
            messagebox.showerror("Validation Error", "Please use XXX-XXX-XXXX for the phone number.", parent=self)
            return False
        return True

    def submit_data(self):
        """Validates data and inserts it into the database."""
        data = {key: widget.get() for key, widget in self.widgets.items()}
        if not self.validate_inputs(data):
            return

        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Customer (Name, Birthday, Email, PhoneNumber, Address, PreferredContact)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (data["Name"], data["Birthday"], data["Email"], data["Phone"], data["Address"], data["Preferred"]))
            conn.commit()
            messagebox.showinfo("Success", "Customer data has been saved.", parent=self)
            self.parent_app.refresh_customer_view() # Refresh the main view
            self.destroy() # Close this entry window
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self)
        finally:
            if conn:
                conn.close()


# --- Main Application Class ---
class CustomerManagerApp:
    def __init__(self, root):
        """Initializes the main application."""
        self.root = root
        self.root.title("Customer Management System")
        self.root.geometry("800x600")
        self.root.columnconfigure(0, weight=2); self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.customers, self.warehouse_buttons = [], []
        self.current_selection = (0, 0)
        self.grid_columns = 5

        self.setup_styles()
        self.create_widgets()
        
        self.setup_database()
        self.initial_load()
        
        self.bind_keys()

    def setup_database(self):
        """Creates the database and table if they don't exist."""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Customer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Birthday TEXT NOT NULL,
                    Email TEXT NOT NULL, PhoneNumber TEXT, Address TEXT, PreferredContact TEXT NOT NULL
                );
            """)
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Setup Error", f"Failed to set up database: {e}")
        finally:
            if conn:
                conn.close()

    def setup_styles(self):
        """Configures ttk styles."""
        style = ttk.Style(self.root)
        style.configure('TLabel', font=('Helvetica', 11))
        style.configure('TEntry', font=('Helvetica', 11))
        style.configure('TButton', font=('Helvetica', 10), padding=10)
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))

    def create_widgets(self):
        """Creates and places all widgets for the main view."""
        # --- Layout Frames ---
        warehouse_frame = ttk.Frame(self.root, padding="10")
        warehouse_frame.grid(row=0, column=0, sticky="nsew")
        warehouse_frame.rowconfigure(1, weight=1)
        warehouse_frame.columnconfigure(0, weight=1)

        details_frame = ttk.Frame(self.root, padding="20", relief="groove")
        details_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # --- Warehouse Widgets ---
        ttk.Label(warehouse_frame, text="Customers in Database", style='Header.TLabel').grid(row=0, column=0)
        self.canvas_frame = ttk.Frame(warehouse_frame)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew", pady=10)

        add_button = ttk.Button(warehouse_frame, text="Add New Customer", command=self.open_entry_window)
        add_button.grid(row=2, column=0, pady=(10, 0), sticky="ew")
        delete_button = ttk.Button(warehouse_frame, text="Delete Selected Customer", command=self.delete_selected_customer)
        delete_button.grid(row=3, column=0, pady=(10, 0), sticky="ew")

        # --- Details Widgets ---
        self.detail_widgets = {}
        fields = ["ID", "Name", "Birthday", "Email", "Phone Number", "Address", "Preferred contact"]
        ttk.Label(details_frame, text="Customer Details", style='Header.TLabel').pack(pady=(0, 20))
        for field in fields:
            row_frame = ttk.Frame(details_frame)
            row_frame.pack(fill="x", pady=4)
            ttk.Label(row_frame, text=f"{field}:", width=20).pack(side="left")
            entry = ttk.Entry(row_frame, state="readonly")
            entry.pack(side="left", expand=True, fill="x")
            self.detail_widgets[field] = entry
            
    def bind_keys(self):
        """Binds arrow keys for navigation."""
        self.root.bind("<KeyPress-Up>", self.handle_key_nav)
        self.root.bind("<KeyPress-Down>", self.handle_key_nav)
        self.root.bind("<KeyPress-Left>", self.handle_key_nav)
        self.root.bind("<KeyPress-Right>", self.handle_key_nav)

    def initial_load(self):
        """Loads data and checks if the DB is empty to prompt the user."""
        self.load_customers_from_db()
        if not self.customers:
            add_first = messagebox.askyesno("Database Empty", "No customers found. Would you like to add one now?")
            if add_first:
                self.open_entry_window()
            else:
                 self.populate_warehouse()
        else:
            self.populate_warehouse()
            if self.warehouse_buttons:
                self.warehouse_buttons[0][0].focus_set()
                self.warehouse_buttons[0][0].invoke()
                
    def open_entry_window(self):
        """Opens the new customer entry form."""
        CustomerEntryWindow(self)

    def load_customers_from_db(self):
        """Fetches all customer records from the database."""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT id, Name, Birthday, Email, PhoneNumber, Address, PreferredContact FROM Customer")
            self.customers = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
            self.customers = []
        finally:
            if conn:
                conn.close()

    def populate_warehouse(self):
        """Creates a grid of buttons representing each customer."""
        row, col = 0, 0
        current_row_buttons = []
        for customer in self.customers:
            btn = ttk.Button(self.canvas_frame, text=f"ID: {customer[0]}\n{customer[1]}",
                             command=lambda cust=customer: self.display_details(cust))
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            self.canvas_frame.columnconfigure(col, weight=1)
            current_row_buttons.append(btn)
            col = (col + 1) % self.grid_columns
            if col == 0:
                self.warehouse_buttons.append(current_row_buttons)
                current_row_buttons = []
                row += 1
        if current_row_buttons:
            self.warehouse_buttons.append(current_row_buttons)

    def display_details(self, customer_data):
        """Updates the read-only fields with selected customer's data."""
        (cust_id, name, bday, email, phone, addr, preferred) = customer_data
        details = {"ID": cust_id, "Name": name, "Birthday": bday, "Email": email,
                   "Phone Number": phone, "Address": addr, "Preferred contact": preferred}
        for field, widget in self.detail_widgets.items():
            widget.config(state="normal")
            widget.delete(0, tk.END)
            widget.insert(0, details.get(field, ""))
            widget.config(state="readonly")
        for r, row_buttons in enumerate(self.warehouse_buttons):
            for c, button in enumerate(row_buttons):
                if button.cget('text').startswith(f"ID: {cust_id}"):
                    self.current_selection = (r, c)
                    return

    def handle_key_nav(self, event):
        """Handles arrow key navigation."""
        if not self.warehouse_buttons: return
        row, col = self.current_selection
        if event.keysym == "Up": row = max(0, row - 1)
        elif event.keysym == "Down": row = min(len(self.warehouse_buttons) - 1, row + 1)
        elif event.keysym == "Left": col = max(0, col - 1)
        elif event.keysym == "Right": col = min(len(self.warehouse_buttons[row]) - 1, col + 1)
        if col >= len(self.warehouse_buttons[row]): col = len(self.warehouse_buttons[row]) - 1
        self.current_selection = (row, col)
        new_button = self.warehouse_buttons[row][col]
        new_button.focus_set()
        new_button.invoke()

    def delete_selected_customer(self):
        """Deletes the currently selected customer after confirmation."""
        if not self.customers or not self.warehouse_buttons: return
        row, col = self.current_selection
        index = row * self.grid_columns + col
        if index >= len(self.customers): return
            
        customer_id, customer_name = self.customers[index][0], self.customers[index][1]
        confirm = messagebox.askyesno("Confirm Delete", f"Permanently delete '{customer_name}' (ID: {customer_id})?")
        if confirm:
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Customer WHERE id = ?", (customer_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Customer '{customer_name}' has been deleted.")
                self.refresh_customer_view()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete customer: {e}")
            finally:
                if conn:
                    conn.close()

    def refresh_customer_view(self):
        """Clears and reloads the customer warehouse view."""
        for widget in self.canvas_frame.winfo_children(): widget.destroy()
        for widget in self.detail_widgets.values():
            widget.config(state="normal"); widget.delete(0, tk.END); widget.config(state="readonly")
        self.customers, self.warehouse_buttons = [], []
        self.current_selection = (0, 0)
        self.load_customers_from_db()
        self.populate_warehouse()
        if self.warehouse_buttons:
            self.warehouse_buttons[0][0].focus_set()
            self.warehouse_buttons[0][0].invoke()


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerManagerApp(root)
    root.mainloop()

