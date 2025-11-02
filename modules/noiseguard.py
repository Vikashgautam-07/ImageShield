from PIL import Image, ImageFilter
import numpy as np

def add_privacy_noise(pil_image, mode="pixelate", intensity=10):
    """
    Applies privacy-preserving transformation based on selected mode.
    Modes: 'pixelate', 'noise', 'blur'
    """
    if mode == "pixelate":
        width, height = pil_image.size
        small = pil_image.resize((width // intensity, height // intensity), resample=Image.BILINEAR)
        return small.resize((width, height), Image.NEAREST)

    elif mode == "noise":
        image_np = np.array(pil_image)
        noise = np.random.normal(0, intensity, image_np.shape).astype(np.int16)
        noisy_image = np.clip(image_np + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_image)

    elif mode == "blur":
        return pil_image.filter(ImageFilter.GaussianBlur(radius=intensity))

    else:
        return pil_image