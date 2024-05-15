from matplotlib import pyplot as plt
import numpy as np
import imageio

def main():
    
    #tempImage = imageio.v2.imread("./test_image_one_channel.png")
    tempImage = make_test_image()
    
    kernels = [2, 3, 5, 8]
    iterations = 5
       
    imageBuffers = []
    imageBuffers.append(np.zeros(tempImage.shape))
    imageBuffers.append(np.zeros(tempImage.shape))

    outImages = []
    for i in range(len(kernels)):
        imageBuffers[0] = np.copy(tempImage)
        outImages.append(blurSummedAreaTable(imageBuffers, kernels[i], iterations))

    print(len(outImages))
    print("Done")

    fig, ax = plt.subplots(5, 1, figsize=(10, 10*5))
    ax[0].imshow(tempImage)
    for i in range(len(outImages)):
        ax[i+1].imshow(outImages[i])

def makeSummedAreaTable(imageIn):
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

def blurSummedAreaTable(imageBuffers, kernel, iterations):
    print("-"*100)
    print("blurring with kernel:", kernel)
    print("-"*100)

    bufferY = len(imageBuffers[0])
    bufferX = len(imageBuffers[0][0])
    
    cursorIn = 0
    cursorOut = 1
    for it in range(iterations):
        imageBuffers[cursorIn] = makeSummedAreaTable(imageBuffers[cursorIn]) 
        for i in range(bufferY):
            for j in range(bufferX):
                imageBuffers[cursorOut][i][j] = blurStep(imageBuffers[cursorIn], kernel, i, j)
        
        cursorIn = cursorOut
        cursorOut = abs(cursorIn-1)
    
    outImage = np.zeros(imageBuffers[0].shape, dtype=np.uint8)
    for i in range(bufferY):
        for j in range(bufferX):
            outImage[i][j] = np.uint8(imageBuffers[cursorIn][i][j])
    
    return outImage



def blurStep(bufferIn, kernel, y, x):
    ymin = y - kernel - 1
    xmin = x - kernel - 1
    ymax = min(y+kernel, len(bufferIn)-1)
    xmax = min(x+kernel, len(bufferIn[0])-1)
    
    dividend = bufferIn[ymax][xmax]

    if not (ymin < 0 or xmin < 0):
        dividend += bufferIn[ymin][xmin] 
    if not (xmin < 0):
        dividend -= bufferIn[ymax][xmin] 
    if not (ymin < 0):
        dividend -= bufferIn[ymin][xmax];

    divisor = min(2*kernel+1, kernel + 1 + y, len(bufferIn) - y + kernel) * min(2*kernel+1, kernel + 1 + x, len(bufferIn) - x + kernel);
  
    return dividend/float(divisor)  



main()
