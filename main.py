import tkinter as tk
from math import floor
import playsound

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

FONT_NAME = "Courier"
WORK_SOUND = "resources/work.mp3"
BREAK_SOUND = "resources/break.mp3"
CHECK_MARK = "✓"


class Pymodoro(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.reps = 0
        self.marks = []
        self.parent = parent
        self.timer = None

        # Labels
        self.timer_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
        self.timer_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
        self.check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))

        # Canvas
        self.canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.bg_image = tk.PhotoImage(file="resources/tomato.png")
        self.canvas.create_image(100, 112, image=self.bg_image)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

        # Buttons
        self.start_button = tk.Button(text="Start", bg=GREEN, font=(FONT_NAME, 10, "bold"), command=self.start_timer)
        self.reset_button = tk.Button(text="Reset", bg=RED, font=(FONT_NAME, 10, "bold"), command=self.reset_timer)

        # Grid
        self.canvas.grid(column=1, row=1)
        self.timer_label.grid(column=1, row=0)
        self.check_marks.grid(column=1, row=3)
        self.start_button.grid(column=0, row=2)
        self.reset_button.grid(column=2, row=2)

    def reset_timer(self):
        self.reps = 0
        self.marks.clear()
        self.check_marks.config(text=self.marks)

        self.start_button.config(state="normal")
        self.timer_label.config(text="Timer")
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.parent.after_cancel(self.timer)

    def start_timer(self):
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        self.reps += 1
        self.start_button.config(state="disabled")

        if self.reps % 8 == 0:
            playsound.playsound(BREAK_SOUND, False)
            self.timer_label.config(text="Long break")
            self.count_down(long_break_sec)

        elif self.reps % 2 == 0:
            playsound.playsound(BREAK_SOUND, False)
            self.timer_label.config(text="Break")
            self.count_down(short_break_sec)
        else:
            playsound.playsound(WORK_SOUND, False)
            self.timer_label.config(text="Work")
            self.count_down(work_sec)

    def count_down(self, count):
        minutes = floor(count / 60)
        seconds = count % 60

        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds == 0:
            seconds = "00"
        elif seconds < 10:
            seconds = f"0{seconds}"

        self.canvas.itemconfig(self.timer_text, text=f"{minutes}:{seconds}")

        if count > 0:
            self.timer = self.parent.after(1000, self.count_down, count - 1)
        else:
            self.start_timer()
            self.marks.clear()

            for _ in range(floor(self.reps / 2)):
                self.marks.append(CHECK_MARK)

            self.check_marks.config(text=self.marks)
            self.parent.deiconify()
            self.parent.lift()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pymodoro")
    root.config(bg=YELLOW, padx=100, pady=50)
    Pymodoro(root)
    root.mainloop()
