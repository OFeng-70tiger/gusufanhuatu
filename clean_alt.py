"""清理 index.html 中所有 alt 属性里的 HTML 标签字符"""
import re, os

PATH = r"C:\Users\EDY\WorkBuddy\Claw\gusu4ta\index.html"
with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

def clean_alt(m):
    inner = m.group(1)
    inner = re.sub(r"<[^>]+>", "", inner)
    return f'alt="{inner}"'

new = re.sub(r'alt="([^"]*)"', clean_alt, html)
with open(PATH, "w", encoding="utf-8") as f:
    f.write(new)

print(f"cleaned. size: {os.path.getsize(PATH)/1024:.1f} KB")
print("sample alt after cleaning:")
for m in re.finditer(r'alt="([^"]{0,60})', new):
    print("  ", m.group(1))
    break