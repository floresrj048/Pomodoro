from datetime import datetime, timedelta
import datetime
from tkinter import *
from tkinter import font
import tkinter as tk

GLOBAL_POMODORO = 7
GLOBAL_BREAKTIME = 5
time_remaining = datetime.timedelta(seconds=GLOBAL_POMODORO)
is_paused = False
main_cycle=True

def configure_label(message,text_size):
    label.configure(text=message, font=(font.Font(family="Arial", size=text_size)))

def set_time_remaining(time):
    global time_remaining
    time_remaining = datetime.timedelta(seconds=time)

def window_popup():
    window.wm_deiconify()
    window.lift()
    window.attributes('-topmost', True)
    window.focus_force()
    window.after_idle(window.attributes, '-topmost', False)

def countdown(length):
    global time_remaining
    global is_paused
    global main_cycle
    global method_called
    global is_reset

    if time_remaining <= datetime.timedelta():
        if main_cycle:
            configure_label("Nice work! Break time.\n Press start to resume.",25)
            set_time_remaining(GLOBAL_BREAKTIME)
            main_cycle=False
            method_called = False
            window_popup()
        
        else:
            configure_label("Back to it.\n Let's do it!",25)
            set_time_remaining(GLOBAL_POMODORO)
            main_cycle=True
            method_called = False
            window_popup()

    elif not is_paused and not is_reset:
        #represents time left
        time_remaining = length
        #prints time left
        print(time_remaining, end="\r")
        #update value on window
        label['text'] = time_remaining

        if length >= datetime.timedelta():
            # delay the program one second
            window.after(1000,countdown,length-datetime.timedelta(seconds=1))

def button_callback():
    global method_called
    global time_remaining
    global is_paused
    global is_reset
    if not method_called:
        if is_paused or is_reset:
            is_paused=False
            is_reset=False
        else:
            configure_label(time_remaining,48) 
        countdown(time_remaining)
        method_called = True

def pause_callback():
    global is_paused
    global method_called 
    is_paused = True
    method_called = False

def reset_callback():
    global method_called
    global time_remaining
    global is_paused
    global main_cycle
    global is_reset
    if not is_reset: 
        set_time_remaining(GLOBAL_POMODORO)
        is_paused = False
        method_called = False
        main_cycle= True
        is_reset = True
        configure_label(time_remaining,48)

method_called=False
is_reset = False

window = Tk()

window.title("Pomodoro Study Buddy")
window.geometry(f"350x150")
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(3, weight=1)

main_frame = Frame(window)
main_frame.pack()

main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

bottom_frame = Frame(window)
bottom_frame.pack()


label_font = font.Font(family="Arial", size=48)    
label = Label(main_frame,text=time_remaining, anchor="center",justify="center", font=label_font)
label.grid(row=0,column=0,sticky="nsew")

start_button = Button(bottom_frame, text="Start", command=button_callback, justify="left")
start_button.grid(column=0, row=2, sticky="w", padx=20, pady=10)

pause_button = Button(bottom_frame, text="Pause", command=pause_callback, justify="center")
pause_button.grid(column=1, row=2, sticky="nsew", padx=20, pady=10)

reset_button = Button(bottom_frame, text="Reset", command=reset_callback, justify="right")
reset_button.grid(column=2, row=2, sticky="e", padx=20, pady=10)

window.resizable(False,False)

window.mainloop()