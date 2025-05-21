from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(filename, size=(800, 400), text="Placeholder Image", bg_color=(240, 240, 240), text_color=(100, 100, 100)):
    # Create the image
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the image
    image.save(filename)
    print(f"Placeholder image created at {filename}")

if __name__ == "__main__":
    # Create placeholder images
    create_placeholder_image("static/images/no-image.jpg", (400, 400), "No Image Available")
    create_placeholder_image("static/images/hero-bg.jpg", (1920, 600), "Hero Background") 