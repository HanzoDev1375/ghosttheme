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


def fetch_ghost_themes():
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()

        tree = response.json().get("tree", [])
        themes = []

        # یافتن تمام دایرکتوری‌های تم
        theme_dirs = {
            item["path"]
            for item in tree
            if item["type"] == "tree" and "/" not in item["path"]
        }

        for theme_dir in theme_dirs:
            theme_data = {
                "theme": "",
                "image": "",
                "background": None,
                "hasbackground": False,
            }

            # بررسی فایل‌های موجود در هر دایرکتوری تم
            for item in tree:
                path = item.get("path", "")
                if path.startswith(f"{theme_dir}/"):
                    filename = os.path.basename(path)

                    if filename.endswith(".ghost"):
                        theme_data["theme"] = (
                            f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{path}"
                        )
                    elif filename.endswith(
                        (".webp", ".png", ".jpeg", ".jpg", ".mp4")
                    ):  # add video Background
                        if "preview" in filename.lower() or "pre" in filename.lower():
                            theme_data["image"] = (
                                f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{path}"
                            )
                        else:
                            theme_data["background"] = (
                                f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{path}"
                            )
                            theme_data["hasbackground"] = True

            # فقط اگر فایل تم وجود داشت اضافه شود
            if theme_data["theme"]:
                themes.append(theme_data)

        return themes

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repo tree: {e}")
        return []


def save_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} themes to {filename}")
        return True
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False


if __name__ == "__main__":
    themes = fetch_ghost_themes()
    if themes:
        if save_json(themes, OUTPUT_FILE):
            print("Operation completed successfully!")
        else:
            print("Failed to save JSON file.")
    else:
        print("No theme files found or error occurred.")