from django.conf import settings
import tempfile
from PIL import Image
from django.core.files.images import ImageFile


def to_camelcase(snake_str):
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def get_social_sharable_image(image_obj, filename):
    # Read image
    image = Image.open(image_obj)

    # Create a social sharable image
    image_width, image_height = image.size
    og_image = Image.new('RGB', (1200, 630), 'black')
    og_image_image_height, og_image_image_width = og_image.size
    offset = ((og_image_image_height - image_width) // 2, (og_image_image_width - image_height) // 2)
    og_image.paste(image, offset)

    # Upload image

    image_obj = tempfile.TemporaryFile(dir=settings.TEMP_DIR)
    og_image.save(image_obj, 'PNG')

    # Return image file obj
    return ImageFile(image_obj)
