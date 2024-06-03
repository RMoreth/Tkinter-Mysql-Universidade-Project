import tkinter as tk

# Function to update the label and button text based on the content of the Text widget


def revise_content():
    # Get the text from the Text widget (from the first character to the end, excluding the last character)
    new_text = text_widget.get("1.0", "end-1c")

    # Update the label text with the new content
    label.config(text=f"Updated Label: {new_text}")

    # Update the button text with the new content
    button.config(text=f"Updated Button: {new_text}")


# Create the main application window
app = tk.Tk()
app.title("Text Automatically Resize in Buttons and Lables")
app.geometry("720x250")

# Create a Text widget with a specified height, width, and word wrapping
text_widget = tk.Text(app, height=3, width=30, wrap="word")
# Insert initial text into the Text widget
text_widget.insert("1.0", "Type here...")

# Create a Label widget with an initial text
label = tk.Label(app, text="Initial Label")

# Create a Button widget with the label "Update Content" and associate it with the update_content function
button = tk.Button(app, text="Update Content", command=revise_content)

# Pack the widgets into the main window with some padding
text_widget.pack(pady=10)
label.pack(pady=10)
button.pack(pady=10)

# Run the Tkinter event loop to keep the application running
app.mainloop()
