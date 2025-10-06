import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox

# --- Configuration ---
# The name of your database file.
DB_FILE = "customers.db"
# The name of the table inside your database.
TABLE_NAME = "Customer" 
# ---------------------

class CustomerViewerApp(tk.Tk):
    """
    A GUI application to view and sort data from a SQLite database.
    """
    def __init__(self):
        super().__init__()
        self.title("Customer Database Viewer")
        self.geometry("900x600") # Set a default window size

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Treeview (Table Display) ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, show="headings")
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # --- Controls and Status Bar ---
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        refresh_button = ttk.Button(
            controls_frame, text="Refresh Data", command=self.load_data
        )
        refresh_button.pack(side=tk.RIGHT)

        self.status_label = ttk.Label(
            controls_frame, text="Loading data...", anchor="w"
        )
        self.status_label.pack(side=tk.LEFT)

        # --- Initial Data Load ---
        self.load_data()

    def load_data(self):
        """
        Clears the current table and reloads all data from the database.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not os.path.exists(DB_FILE):
            messagebox.showerror("Error", f"Database file not found: '{DB_FILE}'")
            self.status_label.config(text="Error: Database file not found.")
            return

        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            rows = cursor.fetchall()
            
            headers = [description[0] for description in cursor.description]

            self.tree["columns"] = headers
            
            for col in headers:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
                self.tree.column(col, width=120, anchor="w")

            for row in rows:
                self.tree.insert("", "end", values=row)

            record_count = len(rows)
            self.status_label.config(text=f"Found {record_count} records.")

        except sqlite3.OperationalError as e:
            error_msg = f"Database Error: {e}\n\nHint: Is the table name '{TABLE_NAME}' correct?"
            messagebox.showerror("Database Error", error_msg)
            self.status_label.config(text="Error: Could not read table.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_label.config(text="An unexpected error occurred.")
        finally:
            if conn:
                conn.close()

    def sort_column(self, col, reverse):
        """
        Sorts the Treeview data when a column header is clicked.
        """
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # --- THIS IS THE CORRECTED SECTION ---
        # The try-except block correctly handles sorting columns with numbers vs. text.
        try:
            # Attempt to sort the data as numbers (floats)
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            # If conversion to float fails, it means the column contains text.
            # Fall back to sorting as case-insensitive strings.
            data.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)

        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)

        # Update the column heading's command to sort in the opposite direction next time
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))


# This makes the script runnable
if __name__ == "__main__":
    app = CustomerViewerApp()
    app.mainloop()