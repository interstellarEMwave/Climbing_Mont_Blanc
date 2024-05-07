import numpy as np
import imageio

def main():
    
    image = np.zeros((81,81), dtype=np.uint8)
    image[40][40] = 255
    
    imageio.v2.imwrite("test_image_one_channel.png", image) 
main()
