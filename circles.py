from PIL import ImageDraw, Image
import random
from time import time

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
DEFAULT_RADIUS = 800
DEFAULT_LINE_WIDTH = 1


class FunctionTypes:
    CIRCLE_ONE = 0
    CIRCLE_MANY = 1
    FUNC_TYPES = (CIRCLE_ONE, CIRCLE_MANY)


class ProcessType:
    save_images = 0
    show_one_image = 1


# if you want to save your images then change PROCESS_TYPE to "save_images"
# and change the output path
PROCESS_TYPE = ProcessType.show_one_image
LOOPS = 20
OUTPUT_PATH = "/images"


def random_hex() -> str:
    def r(): return random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


class Circle:
    def __init__(
            self, x: int, y: int, radius: float,
            outline_color: str, line_width: int = DEFAULT_LINE_WIDTH) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.outline_color = outline_color
        self.line_width = line_width

    def draw(self):
        image_draw.ellipse(
            xy=(
                (self.x - self.radius, self.y - self.radius),
                (self.x + self.radius, self.y + self.radius)
            ),
            outline=self.outline_color,
            width=self.line_width
        )


def draw_circle_one(
        x: int, y: int, radius: float, radius_min: int, radius_change: float,
        circle_line_width: int, circle_line_color: str):

    Circle(
        x=x, y=y, radius=radius, line_width=circle_line_width,
        outline_color=circle_line_color).draw()

    if radius > radius_min:
        radius = radius * radius_change
        draw_circle_one(
            x=x, y=y, radius=radius, radius_min=radius_min, radius_change=radius_change,
            circle_line_width=circle_line_width, circle_line_color=circle_line_color)


def draw_circle_many(
        x: int, y: int, radius: float, circle_line_width: int, circle_line_color: str,
        radius_div: int, radius_max: int, axis: int):

    Circle(
        x=x, y=y, radius=radius, line_width=circle_line_width,
        outline_color=circle_line_color).draw()

    new_radius = int(radius / radius_div)

    circle_params_x = (
        (x + new_radius, y, new_radius),
        (x - new_radius, y, new_radius),
    )

    circle_params_y = (
        (x, y + new_radius, new_radius),
        (x, y - new_radius, new_radius),
    )

    circle_params_x_y = (
        (x + new_radius, y + new_radius, new_radius),
        (x - new_radius, y - new_radius, new_radius),
    )

    circle_params = [*circle_params_x, *circle_params_y, *circle_params_x_y]

    if radius > radius_max:
        for x, y, radius in circle_params[:axis]:
            draw_circle_many(
                x=x, y=y, radius=radius, circle_line_width=circle_line_width,
                circle_line_color=circle_line_color, radius_div=radius_div,
                radius_max=radius_max, axis=axis)


for img in range(LOOPS):
    image = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), random_hex())
    image_draw = ImageDraw.Draw(image)

    func_type = random.choice(FunctionTypes.FUNC_TYPES)
    label = str(time()).replace('.', '_')

    if func_type == FunctionTypes.CIRCLE_ONE:
        draw_circle_one(
            x=int(IMAGE_WIDTH/4),
            y=int(IMAGE_HEIGHT/4),
            radius=random.randint(int(IMAGE_WIDTH/4), IMAGE_WIDTH),
            radius_min=random.randint(1, 100),
            radius_change=random.uniform(0.8, 0.99),
            circle_line_width=random.randint(1, 100),
            circle_line_color=random_hex()
        )
    elif func_type == FunctionTypes.CIRCLE_MANY:
        draw_circle_many(
            x=int(IMAGE_WIDTH / 4),
            y=int(IMAGE_HEIGHT / 4),
            radius=random.randint(int(IMAGE_WIDTH/2), IMAGE_WIDTH),
            circle_line_width=random.randint(1, 3),
            circle_line_color=random_hex(),
            radius_div=random.choice([2, 4]),
            radius_max=random.randint(7, 20),
            axis=random.choice([2, 4, 6])
        )

    if PROCESS_TYPE == ProcessType.show_one_image:
        image.show()
        break
    elif PROCESS_TYPE == ProcessType.save_images:
        image.save(f"{OUTPUT_PATH}/{label}_{img}.png")