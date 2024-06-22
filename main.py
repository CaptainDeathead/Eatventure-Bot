import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror, showinfo
from os import _exit
from json import dumps
from pyautogui import keyDown, keyUp
from threading import Thread
from time import sleep
from data import *

def find_ip_address() -> None:
    ip = askstring("Phone IP Address", "What is your phone's IP Address? (Ensure its running a VNC server and is on the same internet connection as your computer)")
    CONFIG["PHONE_IP_ADDRESS"] = ip

    with open("config.json", "w") as file:
        file.write(dumps(CONFIG))

    showinfo("IP Fix", "Restart the bot!")

try: import bot
except:
    showerror("Failed to find IP!", "Failed to connect to the phone, please try again with a different IP address!")
    find_ip_address()
    _exit(0)

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

class Window:
    WIDTH: int = 800
    HEIGHT: int = 800

    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.title("Eatventure-Bot")
        self.root.config(bg=_from_rgb((60, 0, 150)))

        self.bot_thread: Thread = Thread(target=self.push_bot_step, daemon=True)
        self.sync_bot_pause_thread: Thread = Thread(target=self.sync_bot_pause, daemon=True)

        self.bot_status: bool = False
        self.bot_pause_status: bool = False

        self.title_lbl: tk.Label = tk.Label(self.root, text="Eatventure Bot", bg=_from_rgb((60, 0, 150)), font=("assets/arial.ttf", 50), fg="#FFFFFF")
        self.title_lbl.pack()

        self.bot_status_lbl: tk.Label = tk.Label(self.root, text="Bot status: Not running\n", bg=_from_rgb((60, 0, 150)), font=("assets/arial.ttf", 25), fg="#FF0000")
        self.bot_status_lbl.pack()

        self.ip_lbl: tk.Label = tk.Label(self.root, text="Phone IP address", bg=_from_rgb((60, 0, 150)), font=("assets/arial.ttf", 20), fg="#FFFFFF")
        self.ip_lbl.pack(anchor="n")

        self.ip_entry: tk.Entry = tk.Entry(self.root, bg="#FFFFFF", fg="#000000", font=("assets/arial.ttf", 15))
        self.ip_entry.pack(anchor="n")
        self.ip_entry.insert(0, PHONE_IP_ADDRESS)
        self.ip_entry.config(state='readonly')

        # fill in the blank space
        tk.Label(self.root, text="", bg=_from_rgb((60, 0, 150)), font=("arial.ttf", 150)).pack()

        self.bot_pause_btn: tk.Button = tk.Button(self.root, text="Pause", bg="#888888", fg="#FFAA00", font=("assets/arial.ttf", 35), activebackground="#888888", activeforeground="#FFAA00", command=self.set_bot_pause_state)
        self.bot_pause_btn.place(anchor="center", x=self.WIDTH/2, y=self.HEIGHT/2-100)

        self.bot_run_btn: tk.Button = tk.Button(self.root, text="Start", bg="#0055FF", fg="#00FF00", font=("assets/arial.ttf", 50), activebackground="#0075FF", activeforeground="#00FF00", command=self.set_bot_state)
        self.bot_run_btn.place(anchor="center", x=self.WIDTH/2, y=self.HEIGHT/2)

        self.scroll_lbl: tk.Label = tk.Label(self.root, text=f"Max scrolls", fg="#FFFFFF", bg=_from_rgb((60, 0, 150)), font=("assets/arial.ttf", 25))
        self.scroll_lbl.pack()

        self.scroll_var: tk.IntVar = tk.IntVar(self.root, MAX_SCROLLS)

        self.scroll_slider: tk.Scale = tk.Scale(self.root, from_=0, to=20, orient="horizontal", fg="#FFFFFF", background=_from_rgb((60, 0, 150)), variable=self.scroll_var, command=self.set_scroll)
        self.scroll_slider.pack()

    def set_scroll(self, value: int) -> None:
        bot.MAX_SCROLLS = self.scroll_var.get()

    def set_bot_pause_state(self) -> None:
        if not self.bot_status: return

        if not self.bot_pause_status:
            self.bot_status_lbl.config(text="Bot status: Paused\n", fg="#FFAA00")
            self.bot_pause_btn.config(text="Resume", fg="#00FF00", activeforeground="#00FF00")
            keyDown('f7')
            sleep(0.5)
            keyUp('f7')
        else:
            self.bot_status_lbl.config(text="Bot status: Running\n", fg="#00FF00")
            self.bot_pause_btn.config(text="Pause", fg="#FFAA00", activeforeground="#FFAA00")
            keyDown('f9')
            sleep(0.5)
            keyUp('f9')

        self.bot_pause_status = not self.bot_pause_status

    def set_bot_state(self) -> None:
        if not self.bot_status:
            self.bot_status_lbl.config(text="Bot status: Running\n", fg="#00FF00")
            self.bot_run_btn.config(text="Stop", fg="#FF0000", activeforeground="#FF0000")
            self.bot_pause_btn.config(text="Pause", fg="#FFAA00", bg="#0055FF", activeforeground="#FFAA00", activebackground="#0055FF")

            self.bot_status = True

            bot.main(False)
            self.bot_thread: Thread = Thread(target=self.push_bot_step, daemon=True)
            self.bot_thread.start()

            self.sync_bot_pause_thread: Thread = Thread(target=self.sync_bot_pause, daemon=True)
            self.sync_bot_pause_thread.start()
        else:
            self.bot_status_lbl.config(text="Bot status: Not running\n", fg="#FF0000")
            self.bot_run_btn.config(text="Start", fg="#00FF00", activeforeground="#00FF00")
            self.bot_pause_btn.config(text="Pause", fg="#FFAA00", bg="#888888", activeforeground="#FFAA00", activebackground="#888888")

            self.bot_status = False

            keyDown('f8')
            sleep(0.5)
            keyUp('f8')
            self.bot_thread.join()
            self.sync_bot_pause_thread.join()
            bot.space_pressed = False

    def sync_bot_pause(self) -> None:
        while self.bot_status:
            if bot.paused != self.bot_pause_status: self.set_bot_pause_state()

            sleep(0.1)

    def push_bot_step(self) -> None:
        while self.bot_status:
            try: bot.step_bot()
            except: pass

            if bot.off:
                bot.off = False
                break

    def main(self) -> None:
        self.root.mainloop()

def main():
    window: Window = Window()
    window.main()

if __name__ == "__main__":
    main()
    _exit(0)