import json
import os
from datetime import date
from pathlib import Path

BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "Anime0t4ku/companion-themes")
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPOSITORY}/{BRANCH}"

ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "index.json"
DATES_FILE = ROOT / "theme_dates.json"

THEME_FOLDERS = [
    ("official-themes", "official"),
    ("community-themes", "community"),
]

PREVIEW_EXTENSIONS = [".png", ".jpg", ".jpeg"]


def read_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path, data):
    with path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def find_preview(folder, theme_id, json_stem):
    candidates = []

    for name in (theme_id, json_stem):
        if name:
            for extension in PREVIEW_EXTENSIONS:
                candidates.append(folder / f"{name}{extension}")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def validate_theme(theme_path, data):
    required_fields = ["id", "name", "author", "background", "surface", "accent", "text"]
    missing = [field for field in required_fields if not str(data.get(field, "")).strip()]

    if missing:
        raise ValueError(f"{theme_path} is missing required field(s): {', '.join(missing)}")

    theme_id = str(data["id"]).strip()

    if "/" in theme_id or "\\" in theme_id:
        raise ValueError(f"{theme_path} has an invalid id: {theme_id}")

    return theme_id


def build_index():
    themes = []
    theme_dates = read_json(DATES_FILE, default={})
    today = date.today().isoformat()
    changed_dates = False
    seen_theme_ids = set()

    for folder_name, category in THEME_FOLDERS:
        folder = ROOT / folder_name

        if not folder.exists():
            continue

        for theme_path in sorted(folder.glob("*.json")):
            data = read_json(theme_path)
            theme_id = validate_theme(theme_path, data)
            seen_theme_ids.add(theme_id)

            if theme_id not in theme_dates:
                theme_dates[theme_id] = today
                changed_dates = True

            preview_path = find_preview(folder, theme_id, theme_path.stem)

            entry = {
                "id": theme_id,
                "name": str(data.get("name", theme_id)).strip(),
                "author": str(data.get("author", "Unknown")).strip(),
                "category": category,
                "date_added": theme_dates.get(theme_id, ""),
                "theme_url": f"{RAW_BASE_URL}/{folder_name}/{theme_path.name}",
                "preview_url": f"{RAW_BASE_URL}/{folder_name}/{preview_path.name}" if preview_path else "",
            }

            themes.append(entry)

    cleaned_dates = {
        theme_id: theme_dates[theme_id]
        for theme_id in sorted(theme_dates)
        if theme_id in seen_theme_ids
    }

    if cleaned_dates != theme_dates:
        theme_dates = cleaned_dates
        changed_dates = True

    themes.sort(key=lambda item: (item["category"], item["name"].lower()))

    index = {
        "version": 1,
        "themes": themes,
    }

    return index, theme_dates, changed_dates


def main():
    index, theme_dates, changed_dates = build_index()

    write_json(INDEX_FILE, index)
    write_json(DATES_FILE, theme_dates)

    print(f"Generated {INDEX_FILE} with {len(index['themes'])} theme(s).")

    if changed_dates:
        print(f"Updated {DATES_FILE}.")
    else:
        print(f"{DATES_FILE} is already up to date.")


if __name__ == "__main__":
    main()
