import tkinter as tk
from tkinter import messagebox

# 1. Function to handle the button click and display the output
def on_button_click():
    # Get the text from the entry box
    user_input = entry_box.get()
    
    # Check if the box is empty
    if not user_input:
        messagebox.showerror("Error", "Please enter some text!")
        return

    # Update the output label with the user's text
    output_label.config(text=f"You entered: {user_input}")

# 2. Create the main window
root = tk.Tk()
root.title("Tkinter Practice App")
root.geometry("400x200") # Set a default window size

# 3. Create the input Textbox (Entry Widget)
# The width argument specifies the width in characters.
entry_box = tk.Entry(root, width=40)
# Use the pack geometry manager to place the widget in the window
entry_box.pack(pady=10) # pady adds vertical padding

# 4. Create the Button
# The 'command' argument links the button to the function we defined above
action_button = tk.Button(root, text="Submit Text", command=on_button_click)
action_button.pack(pady=5)

# 5. Create the Output Label (Method of seeing an output)
# Initially, the label is empty or holds a placeholder text
output_label = tk.Label(root, text="Output will appear here...", fg="blue")
output_label.pack(pady=10)

# 6. Start the main event loop
# This keeps the window open and responsive to user actions
root.mainloop()