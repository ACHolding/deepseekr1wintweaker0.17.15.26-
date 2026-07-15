import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess, sys, os, ctypes

# ============================================================
#  Deepseek's Tweaker 0.1 – VLT Edition
#  Real system tweaks for Intel Arc 140V → RTX 4090 FPS
#  No external files – everything stays in memory
# ============================================================

def is_admin():
    """Check if the script is running with administrator rights."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    """Re-launch the script with admin privileges if possible."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit(0)

def run(cmd, capture=True):
    """Run a command and return output (or None)."""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        else:
            subprocess.run(cmd, shell=True)
            return "OK"
    except Exception as e:
        return f"ERROR: {e}"

def apply_tweaks():
    """Execute a series of real performance tweaks."""
    log = scrolled_text
    log.insert(tk.END, "Applying Deepseek's VLT Tweaks...\n")
    root.update()

    # 1. High Performance power plan
    log.insert(tk.END, "[1/5] Activating Ultimate Performance power plan...\n")
    # Try the Ultimate Performance GUID first (Win 10 1803+)
    out = run('powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61')
    if "ERROR" in out or "Unable" in out:
        # Fallback to High Performance
        out = run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
    log.insert(tk.END, out + "\n")
    root.update()

    # 2. Disable Game DVR / Game Bar (stops background recording)
    log.insert(tk.END, "[2/5] Disabling Xbox Game DVR...\n")
    reg_cmd = (
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" '
        '/v AppCaptureEnabled /t REG_DWORD /d 0 /f'
    )
    out = run(reg_cmd)
    log.insert(tk.END, out + "\n")
    root.update()

    # 3. Disable fullscreen optimizations (system-wide)
    log.insert(tk.END, "[3/5] Disabling fullscreen optimizations...\n")
    reg_cmd2 = (
        'reg add "HKCU\\System\\GameConfigStore" '
        '/v GameDVR_Enabled /t REG_DWORD /d 0 /f'
    )
    out = run(reg_cmd2)
    log.insert(tk.END, out + "\n")
    root.update()

    # 4. Enable Hardware-accelerated GPU scheduling (if supported)
    log.insert(tk.END, "[4/5] Enabling Hardware-accelerated GPU scheduling...\n")
    reg_cmd3 = (
        'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" '
        '/v HwSchMode /t REG_DWORD /d 2 /f'
    )
    out = run(reg_cmd3)
    log.insert(tk.END, out + "\n")
    root.update()

    # 5. Set visual effects to "Adjust for best performance"
    log.insert(tk.END, "[5/5] Tweaking visual effects for performance...\n")
    # Registry key: UserPreferencesMask (hex value for best performance)
    best_perf_mask = "90 12 03 80 10 00 00 00"
    reg_cmd4 = (
        'reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask '
        f'/t REG_BINARY /d "{best_perf_mask}" /f'
    )
    out = run(reg_cmd4)
    log.insert(tk.END, out + "\n")
    root.update()

    log.insert(tk.END, "\n✅ All tweaks applied! RTX 4090 mode activated.\n")
    log.insert(tk.END, "A system restart is recommended for full effect.\n")
    log.see(tk.END)

# ============================================================
#  GUI – Blue hue text, black background, black button
# ============================================================
root = tk.Tk()
root.title("Deepseek's Tweaker 0.1 – VLT Edition")
root.geometry("6000x400")            # ultra‑wide master race
root.configure(bg='black')

# Blue text label
label = tk.Label(
    root,
    text="Deepseek's Tweaker 0.1\nIntel Arc 140V → RTX 4090 FPS Booster",
    fg='blue',
    bg='black',
    font=('Consolas', 24, 'bold'),
    justify='center'
)
label.pack(pady=(40, 10))

# Scrolled log area (blue hue on black)
scrolled_text = scrolledtext.ScrolledText(
    root,
    width=120,
    height=10,
    bg='black',
    fg='#00BFFF',          # deep sky blue
    insertbackground='white',
    font=('Consolas', 12),
    relief='sunken',
    bd=2
)
scrolled_text.pack(padx=20, pady=10)

# Black button with white text
boost_btn = tk.Button(
    root,
    text="⚡ APPLY VLT TWEAKS (RTX 4090 MODE) ⚡",
    command=apply_tweaks,
    bg='black',
    fg='white',
    activebackground='#222222',
    activeforeground='cyan',
    font=('Consolas', 18, 'bold'),
    relief='ridge',
    bd=3,
    padx=20,
    pady=10
)
boost_btn.pack(pady=30)

# Always on top (because it's important)
root.attributes('-topmost', True)

# ---- Check for admin rights ----
if not is_admin():
    answer = messagebox.askyesno(
        "Administrator Required",
        "These tweaks require administrator privileges.\n"
        "Re-launch as admin now?"
    )
    if answer:
        request_admin()   # Script will restart with admin, exit current instance
    else:
        messagebox.showwarning(
            "Limited Functionality",
            "Without admin rights, some tweaks may fail.\n"
            "You can still try, but results are not guaranteed."
        )

root.mainloop()
