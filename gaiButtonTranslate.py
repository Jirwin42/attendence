import tkinter as tk

class LabelChangerApp:
    """
    A class-based Tkinter application that displays a greeting in a different
    language whenever the corresponding language button is clicked.
    """
    def __init__(self, master):
        # 1. Initialize the main window (master)
        self.master = master
        master.title("International Greeting App")
        # Adjusted size for vertical buttons
        master.geometry("400x350") 
        master.config(padx=10, pady=10)

        # 2. Define the data (Language and Greeting)
        self.greetings = [
            # Updated language names to native spelling
            {"language": "English", "text": "Hello, world!"},
            {"language": "Español", "text": "¡Hola, mundo!"},
            {"language": "Français", "text": "Bonjour, le monde !"},
            {"language": "Deutsch", "text": "Hallo, Welt!"},
            {"language": "Italiano", "text": "Ciao, mondo!"},
            {"language": "日本語", "text": "こんにちは、世界！"}
        ]

        # 3. Create Widgets

        # Frame to hold the buttons vertically, centered on the screen
        button_frame = tk.Frame(master)
        button_frame.pack(pady=15)

        # Create Buttons dynamically for each language
        for greeting_data in self.greetings:
            language = greeting_data["language"]
            greeting_text = greeting_data["text"]
            
            # Create a button for each language
            button = tk.Button(
                button_frame,
                text=language,
                # Use lambda to bind the specific greeting_text to the set_greeting method
                command=lambda text=greeting_text: self.set_greeting(text),
                font=('Arial', 10),
                # Removed blue coloring (bg, fg, activebackground) for a default look
                relief=tk.RAISED
            )
            # Pack buttons one on top of the other (default pack behavior is side=TOP)
            # fill=tk.X makes all buttons the same width within the frame
            button.pack(pady=2, fill=tk.X) 

        # Create the Output Label (Must be at the bottom)
        # Initialize with the default English greeting
        default_greeting = self.greetings[0]["text"]
        self.output_label = tk.Label(
            master,
            text=default_greeting,
            font=('Arial', 16, 'bold'), # Larger and bolder font for the output
            fg="#020101", # A distinct color for the output message
            pady=20
        )
        self.output_label.pack()

    def set_greeting(self, new_text):
        """
        Sets the text of the output label directly to the provided new_text.
        """
        # 1. Update the label text
        self.output_label.config(text=new_text)

# Execution block to run the application
if __name__ == "__main__":
    # Create the root window instance
    root = tk.Tk()
    
    # Create an instance of the App class, passing the root window as the master
    app = LabelChangerApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()