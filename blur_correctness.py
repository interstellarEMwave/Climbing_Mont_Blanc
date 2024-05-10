from matplotlib import pyplot as plt
import numpy as np
import imageio

def main():
    
    tempImage = imageio.v2.imread("./test_image_one_channel.png")
    image = makeAverageSumTable(tempImage)

    kernels = [2, 3, 5, 8]
    iterations = 5
       
    imageBuffers = []
    imageBuffers.append(np.zeros(image.shape))
    imageBuffers.append(np.zeros(image.shape))

    outImages = []
    for i in range(len(kernels)):
        imageBuffers[0] = np.copy(image)
        outImages.append(naiveBlur(imageBuffers, kernels[i], iterations))

    print(len(outImages))
    print("Done")

    fig, ax = plt.subplots(5, 1, figsize=(10, 10*5))
    ax[0].imshow(image)
    for i in range(len(outImages)):
        ax[i+1].imshow(outImages[i])

def makeAverageSumTable(imageIn):
    imageOut = np.zeros(imageIn.shape, dtype = np.float32)
    for i in range(len(imageIn)):
        for j in range(len(imageIn[0])):
            imageOut[i][j] = imageIn[i][j]
            if(i > 0):
                imageOut[i][j] += imageOut[i-1][j]
            if(j > 0):
                imageOut[i][j] += imageOut[i][j-1]
            if(i > 0 and j > 0):
                imageOut[i][j] -= imageOut[i-1][j-1]
    
    return imageOut

def naiveBlur(imageBuffers, kernel, iterations):
    print("-"*100)
    print("blurring with kernel:", kernel)
    print("-"*100)

    bufferY = len(imageBuffers[0])
    bufferX = len(imageBuffers[0][0])
    
    cursorIn = 0
    cursorOut = 1
    for it in range(iterations):
        for i in range(bufferY):
            for j in range(bufferX):
                imageBuffers[cursorOut][i][j] = naiveBlurStep(imageBuffers[cursorIn], kernel, i, j)
        
        cursorIn = cursorOut
        cursorOut = abs(cursorIn-1)
    
    outImage = np.zeros(imageBuffers[0].shape, dtype=np.uint8)
    for i in range(bufferY):
        for j in range(bufferX):
            outImage[i][j] = np.uint8(imageBuffers[cursorIn][i][j])
    
    return outImage



def naiveBlurStep(bufferIn, kernel, y, x): 
    dividend = 0 
    divisor = 0

    for i in range(max(y-kernel, 0), min(y+kernel+1, len(bufferIn))):
        for j in range(max(x-kernel, 0), min(x+kernel+1, len(bufferIn[0]))):
            dividend += bufferIn[i][j]
            divisor += 1

    return dividend/float(divisor)  



main()
