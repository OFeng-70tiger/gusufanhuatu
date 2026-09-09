"""
压缩 D:\★项目素材\姑苏繁华图-一眼千年-四塔守望 下的 12 张四塔原图：
- 按 EXIF 转正
- 长边缩到 1080px
- JPEG 78% 质量
- 输出到 C:/Users/EDY/WorkBuddy/Claw/gusu4ta/img/
- 同时输出每张图压缩后的字节数
"""
import os, glob
from PIL import Image, ImageOps

SRC = r"D:\★项目素材\姑苏繁华图-一眼千年-四塔守望"
DST = r"C:\Users\EDY\WorkBuddy\Claw\gusu4ta\img"
os.makedirs(DST, exist_ok=True)

files = sorted(glob.glob(os.path.join(SRC, "*.JPG")) + glob.glob(os.path.join(SRC, "*.jpg")))
print(f"found {len(files)} files")

mapping = {
    "上方山塔 (1).JPG": "lengqie-1.jpg",
    "上方山塔 (2).JPG": "lengqie-2.jpg",
    "北寺塔 (1).JPG":   "beisi-1.jpg",
    "北寺塔 (2).JPG":   "beisi-2.jpg",
    "北寺塔 (3).JPG":   "beisi-3.jpg",
    "瑞光塔 (1).JPG":   "ruiguang-1.jpg",
    "瑞光塔 (2).JPG":   "ruiguang-2.jpg",
    "瑞光塔 (3).JPG":   "ruiguang-3.jpg",
    "虎丘塔 (1).JPG":   "huqiu-1.jpg",
    "虎丘塔 (2).JPG":   "huqiu-2.jpg",
    "虎丘塔 (3).JPG":   "huqiu-3.jpg",
}

total_out = 0
for fp in files:
    name = os.path.basename(fp)
    out_name = mapping.get(name)
    if not out_name:
        print(f"SKIP unmapped: {name}")
        continue
    img = Image.open(fp)
    img = ImageOps.exif_transpose(img)  # 按 EXIF 转正
    if img.mode != "RGB":
        img = img.convert("RGB")
    # 长边 960（720px 设计稿下 1.3x 视网膜已足）
    w, h = img.size
    long_side = max(w, h)
    if long_side > 960:
        scale = 960 / long_side
        img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    out_path = os.path.join(DST, out_name)
    img.save(out_path, "JPEG", quality=72, optimize=True, progressive=True)
    sz = os.path.getsize(out_path)
    total_out += sz
    print(f"{name:>20s} -> {out_name}  {w}x{h} -> {img.size[0]}x{img.size[1]}  {sz/1024:.1f} KB")

print(f"\nTOTAL OUT: {total_out/1024:.1f} KB ({total_out/1024/1024:.2f} MB)")