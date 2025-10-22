import tkinter as tk
from tkinter import ttk
import threading
import openai

# --- OpenAI API Configuration ---
# Import the key from your APIKey.py file
try:
    from APIKey import OPENAI_API_KEY
    # Pass the key directly to the client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    API_KEY_IS_SET = True
except ImportError:
    # This will happen if the file doesn't exist
    # or the variable is not found.
    API_KEY_IS_SET = False
except openai.OpenAIError:
    # This might happen if the key is invalid
    API_KEY_IS_SET = False
# ------------------------------


def get_openai_response(question):
    """
    Calls the OpenAI API and returns the answer.
    This function is designed to be run in a separate thread.
    """
    if not API_KEY_IS_SET:
        return "Error: Could not import OPENAI_API_KEY from APIKey.py.\n\nPlease ensure the file exists in the same directory and the variable is named correctly."

    try:
        # Based on the documentation you provided, but adapted for Python
        # and the modern chat completions API.
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using a real, available model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        # Extract the text from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        # Return a formatted error message
        return f"An API error occurred:\n{e}"

def submit_question():
    """
    Handles the submit button click.
    1. Gets the question from the entry box.
    2. Disables the button to prevent multiple clicks.
    3. Shows a "loading" message.
    4. Starts a new thread to call the API.
    """
    question = question_entry.get()
    if not question:
        return  # Do nothing if the entry is empty

    # Disable button and show loading message
    submit_button.config(text="Loading...", state=tk.DISABLED)
    answer_box.delete("1.0", tk.END)
    answer_box.insert(tk.END, "Generating answer, please wait...")

    # Start the API call in a new thread to avoid freezing the GUI
    # The 'daemon=True' ensures the thread will close when the main app closes.
    threading.Thread(target=fetch_answer_and_update_gui, args=(question,), daemon=True).start()

def fetch_answer_and_update_gui(question):
    """
    Worker function that runs in the thread.
    1. Calls the API.
    2. Schedules the GUI update on the main thread.
    """
    # This function runs in the background thread
    answer = get_openai_response(question)
    
    # We must update the GUI from the main thread.
    # root.after(0, ...) schedules 'update_gui' to run in the main loop.
    root.after(0, update_gui_with_answer, answer)

def update_gui_with_answer(answer):
    """
    Updates the GUI with the final answer.
    This function is guaranteed to run on the main thread.
    """
    # Clear the "loading..." message
    answer_box.delete("1.0", tk.END)
    
    # Insert the actual answer
    answer_box.insert(tk.END, answer)
    
    # Re-enable the submit button
    submit_button.config(text="Submit", state=tk.NORMAL)


# --- Set up the main application window ---
root = tk.Tk()
root.title("Q&A Interface (with OpenAI)")
root.geometry("450x300") # Set a default size

# Use a style for a more modern look
style = ttk.Style(root)
style.theme_use("clam")

# --- Create the widgets ---

# 1. Label and Entry for the question
question_frame = ttk.Frame(root)
question_label = ttk.Label(question_frame, text="Enter your question:")
question_entry = ttk.Entry(question_frame, width=50)

# 2. Submit Button
submit_button = ttk.Button(root, text="Submit", command=submit_question)

# 3. Output box for the answer
answer_box = tk.Text(root, height=8, width=50, wrap="word")

# --- Arrange the widgets on the screen using .pack() ---
question_label.pack(side=tk.LEFT, padx=5)
question_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

question_frame.pack(pady=10, padx=10, fill="x")
submit_button.pack(pady=5)
answer_box.pack(pady=10, padx=10, fill="both", expand=True) # Fill both x and y

# --- Start the main event loop ---
root.mainloop()

