#!/usr/bin/env python3
"""
Place a screenshot inside a realistic iPhone-style phone frame.
Usage: python3 phone-frame.py <input-image> [output-image]
"""

import sys
from PIL import Image, ImageDraw

def create_phone_frame(input_path, output_path=None):
    if output_path is None:
        base = input_path.rsplit('.', 1)[0]
        output_path = f"{base}-phone-frame.png"

    # Load screenshot
    screenshot = Image.open(input_path).convert("RGBA")

    # Phone dimensions (iPhone 15 Pro-ish proportions)
    phone_w, phone_h = 390, 844
    bezel = 14
    corner_r = 52
    padding = 40  # space around phone for shadow

    # Scale screenshot to fill the screen area
    scale_x = phone_w / screenshot.width
    scale_y = phone_h / screenshot.height
    scale = max(scale_x, scale_y)
    new_w = int(screenshot.width * scale)
    new_h = int(screenshot.height * scale)
    screenshot = screenshot.resize((new_w, new_h), Image.LANCZOS)

    # Crop to exact phone screen size (from top-center)
    left = (new_w - phone_w) // 2
    screenshot = screenshot.crop((left, 0, left + phone_w, phone_h))

    # Canvas
    outer_w = phone_w + bezel * 2
    outer_h = phone_h + bezel * 2
    canvas_w = outer_w + padding * 2
    canvas_h = outer_h + padding * 2
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    # --- Draw shadow ---
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_offset_x, shadow_offset_y = 4, 8
    for i in range(30, 0, -1):
        alpha = int(4 * (30 - i))
        if alpha > 255:
            alpha = 255
        shadow_draw.rounded_rectangle(
            [padding - i + shadow_offset_x, padding - i + shadow_offset_y,
             padding + outer_w + i + shadow_offset_x, padding + outer_h + i + shadow_offset_y],
            radius=corner_r + i,
            fill=(0, 0, 0, alpha)
        )
    canvas = Image.alpha_composite(canvas, shadow)

    # --- Draw phone body (dark frame) ---
    body = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    body_draw = ImageDraw.Draw(body)

    # Outer shell
    body_draw.rounded_rectangle(
        [padding, padding, padding + outer_w, padding + outer_h],
        radius=corner_r + 2,
        fill=(26, 26, 26, 255)
    )

    # Metallic edge highlight
    body_draw.rounded_rectangle(
        [padding + 1, padding + 1, padding + outer_w - 1, padding + outer_h - 1],
        radius=corner_r + 1,
        outline=(80, 80, 80, 255),
        width=1
    )

    canvas = Image.alpha_composite(canvas, body)

    # --- Create screen with rounded corners (mask) ---
    screen_x = padding + bezel
    screen_y = padding + bezel
    screen_r = corner_r - 6

    # Create rounded rect mask for the screen
    mask = Image.new("L", (phone_w, phone_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, phone_w, phone_h], radius=screen_r, fill=255)

    # Apply mask to screenshot
    screen_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    masked_screenshot = Image.new("RGBA", (phone_w, phone_h), (0, 0, 0, 0))
    masked_screenshot.paste(screenshot, (0, 0), mask)
    screen_layer.paste(masked_screenshot, (screen_x, screen_y), masked_screenshot)

    canvas = Image.alpha_composite(canvas, screen_layer)

    # --- Dynamic Island ---
    di_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    di_draw = ImageDraw.Draw(di_layer)
    di_w, di_h = 126, 37
    di_x = screen_x + (phone_w - di_w) // 2
    di_y = screen_y + 11
    di_draw.rounded_rectangle(
        [di_x, di_y, di_x + di_w, di_y + di_h],
        radius=di_h // 2,
        fill=(0, 0, 0, 255)
    )
    canvas = Image.alpha_composite(canvas, di_layer)

    # --- Home indicator ---
    hi_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    hi_draw = ImageDraw.Draw(hi_layer)
    hi_w, hi_h = 134, 5
    hi_x = screen_x + (phone_w - hi_w) // 2
    hi_y = screen_y + phone_h - 20
    hi_draw.rounded_rectangle(
        [hi_x, hi_y, hi_x + hi_w, hi_y + hi_h],
        radius=hi_h // 2,
        fill=(255, 255, 255, 150)
    )
    canvas = Image.alpha_composite(canvas, hi_layer)

    # --- Side buttons ---
    btn_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    btn_draw = ImageDraw.Draw(btn_layer)
    btn_color = (42, 42, 42, 255)
    bx_right = padding + outer_w
    bx_left = padding - 3

    # Power button (right)
    btn_draw.rounded_rectangle([bx_right, padding + 180, bx_right + 3, padding + 260], radius=1, fill=btn_color)
    # Volume up (left)
    btn_draw.rounded_rectangle([bx_left, padding + 160, bx_left + 3, padding + 210], radius=1, fill=btn_color)
    # Volume down (left)
    btn_draw.rounded_rectangle([bx_left, padding + 220, bx_left + 3, padding + 270], radius=1, fill=btn_color)
    # Silent switch (left)
    btn_draw.rounded_rectangle([bx_left, padding + 120, bx_left + 3, padding + 148], radius=1, fill=btn_color)

    canvas = Image.alpha_composite(canvas, btn_layer)

    # Save
    canvas.save(output_path, "PNG")
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 phone-frame.py <input-image> [output-image]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    create_phone_frame(inp, out)
