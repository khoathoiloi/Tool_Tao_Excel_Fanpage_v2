# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog
from updater import check_for_updates_gui

class UIBuilder:
    @staticmethod
    def build(app):
        style = ttk.Style()
        style.theme_use('clam')
        
        main_frame = ttk.Frame(app.root, padding="12")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Danh sách Fanpage & Định dạng Excel
        group_page = ttk.LabelFrame(main_frame, text=" 1. Danh sách Fanpage & Định dạng Excel ", padding="8")
        group_page.pack(fill=tk.X, pady=(0, 8))

        # Chọn loại file Excel
        f_type = ttk.Frame(group_page)
        f_type.pack(fill=tk.X, pady=(0, 6))
        ttk.Label(f_type, text="Định dạng xuất:", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        app.excel_type_var = tk.StringVar(value="standard")
        r_type_std = ttk.Radiobutton(f_type, text="File Excel Thường (11 cột)", variable=app.excel_type_var, value="standard")
        r_type_tok = ttk.Radiobutton(f_type, text="File Excel Token (12 cột có UID)", variable=app.excel_type_var, value="token")
        r_type_std.pack(side=tk.LEFT, padx=(0, 15))
        r_type_tok.pack(side=tk.LEFT)

        app.input_mode_var = tk.StringVar(value="txt")
        mode_box = ttk.Frame(group_page)
        mode_box.pack(fill=tk.X, pady=(0, 4))
        
        r1 = ttk.Radiobutton(mode_box, text="Nhập từ file TXT", variable=app.input_mode_var, value="txt", command=app.toggle_mode)
        r2 = ttk.Radiobutton(mode_box, text="Nhập trực tiếp (Mỗi dòng 1 Page / UID)", variable=app.input_mode_var, value="manual", command=app.toggle_mode)
        r1.pack(side=tk.LEFT, padx=(0, 15))
        r2.pack(side=tk.LEFT)

        app.frame_txt = ttk.Frame(group_page)
        app.frame_txt.pack(fill=tk.X, pady=2)
        app.entry_txt_path = ttk.Entry(app.frame_txt)
        app.entry_txt_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        btn_txt = ttk.Button(app.frame_txt, text="Chọn File TXT", command=app.browse_txt)
        btn_txt.pack(side=tk.RIGHT)

        app.frame_manual = ttk.Frame(group_page)
        app.text_manual = tk.Text(app.frame_manual, height=4, font=("Segoe UI", 9))
        app.text_manual.pack(fill=tk.X)

        # 2. Kho Video & Quy tắc ghép
        group_setting = ttk.LabelFrame(main_frame, text=" 2. Kho Video & Cấu hình ghép ", padding="8")
        group_setting.pack(fill=tk.X, pady=(0, 8))

        f_kho = ttk.Frame(group_setting)
        f_kho.pack(fill=tk.X, pady=3)
        ttk.Label(f_kho, text="Kho Video:", width=22).pack(side=tk.LEFT)
        app.entry_kho = ttk.Entry(f_kho)
        app.entry_kho.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f_kho, text="Chọn Kho", command=app.browse_kho).pack(side=tk.RIGHT)

        f_ratio = ttk.Frame(group_setting)
        f_ratio.pack(fill=tk.X, pady=3)
        ttk.Label(f_ratio, text="Số Page / 1 Video:", width=22).pack(side=tk.LEFT)
        app.spin_ratio = ttk.Spinbox(f_ratio, from_=1, to=3, width=5)
        app.spin_ratio.set(2)
        app.spin_ratio.pack(side=tk.LEFT, padx=(0, 20))

        # Tùy chọn tránh trùng bài đã lấy & nút reset
        app.chk_avoid_dup_var = tk.BooleanVar(value=True)
        chk_dup = ttk.Checkbutton(f_ratio, text="Ghi nhớ & tránh lấy trùng video đã đăng", variable=app.chk_avoid_dup_var)
        chk_dup.pack(side=tk.LEFT)

        btn_reset_history = ttk.Button(f_ratio, text="🔄 Reset Bộ Nhớ", command=app.reset_history)
        btn_reset_history.pack(side=tk.RIGHT)

        f_domain = ttk.Frame(group_setting)
        f_domain.pack(fill=tk.X, pady=3)
        ttk.Label(f_domain, text="Tên miền ưu tiên (Bình luận):", width=22).pack(side=tk.LEFT)
        app.entry_domain = ttk.Entry(f_domain)
        app.entry_domain.pack(side=tk.LEFT, fill=tk.X, expand=True)

        f_tag = ttk.Frame(group_setting)
        f_tag.pack(fill=tk.X, pady=3)
        ttk.Label(f_tag, text="Hashtag gắn kèm:", width=22).pack(side=tk.LEFT)
        app.entry_tag = ttk.Entry(f_tag)
        app.entry_tag.pack(side=tk.LEFT, fill=tk.X, expand=True)

        f_out = ttk.Frame(group_setting)
        f_out.pack(fill=tk.X, pady=3)
        ttk.Label(f_out, text="Nơi lưu kết quả:", width=22).pack(side=tk.LEFT)
        app.entry_out = ttk.Entry(f_out)
        app.entry_out.insert(0, "D:\\")
        app.entry_out.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(f_out, text="Chọn Nơi Lưu", command=app.browse_out).pack(side=tk.RIGHT)

        # 3. Log
        group_log = ttk.LabelFrame(main_frame, text=" 3. Tiến trình & Nhật ký ", padding="8")
        group_log.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        app.progress = ttk.Progressbar(group_log, orient="horizontal", mode="determinate")
        app.progress.pack(fill=tk.X, pady=(0, 5))

        app.log_text = tk.Text(group_log, height=6, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4")
        app.log_text.pack(fill=tk.BOTH, expand=True)

        # 4. Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        app.btn_check = tk.Button(btn_frame, text="Kiểm Tra Dữ Liệu", font=("Segoe UI", 10), bg="#0288d1", fg="white", relief="flat", padx=15, pady=6, command=app.check_data)
        app.btn_check.pack(side=tk.LEFT, padx=(0, 10))

        app.btn_update = tk.Button(btn_frame, text="⚡ Kiểm Tra Cập Nhật", font=("Segoe UI", 9), bg="#546e7a", fg="white", relief="flat", padx=10, pady=6, command=lambda: check_for_updates_gui(app.root, silent=False))
        app.btn_update.pack(side=tk.LEFT)

        app.btn_start = tk.Button(btn_frame, text="🚀 TẠO FILE EXCEL", font=("Segoe UI", 10, "bold"), bg="#2e7d32", fg="white", relief="flat", padx=20, pady=6, command=app.start_generate)
        app.btn_start.pack(side=tk.RIGHT)
