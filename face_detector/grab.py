import cv2
import urllib
import numpy as np


def _grab_image(path=None, stream=None, url=None):
    if path is not None:
        image = cv2.imread(path)
    else:
        if url is not None:
            resp = urllib.request.urlopen(url)
            data = resp.read()
        elif stream is not None:
            data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image
