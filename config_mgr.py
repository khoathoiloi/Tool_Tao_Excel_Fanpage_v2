# -*- coding: utf-8 -*-
import json
from pathlib import Path
import tkinter as tk

class ConfigMgr:
    def __init__(self):
        self.cfg_dir = Path.home() / ".config_tool_excel"
        self.cfg_dir.mkdir(exist_ok=True)
        self.cfg_file = self.cfg_dir / "config_v2.json"
        self.history_file = self.cfg_dir / "processed_folders.json"

    def save(self, app):
        try:
            data = {
                'kho': app.entry_kho.get().strip(),
                'out': app.entry_out.get().strip(),
                'domain': app.entry_domain.get().strip(),
                'tag': app.entry_tag.get().strip(),
                'ratio': app.spin_ratio.get(),
                'txt': app.entry_txt_path.get().strip(),
                'excel_type': app.excel_type_var.get()
            }
            self.cfg_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def load(self, app):
        if self.cfg_file.exists():
            try:
                data = json.loads(self.cfg_file.read_text(encoding="utf-8"))
                app.entry_kho.insert(0, data.get('kho', ''))
                if data.get('out'):
                    app.entry_out.delete(0, tk.END)
                    app.entry_out.insert(0, data.get('out', 'D:\\'))
                app.entry_domain.insert(0, data.get('domain', ''))
                app.entry_tag.insert(0, data.get('tag', ''))
                app.spin_ratio.set(data.get('ratio', '2'))
                app.entry_txt_path.insert(0, data.get('txt', ''))
                if hasattr(app, 'excel_type_var'):
                    app.excel_type_var.set(data.get('excel_type', 'standard'))
            except Exception:
                pass

    def get_processed_folders(self):
        """Lấy danh sách đường dẫn folder video đã từng được lấy/xuất Excel"""
        if self.history_file.exists():
            try:
                return set(json.loads(self.history_file.read_text(encoding="utf-8")))
            except Exception:
                return set()
        return set()

    def add_processed_folders(self, folder_paths):
        """Lưu thêm các folder đã xử lý vào bộ nhớ"""
        try:
            processed = self.get_processed_folders()
            for p in folder_paths:
                processed.add(str(Path(p).resolve()))
            self.history_file.write_text(json.dumps(list(processed), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def reset_history(self, target_folder=None):
        """Xóa toàn bộ lịch sử hoặc xóa lịch sử của 1 folder cụ thể"""
        try:
            if not target_folder:
                if self.history_file.exists():
                    self.history_file.unlink()
                return True
            else:
                target_str = str(Path(target_folder).resolve())
                processed = self.get_processed_folders()
                # Xóa folder đó hoặc các folder con thuộc target_folder
                new_processed = {p for p in processed if not (p == target_str or p.startswith(target_str + "\\") or p.startswith(target_str + "/"))}
                self.history_file.write_text(json.dumps(list(new_processed), ensure_ascii=False, indent=2), encoding="utf-8")
                return True
        except Exception:
            return False

