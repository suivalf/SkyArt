from PIL import Image, ImageDraw, ImageChops
import random
import colorsys
import cv2
import numpy as np
import glob
import os
import moviepy.video.io.ImageSequenceClip

#ig post: 1080 x 1080 px
#ig story: 1080 x 1920 px
IMAGE_WIDTH=1080
IMAGE_HEIGHT=1920

def random_color(h, s, v):
   float_rgb = colorsys.hsv_to_rgb(h, s, v)
   rgb = [int(x * 255) for x in float_rgb]
   return tuple(rgb)


def interpolate(start_color, end_color, factor: float):
   recip = 1 - factor
   return (
      int(start_color[0] * recip + end_color[0] * factor),
      int(start_color[1] * recip + end_color[1] * factor),
      int(start_color[2] * recip + end_color[2] * factor)
   )

# function for the stars and their respective opacity (from top having opacity 1 to bottom having opaciti 0.x)
def interpolate_with_opacity(start_color, end_color, factor: float, opacity):
   recip = 1 - factor
   return (
      int(start_color[0] * recip + end_color[0] * factor),
      int(start_color[1] * recip + end_color[1] * factor),
      int(start_color[2] * recip + end_color[2] * factor),
      opacity
   )

# function "borrowed" from https://stackoverflow.com/questions/32530345/pil-generating-vertical-gradient-image
def generate_gradient(
        colour1, colour2, width: int, height: int) -> Image:
    """Generate a vertical gradient."""
    base = Image.new('RGBA', (width, height), colour1)
    top = Image.new('RGBA', (width, height), colour2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def circle(draw, center, radius, fill):
    draw.ellipse((center[0] - radius + 1, center[1] - radius + 1, center[0] + radius - 1, center[1] + radius - 1), fill=fill, outline=None)

def draw_stars(draw):
    points_radius = 4.2
    # 10 iterations, one for every 100 pixels down
    for i in range(17):
        points_color = (255, 255, 255, 255 - i*12) #last value represents alpha, the opacity
        points_radius = points_radius - 0.2
        # 50 stars per 100 pixels
        for j in range(30):
            circle(draw, (random.randint(40, IMAGE_WIDTH - 40), random.randint(i*100, i*100 + 100)), random.uniform(points_radius-1, points_radius+1), fill=points_color)

def draw_comets(draw):
    #draw 10 "comets"
    for i in range(3):
        starting_point_x = random.randint(50, IMAGE_WIDTH - 50)
        starting_point_y = random.randint(50, IMAGE_HEIGHT/2)
        start_color = (255, 255, 255, 255 - i*12)
        end_color = (252, 207, 3, 255 - i*20)
        thickness = 0.1
        delta = 0.1  # distance in pixels to move each j iteration
        trail_distance = random.randint(20, 55)
        for j in range(trail_distance):
            points_color = interpolate(start_color, end_color, j / 15)
            thickness = thickness + 0.15
            delta = delta + 2
            circle(draw, (starting_point_x + delta , starting_point_y - delta), thickness, fill=points_color)



#nr of images to make
for i in range(50):
    #generate the whole image with gradient
    top_color = random_color(random.random(), 1, random.uniform(0, 0.5))
    bottom_color = random_color(random.random(), random.uniform(0.2, 0.4), random.uniform(0.1, 0.5))
    image = generate_gradient(top_color,  bottom_color, IMAGE_WIDTH, IMAGE_HEIGHT)
    image_draw = ImageDraw.Draw(image)

    #draw the stars
    draw_stars(image_draw)

    #draw the comets
    #draw_comets(image_draw)

    #start grom bottom rectangle, generate a "sun"
    circle(image_draw, (random.randint(710, 790), random.randint(1415, 1470)), random.randint(45, 60), fill=(254, 252, 215))

    #generate a mountain shape in bottom rerctangle
    image_draw.polygon([(0, random.randint(1710, 1770)), (random.randint(260, 380), random.randint(1505, 1600)), (900, IMAGE_HEIGHT), (0, IMAGE_HEIGHT)], fill=random_color(0, 0, 0))

    #draw 6 rectangles to cover margins and 2 middle sections
    image_draw.rectangle((0,0, 40, IMAGE_HEIGHT), fill=(0, 0, 0))
    image_draw.rectangle((IMAGE_WIDTH - 40, 0, IMAGE_WIDTH, IMAGE_HEIGHT), fill=(0, 0, 0))
    image_draw.rectangle((0, 0, IMAGE_WIDTH, 40), fill=(0, 0, 0))
    image_draw.rectangle((0, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_HEIGHT - 40), fill=(0, 0, 0))
    #first horizontal line
    image_draw.rectangle((0, 620, IMAGE_WIDTH, 660), fill=(0, 0, 0))
    #second horizontal line
    image_draw.rectangle((0, 1260, IMAGE_WIDTH, 1300), fill=(0, 0, 0))


    image.save(f"test_image_{i}.png")

def convert_to_avi():
    img_array = []
    for filename in glob.glob('*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

convert_to_avi()
#convert avi to mp4
#ffmpeg -i file.avi output.mp4