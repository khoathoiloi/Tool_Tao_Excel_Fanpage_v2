# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QFileDialog, QSpinBox,
    QTextEdit, QRadioButton, QProgressBar, QMessageBox,
    QGroupBox, QFormLayout
)
from worker import WorkerThread
from core import scan_and_prepare_data

class ToolTaoExcelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bộ Công Cụ Tạo Excel Fanpage Reels v2.0")
        self.resize(720, 680)
        self.initUI()
        self.load_config()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)

        # 1. Danh sách Fanpage
        page_group = QGroupBox("1. Danh sách Fanpage Facebook")
        page_layout = QVBoxLayout(page_group)

        btn_box = QHBoxLayout()
        self.radio_txt = QRadioButton("Nhập từ file TXT")
        self.radio_manual = QRadioButton("Nhập trực tiếp")
        self.radio_txt.setChecked(True)
        self.radio_txt.toggled.connect(self.toggle_page_input)

        btn_box.addWidget(self.radio_txt)
        btn_box.addWidget(self.radio_manual)
        btn_box.addStretch()
        page_layout.addLayout(btn_box)

        self.txt_widget = QWidget()
        txt_box = QHBoxLayout(self.txt_widget)
        txt_box.setContentsMargins(0, 0, 0, 0)
        self.txt_path_edit = QLineEdit()
        self.txt_path_edit.setPlaceholderText("Đường dẫn file TXT...")
        self.btn_browse_txt = QPushButton("Chọn File TXT")
        self.btn_browse_txt.clicked.connect(self.browse_txt_file)
        txt_box.addWidget(self.txt_path_edit)
        txt_box.addWidget(self.btn_browse_txt)
        page_layout.addWidget(self.txt_widget)

        self.manual_edit = QTextEdit()
        self.manual_edit.setPlaceholderText("Dán danh sách tên Page vào đây (mỗi dòng một Page)...")
        self.manual_edit.setMaximumHeight(80)
        self.manual_edit.hide()
        page_layout.addWidget(self.manual_edit)
        layout.addWidget(page_group)

        # 2. Cấu hình Kho Video & Quy tắc ghép
        setting_group = QGroupBox("2. Kho Video & Cấu hình ghép")
        form_layout = QFormLayout(setting_group)
        form_layout.setSpacing(8)

        kho_box = QHBoxLayout()
        self.kho_path_edit = QLineEdit()
        self.kho_path_edit.setPlaceholderText("Chọn thư mục kho...")
        self.btn_browse_kho = QPushButton("Chọn Kho")
        self.btn_browse_kho.clicked.connect(self.browse_kho)
        kho_box.addWidget(self.kho_path_edit)
        kho_box.addWidget(self.btn_browse_kho)
        form_layout.addRow("Kho Video:", kho_box)

        self.spin_page_per_video = QSpinBox()
        self.spin_page_per_video.setRange(1, 3)
        self.spin_page_per_video.setValue(2)
        form_layout.addRow("Số Page / 1 Video:", self.spin_page_per_video)

        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText("Ví dụ: danhngon.pro (Để trống sẽ lấy link đầu tiên)")
        form_layout.addRow("Tên miền ưu tiên (Bình luận):", self.domain_edit)

        self.hashtag_edit = QLineEdit()
        self.hashtag_edit.setPlaceholderText("Ví dụ: #news #reels (Để trống sẽ không gắn hashtag)")
        form_layout.addRow("Hashtag gắn kèm:", self.hashtag_edit)

        out_box = QHBoxLayout()
        self.out_path_edit = QLineEdit()
        self.out_path_edit.setText("D:\\")
        self.btn_browse_out = QPushButton("Chọn Nơi Lưu")
        self.btn_browse_out.clicked.connect(self.browse_output)
        out_box.addWidget(self.out_path_edit)
        out_box.addWidget(self.btn_browse_out)
        form_layout.addRow("Nơi lưu kết quả:", out_box)

        layout.addWidget(setting_group)

        # 3. Log
        log_group = QGroupBox("3. Tiến trình xử lý")
        log_layout = QVBoxLayout(log_group)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        log_layout.addWidget(self.progress_bar)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setMaximumHeight(110)
        log_layout.addWidget(self.log_edit)
        layout.addWidget(log_group)

        # 4. Action
        action_box = QHBoxLayout()
        self.btn_check = QPushButton("Kiểm Tra Dữ Liệu")
        self.btn_check.setFixedHeight(38)
        self.btn_check.clicked.connect(self.check_data)

        self.btn_start = QPushButton("🚀 TẠO FILE EXCEL")
        self.btn_start.setFixedHeight(38)
        self.btn_start.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; font-size: 13px;")
        self.btn_start.clicked.connect(self.start_generate)

        action_box.addWidget(self.btn_check)
        action_box.addWidget(self.btn_start)
        layout.addLayout(action_box)
