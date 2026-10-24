import base64
import os
from PIL import Image

src_path = r"C:\Users\Farhan\.gemini\antigravity-ide\brain\eb589ce0-9b16-47b0-8d1d-272039565c6e\.user_uploaded\media_1792863615692.png"

img = Image.open(src_path)
bbox = img.getbbox()
cropped = img.crop(bbox)

target_size = 512
margin = 24
content_max = target_size - (margin * 2)

w, h = cropped.size
scale = content_max / max(w, h)
new_w = int(w * scale)
new_h = int(h * scale)
resized_content = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

square_dark = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
offset = ((target_size - new_w) // 2, (target_size - new_h) // 2)
square_dark.paste(resized_content, offset)

# Save PNGs
square_dark.save("static/images/logo-icon.png", "PNG")
square_dark.save("static/images/logo-icon-dark.png", "PNG")

# Favicon PNG
fav = square_dark.resize((64, 64), Image.Resampling.LANCZOS)
fav.save("static/images/favicon.png", "PNG")

# Read base64
with open("static/images/logo-icon.png", "rb") as f:
    b64_data = base64.b64encode(f.read()).decode("utf-8")

# Create logo-icon.svg
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <image href="data:image/png;base64,{b64_data}" width="512" height="512" />
</svg>
'''
with open("static/images/logo-icon.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

with open("static/images/app-icon.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

# Favicon SVG
fav_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="32" height="32">
  <rect width="512" height="512" rx="120" fill="#090d16" />
  <image href="data:image/png;base64,{b64_data}" width="512" height="512" />
</svg>
'''
with open("static/images/favicon.svg", "w", encoding="utf-8") as f:
    f.write(fav_svg)

print("SUCCESS: Logo updated across static/images/logo-icon.png, logo-icon.svg, app-icon.svg, favicon.svg, favicon.png")
