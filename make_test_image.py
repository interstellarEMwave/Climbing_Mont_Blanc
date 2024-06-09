import numpy as np
import imageio
import random

def main():
    
    image = np.zeros((81,81), dtype=np.uint8)
    for i in range(len(image)):
        for j in range(len(image)):
            image[i][j] = random.randint(0, 255)

    imageio.v2.imwrite("test_image_one_channel.png", image) 
main()
