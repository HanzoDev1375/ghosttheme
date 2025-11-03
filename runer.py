import json
import os
import requests

print("Run....")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "HanzoDev1375"
REPO_NAME = "ghosttheme"
API_URL = (
    f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/main?recursive=1"
)
OUTPUT_FILE = "github_theme.json"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
    "Accept": "application/vnd.github+json",
}


def get_file_size(url):
    """Get file size in bytes from a GitHub raw URL"""
    try:
        response = requests.head(url, headers=HEADERS)
        if response.status_code == 200:
            size = int(response.headers.get("content-length", 0))
            return size
        return 0
    except Exception as e:
        print(f"⚠️ Error getting file size for {url}: {e}")
        return 0


def format_file_size(size_bytes):
    """Format file size in human readable format (KB, MB, etc.)"""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"


def fetch_ghost_themes():
    try:
        print("Fetching repository tree...")
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()

        tree = response.json().get("tree", [])
        themes = []

        ghost_files = [item for item in tree if item["path"].endswith(".ghost")]

        for ghost_file in ghost_files:
            theme_dir = os.path.dirname(ghost_file["path"])
            theme_name = os.path.basename(ghost_file["path"])

            theme_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{ghost_file['path']}"

            # Get theme file size
            theme_size_bytes = get_file_size(theme_url)
            theme_size_formatted = format_file_size(theme_size_bytes)

            theme_data = {
                "theme": theme_url,
                "image": "",
                "background": None,
                "hasbackground": False,
                #     "theme_size": theme_size_bytes,  # سایز فایل تم (بایت)
                "theme_size_formatted": theme_size_formatted,  # سایز فایل تم (فرمت خوانا)
                #    "background_size": 0,  # سایز پس‌زمینه اصلی (بایت)
                "background_size_formatted": "0 B",  # سایز پس‌زمینه اصلی (فرمت خوانا)
            }

            for item in tree:
                path = item.get("path", "")
                if not path.startswith(f"{theme_dir}/"):
                    continue

                filename = os.path.basename(path).lower()

                if filename.endswith((".webp", ".png", ".jpeg", ".jpg", ".mp4")):
                    file_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{path}"

                    if "preview" in filename and not filename.endswith(".mp4"):
                        # این فایل پیش‌نمایش است
                        theme_data["image"] = file_url
                    else:
                        # این فایل پس‌زمینه اصلی است
                        theme_data["background"] = file_url
                        theme_data["hasbackground"] = True
                        # Get background file size

                        bg_size_bytes = get_file_size(file_url)
                        # theme_data["background_size"] = bg_size_bytes
                        theme_data["background_size_formatted"] = format_file_size(
                            bg_size_bytes
                        )

            print(f"✅ Found theme: {theme_name}")
            print(f"   ↳ Theme size: {theme_data['theme_size_formatted']}")
            if theme_data["background"]:
                print(f"   ↳ Background: {theme_data['background_size_formatted']}")
            if theme_data["image"]:
                print(f"   ↳ Preview image: {theme_data['image']}")

            themes.append(theme_data)

        return themes

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching repo tree: {e}")
        return []


def save_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(data)} themes to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving JSON file: {e}")
        return False


if __name__ == "__main__":
    themes = fetch_ghost_themes()
    if themes:
        if save_json(themes, OUTPUT_FILE):
            print("✅ Operation completed successfully!")
        else:
            print("❌ Failed to save JSON file.")
    else:
        print("⚠️ No theme files found or error occurred.")