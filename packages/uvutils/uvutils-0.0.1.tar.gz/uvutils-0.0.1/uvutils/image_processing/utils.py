import numpy as np
from cv2 import imencode, imdecode, IMWRITE_JPEG_QUALITY


def float_to_png(images):
    """
    Convert images from [0, 1] (float) to [0, 255] (uint8).

    :param images: Set of images to be converted
    :type images: `list or ndarray`
    :return: Images after being converted to PNGs.
    :rtype: `np.ndarray`
    """

    if not isinstance(images, np.ndarray):
        images = np.array(images)

    images_type = images.dtype.type

    if images_type not in [np.float32, np.float64]:
        raise TypeError(f"Must be float32 or float64, not {images_type}")

    np.clip(images, a_min=0., a_max=1., out=images)

    images *= 255

    return images.astype(np.uint8)


def png_to_jpg(images, quality=75):
    """
    Convert images from png to jpg.

    :param images: Set of images to be converted
    :type images: `list or ndarray`
    :param quality: Quality of resulting JPEGs
    :type quality: `int`
    :return: Images after being compressed as JPEGs.
    :rtype: `np.ndarray`
    """

    if not isinstance(images, np.ndarray):
        images = np.array(images)

    images_type = images.dtype.type

    if images_type != np.uint8:
        raise TypeError(f"Must be uint8, not {images_type}")

    params = [int(IMWRITE_JPEG_QUALITY), quality]
    return np.array([
        imdecode(imencode('.jpg', image, params)[1], -1)
        for image in images
    ])


def png_to_float(images):
    """
    Convert images from png to float.

    :param images: Set of images to be converted
    :type images: `list or ndarray`
    :return: Images after being normalized.
    :rtype: `np.ndarray`
    """

    if not isinstance(images, np.ndarray):
        images = np.array(images)

    images_type = images.dtype.type

    if images_type != np.uint8:
        raise TypeError(f"Must be uint8, not {images_type}")

    images = images.astype('float32')
    images /= 255

    return images
