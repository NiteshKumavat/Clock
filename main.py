from tkinter import *
from tkinter import messagebox
import pygame
import datetime

# Global alarm variable
alarm_set = False
alarm_time = ""

# Reset the alarm
def reset_alarm():
    global alarm_set, alarm_time
    alarm_set = False
    alarm_time = ""
    pygame.mixer.music.stop()
    start_button.config(text="Start the Alarm", bg="white")

# Alarm button logic
def alarm_button():
    global alarm_set, alarm_time
    if start_button.cget("text") == "Stop the Alarm":
        reset_alarm()
    else:
        if not user_alarm.get():
            messagebox.showerror("Alarm is empty", "Please enter the time in the format HH:MM:SS")
            return

        # Validate alarm format
        alarm = user_alarm.get().split(":")
        if len(alarm) == 3 and all(len(part) == 2 and part.isdigit() for part in alarm):
            if int(alarm[0]) < 24 and int(alarm[1]) < 60 and int(alarm[2]) < 60:
                alarm_time = user_alarm.get()
                alarm_set = True
                start_button.config(text="Stop the Alarm", bg="red")
            else:
                messagebox.showerror("Invalid time", "Enter a valid time in HH:MM:SS format")
        else:
            messagebox.showerror("Invalid time", "Enter a valid time in HH:MM:SS format")

# Play ringtone
def play_ringtone():
    pygame.mixer.init()
    pygame.mixer.music.load("ringtone.mp3")
    pygame.mixer.music.play()

# Check alarm continuously
def check_alarm():
    global alarm_set, alarm_time
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if alarm_set and current_time == alarm_time:
        play_ringtone()
        messagebox.showinfo("Alarm Triggered", "The alarm time has been reached!")
        reset_alarm()
    window.after(1000, check_alarm)

# Update the timer display
def update_timer():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    canvas.itemconfig(canvas_time, text=current_time)
    window.after(1000, update_timer)

# Tkinter setup
window = Tk()
window.title("Alarm Clock")

user_alarm = StringVar()

canvas = Canvas(window, width=500, height=200, bg="black")
canvas_time = canvas.create_text(250, 100, text="00:00:00", fill="blue", font=("Arial", 70))
canvas.pack(padx=20, pady=20)

start_button = Button(window, text="Start the Alarm", width=20, height=3, command=alarm_button, font=("Arial", 15))
start_button.pack(padx=20, pady=30, side=LEFT)

alarm_entry = Entry(window, textvariable=user_alarm, width=10, font=("Arial", 35))
alarm_entry.pack(padx=20, pady=30, ipadx=20, ipady=15, side=RIGHT)

update_timer()
check_alarm()

window.mainloop()


