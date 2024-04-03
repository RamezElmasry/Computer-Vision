import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

img = Image.open("5.jpg")
img = img.convert('L')

#image_array = np.array(img)
#value, counts = np.unique(image_array, return_counts=True)
#print("from np:", counts)

def CalculateHistogram(img):
    histogram_values = []
    histogram_counts = []
    count = 0

    for pixel in img.getdata():
        if pixel not in histogram_values:
            histogram_values.append(pixel)
    histogram_values.sort()

    for value in histogram_values:
        for i in range(0, img.size[0]): #loop over columns(width) 
            for j in range(0, img.size[1]): #loop over rows(height)
                v = img.getpixel((i,j))
                if value == v:
                    count += 1
                else:
                    continue
        histogram_counts.append(count)
        count = 0
    
    return histogram_counts
    
def CalculateCumulativeHistogram(histogram_counts):
    cumulative_sum = 0
    cumulative_histogram = []

    for value in histogram_counts:
        cumulative_sum += value
        cumulative_histogram.append(cumulative_sum)

    return cumulative_histogram

def CalculateEqualizedHistogram(cumulative_histogram):
    n = img.size[1]
    m = img.size[0]
    new_values = []
    new = 0

    for value in cumulative_histogram:
        new = abs(round((255 / (n*m)-cumulative_histogram[0]) * (value - cumulative_histogram[0])))
        new_values.append(new)

    return new_values

def CalculateEqualizedImage(img, new_values):
    result = np.empty((img.size[1], img.size[0]), dtype=np.int64)
    #result = img.copy()
    histogram_values = []
    
    for pixel in img.getdata():
        if pixel not in histogram_values:
            histogram_values.append(pixel)
    histogram_values.sort()

    k = 0
    for value in histogram_values:
        for i in range(0, img.size[0]): 
            for j in range(0, img.size[1]):
                v = img.getpixel((i,j))
                if value == v:
                    result[j,i] = new_values[k]
        k += 1

    return result

def SegmentOptimalThresholding(img):
    result = img.copy()
    thresh = 0
    new_thresh = 0
    b_p = []
    f_p = []
    m_f = 0
    k = 0
    if type(img).__module__ == Image.__name__:
        while True:
            if k == 0:
                top_left = img.getpixel((0,0))
                top_right = img.getpixel((img.size[0]-1, 0))
                bottom_left = img.getpixel((0 ,img.size[1]-1))
                bottom_right = img.getpixel((img.size[0]-1, img.size[1]-1))
                m_b = (top_left + bottom_left + top_right + bottom_right) / 4
                for i in range(0, img.size[0]): #loop over columns(width) 
                        for j in range(0, img.size[1]): #loop over rows(height)
                            v = img.getpixel((i,j))
                            if v == top_left or v == top_right or v == bottom_left or v == bottom_right:
                                result.putpixel((i,j), 0)
                                continue
                            else:
                                result.putpixel((i,j), 1)
                                f_p.append(v)
        
                m_f = sum(f_p)/len(f_p)
                thresh = (m_f + m_b)/2
                f_p = []
                k+=1

            else:
                for i in range(0, img.size[0]): #loop over columns(width)
                    for j in range(0, img.size[1]): #loop over rows(height)
                        v = img.getpixel((i,j))
                        if v < thresh:
                            result.putpixel((i,j), 0)
                            b_p.append(v)
                        else:
                            result.putpixel((i,j), 1)
                            f_p.append(v)
                
                m_b = sum(b_p)/len(b_p)
                m_f = sum(f_p)/len(f_p)
                new_thresh = (m_b + m_f)/2
                if new_thresh == thresh:
                    break
                else:
                    thresh = new_thresh
                    b_p = []
                    f_p = []
                    k+=1
    else:
        while True:
            if k == 0:
                top_left = img[0,0]
                top_right = img[img.shape[0]-1, 0]
                bottom_left = img[0 ,img.shape[1]-1]
                bottom_right = img[img.shape[0]-1, img.shape[1]-1]
                m_b = (top_left + bottom_left + top_right + bottom_right) / 4
                #print(top_left,top_right,bottom_left,bottom_right)
                for i in range(0, img.shape[0]):  
                        for j in range(0, img.shape[1]): 
                            v = img[i,j]
                            if v == top_left or v == top_right or v == bottom_left or v == bottom_right:
                                result[i,j] = 0
                                continue
                            else:
                                result[i,j] = 1
                                f_p.append(v)
                #print(m_f,m_b)
                #print(len(f_p),len(b_p))
                m_f = sum(f_p)/len(f_p)
                thresh = (m_f + m_b)/2
                f_p = []
                k+=1
            else:
                for i in range(0, img.shape[0]): 
                    for j in range(0, img.shape[1]): 
                        v = img[i,j]
                        if v < thresh:
                            result[i,j] = 0
                            b_p.append(v)
                        else:
                            result[i,j] = 1
                            f_p.append(v)

                print(m_f,m_b)
                print(len(f_p),len(b_p))
                m_b = sum(b_p)/len(b_p)
                m_f = abs(sum(f_p)/len(f_p))
                new_thresh = (m_b + m_f)/2
                if new_thresh == thresh:
                    break
                else:
                    thresh = new_thresh
                    b_p = []
                    f_p = []
                    k+=1

    return result


segmented_img = SegmentOptimalThresholding(img)
count = CalculateHistogram(img)
cumulative = CalculateCumulativeHistogram(count)
new_values = CalculateEqualizedHistogram(cumulative)
equalized_img = CalculateEqualizedImage(img, new_values)

norm = np.linalg.norm(equalized_img)
equalized_img1 = equalized_img/norm
segmented_img1 = SegmentOptimalThresholding(equalized_img1)

#original image
plt.subplot(2,2,1)
plt.imshow(img, cmap = 'gray')
plt.title('Original Image')
#segmentation of original image
plt.subplot(2,2,2)
plt.imshow(segmented_img, cmap = 'gray')
plt.title('Segmenting Original Image')
#Equalized image 
plt.subplot(2,2,3)
plt.imshow(equalized_img, cmap = 'gray')
plt.title('Equalized Image')
#segmentation of equalized image
plt.subplot(2,2,4)
plt.imshow(segmented_img1, cmap = 'gray')
plt.title('Segmented Equalized Image')
plt.show()