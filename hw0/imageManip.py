import math
import numpy as np
from PIL import Image
from skimage import io
from skimage.color import rgb2gray, rgb2lab, rgb2hsv


def load(image_path):
    """Loads an image from a file path.

    HINT: Look up `skimage.io.imread()` function.

    Args:
        image_path: file path to the image.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    # YOUR CODE HERE
    # Use skimage io.imread
    out = io.imread(image_path)
    print(out)
    # END YOUR CODE

    # Let's convert the image to be between the correct range.
    out = out.astype(np.float64) / 255
    return out


def dim_image(image):
    """Change the value of every pixel by following

                        x_n = 0.5*x_p^2

    where x_n is the new value and x_p is the original value.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    out = None

    # YOUR CODE HERE
    out = 0.5 * np.square(image)
    # END YOUR CODE

    return out


def convert_to_grey_scale(image):
    """Change image to gray scale.

    HINT: Look at `skimage.color` library to see if there is a function
    there you can use.

    Args:
        image: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    # YOUR CODE HERE
    out = rgb2gray(image)
    # END YOUR CODE

    return out


def rgb_exclusion(image, channel):
    """Return image **excluding** the rgb channel specified

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "R", "G" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    # YOUR CODE HERE
    RGB = ['R', 'G', 'B']
    out = image.copy()
    out[..., RGB.index(channel)] = 0

    # END YOUR CODE

    return out


def lab_decomposition(image, channel):
    """Decomposes the image into LAB and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "L", "A" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    lab = rgb2lab(image)

    # YOUR CODE HERE
    LAB = ['L', 'A', 'B']
    out = lab[..., LAB.index(channel)]
    # END YOUR CODE

    return out


def hsv_decomposition(image, channel):
    """Decomposes the image into HSV and only returns the channel specified.

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "H", "S" or "V".

    Returns:
        out: numpy array of shape(image_height, image_width).
    """

    hsv = rgb2hsv(image)

    # YOUR CODE HERE
    HSV = ['H', 'S', 'V']
    out = hsv[..., HSV.index(channel)]

    # END YOUR CODE

    return out


def mix_images(image1, image2, channel1, channel2):
    """Combines image1 and image2 by taking the left half of image1
    and the right half of image2. The final combination also excludes
    channel1 from image1 and channel2 from image2 for each image.

    HINTS: Use `rgb_exclusion()` you implemented earlier as a helper
    function. Also look up `np.concatenate()` to help you combine images.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).
        image2: numpy array of shape(image_height, image_width, 3).
        channel1: str specifying channel used for image1.
        channel2: str specifying channel used for image2.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    # YOUR CODE HERE
    image1 = rgb_exclusion(image1, channel1)
    image2 = rgb_exclusion(image2, channel2)
    height, width, _ = image1.shape
    cut = width // 2
    s1 = image1[:, :cut]
    s2 = image2[:, cut:]
    out = np.concatenate((s1, s2), axis=1)

    # END YOUR CODE

    return out


def mix_quadrants(image):
    """THIS IS AN EXTRA CREDIT FUNCTION.

    This function takes an image, and performs a different operation
    to each of the 4 quadrants of the image. Then it combines the 4
    quadrants back together.

    Here are the 4 operations you should perform on the 4 quadrants:
        Top left quadrant: Remove the 'R' channel using `rgb_exclusion()`.
        Top right quadrant: Dim the quadrant using `dim_image()`.
        Bottom left quadrant: Brighthen the quadrant using the function:
            x_n = x_p^0.5
        Bottom right quadrant: Remove the 'R' channel using `rgb_exclusion()`.

    Args:
        image1: numpy array of shape(image_height, image_width, 3).

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """

    # YOUR CODE HERE
    upper_half = np.hsplit(np.vsplit(image, 2)[0], 2)
    lower_half = np.hsplit(np.vsplit(image, 2)[1], 2)

    top_left = rgb_exclusion(upper_half[0], 'R')
    top_right = dim_image(upper_half[1])
    bottom_left = lower_half[0]**0.5
    bottom_right = rgb_exclusion(lower_half[1], 'R')

    out = np.vstack([np.hstack([top_left, top_right]), np.hstack([bottom_left, bottom_right])])
    # END YOUR CODE

    return out
