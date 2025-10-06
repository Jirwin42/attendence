# attendence

## Respoitory for various attencence files.

# Python Tkinter GUI Project: Customer Management

This repository contains a collection of Python scripts demonstrating GUI development using the `tkinter` library. The main application is a Customer Management System that interacts with a SQLite database. Additional scripts are included as examples of various Tkinter concepts.

## Core Components

The primary components of this project are the main management application, a table-based data viewer, and the SQLite database they both use.

### `databaseManagement.py`
This is the main application for managing customer information. It provides a user-friendly interface to perform CRUD (Create, Read, Update, Delete) operations, although updating is implicitly handled by deleting and re-adding.

**Key Features:**
* **Visual Grid:** Displays all customers from the database in a navigable button grid.
* **Add Customers:** Opens a separate window to add a new customer with input validation for email, phone number, and birthday formats.
* **Delete Customers:** Allows for the deletion of the currently selected customer with a confirmation prompt.
* **Detailed View:** Shows all information for a selected customer in a read-only details panel.
* **Keyboard Navigation:** Use arrow keys to navigate between customer buttons.

### `readDatabase.py`
A standalone GUI application for viewing the data within the `customers.db` file in a clean, tabular format.

**Key Features:**
* **Table View:** Displays all records from the `Customer` table in a sortable grid.
* **Column Sorting:** Click on any column header to sort the data in ascending or descending order.
* **Refresh Data:** A button to reload the data from the database to see any new changes.
* **Status Bar:** Shows the total number of customer records found.

### `customers.db`
This is the SQLite database file where all customer information is stored.

* **Table Name:** `Customer`
* **Schema:** The table includes the following columns:
    * `id` (INTEGER, Primary Key, Autoincrement)
    * `Name` (TEXT)
    * `Birthday` (TEXT)
    * `Email` (TEXT)
    * `PhoneNumber` (TEXT)
    * `Address` (TEXT)
    * `PreferredContact` (TEXT)

## Additional Example Scripts

These files are smaller, self-contained examples demonstrating specific Tkinter features.

* **`firstGUI.py`**: A very basic "Hello, World" style Tkinter application. It includes an input box, a submit button, and a label to display the user's input. It's an excellent starting point for understanding the fundamentals of Tkinter widgets and event handling.

* **`gaiFeedbackPage.py`**: A script that creates a simple customer feedback form. It includes fields for name, email, and a multi-line text box for feedback. When submitted, the data is printed to the console.

* **`gaiButtonTranslate.py`**: A class-based application that demonstrates updating a widget's text dynamically.
It features several buttons, each labeled with a language. Clicking a button displays "Hello, world!" in that language in a central label.

## Prerequisites

* Python 3
* Tkinter library (usually included with standard Python installations)
* SQLite3 library (included with standard Python installations)

No external libraries are required to run these scripts.

## How to Run

Ensure all files are in the same directory. Open a terminal or command prompt, navigate to that directory, and run one of the main scripts.

**To run the main Customer Management System:**
```bash
python databaseManagement.py