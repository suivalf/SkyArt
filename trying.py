from PIL import Image, ImageDraw, ImageChops
import random
import colorsys
#ig post: 1080 x 1080 px
#ig story: 1080 x 1920 px
def random_color():
   h = random.random()
   s = 1
   v = 1
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

def circle(draw, center, radius, fill):
    draw.ellipse((center[0] - radius + 1, center[1] - radius + 1, center[0] + radius - 1, center[1] + radius - 1), fill=fill, outline=None)


def generate_art(path: str):
   print("Generating...")
   target_size_px = 1080
   scale_factor = 5
   image_size = (target_size_px * scale_factor, target_size_px * scale_factor)
   image_bg_color = (0, 0, 0)
   start_color = random_color()
   end_color = random_color()
   image_padding = 15 * scale_factor
   image = Image.new("RGB", image_size, image_bg_color)
   image_draw = ImageDraw.Draw(image)
   thickness = 0
   points = []

   # Generate the points
   for _ in range(15):
      random_point = (
         random.randint(image_padding, image_size[0] - image_padding),
         random.randint(image_padding, image_size[1] - image_padding)
      )
      points.append(random_point)

   # Draw bounding box
   min_x = min([p[0] for p in points])
   max_x = max([p[0] for p in points])
   min_y = min([p[1] for p in points])
   max_y = max([p[1] for p in points])

   # Center the image
   delta_x = min_x - (image_size[0] - max_x)
   delta_y = min_y - (image_size[0] - max_y)
   for i, point in enumerate(points):
      points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

   #Draw the points all connected
   for i, point in enumerate(points):
      # overlay canvas
      overlay_image = Image.new("RGB", image_size, image_bg_color)
      overlay_draw = ImageDraw.Draw(overlay_image)
      p1 = point
      if i == len(points) - 1:
         p2 = points[0]
      else:
         p2 = points[i + 1]
      line_xy = (p1, p2)
      line_color = interpolate(start_color, end_color, i / (len(points) - 1))
      points_color = interpolate(end_color, start_color, i / (len(points) - 1))
      thickness += scale_factor
      #draw a line between 2 points
      overlay_draw.line(line_xy, fill=line_color, width=thickness)
      #draw a circle at each line's endpoints to make it round
      #circle(overlay_draw, (p1[0], p1[1]), thickness / 2, line_color)
      circle(overlay_draw, (p2[0], p2[1]), thickness / 2, line_color)
      for j in range(i*2):
         circle(overlay_draw, (random.randint(image_padding, target_size_px * scale_factor - image_padding), random.randint(image_padding, target_size_px * scale_factor - image_padding)), thickness / 2, points_color)

      image = ImageChops.add(image, overlay_image)

   """
   #Draw triangles
   for i, point in enumerate(points):
      # overlay canvas
      overlay_image = Image.new("RGB", image_size, image_bg_color)
      overlay_draw = ImageDraw.Draw(overlay_image)
      if (i + 1) % 3 == 0:
         p2 = points[i - 2]
         p1 = points[i]
         # One "shape" done, reset thickness and colors
         thickness = 0
         start_color = random_color()
         end_color = random_color()
      else:
         p1 = point
         p2 = points[i + 1]
      line_xy = (p1, p2)
      line_color = interpolate(start_color, end_color, i / (len(points) - 1))
      thickness += scale_factor * 3
      # draw a line between 2 points
      overlay_draw.line(line_xy, fill=line_color, width=thickness)
      # draw a circle at each line's endpoints to make it round
      # circle(overlay_draw, (p1[0], p1[1]), thickness / 2, line_color)
      circle(overlay_draw, (p2[0], p2[1]), thickness / 2, line_color)
      image = ImageChops.add(image, overlay_image)
   """
   #Resize image
   image = image.resize((target_size_px, target_size_px), resample=Image.ANTIALIAS)
   #Save the image
   image.save(path)

if __name__ == "__main__":
   for i in range(10):
      generate_art(f"images/test_image_{i}.png")
