import os
import sys
from PIL import Image, ImageDraw, ImageFont

def convert_date_format(date_str):
    """ Convert date from yyyyMMdd to dd/MM/yyyy format """
    try:
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"Date: {day}/{month}/{year}"
    except Exception as e:
        print(f"Error formatting date: {e}")
        return "Date: Unknown Date"

def create_image_with_text(text_lines, output_path):
    """ Create a 300x200 image with transparent background and add text lines """
    width, height = 500, 300
    font_size = 50
    margin = 10

    # Create an image with transparent background
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Load a truetype or opentype font file, and create a font object
    font_path = "E:\MyData\Font\static\KodeMono-Bold.ttf"  # You may need to provide the path to your font file
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size and position for each line
    text_height_total = sum(draw.textbbox((0, 0), line, font=font)[3] for line in text_lines)
    text_height_total += margin * (len(text_lines) - 1)  # Add margin between lines
    y_offset = (height - text_height_total) // 2

    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_height = bbox[3] - bbox[1]
        text_x = 10  # Align text to the left
        draw.text((text_x, y_offset), line, font=font, fill=(255, 255, 255, 255))
        y_offset += text_height + margin  # Add margin between lines

    # Save the image
    image.save(output_path)

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_count = 1
    for filename in os.listdir(input_folder):
        if filename.startswith("IMG_") and filename.endswith(".jpg"):
            date_str = filename.split('_')[1]
            formatted_date = convert_date_format(date_str)
            
            text_lines = [f"No: {image_count}", formatted_date]

            output_filename = f'%04d.png' % image_count
            output_path = os.path.join(output_folder, output_filename)
            create_image_with_text(text_lines, output_path)
            print(f"Processed {filename} -> {output_filename}")
            image_count += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: dateText.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    process_images(input_folder, output_folder)
