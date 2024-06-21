import numpy as np
import imageio
import random

def make_test_image():
    
    image = np.zeros((81,81), dtype=np.uint8)
    
    #for i in range(81):
    #    for j in range(81):
    #        image[i][j] = np.random.randint(0, 255)

    rad = 15
    for i in range(81):
        for j in range(81):
            if((40-i)**2 + (40-j)**2 < rad**2):
                image[i][j] = 255

    imageio.v2.imwrite("test_image_one_channel.png", image)
    return image
