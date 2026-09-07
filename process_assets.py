import os
from PIL import Image, ImageFilter

def remove_black_background(input_path, output_path, threshold=25):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        # Distância do preto
        brightness = (r + g + b) / 3
        if brightness < threshold:
            new_data.append((r, g, b, 0))
        elif brightness < threshold + 25:
            # Suavização na borda
            factor = (brightness - threshold) / 25.0
            new_data.append((r, g, b, int(255 * factor)))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Processed: {output_path}")

def remove_white_background(input_path, output_path, threshold=235):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        # Se for próximo do branco
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))
        elif r > threshold - 30 and g > threshold - 30 and b > threshold - 30:
            avg = (r + g + b) / 3.0
            factor = (255 - avg) / 30.0
            new_data.append((r, g, b, int(255 * factor)))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Processed: {output_path}")

def process_additive_vfx(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        lum = int(0.299 * r + 0.587 * g + 0.114 * b)
        if lum < 15:
            new_data.append((0, 0, 0, 0))
        else:
            alpha = min(255, int(lum * 1.5))
            new_data.append((r, g, b, alpha))
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Processed VFX: {output_path}")

def process_platform_tile(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    # A área da plataforma fica aproximadamente no meio (y: 180 a 680)
    crop_box = (0, int(h * 0.22), w, int(h * 0.88))
    cropped = img.crop(crop_box)
    cropped.save(output_path, "PNG")
    print(f"Processed Platform: {output_path}")

if __name__ == "__main__":
    remove_black_background("sprite_kai.jpg", "sprite_kai.png", threshold=20)
    remove_white_background("sprite_baozhi.jpg", "sprite_baozhi.png", threshold=238)
    process_additive_vfx("vfx_slash.jpg", "vfx_slash.png")
    process_platform_tile("tile_platform.jpg", "tile_platform.png")
    print("All assets processed successfully!")
