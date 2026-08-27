# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal
from core import scan_and_prepare_data
from excel_writer import export_excel_file

class WorkerThread(QThread):
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        try:
            pages = self.config['pages']
            kho_path = self.config['kho_path']
            pages_per_video = self.config['pages_per_video']
            domain_filter = self.config['domain_filter']
            hashtag = self.config['hashtag']
            output_dir = self.config['output_dir']

            if not pages:
                self.error.emit("Danh sách Page trống!")
                return

            self.progress.emit(0, 0, "Đang quét danh sách thư mục video...")
            valid_items = scan_and_prepare_data(kho_path, domain_filter, hashtag)

            if not valid_items:
                self.error.emit("Không tìm thấy folder hoặc video MP4 hợp lệ trong kho!")
                return

            self.progress.emit(0, len(pages), f"Tìm thấy {len(valid_items)} video. Đang tạo file Excel...")

            def update_progress(curr, total, msg):
                self.progress.emit(curr, total, msg)

            result = export_excel_file(
                valid_items=valid_items,
                pages=pages,
                pages_per_video=pages_per_video,
                kho_path_str=kho_path,
                output_dir_str=output_dir,
                progress_cb=update_progress
            )

            self.finished.emit(result)

        except Exception as e:
            self.error.emit(f"Lỗi: {str(e)}")
