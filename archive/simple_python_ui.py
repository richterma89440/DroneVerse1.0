import tkinter as tk


def button_click():
    print("Button wurde geklickt!")


def checkbox_toggle():
    print("Checkbox wurde umgeschaltet!")


def entry_submit():
    text = entry.get()
    print("Eingabe:", text)


# Fenster erstellen
window = tk.Tk()

# Button erstellen
button = tk.Button(
    window,
    text="Klick mich!",
    command=button_click,
    bg="white",
    fg="purple",
    relief=tk.RAISED,
)
button.configure(font=("Arial", 12, "bold"))
button.pack()

# Checkbox erstellen
checkbox = tk.Checkbutton(window, text="Checkbox", command=checkbox_toggle)
checkbox.pack()

# Eingabefeld erstellen
entry = tk.Entry(window)
entry.pack()

# Submit-Button für das Eingabefeld erstellen
submit_button = tk.Button(window, text="Submit", command=entry_submit)
submit_button.pack()

# Toggle-Button erstellen
toggle_button_state = tk.BooleanVar()
toggle_button = tk.Checkbutton(window, text="Toggle", variable=toggle_button_state)
toggle_button.pack()

# Fenster anzeigen
window.mainloop()
