from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha(width=250, height=70, font_size=36):
    # Create a new image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()

    # Generate random characters
    characters = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Draw characters on the image
    for i, char in enumerate(characters):
        x = 10 + i * (font_size + 5)
        y = random.randint(0, height - font_size)
        draw.text((x, y), char, font=font, fill=(0, 0, 0))

    # Add noise - random lines
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0), width=1)

    # Add noise - random dots
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(0, 0, 0))

    return image, characters