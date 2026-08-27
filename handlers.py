# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
from worker import WorkerThread
from core import scan_and_prepare_data

class AppHandlers:
    @staticmethod
    def check_data(app):
        pages = app.get_pages_list()
        kho_path = app.kho_path_edit.text().strip()
        pages_per_video = app.spin_page_per_video.value()

        app.log_edit.clear()
        app.log_edit.append(f"📌 Tổng số Fanpage: {len(pages)}")

        if not kho_path or not os.path.isdir(kho_path):
            app.log_edit.append("❌ Kho video chưa hợp lệ!")
            return

        valid_items = scan_and_prepare_data(kho_path, app.domain_edit.text(), app.hashtag_edit.text())
        valid_count = len(valid_items)

        app.log_edit.append(f"📌 Tổng số folder video hợp lệ: {valid_count}")
        pages_capacity = valid_count * pages_per_video
        app.log_edit.append(f"📌 Với tỷ lệ {pages_per_video} Page/video, phục vụ tối đa: {pages_capacity} Page.")

        if len(pages) > pages_capacity:
            diff = len(pages) - pages_capacity
            app.log_edit.append(f"⚠️ Cảnh báo: Thiếu {diff} slot video. Số Page dư sẽ xuất vào file page-chua-dang.txt.")
        else:
            app.log_edit.append("✅ Dữ liệu hoàn toàn đầy đủ và sẵn sàng!")

    @staticmethod
    def start_generate(app):
        pages = app.get_pages_list()
        if not pages:
            QMessageBox.warning(app, "Lỗi", "Vui lòng nhập danh sách Page!")
            return

        kho_path = app.kho_path_edit.text().strip()
        if not kho_path or not os.path.isdir(kho_path):
            QMessageBox.warning(app, "Lỗi", "Vui lòng chọn Kho Video hợp lệ!")
            return

        out_path = app.out_path_edit.text().strip() or "D:\\"
        app.save_config()

        config = {
            'pages': pages,
            'kho_path': kho_path,
            'pages_per_video': app.spin_page_per_video.value(),
            'domain_filter': app.domain_edit.text().strip(),
            'hashtag': app.hashtag_edit.text().strip(),
            'output_dir': out_path
        }

        app.btn_start.setEnabled(False)
        app.btn_check.setEnabled(False)
        app.log_edit.clear()

        app.worker = WorkerThread(config)
        app.worker.progress.connect(app.on_progress)
        app.worker.finished.connect(app.on_finished)
        app.worker.error.connect(app.on_error)
        app.worker.start()
