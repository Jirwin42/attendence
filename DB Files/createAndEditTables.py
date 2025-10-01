import sqlite3
import sys

# Define the name of the database file
DB_FILE = "mydatabase.db"

# --- Helper Functions ---

def table_exists(cursor, table_name):
    """Checks if a table with the given name already exists in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def get_valid_name(prompt_message, is_column=False):
    """Gets and validates a name for a table or column."""
    while True:
        name = input(prompt_message).strip()
        # Allow empty input for finishing column definitions
        if is_column and not name:
            return None
        if not name.isidentifier():
            print(f"Error: '{name}' is not a valid identifier.")
            print("Please use only letters, numbers, or underscores, and do not start with a number.")
        else:
            return name

def get_column_definitions(is_new_table=True):
    """Interactively gets a list of column definitions from the user."""
    column_definitions = []
    primary_key_defined = not is_new_table

    print("\n--- Define Columns ---")
    if is_new_table:
        print("Enter column details. Press Enter on an empty column name when finished.")
    
    while True:
        col_name = get_valid_name("Enter column name: ", is_column=is_new_table)
        if not col_name:
            break

        print("Select the data type:")
        data_types = ["INTEGER", "TEXT", "REAL", "BLOB", "NUMERIC"]
        for i, dtype in enumerate(data_types, 1):
            print(f"  {i}. {dtype}")

        while True:
            try:
                choice = int(input(f"Enter choice (1-{len(data_types)}): "))
                if 1 <= choice <= len(data_types):
                    col_type = data_types[choice - 1]
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        col_parts = [col_name, col_type]
        if not primary_key_defined:
            if input("Is this the PRIMARY KEY? (y/n): ").lower() == 'y':
                col_parts.append("PRIMARY KEY")
                primary_key_defined = True

        if input("Can this column be empty (allow NULLs)? (y/n): ").lower() == 'n':
            col_parts.append("NOT NULL")
        if input("Must values in this column be UNIQUE? (y/n): ").lower() == 'y':
            col_parts.append("UNIQUE")

        column_definitions.append(" ".join(col_parts))
        print(f"--> Added: `{' '.join(col_parts)}`\n")
        
        if not is_new_table: # If adding one column, we are done.
            break

    return column_definitions

# --- Core Functionality ---

def view_table_schema(conn, table_name):
    """Reads and prints the schema for a given table."""
    print(f"\n--- Schema for table: {table_name} ---")
    cursor = conn.cursor()
    try:
        # PRAGMA is a special SQLite command to get metadata
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        if not schema:
            print("Table not found or has no columns.")
            return

        print(f"{'ID':<5} {'Name':<20} {'Type':<15} {'Not Null':<10} {'Default':<10} {'PK':<5}")
        print("-" * 70)
        for col in schema:
            cid, name, dtype, notnull, dflt_value, pk = col
            print(f"{cid:<5} {name:<20} {dtype:<15} {str(bool(notnull)):<10} {str(dflt_value):<10} {str(bool(pk)):<5}")
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")

def create_new_table():
    """Guides the user through creating a new table, with a failsafe for name conflicts."""
    table_name = get_valid_name("Enter the name for the new table: ")
    if not table_name: return

    new_columns = get_column_definitions()
    if not new_columns:
        print("No columns defined. Aborting table creation.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # The Failsafe for existing tables
            if table_exists(cursor, table_name):
                print(f"\nWarning: A table named '{table_name}' already exists.")
                print("Choose an action:")
                print("  1. Abort (make no changes)")
                print("  2. Overwrite the existing table (ALL ITS DATA WILL BE LOST)")
                print("  3. Add the newly defined columns to the existing table")
                
                choice = input("Enter choice (1-3): ")

                if choice == '2':
                    print(f"WARNING: This will permanently delete the table '{table_name}' and all its data.")
                    confirm = input("Type 'OVERWRITE' to confirm: ")
                    if confirm == 'OVERWRITE':
                        cursor.execute(f"DROP TABLE {table_name}")
                        print("Old table dropped.")
                    else:
                        print("Confirmation failed. Aborting.")
                        return
                elif choice == '3':
                    # This is the "combine" option
                    print("Adding new columns to existing table...")
                    for col_def in new_columns:
                        try:
                            # We can't use '?' for column definitions, so f-string is needed.
                            # The name was validated earlier by get_valid_name.
                            alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {col_def}"
                            cursor.execute(alter_sql)
                            print(f"  -> Successfully added column: {col_def}")
                        except sqlite3.OperationalError as e:
                            print(f"  -> Could not add column '{col_def.split()[0]}'. Reason: {e}")
                    return # End the function here
                else:
                    print("Aborting table creation.")
                    return

            # Proceed with original creation if table didn't exist or user chose to overwrite
            columns_sql = ", ".join(new_columns)
            create_sql = f"CREATE TABLE {table_name} ({columns_sql});"
            print("\nExecuting SQL:", create_sql)
            cursor.execute(create_sql)
            print(f"\nSuccess! Table '{table_name}' created.")

    except sqlite3.OperationalError as e:
        print(f"\nAn SQLite error occurred: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def manage_existing_table():
    """Provides a menu to view and edit an existing table's schema."""
    table_name = get_valid_name("Enter the name of the table to manage: ")
    if not table_name: return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            if not table_exists(cursor, table_name):
                print(f"Error: Table '{table_name}' not found.")
                return

            while True:
                view_table_schema(conn, table_name)
                print("\n--- Manage Table Menu ---")
                print("  1. Add a new column")
                print("  2. Rename a column")
                print("  3. Drop a column")
                print("  4. Rename this table")
                print("  5. Return to Main Menu")
                choice = input("Enter choice: ")

                if choice == '1':
                    new_col = get_column_definitions(is_new_table=False)
                    if new_col:
                        try:
                            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_col[0]}")
                            print("Column added successfully.")
                        except sqlite3.OperationalError as e:
                            print(f"Error adding column: {e}")
                elif choice == '2':
                    old_col = get_valid_name("Enter current column name to rename: ")
                    new_col = get_valid_name("Enter the new column name: ")
                    try:
                        cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_col} TO {new_col}")
                        print("Column renamed successfully.")
                    except sqlite3.OperationalError as e:
                        print(f"Error renaming column: {e}. Note: This requires a modern version of SQLite.")
                elif choice == '3':
                    col_to_drop = get_valid_name("Enter column name to drop: ")
                    try:
                        cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {col_to_drop}")
                        print("Column dropped successfully.")
                    except sqlite3.OperationalError as e:
                        print(f"Error dropping column: {e}. Note: This requires a modern version of SQLite.")
                elif choice == '4':
                    new_table_name = get_valid_name("Enter the new name for this table: ")
                    try:
                        cursor.execute(f"ALTER TABLE {table_name} RENAME TO {new_table_name}")
                        print(f"Table successfully renamed from '{table_name}' to '{new_table_name}'.")
                        table_name = new_table_name # Update name for the loop
                    except sqlite3.OperationalError as e:
                        print(f"Error renaming table: {e}")
                elif choice == '5':
                    break
                else:
                    print("Invalid choice.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Main Application Loop ---

def main():
    """Main menu for the database management script."""
    while True:
        print("\n===== SQLite Database Manager =====")
        print("Today's Date:", "Wednesday, October 1, 2025")
        print("Location:", "Cookeville, Tennessee")
        print("---------------------------------")
        print("1. Create a new table")
        print("2. View/Edit an existing table")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_new_table()
        elif choice == '2':
            manage_existing_table()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()