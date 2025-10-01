import sqlite3
import sys

# Define the name of the database file
DB_FILE = "mydatabase.db"

def get_valid_name(prompt_message):
    """Gets and validates a name for a table or column."""
    while True:
        name = input(prompt_message).strip()
        if not name:
            return None # Return None if user wants to stop adding columns
        if name.isidentifier():
            return name
        else:
            print(f"Error: '{name}' is not a valid identifier.")
            print("Please use only letters, numbers, or underscores, and do not start with a number.")

def create_interactive_table():
    """
    Connects to an SQLite database and creates a new table with a schema
    defined interactively by the user.
    """
    # 1. Get and validate the table name
    table_name = get_valid_name("Please enter the name for the new table: ")
    if not table_name:
        print("Table name cannot be empty. Exiting.")
        return

    column_definitions = []
    primary_key_defined = False

    print("\n--- Define Table Columns ---")
    print("Enter column details one by one. Press Enter on an empty column name when finished.")

    while True:
        # 2. Get and validate the column name
        col_name = get_valid_name("Enter column name (or press Enter to finish): ")
        if not col_name:
            break

        # 3. Get the column data type
        print("Select the data type for this column:")
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
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # 4. Get column constraints
        col_parts = [col_name, col_type]
        
        # Primary Key
        if not primary_key_defined:
            if input("Is this the PRIMARY KEY? (y/n): ").lower() == 'y':
                col_parts.append("PRIMARY KEY")
                primary_key_defined = True

        # Not Null
        if input("Can this column be empty (allow NULLs)? (y/n): ").lower() == 'n':
            col_parts.append("NOT NULL")

        # Unique
        if input("Must all values in this column be UNIQUE? (y/n): ").lower() == 'y':
            col_parts.append("UNIQUE")

        column_definitions.append(" ".join(col_parts))
        print(f"--> Column added: `{' '.join(col_parts)}`\n")

    if not column_definitions:
        print("No columns were defined. Table not created.")
        return

    # 5. Assemble the final SQL statement
    columns_sql = ", ".join(column_definitions)
    create_table_sql = f"CREATE TABLE {table_name} ({columns_sql});"

    print("\n--- Review Final SQL Statement ---")
    print(create_table_sql)
    
    if input("\nExecute this command to create the table? (y/n): ").lower() != 'y':
        print("Table creation cancelled by user.")
        return

    # 6. Connect and execute
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            print(f"\nSuccess! Table '{table_name}' has been created in '{DB_FILE}'.")
    except sqlite3.OperationalError as e:
        print(f"\nAn SQLite error occurred: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# Main execution block
if __name__ == "__main__":
    create_interactive_table()