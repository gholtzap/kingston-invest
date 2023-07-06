from PIL import Image
import os
import math

def create_collage(directory, output_filename):
    images = [file for file in os.listdir(directory) if file.endswith(".png")]

    image_files = [Image.open(os.path.join(directory, image)) for image in images]
    widths, heights = zip(*(i.size for i in image_files))

    max_width = max(widths)
    max_height = max(heights)

    num_images = len(images)
    x_grid = y_grid = math.ceil(math.sqrt(num_images))

    collage = Image.new('RGB', (x_grid * max_width, y_grid * max_height))

    for i in range(y_grid):
        for j in range(x_grid):
            if i * x_grid + j < num_images:  # Check if there is an image left
                image = image_files[i * x_grid + j]
                collage.paste(image, (j * max_width, i * max_height))

    collage.save(output_filename)

create_collage("static/images/custom_indices", "collage.png")
