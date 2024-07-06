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
        outImages.append(blurSummedAreaTableAsSections(imageBuffers, kernels[i], iterations))

    print(len(outImages))
    print("Done")

    fig2, ax = plt.subplots(5, 1, figsize=(10, 10*5))
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

def makeSeparation(imageIn, kernel):
    imageHeight = len(imageIn)
    imageWidth = len(imageIn[0])
    kernelWidth = kernel*2 + 1
    out = []

    for i in range(kernelWidth):
        out.append([])
        for j in range(kernelWidth):
            out[i].append(np.zeros(((imageHeight+4*kernel)//kernelWidth, (imageWidth+4*kernel)//kernelWidth), dtype = np.float32))

    for i in range(imageHeight + kernelWidth - 1):
        for j in range(imageWidth + kernelWidth - 1):
            out[i%kernelWidth][j%kernelWidth][i//kernelWidth][j//kernelWidth] = imageIn[min(i, imageHeight - 1)][min(j, imageWidth-1)]

    return out


def blurSummedAreaTableAsSections(imageBuffers, kernel, iterations):
    print("-"*100)
    print("blurring with kernel:", kernel)
    print("-"*100)

    bufferY = len(imageBuffers[0])
    bufferX = len(imageBuffers[0][0])

    cursorIn = 0
    cursorOut = 1

    for it in range(iterations):
        imageBuffers[cursorIn] = makeSummedAreaTable(imageBuffers[cursorIn]) 
        image = makeSeparation(imageBuffers[cursorIn], kernel)

        for y1 in range(2*kernel + 1):
            for x1 in range(2*kernel + 1):
                blurSection(image, imageBuffers[cursorOut], kernel, y1, x1)

        cursorIn = cursorOut
        cursorOut = abs(cursorIn-1)

    outImage = np.zeros(imageBuffers[0].shape, dtype=np.uint8)
    for i in range(bufferY):
        for j in range(bufferX):
            outImage[i][j] = np.uint8(imageBuffers[cursorIn][i][j])

    return outImage

def blurSection(image, outImage, kernel, y1, x1):
    outImageHeight = len(outImage)
    outImageWidth = len(outImage[0])
    kernelWidth = 2*kernel + 1

    for y2 in range(1-(y1+1)//(kernel+1), (outImageHeight+3*kernel-y1)//kernelWidth):
        for x2 in range(1-(x1+1)//(kernel+1), (outImageWidth+3*kernel-x1)//kernelWidth):
            out = image[y1][x1][y2][x2]
            if(y2 > 0 and x2 > 0):
                out += image[y1][x1][y2-1][x2-1]
            if(y2 > 0):
                out -= image[y1][x1][y2-1][x2]
            if(x2 > 0):
                out -= image[y1][x1][y2][x2-1]

            divisor = min(kernelWidth,y2*kernelWidth + y1 + 1, outImageHeight - y2*kernelWidth - y1 +2*kernel) * min(kernelWidth, x2*kernelWidth + x1 + 1, outImageWidth - x2*kernelWidth - x1 + 2*kernel);
            outImage[y2*kernelWidth + y1 - kernel][x2*kernelWidth + x1 - kernel] = out/float(divisor)

  


main()
