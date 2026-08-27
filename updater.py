# -*- coding: utf-8 -*-
import os
import sys
import json
import urllib.request
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

CURRENT_VERSION = "2.0.1"
GITHUB_REPO = "khoathoiloi/Tool_Tao_Excel_Fanpage_v2"

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    CURRENT_EXE = sys.executable
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    CURRENT_EXE = None

def is_newer_version(latest, current):
    try:
        l_parts = [int(p) for p in latest.split('.')]
        c_parts = [int(p) for p in current.split('.')]
        return l_parts > c_parts
    except Exception:
        return latest != current

def check_for_updates_gui(root, silent=True):
    """Kiểm tra bản cập nhật mới trong luồng riêng để không chặn giao diện"""
    def _worker():
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={"User-Agent": "Tool-Fanpage-App"})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    body = data.get("body", "Cải tiến hiệu năng và sửa lỗi.")
                    
                    download_url = None
                    for asset in data.get("assets", []):
                        if asset.get("name", "").endswith(".exe"):
                            download_url = asset.get("browser_download_url")
                            break

                    if latest_tag and is_newer_version(latest_tag, CURRENT_VERSION) and download_url:
                        root.after(0, lambda: _prompt_update(root, latest_tag, body, download_url))
                    else:
                        if not silent:
                            root.after(0, lambda: messagebox.showinfo(
                                "Kiểm Tra Cập Nhật",
                                f"Bạn đang sử dụng phiên bản mới nhất (v{CURRENT_VERSION})! 🎉"
                            ))
        except Exception as e:
            if not silent:
                root.after(0, lambda: messagebox.showwarning(
                    "Cập Nhật",
                    f"Không thể kết nối đến máy chủ cập nhật: {e}"
                ))

    threading.Thread(target=_worker, daemon=True).start()

def _prompt_update(root, latest_tag, body, download_url):
    msg = f"🎉 ĐÃ CÓ BẢN CẬP NHẬT MỚI: v{latest_tag}\n(Phiên bản hiện tại: v{CURRENT_VERSION})\n\n"
    msg += f"📝 Nội dung cập nhật:\n{body}\n\n"
    msg += "👉 Bạn có muốn tự động tải về và nâng cấp ngay bây giờ không?"
    
    if messagebox.askyesno("Phát Hiện Bản Cập Nhật Mới", msg, parent=root):
        _start_download_dialog(root, latest_tag, download_url)

def _start_download_dialog(root, new_version, download_url):
    if not CURRENT_EXE:
        messagebox.showinfo("Cập Nhật", f"Bạn đang chạy từ mã nguồn Python. Vui lòng tải file tại:\n{download_url}", parent=root)
        return

    win = tk.Toplevel(root)
    win.title("Đang Cập Nhật Ứng Dụng")
    win.geometry("400x140")
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    lbl_status = ttk.Label(win, text=f"Đang tải bản cập nhật v{new_version}...", font=("Segoe UI", 10))
    lbl_status.pack(pady=(15, 8))

    prog = ttk.Progressbar(win, orient="horizontal", mode="determinate", length=340)
    prog.pack(pady=5)

    lbl_detail = ttk.Label(win, text="Chuẩn bị tải...", font=("Segoe UI", 9), foreground="#666")
    lbl_detail.pack(pady=(2, 10))

    new_exe_path = CURRENT_EXE + ".new"

    def _download_thread():
        def reporthook(blocknum, blocksize, totalsize):
            read = blocknum * blocksize
            if totalsize > 0:
                pct = min(100, int(read * 100 / totalsize))
                mb_read = read / (1024 * 1024)
                mb_total = totalsize / (1024 * 1024)
                win.after(0, lambda: prog.config(value=pct))
                win.after(0, lambda: lbl_detail.config(text=f"{pct}% ({mb_read:.1f}MB / {mb_total:.1f}MB)"))

        try:
            urllib.request.urlretrieve(download_url, new_exe_path, reporthook)
            win.after(0, lambda: lbl_status.config(text="✅ Tải thành công! Đang khởi động lại..."))
            
            bat_script = f"""@echo off
timeout /t 2 /nobreak > nul
move /y "{new_exe_path}" "{CURRENT_EXE}"
start "" "{CURRENT_EXE}"
del "%~f0"
"""
            updater_bat = os.path.join(APP_DIR, "updater.bat")
            with open(updater_bat, "w", encoding="utf-8") as f:
                f.write(bat_script)
                
            subprocess.Popen(["cmd.exe", "/c", updater_bat], close_fds=True)
            root.after(1000, sys.exit)
        except Exception as e:
            win.after(0, lambda: messagebox.showerror("Lỗi Cập Nhật", f"Không thể tải bản cập nhật: {e}", parent=win))
            win.after(0, win.destroy)
            if os.path.exists(new_exe_path):
                try: os.remove(new_exe_path)
                except: pass

    threading.Thread(target=_download_thread, daemon=True).start()
