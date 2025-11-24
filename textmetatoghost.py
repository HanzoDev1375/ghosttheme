import json
from typing import Dict, Any


class ExactVSCodeToAndroidMapper:
    def __init__(self):
        # تم اصلی اندروید شما با رنگهای Darcula
        self.original_android_theme = {
            "javafield": "#FFC66D",  # Function
            "tabimagecolorfilter": "#CC8242",  # Keyword
            "fabbackgroundcolorcolor": "#2B2B2B",  # lineHighlight
            "htmlstr": "#6A8759",  # Strings
            "pykeyword": "#CC8242",  # Keyword
            "text_normal": "#CCCCCC",  # foreground
            "tskeyword": "#CC8242",  # Keyword
            "line_number_background": "#00000000",  # transparent
            "auto_comp_panel_corner": "#57f6c0",  # highlightedDelimitersForeground
            "menuPosBackground": "#2B2B2B",  # lineHighlight
            "breaklevel8": "#9E7BB0",  # User-defined constant
            "breaklevel7": "#7A9EC2",  # Types
            "phpsymbol": "#7A9EC2",  # Types
            "breaklevel6": "#6A8759",  # Strings
            "breaklevel5": "#CC8242",  # Keyword
            "breaklevel4": "#FFC66D",  # Function
            "breaklevel3": "#9E7BB0",  # User-defined constant
            "breaklevel2": "#7A9EC2",  # Types
            "breaklevel1": "#CC8242",  # Keyword
            "toolbarcolor": "#242424",  # background
            "pynumber": "#7A9EC2",  # Number
            "javatype": "#7A9EC2",  # Types
            "auto_comp_panel_bg": "#242424",  # background
            "tssymbols": "#9E7BB0",  # User-defined constant
            "csskeyword": "#CC8242",  # Keyword
            "literal": "#9E7BB0",  # User-defined constant
            "toolbartextcolor": "#CCCCCC",  # foreground
            "phphtmlattr": "#CCCCCC",  # foreground
            "line_number": "#707070",  # Comment
            "block_line_current": "#214283",  # selection
            "tscolormatch3": "#7A9EC2",  # Types
            "whole_background": "#00000000",  # transparent
            "tscolormatch4": "#FFC66D",  # Function
            "attribute_name": "#CCCCCC",  # Tag attribute
            "tscolormatch1": "#CC8242",  # Keyword
            "tscolormatch2": "#9E7BB0",  # User-defined constant
            "tscolormatch7": "#6A8759",  # Strings
            "javakeywordoprator": "#CCCCCC",  # Operator Keywords
            "javanumber": "#7A9EC2",  # Number
            "menubackground": "#242424",  # background
            "tscolormatch5": "#CC8242",  # Keyword
            "javakeyword": "#CC8242",  # Keyword
            "tscolormatch6": "#FFC66D",  # Function
            "phpcolormatch3": "#7A9EC2",  # Types
            "phpcolormatch2": "#9E7BB0",  # User-defined constant
            "phpcolormatch5": "#CC8242",  # Keyword
            "phpcolormatch4": "#FFC66D",  # Function
            "phpcolormatch6": "#6A8759",  # Strings
            "line_divider": "#2B2B2B",  # lineHighlight
            "fabimagecolor": "#CCCCCC",  # foreground
            "textcolorforgrand": "#CCCCCC",  # foreground
            "navstatusbar": "#242424",  # background
            "phpcolormatch1": "#CC8242",  # Keyword
            "current_line": "#2B2B2B",  # lineHighlight
            "pystring": "#6A8759",  # Strings
            "jskeyword": "#CC8242",  # Keyword
            "textcolorinier": "#CCCCCC",  # foreground
            "javastring": "#6A8759",  # Strings
            "tsattr": "#CCCCCC",  # Tag attribute
            "backgroundcolorlinear": "#242424",  # background
            "operator": "#CCCCCC",  # Operator Keywords
            "pysymbol": "#9E7BB0",  # User-defined constant
            "selection_handle": "#214283",  # selection
            "phpkeyword": "#CC8242",  # Keyword
            "tabback": "#242424",  # background
            "javafun": "#FFC66D",  # Function
            "keyword": "#CC8242",  # Keyword
            "jsfun": "#FFC66D",  # Function
            "pycolormatch3": "#CC8242",  # Keyword
            "pycolormatch4": "#FFC66D",  # Function
            "htmltag": "#FFC66D",  # Tag name
            "phphtmlkeyword": "#CC8242",  # Keyword
            "htmlattrname": "#CCCCCC",  # Tag attribute
            "pycolormatch1": "#CC8242",  # Keyword
            "pycolormatch2": "#9E7BB0",  # User-defined constant
            "javaparament": "#CCCCCC",  # Function Argument
            "identifier_name": "#FFC66D",  # Function
            "ninja": "#CC8242",  # Keyword
            "fabcolorstroker": "#214283",  # selection
            "htmlblocknormal": "#707070",  # Comment
            "tabtextcolor": "#CCCCCC",  # foreground
            "block_line": "#2B2B2B",  # lineHighlight
            "htmlblockhash": "#707070",  # Comment
            "menuPosTextColor": "#CCCCCC",  # foreground
            "selection_insert": "#214283",  # selection
            "textcolorigor": "#CC8242",  # Keyword
            "jsattr": "#CCCCCC",  # Tag attribute
            "imagecolor": "#9E7BB0",  # User-defined constant
            "phpattr": "#CCCCCC",  # Tag attribute
            "jsstring": "#6A8759",  # Strings
            "html_tag": "#FFC66D",  # Tag name
            "javaoprator": "#CCCCCC",  # Operator Keywords
            "htmlattr": "#CCCCCC",  # Tag attribute
            "htmlsymbol": "#9E7BB0",  # User-defined constant
            "print": "#7A9EC2",  # Number
            "textcolorhder": "#CC8242",  # Keyword
            "syombolbartextcolor": "#FFC66D",  # Function
            "displaytextcolortab": "#CC8242",  # Keyword
            "comment": "#707070",  # Comment
            "attribute_value": "#6A8759",  # Strings
            "jsoprator": "#CCCCCC",  # Operator Keywords
            "non_printable_char": "#2B2B2B",  # lineHighlight
        }

        self.vs_code_colors = {}

        # قوانین نگاشت از VS Code به اندروید - به روز شده برای Darcula
        self.mapping_rules = {
            # نگاشتهای اصلی
            "editor.background": [
                "backgroundcolorlinear",
                "navstatusbar",
                "toolbarcolor",
                "menubackground",
                "auto_comp_panel_bg",
            ],
            "editor.foreground": [
                "textcolorforgrand",
                "toolbartextcolor",
                "tabtextcolor",
                "textcolorinier",
                "tabback",
                "auto_comp_panel_corner",
                "menuPosTextColor",
            ],
            "editor.lineHighlightBackground": [
                "current_line",
                "block_line",
                "line_divider",
            ],
            "editor.selectionBackground": [
                "selection_insert",
                "fabcolorstroker",
                "block_line_current",
                "selection_handle",
            ],
            "editorLineNumber.foreground": ["line_number"],
            "editorIndentGuide.background": ["block_line", "line_divider"],
            "editorIndentGuide.activeBackground": ["block_line_current"],
            "keyword": [
                "keyword",
                "javakeyword",
                "pykeyword",
                "tskeyword",
                "jskeyword",
                "phpkeyword",
                "csskeyword",
                "phphtmlkeyword",
                "textcolorigor",
                "textcolorhder",
                "displaytextcolortab",
                "ninja",
            ],
            "storage": ["javakeyword", "phpkeyword", "pykeyword", "tskeyword"],
            "keyword.operator": [
                "operator",
                "javaoprator",
                "jsoprator",
                "javakeywordoprator",
            ],
            # رشتهها
            "string": [
                "javastring",
                "pystring",
                "jsstring",
                "htmlstr",
                "attribute_value",
            ],
            # کامنتها
            "comment": ["comment", "htmlblocknormal", "htmlblockhash"],
            # توابع
            "entity.name.function": [
                "javafun",
                "jsfun",
                "identifier_name",
                "syombolbartextcolor",
            ],
            "support.function": ["javafun", "jsfun"],
            # انواع داده
            "entity.name.type": ["javatype"],
            "support.type": ["javatype", "phpsymbol"],
            # اعداد
            "constant.numeric": ["javanumber", "pynumber", "print"],
            # نمادها و ثابتها
            "variable": ["phpsymbol", "pysymbol", "tssymbols", "literal", "htmlsymbol"],
            "support.constant": ["phpsymbol"],
            "constant.character": ["literal"],
            "constant.other": ["literal", "tssymbols"],
            # ویژگیها
            "entity.other.attribute-name": [
                "attribute_name",
                "phpattr",
                "jsattr",
                "htmlattr",
                "htmlattrname",
                "phphtmlattr",
                "tsattr",
            ],
            # تگهای HTML
            "entity.name.tag": ["htmltag", "html_tag"],
            # UI elements
            "activityBar.foreground": ["fabimagecolor"],
            "statusBar.background": ["toolbarcolor"],
            "button.background": ["fabcolorstroker"],
            "button.hoverBackground": ["fabbackgroundcolorcolor"],
            "dropdown.background": ["auto_comp_panel_bg"],
            "editor.wordHighlightBorder": ["auto_comp_panel_corner"],
            "titleBar.activeBackground": ["displaytextcolortab"],
            "badge.background": ["syombolbartextcolor"],
            "editorWhitespace.foreground": ["non_printable_char"],
            # پارامترهای تابع
            "variable.parameter": ["javaparament"],
            # breaklevel ها
            "storage.modifier": ["breaklevel1", "breaklevel5"],
            "variable.language": ["breaklevel2"],
            "keyword.operator.word": ["breaklevel3"],
            "constant.other.symbol": ["breaklevel4"],
            "support.type.object": ["breaklevel6"],
            "punctuation.definition.heading": ["breaklevel7"],
            "variable.other.class": ["breaklevel8"],
            # phpcolormatch ها
            "support.constant.php": ["phpcolormatch1"],
            "variable.other.php": ["phpcolormatch2"],
            "storage.type.php": ["phpcolormatch3"],
            "entity.name.function.php": ["phpcolormatch4"],
            "keyword.other.php": ["phpcolormatch5"],
            "support.class.php": ["phpcolormatch6"],
            # tscolormatch ها
            "punctuation.separator.key-value": ["tscolormatch1"],
            "keyword.operator.expression.import": ["tscolormatch2"],
            "support.constant.math": ["tscolormatch3"],
            "support.constant.property.math": ["tscolormatch4"],
            "variable.other.constant": ["tscolormatch5"],
            "support.module.node": ["tscolormatch6"],
            "keyword.operator.new": ["tscolormatch7"],
            # pycolormatch ها
            "punctuation.separator.period.python": ["pycolormatch1", "pycolormatch2"],
            "keyword.operator.logical.python": ["pycolormatch3"],
            "meta.function-call.generic.python": ["pycolormatch4"],
        }

    def convert_vscode_to_android(self, vs_code_theme_json: str) -> Dict[str, str]:
        """تبدیل تم VS Code به تم اندروید"""
        try:
            vs_theme = json.loads(vs_code_theme_json)
            self._extract_vs_code_colors(vs_theme)
            return self._apply_color_mapping()

        except Exception as e:
            print(f"خطا در تبدیل: {e}")
            return self.original_android_theme.copy()

    def _extract_vs_code_colors(self, vs_theme: Dict[str, Any]):
        """استخراج رنگها از تم VS Code"""
        self.vs_code_colors = {}
        print("🔍 در حال استخراج رنگها از تم VS Code...")

        # استخراج از بخش settings (قالب جدید)
        if "settings" in vs_theme:
            for i, setting in enumerate(vs_theme["settings"]):
                if "settings" in setting:
                    settings_dict = setting["settings"]

                    # دیباگ: چاپ تمام کلیدهای موجود در settings
                    if i == 0:  # فقط برای اولین setting چاپ کن
                        print(
                            f"📋 کلیدهای موجود در settings: {list(settings_dict.keys())}"
                        )

                    # رنگهای عمومی - مستقیماً از setting می‌گیریم
                    if "foreground" in settings_dict:
                        self.vs_code_colors["editor.foreground"] = settings_dict[
                            "foreground"
                        ]
                        print(f"🎨 foreground: {settings_dict['foreground']}")
                    if "background" in settings_dict:
                        self.vs_code_colors["editor.background"] = settings_dict[
                            "background"
                        ]
                        print(f"🎨 background: {settings_dict['background']}")
                    if "lineHighlight" in settings_dict:
                        self.vs_code_colors["editor.lineHighlightBackground"] = (
                            settings_dict["lineHighlight"]
                        )
                        print(f"🎨 lineHighlight: {settings_dict['lineHighlight']}")
                    if "selection" in settings_dict:
                        self.vs_code_colors["editor.selectionBackground"] = (
                            settings_dict["selection"]
                        )
                        print(f"🎨 selection: {settings_dict['selection']}")
                    if "highlightedDelimitersForeground" in settings_dict:
                        # اینجا درستش کردم - بدون editor.
                        self.vs_code_colors["highlightedDelimitersForeground"] = (
                            settings_dict["highlightedDelimitersForeground"]
                        )
                        print(
                            f"🎨 highlightedDelimitersForeground: {settings_dict['highlightedDelimitersForeground']}"
                        )

                # رنگهای scope-based
                if (
                    "scope" in setting
                    and "settings" in setting
                    and "foreground" in setting["settings"]
                ):
                    scope = setting["scope"]
                    color = setting["settings"]["foreground"]

                    # دیباگ برای scopeهای مهم
                    important_scopes = [
                        "keyword",
                        "string",
                        "comment",
                        "entity.name.function",
                    ]
                    if any(important in str(scope) for important in important_scopes):
                        print(f"🎨 scope '{scope}': {color}")

                    if isinstance(scope, list):
                        for s in scope:
                            s_clean = s.strip()
                            self.vs_code_colors[s_clean] = color
                    else:
                        scope_clean = scope.strip()
                        self.vs_code_colors[scope_clean] = color

        print(f"📊 تعداد رنگهای استخراج شده: {len(self.vs_code_colors)}")

    def _find_vs_code_color(self, pattern: str) -> str:
        """پیدا کردن رنگ در VS Code بر اساس الگو"""
        # اول سعی کن دقیق پیدا کنی
        if pattern in self.vs_code_colors:
            print(f"✅ رنگ پیدا شد برای '{pattern}': {self.vs_code_colors[pattern]}")
            return self.vs_code_colors[pattern]

        # اگر نه، به صورت partial search در کلیدها
        for vs_key in self.vs_code_colors.keys():
            if pattern in vs_key:
                print(
                    f"🔍 رنگ پیدا شد (partial) برای '{pattern}' در '{vs_key}': {self.vs_code_colors[vs_key]}"
                )
                return self.vs_code_colors[vs_key]

        print(f"❌ رنگ پیدا نشد برای: {pattern}")
        return None

    def _apply_color_mapping(self) -> Dict[str, str]:
        """اعمال نگاشت رنگها"""
        new_android_theme = self.original_android_theme.copy()

        changes_made = []

        for vs_pattern, android_keys in self.mapping_rules.items():
            vs_color = self._find_vs_code_color(vs_pattern)

            if vs_color:
                formatted_color = self._format_color_for_android(vs_color)

                for android_key in android_keys:
                    if android_key in new_android_theme:
                        old_color = new_android_theme[android_key]
                        new_android_theme[android_key] = formatted_color
                        changes_made.append(
                            f"{vs_pattern} -> {android_key}: {old_color} → {formatted_color}"
                        )

        # نمایش تغییرات
        print(f"🔄 تعداد تغییرات: {len(changes_made)}")
        for change in changes_made:
            print(f"  {change}")

        return new_android_theme

    def _format_color_for_android(self, color: str) -> str:
        """فرمت کردن رنگ برای اندروید"""
        if color.startswith("#"):
            if len(color) == 7:  # #RRGGBB
                return f"#FF{color[1:]}".upper()
            elif len(color) == 9:  # #AARRGGBB
                return color.upper()
        return color

    def save_android_theme_json(self, output_file: str, android_theme: Dict[str, str]):
        """ذخیره تم اندروید به صورت JSON"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(android_theme, f, indent=2, ensure_ascii=False)

            print(f"✅ تم اندروید با موفقیت در {output_file} ذخیره شد")
            print(f"📊 تعداد کل رنگها: {len(android_theme)}")

        except Exception as e:
            print(f"❌ خطا در ذخیره فایل: {e}")


# استفاده از کلاس
def main():
    converter = ExactVSCodeToAndroidMapper()

    # خواندن تم VS Code Darcula
    try:
        with open(
            "/storage/emulated/0/apkapp/darcula.json", "r", encoding="utf-8"
        ) as f:
            vs_code_theme = f.read()
    except FileNotFoundError:
        print("❌ فایل darcula.json یافت نشد!")
        return

    print("🔄 در حال تبدیل تم Darcula به تم اندروید...")

    # تبدیل تم
    new_android_theme = converter.convert_vscode_to_android(vs_code_theme)

    # ذخیره تم جدید
    converter.save_android_theme_json(
        "/storage/emulated/0/apkapp/darcula.ghost", new_android_theme
    )

    # نمایش نمونهای از رنگهای مهم
    print("\n🎨 نمونهای از رنگهای تبدیل شده:")
    important_keys = [
        "backgroundcolorlinear",
        "tabback",
        "keyword",
        "comment",
        "javastring",
        "javafun",
        "auto_comp_panel_corner",  # این باید highlightedDelimitersForeground باشد
    ]
    for key in important_keys:
        if key in new_android_theme:
            print(f"  {key}: {new_android_theme[key]}")


if __name__ == "__main__":
    main()