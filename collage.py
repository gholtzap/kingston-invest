from PIL import Image, ImageOps
import os

folders,images = ['static/images/big_tech', 'static/images/cancelled', 'static/images/misc'],[]

# Load all images from the directories
for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith('.png'): 
            img = Image.open(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
                print(f'Loaded image {filename} from {folder}')

if not images:
    print('No images were loaded. Exiting.')
    exit()

images_per_row = 4
image_width = 833
image_height = 529

# Calculate the size of the output image
num_of_images = len(images)
num_of_rows = (num_of_images // images_per_row) + (1 if num_of_images % images_per_row != 0 else 0)
total_width = image_width * images_per_row
total_height = image_height * num_of_rows

new_image = Image.new('RGB', (total_width, total_height))

for index, image in enumerate(images):
    x = image_width * (index % images_per_row)
    y = image_height * (index // images_per_row)
    new_image.paste(image, (x, y))

border_size = 200
border_color = 'black'
new_image = ImageOps.expand(new_image, border=border_size, fill=border_color)

new_image.save('collage.jpg')
