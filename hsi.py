#!/usr/bin/env python3
import os
import json
from pathlib import Path

def generate_theme_catalog():
    # Get repository info from environment
    repo = os.environ.get('GITHUB_REPOSITORY', 'HanzoDev1375/ghosttheme')
    base_url = f'https://raw.githubusercontent.com/{repo}/main/'
    
    themes = []
    backgrounds = []

    # Scan all files recursively
    for root, _, files in os.walk('.'):
        for file in files:
            file_path = Path(root) / file
            rel_path = str(file_path.relative_to('.'))
            
            # Skip files in .github directory
            if rel_path.startswith('.github/'):
                continue
                
            # Process theme files
            if file.endswith('.ghost'):
                theme = {
                    'theme': base_url + rel_path,
                    'image': None,
                    'background': None,
                    'hasbackground': False
                }
                
                # Find matching image
                for ext in ['.png', '.webp', '.jpg', '.jpeg']:
                    img_path = file_path.with_suffix(ext)
                    if img_path.exists():
                        theme['image'] = base_url + str(img_path.relative_to('.'))
                        break
                
                themes.append(theme)
            
            # Process background images
            elif file.lower().endswith(('.jpeg', '.jpg')):
                bg_name = file.lower()
                if 'background' in bg_name or 'back' in bg_name:
                    backgrounds.append({
                        'path': rel_path,
                        'url': base_url + rel_path,
                        'dir': os.path.dirname(rel_path)
                    })

    # Match backgrounds with themes
    for bg in backgrounds:
        for theme in themes:
            theme_path = theme['theme'].replace(base_url, '')
            theme_dir = os.path.dirname(theme_path)
            
            # Match by directory
            if bg['dir'] == theme_dir:
                theme['background'] = bg['url']
                theme['hasbackground'] = True
                break
            
            # Match by name pattern
            theme_name = os.path.basename(theme_path).replace('.ghost', '').lower()
            if theme_name in bg['path'].lower():
                theme['background'] = bg['url']
                theme['hasbackground'] = True
                break

    # Save as JSON
    with open('themes.json', 'w') as f:
        json.dump(themes, f, indent=2)
    
    print(f"Successfully generated catalog with {len(themes)} themes")

if __name__ == '__main__':
    generate_theme_catalog()