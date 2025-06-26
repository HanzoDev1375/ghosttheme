import os
import json

def edittheme(directory, key, value):
    if not os.path.exists(directory):
        print("dir not found" + directory)
        return

    for root, dirs, files in os.walk(directory):  # Fixed to capture all three values
        for filename in files:
            if filename.endswith('.ghost'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"خطا در بارگذاری فایل JSON '{filename}': {e}")
                    continue
                
                if isinstance(data, dict):
                    data[key] = value
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                        print(f"فایل '{filename}' به‌روزرسانی شد.")
                else:
                    print(f"فایل '{filename}' یک دیکشنری معتبر نیست.")

def update_json_files(directory, key, key_to_read):
    if not os.path.exists(directory):
        print("Dir not found " + directory)
        return

    for root, dirs, files in os.walk(directory):  # Fixed to capture all three values
        for filename in files:
            if filename.endswith('.ghost'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"Error not Open Ghost '{filename}': {e}")
                    continue
                
                if isinstance(data, dict):
                    if key_to_read in data:
                        value = data[key_to_read]
                        data[key] = value
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                            print(f"File '{filename}' File Was updated with value from '{key_to_read}'.")
                    else:
                        print(f"Key '{key_to_read}' not found in '{filename}'.")
                else:
                    print(f"File '{filename}' Not a valid dictionary.")

directory_path = input("Enter Folder Ghost file: ")
key_to_add = input("Open Key Name: ")
key_to_read = input("Enter Key Name to read value from: ")

update_json_files(directory_path, key_to_add, key_to_read)