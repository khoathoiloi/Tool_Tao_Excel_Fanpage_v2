# -*- coding: utf-8 -*-
import os
import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core import scan_and_prepare_data
from excel_writer import export_excel_file
from config_mgr import ConfigMgr

class ToolTaoExcelTkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bộ Công Cụ Tạo Excel Fanpage Reels v2.0")
        self.root.geometry("680x640")
        self.root.minsize(620, 580)
        self.cfg_mgr = ConfigMgr()
        
        self.build_ui()
        self.cfg_mgr.load(self)
