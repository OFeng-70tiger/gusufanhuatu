"""
将 11 张实景照片嵌入 gusu4ta/index.html：
- 每张图 base64 嵌入 (data:image/jpeg;base64,...)
- 在每塔卡的 .tower-in 顶部插入主图 + 图说
- 虎丘塔额外加入「双塔同框」横图专题（huqiu-2）
"""
import os, base64, re

IMG_DIR = r"C:\Users\EDY\WorkBuddy\Claw\gusu4ta\img"
HTML_PATH = r"C:\Users\EDY\WorkBuddy\Claw\gusu4ta\index.html"

def b64(name):
    with open(os.path.join(IMG_DIR, name), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

# 各塔照片与图说（手机摄影实战视角）
PLANS = {
    "lengqie": {
        "main":  ("lengqie-1.jpg", "上方山巅 · 楞伽塔全貌 · 杉林掩映"),
        "strip": [("lengqie-2.jpg", "近望 · 上方山下城市远景")],
    },
    "ruiguang": {
        "main":  ("ruiguang-3.jpg", "盘门段 · 瑞光塔通体 · 蓝天映衬"),
        "strip": [
            ("ruiguang-1.jpg", "仰观 · 砖木檐角与白墙"),
            ("ruiguang-2.jpg", "塔身红漆与城楼"),
        ],
    },
    "beisi": {
        "main":  ("beisi-1.jpg", "古城中轴 · 北寺塔通体 · 黑瓦粉墙环抱"),
        "strip": [
            ("beisi-2.jpg", "近仰 · 塔檐与天空"),
            ("beisi-3.jpg", "城北天际 · 塔下民居"),
        ],
    },
    "huqiu": {
        "main":  ("huqiu-1.jpg", "虎丘山顶 · 云岩寺塔 · 中国第一斜塔"),
        "strip": [
            ("huqiu-3.jpg", "林梢环抱 · 千年斜塔"),
        ],
    },
}

def photo_html(file_name, caption, kind="main"):
    # 简化 alt：去掉所有 HTML 标签与双引号
    import re as _re
    alt = _re.sub(r"<[^>]+>", "", caption).replace('"', "").strip()
    data = b64(file_name)
    if kind == "main":
        return f'''      <div class="tower-photo">
        <img src="data:image/jpeg;base64,{data}" alt="{alt}">
        <div class="tower-photo-cap">△ {caption}</div>
      </div>
'''
    elif kind == "strip":
        return f'''        <div class="tower-photo">
          <img src="data:image/jpeg;base64,{data}" alt="{alt}">
          <div class="tower-photo-cap">△ {caption}</div>
        </div>
'''
    elif kind == "duo":
        return f'''      <div class="duo-panel">
        <img src="data:image/jpeg;base64,{data}" alt="{alt}">
        <div class="duo-cap">{caption}</div>
      </div>
'''

def build_tower_block(plan_key, plan):
    main_name, main_cap = plan["main"]
    parts = [photo_html(main_name, main_cap, "main")]
    if plan.get("strip"):
        parts.append('      <div class="tower-photos">\n')
        for fname, cap in plan["strip"]:
            parts.append(photo_html(fname, cap, "strip"))
        parts.append('      </div>\n')
    return "".join(parts)

# 读取 HTML
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 替换每塔标记
for key, plan in PLANS.items():
    marker = f"<!-- @photos:{key} -->\n"
    if marker not in html:
        raise RuntimeError(f"missing marker for {key}")
    html = html.replace(marker, build_tower_block(key, plan), 1)

# 虎丘塔双塔同框专题 —— 插入在 huqiu 卡的 hbar-row 之前
duo_html = photo_html("huqiu-2.jpg",
    '实景同框：<b>虎丘塔</b>与远处<b>北寺塔</b>同框一城天际——这是 1759 年徐扬画中"出阊门转山塘，至虎丘止"的当代读法。两塔相距约 4 公里，以古城的 76 米天际线为限，<b>近塔斜而不倒、远塔正而守中</b>。',
    "duo")
anchor = '<div class="hbar-row"><div class="t"><b>虎丘塔 47.7米</b><span>（一说47.5米）</span></div><div class="hbar"><i style="--w:63%"></i></div></div>'
if anchor not in html:
    raise RuntimeError("huqiu anchor not found")
html = html.replace(anchor, duo_html + "      " + anchor, 1)

# 写入
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

# 报告
sz = os.path.getsize(HTML_PATH)
print(f"written {HTML_PATH}")
print(f"final HTML size: {sz/1024:.1f} KB ({sz/1024/1024:.2f} MB)")