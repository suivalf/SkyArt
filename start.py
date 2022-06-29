import glob
import os

from PIL import Image, ImageDraw
import random
import uuid
import moviepy.editor as mp

def create_gif():
    ids = []
    my_images = []
    for i in range(100):
        run_id = uuid.uuid1()
        ids.append(run_id)
        #print(f'Processing run nr.: {run_id}')

        image = Image.new('RGB', (2000, 2000))
        width, height = image.size

        rectangle_width = 500
        rectangle_height = 500

        number_of_squares = random.randint(400, 500)

        draw_image = ImageDraw.Draw(image)
        for i in range(number_of_squares):
            rectangle_x = random.randint(0, width)
            rectangle_y = random.randint(0, height)

            rectangle_shape = [
                (rectangle_x, rectangle_y),
                (rectangle_x + random.randint(10, 30), rectangle_y - random.randint(10, 30))
            ]
            draw_image.line(
                rectangle_shape,
                fill=(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                ),
                width=5
            )

            draw_image.rectangle([(rectangle_x, rectangle_y),
                                  (rectangle_x + random.randint(10, 30), rectangle_y - random.randint(10, 30))],
                                 fill=(
                                     random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255)
                                 ),
                                 width=5
                                 )
        image.save(f'./{run_id}.png')
        im1 = Image.open(f'./{run_id}.png')
        my_images.append(im1)

    #append images together to form a GIF
    image.save('out.gif', save_all=True, append_images= my_images, duration=60, loop=0)

    #delete all .png files after done using them
    pngs = os.listdir(f'./')
    for image in pngs:
        if image.endswith(".png"):
            os.remove(image)

    #convert the gif to mp4
    clip = mp.VideoFileClip("out.gif")
    clip.write_videofile("out.mp4")

