import tkinter as tk
from tkinter import messagebox

def submit_feedback():
    """
    Retrieves text from all entry fields, prints it to the console,
    and then clears the fields.
    """
    # Get text from Entry and Text widgets
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    feedback = feedback_text_box.get("1.0", tk.END).strip()

    # Check if the user has entered any feedback (feedback is mandatory)
    if feedback:
        print("--- New Customer Feedback ---")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Feedback: {feedback}")
        print("---------------------------\n")

        # Clear all the entry fields
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        feedback_text_box.delete("1.0", tk.END)

        # Optional: Show a success message to the user
        messagebox.showinfo("Success", "Thank you! Your feedback has been submitted.")
    else:
        # Optional: Show an error if the feedback submission is empty
        messagebox.showwarning("Empty Field", "Please enter your feedback before submitting.")

# --- UI Setup ---

# 1. Create the main application window
window = tk.Tk()
window.title("Customer Feedback")
window.geometry("500x450") # Adjusted size for new fields
window.config(padx=20, pady=20) # Add some padding around the window

# Use the grid layout manager for better alignment
window.columnconfigure(1, weight=1) # Allow the entry column to expand

# 2. Create and place the widgets
# --- Main Instruction ---
main_instruction_label = tk.Label(window, text="Please provide feedback on your experience", font=("Arial", 14, "bold"))
main_instruction_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

# --- Name Row ---
name_label = tk.Label(window, text="Name:", font=("Arial", 12))
name_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

name_entry = tk.Entry(window, font=("Arial", 10), width=40)
name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# --- Email Row ---
email_label = tk.Label(window, text="Email:", font=("Arial", 12))
email_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

email_entry = tk.Entry(window, font=("Arial", 10), width=40)
email_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# --- Feedback Row ---
feedback_label = tk.Label(window, text="Feedback:", font=("Arial", 12))
feedback_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

feedback_text_box = tk.Text(window, height=10, width=50, wrap=tk.WORD, font=("Arial", 10))
feedback_text_box.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
window.rowconfigure(3, weight=1) # Allow the text box row to expand vertically

# --- Submit Button ---
# The 'command' option is linked to our submit_feedback function
submit_button = tk.Button(window, text="Submit", command=submit_feedback, font=("Arial", 11, "bold"))
submit_button.grid(row=4, column=1, sticky="e", pady=10)

# 3. Start the Tkinter event loop
# This line keeps the window open and listens for events (like button clicks)
window.mainloop()