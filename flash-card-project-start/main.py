from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FRENCH_FONT = ("Ariel", 40, "italic")
ENGLISH_FONT = ("Ariel", 60, "bold")
timer = None
gen_word = {}

# -----------------Generate New Word ----------------------------------------------------------------------------
def gen_eng():
    canvas.itemconfig(canvas_image,image=photo_new)
    canvas.itemconfig(canvas_french, text="English", fill = "white")


def generate_word():
    global gen_word
    gen_word = random.choice(data_dict)
    canvas.itemconfig(canvas_image, image=photo_old)
    canvas.itemconfig(canvas_french,text="French", fill = "black")
    canvas.itemconfig(canvas_english, text=gen_word["French"], fill = "black")

    global timer
    timer = window.after(3000, gen_eng)


def remove_word():
    global gen_word, timer
    data_dict.remove(gen_word)
    updated_to_learn = pandas.DataFrame(data_dict)
    updated_to_learn.to_csv("data/to_learn.txt", index=False)
    window.after_cancel(timer)
    generate_word()

# ------------------Window Screen --------------------------------------------------------------------------------

window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, gen_eng)


try:
    with open("data/to_learn.csv") as file:
        data = pandas.read_csv(file)
except FileNotFoundError:
    with open("data/French_words.csv") as file:
        data = pandas.read_csv(file)
finally:
    data_dict = data.to_dict(orient="records")

# print(data_dict)

photo_old = PhotoImage(file="images/card_front.png")
photo_new = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=550, highlightthicknes=0, bg=BACKGROUND_COLOR)
canvas_image=canvas.create_image(400, 280, image=photo_old)
v = random.randint(0, 99)
canvas_french = canvas.create_text(400, 150, text="", font=FRENCH_FONT)
canvas_english = canvas.create_text(400, 263, text="", font=ENGLISH_FONT)
canvas.grid(row=0, column=0, columnspan=2)


#Button images for left and right
image_left = PhotoImage(file="images/wrong.png")
button_left = Button(image=image_left, highlightthickness=0, bg=BACKGROUND_COLOR, width=100, height=100,
                     command=generate_word)
button_left.grid(row=1, column=0)
image_right = PhotoImage(file="images/right.png")
button_right = Button(image=image_right, highlightthickness=0, bg=BACKGROUND_COLOR, width=100, height=100,
                      command=remove_word)
button_right.grid(row=1, column=1)

generate_word()
window.mainloop()
