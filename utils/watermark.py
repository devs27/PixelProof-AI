from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math
from datetime import datetime

def _get_font(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        "C:\\Windows\\Fonts\\courbd.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            try: return ImageFont.truetype(fp, size)
            except: pass
    return ImageFont.load_default()

def apply_watermark(src_path, dst_path, username, confidence):
    img  = Image.open(src_path).convert("RGBA")
    w, h = img.size
    blurred = img.filter(ImageFilter.GaussianBlur(radius=8))
    overlay = Image.new("RGBA", (w, h), (180, 0, 0, 60))
    base    = Image.alpha_composite(blurred, overlay)
    txt_layer  = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw       = ImageDraw.Draw(txt_layer)
    main_font  = _get_font(max(20, w // 18))
    small_font = _get_font(max(12, w // 32))
    main_text  = "DEEPFAKE DETECTED"
    try:
        bbox = draw.textbbox((0, 0), main_text, font=main_font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    except AttributeError:
        tw, th = draw.textsize(main_text, font=main_font)
    spacing = th + max(30, h // 12)
    for row in range(-2, math.ceil(h/spacing)+4):
        for col in range(-2, math.ceil(w/(tw+40))+4):
            x = col * (tw + 40)
            y = row * spacing
            draw.text((x, y), f"⚠ {main_text} ⚠", font=main_font, fill=(255,50,50,150))
    txt_rotated = txt_layer.rotate(-30, expand=False)
    base = Image.alpha_composite(base, txt_rotated)
    draw2  = ImageDraw.Draw(base)
    bar_h  = max(28, h // 16)
    ts     = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    info   = f"USER: {username}  |  CONF: {confidence*100:.1f}%  |  {ts}"
    draw2.rectangle([(0, h-bar_h), (w, h)], fill=(0,0,0,220))
    draw2.text((8, h-bar_h+6), info, font=small_font, fill=(255,80,80,255))
    draw2.rectangle([(0, 0), (w, bar_h)], fill=(160,0,0,200))
    draw2.text((8, 6), "LOCKED — PixelProof AI — ACCESS RESTRICTED", font=small_font, fill=(255,255,255,255))
    base.convert("RGB").save(dst_path, quality=85)
