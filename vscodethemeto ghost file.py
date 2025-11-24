import json
from typing import Dict, Any


class ExactVSCodeToAndroidMapper:
    def __init__(self):
        # تم اصلی اندروید شما
        self.original_android_theme = {
            "javafield": "#ffff0e54",
            "tabimagecolorfilter": "#fffc5469",
            "fabbackgroundcolorcolor": "#ff2f0600",
            "htmlstr": "#ffffae1c",
            "pykeyword": "#ffff2b38",
            "text_normal": "#ffffb8b8",
            "tskeyword": "#ffff6363",
            "line_number_background": "#00000000",
            "auto_comp_panel_corner": "#56B6C2",
            "menuPosBackground": "#ff2e0006",
            "breaklevel8": "#FF6F61",
            "breaklevel7": "#FFD166",
            "phpsymbol": "#61AFEF",
            "breaklevel6": "#6BD1FF",
            "breaklevel5": "#A7F3D0",
            "breaklevel4": "#FBCFE8",
            "breaklevel3": "#E0AAFF",
            "breaklevel2": "#FFE0B2",
            "breaklevel1": "#F4BFBF",
            "toolbarcolor": "#191919",
            "pynumber": "#ff7cfd54",
            "javatype": "#ffff8080",
            "auto_comp_panel_bg": "#1A1A1A",
            "tssymbols": "#ff80ff97",
            "csskeyword": "#ffff7186",
            "literal": "#fff26ea4",
            "toolbartextcolor": "#FAFAFA",
            "phphtmlattr": "#ffff5547",
            "line_number": "#ffff7178",
            "block_line_current": "#ffff7163",
            "tscolormatch3": "#00C4B4",
            "whole_background": "#00000000",
            "tscolormatch4": "#ffa2f3ff",
            "attribute_name": "#D19A66",
            "tscolormatch1": "#00BFFF",
            "tscolormatch2": "#E06C75",
            "tscolormatch7": "#ffff542b",
            "javakeywordoprator": "#ffa0ff63",
            "javanumber": "#ffffdf0e",
            "menubackground": "#ff340001",
            "tscolormatch5": "#fffa8be3",
            "javakeyword": "#ff63ffea",
            "tscolormatch6": "#C0FFEE",
            "phpcolormatch3": "#FF6F91",
            "phpcolormatch2": "#98C379",
            "phpcolormatch5": "#C678DD",
            "phpcolormatch4": "#D19A66",
            "phpcolormatch6": "#56B6C2",
            "line_divider": "#00222222",
            "fabimagecolor": "#ffff9caa",
            "textcolorforgrand": "#F8F8F2",
            "navstatusbar": "#00000000",
            "phpcolormatch1": "#FFAC81",
            "current_line": "#84420404",
            "pystring": "#ff47ffd6",
            "jskeyword": "#ffff7178",
            "textcolorinier": "#D3CCE3",
            "javastring": "#ffc799fb",
            "tsattr": "#EBCB8B",
            "backgroundcolorlinear": "#691e1e1e",
            "operator": "#F0F0F0",
            "pysymbol": "#ffff8b0e",
            "selection_handle": "#ffef00d6",
            "phpkeyword": "#FF7676",
            "tabback": "#ffff555c",
            "javafun": "#ffffb9ff",
            "keyword": "#FF6F61",
            "jsfun": "#ffecff55",
            "pycolormatch3": "#ffffef63",
            "pycolormatch4": "#fffa7db4",
            "htmltag": "#ffff5547",
            "phphtmlkeyword": "#fff65f44",
            "htmlattrname": "#ff71abff",
            "pycolormatch1": "#ffe6b8ff",
            "pycolormatch2": "#ff8ee3ff",
            "javaparament": "#fffa6e2a",
            "identifier_name": "#ff17baff",
            "ninja": "#ffffb52b",
            "fabcolorstroker": "#ffff0e1c",
            "htmlblocknormal": "#ffff003f",
            "tabtextcolor": "#ffff9caa",
            "block_line": "#ffffb547",
            "htmlblockhash": "#ffff0045",
            "menuPosTextColor": "#ffff6363",
            "selection_insert": "#ff42003b",
            "textcolorigor": "#ffff00ce",
            "jsattr": "#ff54fdaa",
            "imagecolor": "#D0A9F5",
            "phpattr": "#fffd6f46",
            "jsstring": "#ff9dfa61",
            "html_tag": "#ffffca39",
            "javaoprator": "#ff00ffa5",
            "htmlattr": "#ffffbe71",
            "htmlsymbol": "#ffff80c5",
            "print": "#fffe8400",
            "textcolorhder": "#D19A66",
            "syombolbartextcolor": "#FFAAFF",
            "displaytextcolortab": "#F4A261",
            "comment": "#6272A4",
            "attribute_value": "#FFB86C",
            "jsoprator": "#ffff8655",
            "non_printable_char": "#ff9cffdc",
        }

        self.vs_code_colors = {}

        # قوانین نگاشت از VS Code به اندروید
        self.mapping_rules = {
            # نگاشتهای دقیق که گفتید
            "editor.background": ["backgroundcolorlinear", "navstatusbar"],
            "tab.activeForeground": ["tabback", "tabtextcolor"],
            "menu.separatorBackground": ["menuPosBackground", "menubackground"],
            "menu.foreground": ["menuPosTextColor"],
            "invalid.illegal": ["htmlblocknormal", "htmlblockhash"],
            "invalid.illegal.bad-ampersand.html": ["htmlblocknormal", "htmlblockhash"],
            "meta.method.java": ["javafield"],
            "punctuation.separator.key-value": ["tscolormatch1"],
            "keyword.operator.expression.import": ["tscolormatch2"],
            "support.constant.math": ["tscolormatch3"],
            "support.constant.property.math": ["tscolormatch4"],
            "variable.other.constant": ["tscolormatch5"],
            "support.module.node": ["tscolormatch6"],
            "keyword.operator.new": ["tscolormatch7"],
            "punctuation.separator.period.python": ["pycolormatch1"],
            "punctuation.separator.period.python": ["pycolormatch2"],
            "keyword.operator.logical.python": ["pycolormatch3"],
            "meta.function-call.generic.python": ["pycolormatch4"],
            "dropdown.background": ["auto_comp_panel_bg"],
            "editor.wordHighlightBorder": ["auto_comp_panel_corner"],
            "activityBar.background": ["fabbackgroundcolorcolor"],
            "activityBar.foreground": ["fabimagecolor"],
            "markup.underline.link.image.markdown": [
                "tabimagecolorfilter",
                "imagecolor",
            ],
            # کلمات کلیدی
            "keyword": [
                "keyword",
                "javakeyword",
                "pykeyword",
                "tskeyword",
                "jskeyword",
                "phpkeyword",
                "csskeyword",
                "phphtmlkeyword",
            ],
            "storage": ["javakeyword", "phpkeyword"],
            # رشتهها
            "string": ["javastring", "pystring", "jsstring", "htmlstr"],
            # کامنتها
            "comment": ["comment"],
            # توابع
            "entity.name.function": ["javafun", "jsfun"],
            "support.function": ["javafun", "jsfun"],
            # انواع داده
            "entity.name.type": ["javatype"],
            "support.type": ["javatype"],
            "punctuation.quasi.element": ["literal"],
            "support.constant.property-value": ["print"],
            # اعداد
            "constant.numeric": ["javanumber", "pynumber"],
            # عملگرها
            "keyword.operator": [
                "operator",
                "javaoprator",
                "jsoprator",
                "javakeywordoprator",
            ],
            # پسزمینه
            "editor.lineHighlightBackground": ["current_line"],
            "editor.selectionBackground": ["selection_insert"],
            # خط اعداد
            "editorLineNumber.foreground": ["line_number"],
            "meta.method.identifier.java": ["identifier_name"],
            # نمادها
            "variable": ["phpsymbol", "pysymbol", "tssymbols"],
            "support.constant": ["phpsymbol"],
            # ویژگیها
            "entity.other.attribute-name": [
                "attribute_name",
                "phpattr",
                "jsattr",
                "htmlattr",
            ],
            # مقادیر ویژگیها
            "string.quoted": ["attribute_value"],
            # تگهای HTML
            "entity.name.tag": ["htmltag", "html_tag"],
            # نام ویژگیهای HTML
            "entity.other.attribute-name": ["htmlattrname", "phphtmlattr"],
            # اضافه کردن این خطوط به mapping_rules
            "statusBar.background": ["toolbarcolor"],
            "editorIndentGuide.background": ["line_divider"],
            "editor.foreground": ["textcolorforgrand"],
            "input.foreground": ["textcolorinier"],
            "editorCursor.foreground": ["selection_handle"],
            "variable.parameter": ["javaparament"],
            "entity.name.section": ["ninja"],
            "button.background": ["fabcolorstroker"],
            "editorBracketMatch.background": ["block_line"],
            "badge.background": ["syombolbartextcolor"],
            "titleBar.activeBackground": ["displaytextcolortab"],
            "editorWhitespace.foreground": ["non_printable_char"],
            # برای breaklevel ها (هر سطح برای چیز متفاوت)
            "storage.modifier.lifetime.rust": ["breaklevel1"],
            "variable.language.rust": ["breaklevel2"],
            "keyword.operator.word": ["breaklevel3"],
            "constant.other.symbol": ["breaklevel4"],
            "punctuation.separator.list.comma.css": ["breaklevel5"],
            "support.type.object.dom": ["breaklevel6"],
            "punctuation.definition.heading.markdown": ["breaklevel7"],
            "variable.other.class.js": ["breaklevel8"],
            # برای phpcolormatch ها
            "support.constant.php": ["phpcolormatch1"],
            "variable.other.php": ["phpcolormatch2"],
            "storage.type.php": ["phpcolormatch3"],
            "entity.name.function.php": ["phpcolormatch4"],
            "keyword.other.php": ["phpcolormatch5"],
            "support.class.php": ["phpcolormatch6"],
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

        # استخراج از بخش colors (رنگهای UI)
        if "colors" in vs_theme:
            for key, color in vs_theme["colors"].items():
                self.vs_code_colors[key] = color

        # استخراج از بخش tokenColors (رنگهای سینتکس)
        if "tokenColors" in vs_theme:
            for token in vs_theme["tokenColors"]:
                if (
                    "scope" in token
                    and "settings" in token
                    and "foreground" in token["settings"]
                ):
                    scope = token["scope"]
                    color = token["settings"]["foreground"]

                    if isinstance(scope, list):
                        for s in scope:
                            self.vs_code_colors[s] = color
                    else:
                        self.vs_code_colors[scope] = color

        # استخراج از بخش semanticTokenColors
        if "semanticTokenColors" in vs_theme:
            for key, value in vs_theme["semanticTokenColors"].items():
                if isinstance(value, dict) and "foreground" in value:
                    self.vs_code_colors[key] = value["foreground"]
                elif isinstance(value, str):
                    self.vs_code_colors[key] = value

    def _find_vs_code_color(self, pattern: str) -> str:
        """پیدا کردن رنگ در VS Code بر اساس الگو"""
        # اگر pattern دقیقاً در vs_code_colors وجود داشت
        if pattern in self.vs_code_colors:
            return self.vs_code_colors[pattern]

        # اگر نه، به صورت partial search
        for vs_key in self.vs_code_colors.keys():
            if pattern in vs_key:
                return self.vs_code_colors[vs_key]
        return None

    def _apply_color_mapping(self) -> Dict[str, str]:
        """اعمال نگاشت رنگها"""
        new_android_theme = self.original_android_theme.copy()

        changes_made = []

        for vs_pattern, android_keys in self.mapping_rules.items():
            vs_color = self._find_vs_code_color(vs_pattern)

            if vs_color:
                # تبدیل فرمت رنگ اگر لازم باشد
                formatted_color = self._format_color_for_android(vs_color)

                for android_key in android_keys:
                    if android_key in new_android_theme:
                        old_color = new_android_theme[android_key]
                        new_android_theme[android_key] = formatted_color
                        changes_made.append(
                            f"{vs_pattern} -> {android_key}: {old_color} → {formatted_color}"
                        )

        # نمایش تغییرات
        print(f"تعداد تغییرات: {len(changes_made)}")
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

    # خواندن تم VS Code
    try:
        with open(
            "/storage/emulated/0/apkapp/dracula-soft.json", "r", encoding="utf-8"
        ) as f:
            vs_code_theme = f.read()
    except FileNotFoundError as e:
        print(f"❌ فایل OneDark-Pro-mix.json یافت نشد!{e}")
        return

    print("🔄 در حال تبدیل تم VS Code به تم اندروید...")

    # تبدیل تم
    new_android_theme = converter.convert_vscode_to_android(vs_code_theme)

    # ذخیره تم جدید
    converter.save_android_theme_json(
        "/storage/emulated/0/apkapp/theme/dracula-soft.ghost", new_android_theme
    )

    # نمایش نمونهای از رنگهای مهم
    print("\n🎨 نمونهای از رنگهای تبدیل شده:")
    important_keys = ["backgroundcolorlinear", "tabback", "keyword", "comment"]
    for key in important_keys:
        if key in new_android_theme:
            print(f"  {key}: {new_android_theme[key]}")


if __name__ == "__main__":
    main()