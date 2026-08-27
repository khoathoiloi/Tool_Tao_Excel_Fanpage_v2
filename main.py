# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from config_mgr import ConfigMgr
from ui_builder import UIBuilder
from app_controller import AppController

class ToolTaoExcelTkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bộ Công Cụ Tạo Excel Fanpage Reels v2.0")
        self.root.geometry("700x680")
        self.root.minsize(640, 600)
        self.cfg_mgr = ConfigMgr()
        
        UIBuilder.build(self)
        self.cfg_mgr.load(self)

    def toggle_mode(self):
        AppController.toggle_mode(self)

    def browse_txt(self):
        AppController.browse_txt(self)

    def browse_kho(self):
        AppController.browse_kho(self)

    def browse_out(self):
        AppController.browse_out(self)

    def reset_history(self):
        AppController.reset_history(self)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def check_data(self):
        AppController.check_data(self)

    def start_generate(self):
        AppController.start_generate(self)

    def on_success(self, result):
        self.progress['value'] = 100
        self.btn_start.config(state=tk.NORMAL)
        self.btn_check.config(state=tk.NORMAL)

        last_f = result.get('last_folder_used')
        last_f_name = Path(last_f).name if last_f else "Không có"

        msg = f"🎉 ĐÃ TẠO FILE EXCEL THÀNH CÔNG!\n\n"
        msg += f"📁 File Excel: {result['excel_path']}\n"
        msg += f"✅ Đã xử lý: {result['total_pages_done']} Page ({result['total_videos_used']} video)\n"
        msg += f"📂 Folder cuối cùng đã lấy: {last_f_name} ({last_f})\n"
        if result['total_pages_left'] > 0:
            msg += f"⚠️ Số Page còn dư: {result['total_pages_left']} (Đã xuất tại: {result['unused_file']})\n"

        self.log("--------------------------------------")
        self.log(msg)
        messagebox.showinfo("Thành Công", msg)

    def on_error(self, err_msg):
        self.btn_start.config(state=tk.NORMAL)
        self.btn_check.config(state=tk.NORMAL)
        self.log(f"❌ {err_msg}")
        messagebox.showerror("Lỗi", err_msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = ToolTaoExcelTkApp(root)
    root.mainloop()


