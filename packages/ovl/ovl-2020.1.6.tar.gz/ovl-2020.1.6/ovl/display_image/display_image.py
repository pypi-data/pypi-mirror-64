import cv2
from numpy import vstack, hstack, ndarray

WINDOWS = []


def stitch_images(images):
    width, height = images[0].shape
    stitched_image = cv2.imread(images[0]) if type(images[0]) is str else images[0]
    for image in images[1:]:
        if type(image) is str:
            image = cv2.imread(image)
        image_shape = image.shape
        if width + image_shape[0] > height + image_shape[1]:
            stitched_image = vstack((stitched_image, image))
            width += image_shape[0]
        else:
            stitched_image = hstack((stitched_image, image))
            height += image_shape[1]
    return stitched_image


def show_image(image, window_name, delay):
    cv2.imshow(window_name, image)
    pressed_key = cv2.waitKey(delay)
    return pressed_key


def display_image(image, window_name='image', delay=0, resizable=False):
    """
     The function displays the image whose path is received.
    :param image: Represents an image path (string), an already open image in the for of a numpy array (ndarray)
                  or a list of images (strings and arrays are valid)
    :param window_name: Name of the Window that displays the images
    :param delay: The delay before the image stops
    :param resizable: A boolean that determines whether the image window is resizable or not
    :return: the key pressed while image was displayed
    """
    if type(image) is str:
        image = cv2.imread(image)
    elif type(image) is list:
        image = stitch_images(image)
    elif type(image) is not ndarray:
        raise TypeError("Invalid image given, image must be an image, a path to an image or a list of images")

    if resizable:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    return show_image(image, window_name, delay)


