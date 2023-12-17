from PIL import Image, ImageOps
import os
import logging
import coloredlogs

# Set up logging with coloredlogs
coloredlogs.install(level='INFO')
logging.basicConfig(level=logging.INFO)

folders, images = ['static/images/'], []
border_order = {"cyan": 1, "orange": 2, "magenta": 3, "none": 4}
image_data = []

for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            img = Image.open(os.path.join(folder, filename))
            if img is not None:
                border_color = "none"
                for spine_color in border_order.keys():
                    if spine_color in filename:
                        border_color = spine_color
                        break
                image_data.append((img, border_order[border_color]))
                logging.info(f'Loaded image {filename} from {folder} with border {border_color}')

if not image_data:
    logging.warning('No images were loaded. Exiting.')
    exit()

# Sort images based on border order
image_data.sort(key=lambda x: x[1])
images = [img[0] for img in image_data]
if not images:
    logging.warning('No images were loaded. Exiting.')
    exit()

images_per_row = 4
image_width = 833
image_height = 529

num_of_images = len(images)
num_of_rows = (num_of_images // images_per_row) + \
    (1 if num_of_images % images_per_row != 0 else 0)
total_width = image_width * images_per_row
total_height = image_height * num_of_rows

new_image = Image.new('RGB', (total_width, total_height))

for index, image in enumerate(images):
    x = image_width * (index % images_per_row)
    y = image_height * (index // images_per_row)
    
    resized_image = image.resize((image_width, image_height))
    new_image.paste(resized_image, (x, y))

border_size = 200
border_color = 'black'
new_image = ImageOps.expand(new_image, border=border_size, fill=border_color)

new_image.save('collage.png')
logging.info('Collage image saved as collage.png')
print("\n")