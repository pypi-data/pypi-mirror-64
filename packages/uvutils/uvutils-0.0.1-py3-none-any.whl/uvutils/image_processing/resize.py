import numpy as np
from PIL import Image
from .utils import float_to_png


def resize(images, target=(32, 32), filter=Image.LANCZOS):
    """
    Resize images from one set of dimensions to another

    :param images: Set of images to be resized
    :type images: `list or ndarray`
    :param target: Target dimensions
    :type target: `(int, int)`
    :param filter: Image resampling filter
    :type filter: `PIL.Image.[NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS]`
    :return: Images after being resampled to `target` size.
    :rtype: `np.ndarray`
    """
    if not isinstance(images, np.ndarray):
        images = np.array(images)

    images_type = images.dtype.type

    if images_type not in [np.float32, np.float64, np.uint8]:
        raise TypeError(
            f"Must be float32, float64, or uint8, not {images_type}")

    if images_type in [np.float32, np.float64]:
        np.clip(images, a_min=0., a_max=1., out=images)
        images = float_to_png(images)

    resized_images = np.array([
        np.asarray(Image.fromarray(image, "RGB").resize(target, filter))
        for image in images
    ])

    if images_type in [np.float32, np.float64]:
        resized_images = resized_images.astype(images_type, copy=False)
        resized_images /= 255

    return resized_images
