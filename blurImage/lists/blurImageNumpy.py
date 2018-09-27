from __future__ import division
from PIL import Image
import numpy as np


def getDimensionFromBlurryFactor(blurryFactor):
        if blurryFactor == 0:
                return 0
        if blurryFactor == 1:
                return 3
        else:
                return getDimensionFromBlurryFactor(blurryFactor - 1) + 2

def blurryPhoto(foto, blurryFactor, queue=None):
        minRow = 0
        maxRow = 0
        minColumn = 0
        maxColumn = 0
        fotoCopy = foto.copy()
        image2array = np.array(fotoCopy)
        kernelSize = getDimensionFromBlurryFactor(blurryFactor)
        for i in range(image2array.shape[0]):
                for j in range(image2array.shape[1]):
                        minRow = i - blurryFactor if i - blurryFactor >= 0 else 0
                        maxRow = i + blurryFactor + 1 if i + blurryFactor + 1 < image2array.shape[0] else image2array.shape[0]
                        minColumn = j - blurryFactor if j - blurryFactor >= 0 else 0
                        maxColumn = j + blurryFactor + 1 if j + blurryFactor + 1 < image2array.shape[1] else image2array.shape[1]
                        image2array[i, j] = np.mean(np.mean(image2array[minRow:maxRow, minColumn:maxColumn], axis=0),axis=0)
                status = "Calculating: {}%".format(int(i/image2array.shape[0]*100))
                print(status)
                if queue:
                    queue.put(status)
        array2image = Image.fromarray(image2array)
        if queue != None:
                queue.put("Done")
        
        return array2image

if __name__ == "__main__":
        import time
        blurryFactor = int(input('Insert blurr factor: '))
        #blurryFactor = 2
        start_time = time.time()
        print("Calculating...")
        foto = Image.open("test.jpeg")
        blurriedPhoto = blurryPhoto(foto, blurryFactor)
        print("--- %s seconds ---" % (time.time() - start_time))
        blurriedPhoto.show()
        
        
