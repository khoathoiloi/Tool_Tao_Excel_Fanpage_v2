# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

def _extract_links_and_title_from_file(file_path: Path):
    """Trích xuất candidate_links và title từ một file text bất kỳ"""
    candidate_links = []
    title = ""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        for line in lines:
            lower_line = line.lower()
            if lower_line.startswith("link đã đăng:") or lower_line.startswith("link:"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    candidate_links.append(parts[1].strip())
            elif lower_line.startswith("tiêu đề đã đăng:") or lower_line.startswith("tiêu đề:"):
                parts = line.split(":", 1)
                if len(parts) > 1 and not title:
                    title = parts[1].strip()
            elif lower_line.startswith("tiêu đề link youtube:"):
                parts = line.split(":", 1)
                if len(parts) > 1 and not title:
                    title = parts[1].strip()
            else:
                urls = re.findall(r'https?://[^\s]+', line)
                for u in urls:
                    candidate_links.append(u.strip())
    except Exception:
        pass
    return candidate_links, title

def _process_single_folder(folder: Path, domain_filter: str = "", hashtag: str = ""):
    """Xử lý 1 folder chứa video và file link-da-dang.txt hoặc các file chứa link khác"""
    mp4_files = [
        f for f in folder.glob("*.mp4")
        if f.name.lower() != "video-9x16.mp4"
    ]
    if not mp4_files:
        return None

    txt_file = folder / "link-da-dang.txt"
    video_file = mp4_files[0]
    first_comment = ""
    title = ""
    raw_link = ""

    candidate_links = []
    # 1. Đọc thử file link-da-dang.txt trước
    if txt_file.exists():
        candidate_links, extracted_title = _extract_links_and_title_from_file(txt_file)
        if extracted_title:
            title = extracted_title

        if candidate_links:
            if domain_filter:
                matched = [l for l in candidate_links if domain_filter in l.lower()]
                if matched:
                    raw_link = matched[0]
            else:
                raw_link = candidate_links[0]

    # 2. Nếu domain_filter được chỉ định và link-da-dang.txt không có link khớp:
    # -> Quét lại toàn bộ các file khác trong folder để tìm file chứa link có domain_filter
    if domain_filter and not raw_link:
        ignore_exts = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.srt', '.png', '.jpg', '.jpeg', '.gif', '.rar', '.zip', '.tmp'}
        other_files = [
            f for f in folder.iterdir()
            if f.is_file() and f != txt_file and f.suffix.lower() not in ignore_exts
        ]
        
        for other_file in other_files:
            file_links, file_title = _extract_links_and_title_from_file(other_file)
            if file_title and not title:
                title = file_title
            
            matched = [l for l in file_links if domain_filter in l.lower()]
            if matched:
                raw_link = matched[0]
                break

    # 3. Nếu vẫn không tìm thấy link theo domain_filter, fallback về link đầu tiên của link-da-dang.txt (nếu có)
    if not raw_link and candidate_links:
        raw_link = candidate_links[0]

    if raw_link:
        first_comment = f"watch full here 👉: {raw_link}"

    if not title:
        title = video_file.stem
        if "-" in title and " " not in title:
            title = title.replace("-", " ").title()

    caption = title
    if hashtag:
        tags = []
        for t in re.split(r'[,; ]+', hashtag):
            t = t.strip()
            if not t:
                continue
            if not t.startswith("#"):
                t = "#" + t
            tags.append(t)
        if tags:
            caption = f"{title} {' '.join(tags)}"

    return {
        'folder': folder.name,
        'folder_path': str(folder.resolve()),
        'video_path': str(video_file.resolve()),
        'title': title,
        'caption': caption,
        'first_comment': first_comment
    }

def scan_and_prepare_data(kho_path_str, domain_filter="", hashtag="", exclude_folders=None):
    kho_path = Path(kho_path_str)
    if not kho_path.exists() or not kho_path.is_dir():
        return []

    domain_filter = domain_filter.strip().lower()
    hashtag = hashtag.strip()
    exclude_set = {str(Path(p).resolve()) for p in exclude_folders} if exclude_folders else set()

    valid_items = []
    
    # 1. Kiểm tra xem chính thư mục được chọn có chứa video trực tiếp hay không
    item_self = _process_single_folder(kho_path, domain_filter, hashtag)
    if item_self:
        if item_self['folder_path'] not in exclude_set:
            valid_items.append(item_self)

    # 2. Quét các thư mục con bên trong (nếu chọn folder cha chứa nhiều bài/folder con)
    subfolders = sorted([f for f in kho_path.iterdir() if f.is_dir()])
    for folder in subfolders:
        if str(folder.resolve()) in exclude_set:
            continue
        item = _process_single_folder(folder, domain_filter, hashtag)
        if item and item['folder_path'] not in exclude_set:
            valid_items.append(item)

    return valid_items
