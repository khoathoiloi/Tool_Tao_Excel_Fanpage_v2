# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from worker import WorkerThread
from core import scan_and_prepare_data

class AppActions:
    @staticmethod
    def toggle_page_input(app):
        if app.radio_txt.isChecked():
            app.txt_widget.show()
            app.manual_edit.hide()
        else:
            app.txt_widget.hide()
            app.manual_edit.show()

    @staticmethod
    def browse_txt_file(app):
        file, _ = QFileDialog.getOpenFileName(app, "Chọn file TXT danh sách Page", "", "Text Files (*.txt);;All Files (*)")
        if file:
            app.txt_path_edit.setText(file)

    @staticmethod
    def browse_kho(app):
        directory = QFileDialog.getExistingDirectory(app, "Chọn Kho Video")
        if directory:
            app.kho_path_edit.setText(directory)

    @staticmethod
    def browse_output(app):
        directory = QFileDialog.getExistingDirectory(app, "Chọn Nơi Lưu Kết Quả")
        if directory:
            app.out_path_edit.setText(directory)

    @staticmethod
    def get_pages_list(app):
        pages = []
        if app.radio_txt.isChecked():
            path_str = app.txt_path_edit.text().strip()
            if path_str and os.path.exists(path_str):
                with open(path_str, "r", encoding="utf-8", errors="ignore") as f:
                    pages = [l.strip() for l in f if l.strip()]
        else:
            text = app.manual_edit.toPlainText()
            pages = [l.strip() for l in text.splitlines() if l.strip()]
        return pages
