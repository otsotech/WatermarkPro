import os
import time
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

watermark_text = 'YOUR NAME HERE'
font_path = 'font.ttf'
font_size = 18
font = ImageFont.truetype(font_path, font_size)

input_dir = 'input'
output_dir = 'output'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

start_time = time.time()

num_images = sum(1 for filename in os.listdir(input_dir)
                 if filename.endswith('.jpg') or filename.endswith('.png'))

with tqdm(total=num_images) as progress_bar:
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            image = Image.open(image_path).convert('RGB')
            image_width, image_height = image.size

            watermark_size = (200, 50)
            brightest_area = None
            brightest_brightness = 0
            for x in range(0, image_width - watermark_size[0], 50):
                for y in range(0, image_height - watermark_size[1], 50):
                    area = image.crop((x, y, x + watermark_size[0], y + watermark_size[1]))
                    brightness = sum(area.convert('L').getdata()) / (watermark_size[0] * watermark_size[1])
                    if brightness > brightest_brightness:
                        brightest_brightness = brightness
                        brightest_area = (x, y)

            watermark_image = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark_image)
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            text_x = brightest_area[0] + (watermark_size[0] - text_width) // 2
            text_y = brightest_area[1] + (watermark_size[1] - text_height) // 2

            min_edge_dist = 10 
            if text_x < min_edge_dist:
                text_x = min_edge_dist
            elif text_x + text_width > image_width - min_edge_dist:
                text_x = image_width - text_width - min_edge_dist
            if text_y < min_edge_dist:
                text_y = min_edge_dist
            elif text_y + text_height > image_height - min_edge_dist:
                text_y = image_height - text_height - min_edge_dist

            draw.text((text_x, text_y), watermark_text, font=font, fill=(0, 0, 0, 255))

            watermarked_image = Image.alpha_composite(image.convert('RGBA'), watermark_image)
            watermarked_image = watermarked_image.convert('RGB')

            watermarked_image.save(output_path)

            progress_bar.update(1)

elapsed_time = time.time() - start_time
print(f"Processed {num_images} images in {elapsed_time:.2f} seconds.")
