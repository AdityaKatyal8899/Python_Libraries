import yt_dlp

def readable_size(size_bytes):
    if not size_bytes:
        return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def is_reasonable(filesize, height):
    """Filter out suspiciously small or oversized formats based on resolution."""
    if not filesize or not height:
        return False

    # Expected min file size (per 60s video) — can tweak as needed
    expected_min = {
        144: 0.5,    # MB
        240: 1,
        360: 2,
        480: 3,
        720: 5,
        1080: 8,
        1440: 12,
        2160: 20
    }

    # Match nearest resolution threshold
    base_size_mb = max([v for k, v in expected_min.items() if height >= k], default=2)
    return filesize >= base_size_mb * 1024 * 1024  # convert MB to bytes


def sort_and_print_formats(formats):
    allowed_video_audio = []
    blocked_video_audio = []
    video_only_all = {}
    audio_only_all = []

    for f in formats:
        fmt_id = f.get("format_id")
        vcodec = f.get("vcodec")
        acodec = f.get("acodec")
        width = f.get("width") or 0
        height = f.get("height") or 0
        filesize = f.get("filesize") or f.get("filesize_approx")
        ext = f.get("ext", "unknown")
        format_note = f.get("format_note", "").lower()

        if not fmt_id or not filesize:
            continue

        info = {
            "id": fmt_id,
            "ext": ext,
            "res": f"{width}x{height}" if width and height else format_note,
            "height": height,
            "width": width,
            "filesize": filesize,
            "size_str": readable_size(filesize),
            "format_note": format_note
        }

        # Video+Audio handling
        if vcodec != "none" and acodec != "none":
            if height == 360 and filesize >= 10 * 1024 * 1024:
                allowed_video_audio.append(info)
            else:
                # Doesn't meet criteria, but show it as blocked
                blocked_video_audio.append(info)

        # Video-only
        elif vcodec != "none" and acodec == "none":
            if filesize < 2.5 * 1024 * 1024:
                continue  # skip small video-only formats

            resolution_key = f"{width}x{height}"
            if resolution_key in ["426x240", "640x360", "854x480"]:
                prev = video_only_all.get(resolution_key)
                if not prev or filesize > prev["filesize"]:
                    video_only_all[resolution_key] = info
            else:
                video_only_all[fmt_id] = info

        # Audio-only
        elif acodec != "none" and vcodec == "none":
            if "low" in format_note or "tiny" in format_note:
                continue
            audio_only_all.append(info)

    video_only = list(video_only_all.values())

    allowed_video_audio.sort(key=lambda x: x["height"], reverse=True)
    blocked_video_audio.sort(key=lambda x: x["height"], reverse=True)
    video_only.sort(key=lambda x: x["height"], reverse=True)
    audio_only_all.sort(key=lambda x: x["filesize"], reverse=True)

    def printer(title, lst, blocked=False):
        status = " (Not downloadable)" if blocked else ""
        print(f"\n🔹 {title}{status} ({len(lst)} formats):")
        for f in lst:
            print(f"[{f['id']}] {f['res']} - {f['ext']} - {f['size_str']}")

    printer("Video + Audio (Allowed)", allowed_video_audio)
    printer("Video + Audio (Blocked)", blocked_video_audio, blocked=True)
    printer("Video Only", video_only)
    printer("Audio Only", audio_only_all)

    # Valid IDs exclude blocked video+audio formats
    valid_ids = [f["id"] for f in allowed_video_audio + video_only + audio_only_all]
    return valid_ids



def downloader(link):
    # Use cookies for info extraction
    info_opts = {'cookiefile': 'youtube_cookies.txt'}
    try:
        with yt_dlp.YoutubeDL(info_opts) as ydl_info:
            vid_info = ydl_info.extract_info(link, download=False)
    except Exception as e:
        print("❌ Error during info extraction:", e)
        return

    fvalid_ids = sort_and_print_formats(vid_info.get("formats", []))

    choice = input("\nEnter format ID(s) (comma-separated): ").strip()

    selected_ids = [x.strip() for x in choice.split(',') if x.strip()]
    invalid_ids = [x for x in selected_ids if x not in fvalid_ids]

    if invalid_ids:
        print(f"❌ Invalid format IDs: {', '.join(invalid_ids)}")
        return
    for fmt in selected_ids:
        print(f"\n⬇️ Downloading format [{fmt}]...")
        ydl_opts = {
            'format': fmt,
            'outtmpl': f'%(title)s_{fmt}.%(ext)s',
            'merge_output_format': 'mp4',
            'cookiefile': 'youtube_cookies.txt'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except Exception as e:
            print(f"❌ Error downloading format {fmt}:", e)


if __name__ == "__main__":
    while True:
        link = input("🔗 Enter YouTube URL: ").strip()
        if not link:
            continue
        confirm = input("✅ Is this the correct link? (y/n): ").lower()
        if confirm == 'y':
            downloader(link)
        else:
            print("🔁 Please re-enter the correct link.\n")
