import os
import glob
import json
import argparse
import re


FOOD_INGREDIENTS = {
    "pizza": ["flour", "tomato sauce", "cheese", "olive oil", "yeast"],
    "salad": ["lettuce", "tomato", "cucumber", "olive oil", "vinegar"],
    "pasta": ["pasta", "tomato", "garlic", "olive oil", "parmesan"],
    "smoothie": ["banana", "milk", "honey", "berries"],
    "sandwich": ["bread", "lettuce", "tomato", "cheese", "mayo"]
}


def parse_filename_meta(filename: str):
    base = os.path.splitext(filename)[0]
    post_num = None
    desc_num = None
    m = re.search(r"post_(\d+)_description_(\d+)", base)
    if m:
        post_num = int(m.group(1))
        desc_num = int(m.group(2))
    return post_num, desc_num


def read_text_files(input_dir: str):
    files = glob.glob(os.path.join(input_dir, "**", "*.txt"), recursive=True)
    files = sorted(files)
    entries = []

    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except Exception:
            continue

        filename = os.path.basename(path)
        folder = os.path.relpath(os.path.dirname(path), start=input_dir)
        if folder == ".":
            folder = os.path.basename(input_dir)

        post_num, desc_num = parse_filename_meta(filename)

        entries.append({
            "source_path": os.path.normpath(path),
            "source_folder": folder,
            "filename": filename,
            "post_number": post_num,
            "description_number": desc_num,
            "raw_text": content,
            "lines": content.splitlines() if content else []
        })

    return entries


def find_foods_in_text(text: str, food_db: dict):
    text_lower = text.lower()
    found = []
    for food, ingredients in food_db.items():
        # match whole word to reduce false positives
        if re.search(r"\b" + re.escape(food) + r"\b", text_lower):
            found.append({"food": food, "ingredients": ingredients})
    return found


def load_food_map(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # expect dict of food -> [ingredients]
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    p = argparse.ArgumentParser(description="Transform OCR text files to JSON and map foods to ingredients.")
    p.add_argument("--input", default="ocr_results", help="Input directory containing text files (default: ocr_results)")
    p.add_argument("--out-json", default="ocr_data.json", help="Output JSON for OCR data (default: ocr_data.json)")
    p.add_argument("--food-out", default="food_analysis.json", help="Output JSON for food analysis (default: food_analysis.json)")
    p.add_argument("--food-map", help="Optional JSON file with food->ingredients mapping")
    p.add_argument("--folders", help="Comma-separated list of subfolders to include (e.g. manskis_wellness,soul.body.mindd)")
    p.add_argument("--per-folder", action="store_true", help="Write separate food analysis JSON per folder when detecting foods")
    p.add_argument("--detect-foods", action="store_true", help="Detect foods using built-in or custom mapping")
    args = p.parse_args()

    if not os.path.exists(args.input):
        print(f"Input directory not found: {args.input}")
        return

    entries = read_text_files(args.input)

    # If folders specified, filter entries to only those folders
    if args.folders:
        wanted = {f.strip() for f in args.folders.split(',') if f.strip()}
        filtered = [e for e in entries if e.get("source_folder") in wanted]
        print(f"Filtering to folders: {', '.join(sorted(wanted))} -> {len(filtered)} entries kept")
        entries = filtered

    save_json(args.out_json, entries)
    print(f"Saved {len(entries)} OCR entries to {args.out_json}")

    food_db = FOOD_INGREDIENTS
    if args.food_map:
        custom = load_food_map(args.food_map)
        if custom is None:
            print(f"Warning: failed to load custom food map {args.food_map}; using default mapping.")
        else:
            food_db = custom

    if args.detect_foods:
        if args.per_folder:
            # Group entries by source_folder and write one food analysis file per folder
            groups = {}
            for e in entries:
                folder = e.get("source_folder") or "unknown"
                groups.setdefault(folder, []).append(e)

            for folder, group_entries in groups.items():
                results = []
                for e in group_entries:
                    raw = e.get("raw_text", "")
                    found = find_foods_in_text(raw, food_db)
                    results.append({
                        "filename": e["filename"],
                        "post_number": e["post_number"],
                        "foods_detected": found
                    })

                safe_folder = re.sub(r"[^0-9A-Za-z._-]", "_", folder)
                base, ext = os.path.splitext(args.food_out)
                out_path = f"{base}_{safe_folder}{ext}"
                save_json(out_path, results)
                print(f"Saved food analysis for {len(results)} entries to {out_path}")
        else:
            results = []
            for e in entries:
                raw = e.get("raw_text", "")
                found = find_foods_in_text(raw, food_db)
                results.append({
                    "filename": e["filename"],
                    "post_number": e["post_number"],
                    "foods_detected": found
                })
            save_json(args.food_out, results)
            print(f"Saved food analysis for {len(results)} entries to {args.food_out}")


if __name__ == "__main__":
    main()
