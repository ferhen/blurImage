
from __future__ import division
from PIL import Image

def getDimensionFromBlurryFactor(blurryFactor):
        if blurryFactor == 0:
                return 0
        if blurryFactor == 1:
                return 3
        else:
                return getDimensionFromBlurryFactor(blurryFactor - 1) + 2

def blurryPhoto(foto, blurryFactor, queue=None):
        fotoCopy = foto.copy()
        fotoLoad = fotoCopy.load()
        kernelSize = getDimensionFromBlurryFactor(blurryFactor)
        for i in range(foto.size[0]):
                for j in range(foto.size[1]):
                        redKernelColorSum = 0
                        greenKernelColorSum = 0
                        blueKernelColorSum = 0
                        count = 0
                        for iKernel in range(kernelSize):
                                for jKernel in range(kernelSize):
                                        if i - blurryFactor + iKernel >= 0 and i - blurryFactor + iKernel < fotoCopy.size[0] and j - blurryFactor + jKernel >=0 and j - blurryFactor + jKernel < fotoCopy.size[1]:
                                                redKernelColorSum += fotoLoad[i - blurryFactor + iKernel, j - blurryFactor + jKernel][0]
                                                greenKernelColorSum += fotoLoad[i - blurryFactor + iKernel, j - blurryFactor + jKernel][1]
                                                blueKernelColorSum += fotoLoad[i - blurryFactor + iKernel, j - blurryFactor + jKernel][2]
                                                count = count + 1
                        redKernelAverage = int(redKernelColorSum / count)
                        greenKernelAverage = int(greenKernelColorSum / count)
                        blueKernelAverage = int(blueKernelColorSum / count)
                        fotoLoad[i,j] = (redKernelAverage, greenKernelAverage, blueKernelAverage)

                status = "Calculating: {}%".format(int(i/fotoCopy.size[0]*100))
                print(status)
                if queue:
                    queue.put(status)
        queue.put("Done")
        return fotoCopy

if __name__ == "__main__":
        blurryFactor = int(input('Insert blurr factor: '))
        print("Calculating...")
        foto = Image.open("test.jpeg")

        blurriedPhoto = blurryPhoto(foto, blurryFactor)
        blurriedPhoto.show()
