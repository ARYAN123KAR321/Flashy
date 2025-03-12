from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card={}
data_dict={}

try:
    data=pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data=pandas.read_csv("data/french_words.csv")
    data_dict=original_data.to_dict(orient="records")
else:
    data_dict=data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card=random.choice(data_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=front_card)
    flip_timer=window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_card)

def is_known():
    data_dict.remove(current_card)
    new_data=pandas.DataFrame(data_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window=Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer=window.after(3000, flip_card)

canvas=Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card_background=canvas.create_image(400, 263, image=front_card)
card_title=canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word=canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=next_card)
cross_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)

next_card()

window.mainloop()