import tkinter as tk
import threading
import yt_dlp
import os
import itertools
import winsound

# ================= APP INFO =================
APP_NAME = "YT-HACKER"
BUILD = "v1.3.8"
DEV_NAME = "Stanley Gachara Mwangi"
MODE = "HD VIDEO + PLAYLIST"

# ================= COLORS =================
BG = "#0b0f0c"
FG = "#00ff88"
ACCENT = "#00ffaa"

DOWNLOAD_DIR = "downloads"

# ================= STATE =================
current_state = "IDLE"  # IDLE | SCANNING | COMPLETE | ERROR

cursor_cycle = itertools.cycle(["█", " "])
scan_cycle = itertools.cycle([".", "..", "..."])

# ================= SOUND =================
def key_sound(event=None):
    winsound.Beep(1200, 25)

def click_sound():
    winsound.Beep(800, 80)

# ================= TERMINAL =================
def log(msg):
    terminal.insert(tk.END, msg + "\n")
    terminal.see(tk.END)

# ================= STATUS LOOP =================
def status_loop():
    if current_state == "IDLE":
        status_label.config(
            text=f"STATUS: IDLE {next(cursor_cycle)}"
        )

    elif current_state == "SCANNING":
        status_label.config(
            text=f"STATUS: SCANNING{next(scan_cycle)}"
        )

    elif current_state == "COMPLETE":
        status_label.config(text="STATUS: COMPLETE ✔")

    elif current_state == "ERROR":
        status_label.config(text="STATUS: FAILURE ✖")

    root.after(400, status_loop)

# ================= DOWNLOAD =================
def start_download():
    global current_state

    url = url_entry.get().strip()
    if not url:
        log("[X] No target URL supplied")
        return

    click_sound()
    current_state = "SCANNING"
    progress_bar.set(0)

    log("[*] Target locked")
    log("[*] Deploying HD payload")

    def run():
        global current_state
        try:
            ydl_opts = {
                "outtmpl": os.path.join(
                    DOWNLOAD_DIR,
                    "%(playlist_title)s/%(title)s.%(ext)s"
                ),
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "noplaylist": False,
                "progress_hooks": [progress_hook],
                "quiet": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            current_state = "COMPLETE"
            log("[✓] Download completed successfully")

        except Exception as e:
            current_state = "ERROR"
            log(f"[X] ERROR: {e}")

    threading.Thread(target=run, daemon=True).start()

def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "0%").replace("%", "").strip()
        speed = d.get("_speed_str", "")
        try:
            progress_bar.set(float(percent))
        except:
            pass
        log(f"[DL] {percent}% @ {speed}")

    elif d["status"] == "finished":
        log("[*] Merging audio + video")

# ================= GUI =================
root = tk.Tk()
root.title(f"{APP_NAME} {BUILD} | {DEV_NAME}")
root.geometry("960x580")
root.configure(bg=BG)

title = tk.Label(
    root,
    text=f"{APP_NAME} // {MODE}",
    fg=ACCENT,
    bg=BG,
    font=("Consolas", 18, "bold")
)
title.pack(pady=8)

dev_label = tk.Label(
    root,
    text=f"DEV: {DEV_NAME} | BUILD: {BUILD}",
    fg=FG,
    bg=BG,
    font=("Consolas", 10)
)
dev_label.pack()

status_label = tk.Label(
    root,
    text="STATUS: BOOTING █",
    fg=FG,
    bg=BG,
    font=("Consolas", 10)
)
status_label.pack(pady=4)

url_entry = tk.Entry(
    root,
    width=110,
    bg="black",
    fg=FG,
    insertbackground=FG,
    font=("Consolas", 11)
)
url_entry.pack(pady=6)
url_entry.bind("<KeyPress>", key_sound)

btn = tk.Button(
    root,
    text="EXECUTE",
    bg="black",
    fg=ACCENT,
    font=("Consolas", 11, "bold"),
    command=start_download
)
btn.pack(pady=6)

progress_bar = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
    length=920,
    bg=BG,
    fg=FG,
    highlightthickness=0,
    troughcolor="black"
)
progress_bar.pack(pady=6)

terminal = tk.Text(
    root,
    bg="black",
    fg=FG,
    font=("Consolas", 10),
    relief="flat"
)
terminal.pack(expand=True, fill="both", padx=14, pady=14)

# ================= BOOT =================
boot_lines = [
    "[+] Initializing neural shell...",
    f"[+] Developer authenticated: {DEV_NAME}",
    f"[+] Build loaded: {BUILD}",
    "[+] Loading yt-dlp core...",
    "[+] Enabling HD streams...",
    "[+] Playlist module online",
    "[+] Terminal ready"
]

def boot_sequence(lines, i=0):
    if i < len(lines):
        log(lines[i])
        root.after(260, boot_sequence, lines, i + 1)

boot_sequence(boot_lines)
status_loop()

root.mainloop()
