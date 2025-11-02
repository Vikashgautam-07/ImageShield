from PIL import Image, ImageDraw, ImageFont

def generate_safe_preview(pil_image, text="SAFE SHARE", opacity=100, angle=0, position="bottom-right"):
    """
    Strips metadata and adds a watermark to the image.
    Input: PIL image, watermark text, opacity, angle
    Output: PIL image with watermark and no EXIF metadata
    """
    # Strip metadata
    clean_image = Image.new("RGBA", pil_image.size)
    clean_image.putdata(list(pil_image.convert("RGBA").getdata()))

    width, height = clean_image.size
    font_size = int(min(width, height) * 0.1)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Create watermark layer
    watermark_layer = Image.new("RGBA", clean_image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font=font)

    positions = {
    "bottom-right": (width - text_width - 10, height - text_height - 10),
    "bottom-left": (10, height - text_height - 10),
    "top-right": (width - text_width - 10, 10),
    "top-left": (10, 10),
    "center": ((width - text_width) // 2, (height - text_height) // 2)
    }
    pos = positions.get(position, (width - text_width - 10, height - text_height - 10))
    draw.text(pos, text, font=font, fill=(255, 255, 255, opacity))

    # Rotate watermark layer and resize back to original
    if angle != 0:
        rotated = watermark_layer.rotate(angle, expand=1)
        watermark_layer = rotated.resize(clean_image.size)

    # Composite watermark onto image
    combined = Image.alpha_composite(clean_image, watermark_layer)
    return combined.convert("RGB")