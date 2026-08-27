# -*- coding: utf-8 -*-
import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from core import scan_and_prepare_data
from excel_writer import export_excel_file

class AppController:
    @staticmethod
    def toggle_mode(app):
        if app.input_mode_var.get() == "txt":
            app.frame_manual.pack_forget()
            app.frame_txt.pack(fill=tk.X, pady=2)
        else:
            app.frame_txt.pack_forget()
            app.frame_manual.pack(fill=tk.X, pady=2)

    @staticmethod
    def browse_txt(app):
        f = filedialog.askopenfilename(title="Chọn file TXT danh sách Page", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if f:
            app.entry_txt_path.delete(0, tk.END)
            app.entry_txt_path.insert(0, f)

    @staticmethod
    def browse_kho(app):
        d = filedialog.askdirectory(title="Chọn Kho Video")
        if d:
            app.entry_kho.delete(0, tk.END)
            app.entry_kho.insert(0, d)

    @staticmethod
    def browse_out(app):
        d = filedialog.askdirectory(title="Chọn Nơi Lưu Kết Quả")
        if d:
            app.entry_out.delete(0, tk.END)
            app.entry_out.insert(0, d)

    @staticmethod
    def get_pages(app):
        mode = getattr(app, 'excel_type_var', None)
        excel_type = mode.get() if mode else "standard"

        raw_lines = []
        if app.input_mode_var.get() == "txt":
            p = app.entry_txt_path.get().strip()
            if p and os.path.exists(p):
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    raw_lines = [l.strip() for l in f if l.strip()]
        else:
            txt = app.text_manual.get("1.0", tk.END)
            raw_lines = [l.strip() for l in txt.splitlines() if l.strip()]

        if excel_type == "token":
            parsed = []
            for idx, line in enumerate(raw_lines):
                # Tách nếu có ký tự phân cách |, \t, hoặc ,
                if "|" in line:
                    parts = [pt.strip() for pt in line.split("|", 1)]
                    p_name, uid = parts[0], parts[1]
                elif "\t" in line:
                    parts = [pt.strip() for pt in line.split("\t", 1)]
                    p_name, uid = parts[0], parts[1]
                elif "," in line:
                    parts = [pt.strip() for pt in line.split(",", 1)]
                    p_name, uid = parts[0], parts[1]
                else:
                    # Người dùng chỉ nhập mỗi UID
                    uid = line.strip()
                    # Tự động gán ký tự đại diện cho Trang (a, b, c, ... hoặc p1, p2)
                    p_name = chr(ord('a') + (idx % 26)) if len(raw_lines) <= 26 else f"p{idx+1}"

                # Nếu bị đảo vị trí (UID đứng trước dạng số, tên đứng sau)
                if uid and not uid.isdigit() and p_name.isdigit():
                    p_name, uid = uid, p_name

                parsed.append({
                    'raw': line,
                    'page_name': p_name,
                    'uid': uid
                })
            return parsed
        else:
            return raw_lines

    @staticmethod
    def check_data(app):
        pages = AppController.get_pages(app)
        kho = app.entry_kho.get().strip()
        mode = getattr(app, 'excel_type_var', None)
        excel_type = mode.get() if mode else "standard"
        type_label = "File Excel Token (12 cột có UID)" if excel_type == "token" else "File Excel Thường (11 cột)"

        try:
            ratio = int(app.spin_ratio.get())
        except ValueError:
            ratio = 2

        app.log_text.delete("1.0", tk.END)
        app.log(f"📋 Định dạng đang chọn: {type_label}")
        app.log(f"📌 Tổng số Fanpage / UID: {len(pages)}")

        if not kho or not os.path.isdir(kho):
            app.log("❌ Kho video chưa hợp lệ!")
            return

        exclude_folders = app.cfg_mgr.get_processed_folders() if app.chk_avoid_dup_var.get() else set()
        valid_items = scan_and_prepare_data(
            kho, 
            app.entry_domain.get().strip(), 
            app.entry_tag.get().strip(),
            exclude_folders=exclude_folders
        )
        valid_count = len(valid_items)

        if app.chk_avoid_dup_var.get():
            all_items = scan_and_prepare_data(kho, app.entry_domain.get().strip(), app.entry_tag.get().strip())
            skipped = len(all_items) - valid_count
            app.log(f"📌 Tổng số folder video khả dụng: {valid_count} (Đã bỏ qua {skipped} folder đã dùng)")
            if exclude_folders:
                # Tìm folder cuối cùng đã dùng thuộc kho này
                kho_res = str(Path(kho).resolve())
                matched_used = [f for f in exclude_folders if f == kho_res or f.startswith(kho_res + "\\") or f.startswith(kho_res + "/")]
                if matched_used:
                    last_used_item = sorted(matched_used)[-1]
                    app.log(f"📂 Folder đã lấy gần nhất: {Path(last_used_item).name} ({last_used_item})")
        else:
            app.log(f"📌 Tổng số folder video hợp lệ: {valid_count}")


        cap = valid_count * ratio
        app.log(f"📌 Với tỷ lệ {ratio} Page/video, phục vụ tối đa: {cap} Page.")

        if len(pages) > cap:
            app.log(f"⚠️ Thiếu {len(pages) - cap} slot video. Số Page dư sẽ xuất ra file page-chua-dang.txt.")
        else:
            app.log("✅ Dữ liệu hoàn toàn đầy đủ và sẵn sàng!")

    @staticmethod
    def reset_history(app):
        kho = app.entry_kho.get().strip()
        msg = "Bạn có chắc chắn muốn reset bộ nhớ các folder đã lấy?\n\n"
        if kho and os.path.isdir(kho):
            msg += f"- Bấm [Yes] để reset cho riêng kho: {kho}\n- Bấm [No] để reset toàn bộ tất cả các kho"
            choice = messagebox.askyesnocancel("Reset bộ nhớ folder", msg)
            if choice is True:
                app.cfg_mgr.reset_history(target_folder=kho)
                app.log(f"🔄 Đã xóa bộ nhớ cho kho: {kho}")
                messagebox.showinfo("Thông báo", f"Đã reset bộ nhớ cho kho:\n{kho}")
            elif choice is False:
                app.cfg_mgr.reset_history()
                app.log("🔄 Đã xóa toàn bộ lịch sử bộ nhớ các kho!")
                messagebox.showinfo("Thông báo", "Đã reset toàn bộ bộ nhớ folder!")
        else:
            if messagebox.askyesno("Reset bộ nhớ", "Bạn có chắc chắn muốn xóa toàn bộ danh sách folder đã từng lấy không?"):
                app.cfg_mgr.reset_history()
                app.log("🔄 Đã xóa toàn bộ lịch sử bộ nhớ các kho!")
                messagebox.showinfo("Thông báo", "Đã reset toàn bộ bộ nhớ folder!")


    @staticmethod
    def start_generate(app):
        pages = AppController.get_pages(app)
        if not pages:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập hoặc chọn file TXT danh sách Page / UID!")
            return

        kho = app.entry_kho.get().strip()
        if not kho or not os.path.isdir(kho):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn Kho Video hợp lệ!")
            return

        try:
            ratio = int(app.spin_ratio.get())
        except ValueError:
            ratio = 2

        domain = app.entry_domain.get().strip()
        tag = app.entry_tag.get().strip()
        out = app.entry_out.get().strip() or "D:\\"
        avoid_dup = app.chk_avoid_dup_var.get()
        excel_type = app.excel_type_var.get()

        app.cfg_mgr.save(app)

        app.btn_start.config(state=tk.DISABLED)
        app.btn_check.config(state=tk.DISABLED)
        app.log_text.delete("1.0", tk.END)
        app.progress['value'] = 0

        def run_thread():
            try:
                app.log("Đang quét danh sách video trong kho...")
                exclude_folders = app.cfg_mgr.get_processed_folders() if avoid_dup else set()
                valid_items = scan_and_prepare_data(kho, domain, tag, exclude_folders=exclude_folders)
                if not valid_items:
                    app.root.after(0, lambda: app.on_error("Không tìm thấy folder hoặc video MP4 khả dụng nào trong kho (Có thể tất cả đã được lấy)!"))
                    return

                def update_prog(curr, total, msg):
                    if total > 0:
                        pct = int((curr / total) * 100)
                        app.root.after(0, lambda: app.progress.config(value=pct))
                    app.root.after(0, lambda: app.log(msg))

                result = export_excel_file(
                    valid_items=valid_items,
                    pages=pages,
                    pages_per_video=ratio,
                    kho_path_str=kho,
                    output_dir_str=out,
                    progress_cb=update_prog,
                    excel_type=excel_type
                )

                if avoid_dup and result.get('used_folders'):
                    app.cfg_mgr.add_processed_folders(result['used_folders'])

                app.root.after(0, lambda: app.on_success(result))
            except Exception as e:
                app.root.after(0, lambda: app.on_error(str(e)))

        threading.Thread(target=run_thread, daemon=True).start()
