import tkinter as tk
import random

# Screen Setup
root = tk.Tk()
root.title("Flashcard App")
root.geometry("800x450")
root.config(bg="#babcc0")

# Frames
quiz_screen = tk.Frame(root, bg="#babcc0")
practice_screen = tk.Frame(root, bg="#babcc0")
main_screen = tk.Frame(root, bg="#babcc0")

for frame in (main_screen, quiz_screen, practice_screen):
    frame.place(x=0, y=0, width=800, height=450)

# Global Variables
flashcard_set_pady, new_termy = 10, 250

# Flashcard Classes
class Flashcards:
    class FlashcardEntry:
        def __init__(self, parent, hint, user_input, entry_widget):
            self.hint = hint
            self.user_input = user_input
            self.entry_widget = entry_widget
            self.entry_widget.insert(tk.INSERT, self.hint)
            self.entry_widget.bind("<Button-1>", self.click_function)

        def click_function(self, event):
            self.entry_widget.delete(0, tk.END)

# Functions
def add_flashcard():
    global new_termy
    Flashcards.FlashcardEntry(main_screen, "Enter Term", "", tk.Entry(main_screen)).entry_widget.place(x=100, y=new_termy, width=200)
    Flashcards.FlashcardEntry(main_screen, "Enter Definition", "", tk.Entry(main_screen)).entry_widget.place(x=350, y=new_termy, width=200)
    new_termy += 50

def show_frame(frame):
    frame.tkraise()

# Flashcard Data and State
flashcards_data = []
current_index = 0
showing_term = True

def collect_flashcards():
    global flashcards_data
    flashcards_data.clear()
    entries = []
    for widget in main_screen.winfo_children():
        if isinstance(widget, tk.Entry):
            x, y = widget.winfo_x(), widget.winfo_y()
            text = widget.get()
            entries.append((x, y, text))
    entries.sort(key=lambda item: item[1])  # sort by y-coordinate
    flashcards_data = [(entries[i][2], entries[i+1][2]) for i in range(0, len(entries), 2)]

def start_practice():
    collect_flashcards()
    global current_index, showing_term
    current_index = 0
    showing_term = True
    show_frame(practice_screen)
    show_flashcard()

def show_flashcard():
    if not flashcards_data:
        flash_label.config(text="No flashcards available")
        return
    card = flashcards_data[current_index]
    flash_label.config(text=card[0] if showing_term else card[1])
    if practice_screen.winfo_exists():
        if showing_term:
            def_label.place_forget()
            term_label.place(x=100, y=25, width=600, height=100)
        else:
            term_label.place_forget()
            def_label.place(x=100, y=25, width=600, height=100)

def flip_flashcard():
    global showing_term
    showing_term = not showing_term
    show_flashcard()

def next_flashcard():
    global current_index, showing_term
    if current_index < len(flashcards_data) - 1:
        current_index += 1
        showing_term = True
        show_flashcard()

def previous_flashcard():
    global current_index, showing_term
    if current_index > 0:
        current_index -= 1
        showing_term = True
        show_flashcard()

def start_quiz():
    collect_flashcards()
    if not flashcards_data:
        return

    for widget in quiz_screen.winfo_children():
        if widget != back_button:
            widget.destroy()

    valid_flashcards = [
        (term, definition)
        for term, definition in flashcards_data
        if term.strip() not in ("", "Enter Term", "Enter Flashcard") and
           definition.strip() not in ("", "Enter Definition")
    ]

    if not valid_flashcards:
        return

    terms = [term for term, _ in valid_flashcards]
    definitions = [definition for _, definition in valid_flashcards]
    random.shuffle(definitions)

    tk.Label(quiz_screen, text="Term", font=("Arial", 14, "bold"), bg="#babcc0").place(x=150, y=10)
    tk.Label(quiz_screen, text="Definition", font=("Arial", 14, "bold"), bg="#babcc0").place(x=350, y=10)
    tk.Label(quiz_screen, text="True / False", font=("Arial", 14, "bold"), bg="#babcc0").place(x=610, y=10)

    for i, (term, definition) in enumerate(zip(terms, definitions)):
        y = 50 + i * 60
        tk.Label(quiz_screen, text=term, font=("Arial", 14), bg="#babcc0").place(x=150, y=y)
        tk.Label(quiz_screen, text=definition, font=("Arial", 14), bg="#babcc0").place(x=350, y=y)
        tk.Checkbutton(quiz_screen, bg="#babcc0").place(x=610, y=y)

# Initialize Flashcards
yval = 50
spacing = 50
initial_y_positions = [yval, yval+spacing, yval+spacing*2, yval+spacing*3]
for y in initial_y_positions:
    Flashcards.FlashcardEntry(main_screen, "Enter Term", "", tk.Entry(main_screen)).entry_widget.place(x=100, y=y, width=200)
    Flashcards.FlashcardEntry(main_screen, "Enter Definition", "", tk.Entry(main_screen)).entry_widget.place(x=350, y=y, width=200)

flash_label = tk.Label(practice_screen, text="", font=("Arial", 20), bg="#babcc0", wraplength=600)
flash_label.place(x=100, y=150, width=600, height=100)

def_label = tk.Label(practice_screen, text="Definition", font=("Arial", 20), bg="#babcc0", wraplength=600)
term_label = tk.Label(practice_screen, text="Term", font=("Arial", 20), bg="#babcc0", wraplength=600)

tk.Button(main_screen, text="Add Flashcard", font=("Arial", 12), command=add_flashcard).place(x=600, y=50)
tk.Button(main_screen, text="Start Practice", font=("Arial", 12), command=start_practice).place(x=600, y=100)
tk.Button(main_screen, text="Start Quiz", font=("Arial", 12), command=lambda: [show_frame(quiz_screen), start_quiz(), root.geometry("850x450")]).place(x=600, y=150)

tk.Button(practice_screen, text="Back", font=("Arial", 20), command=lambda: show_frame(main_screen)).place(x=10, y=10)
tk.Button(practice_screen, text="<", font=("Arial", 25), command=previous_flashcard).place(x=250, y=350)
tk.Button(practice_screen, text="FLIP", font=("Arial", 25), command=flip_flashcard).place(x=350, y=350)
tk.Button(practice_screen, text=">", font=("Arial", 25), command=next_flashcard).place(x=500, y=350)

back_button = tk.Button(quiz_screen, text="Back", font=("Arial", 10), command=lambda: show_frame(main_screen))
back_button.place(x=40, y=10)

show_frame(main_screen)
root.mainloop()
