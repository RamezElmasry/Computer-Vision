import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

img = Image.open("f2.png")
gray = img.convert('L')
image_array = np.array(gray)
#print(image_array)

S_arr = np.empty((image_array.shape[0],image_array.shape[1]))
II_arr = np.empty((image_array.shape[0],image_array.shape[1]))

n = 330
ls = 0

def CalculateIntegral(img):
    #Calculate S
    sum = 0
    for i in range(0, img.shape[0]): #loop over rows(height)
        for j in range(0, img.shape[1]): #loop over cols(width)
            sum = sum + img[i,j]
            S_arr[i,j] = sum 
        sum = 0
    #print(S_arr)

    #calculate II
    for i in range(0, img.shape[1]): #loop over cols
        for j in range(0, img.shape[0]): #loop over rows
            sum = sum + S_arr[j,i]
            II_arr[j,i] = sum
        sum = 0
    #((top,bottom),(left,right))
    #II_arr_paded = np.pad(II_arr,((1,0),(1,0)))
    #print(II_arr)
    #print(II_arr_paded)
    return II_arr

def CalculateLocalSum(integral_img, p0, p1):
    #print(p1)
    ls = integral_img[p1]
    s = 0
    # check on borders
    if(p0[0]!= 0):
        ls -= integral_img[p0[0]-1, p1[1]]
        s+=1

    if(p0[1] != 0):
        ls -= integral_img[p1[0], p0[1]-1]
        s+=1

    if(s == 2):
        ls += integral_img[p0[0]-1, p0[1]-1]

    return ls

def DetectEye(integral_img, n):
    score = 0
    max = 0
    max_pos = ()
    m = round(0.15*n)

    
    p1 = (round(-0.5*m), round(-0.5*n))
    p2 = (0, round(-0.05*n))
    p3 = (0, round(-0.5*n))
    p4 = (round(0.5*m), round(-0.05*n))
    p5 = (round(-0.5*m), round(0.05*n))
    p6 = (0, round(0.5*n))
    p7 = (0, round(0.05*n))
    p8 = (round(0.5*m), round(0.5*n))
    p9 = (round(0.833*m), round(-0.325*n))
    p10 = (round(2*m), round(-0.225*n))
    p11 = (round(0.833*m), round(-0.1*n))
    p12 = (round(2*m),round(0.1*n))
    p13 = (round(0.833*m), round(0.225*n))
    p14 = (round(2*m), round(0.325*n))

    ref_p1,ref_p2,ref_p3,ref_p4,ref_p5,ref_p6,ref_p7,ref_p8,ref_p9,ref_p10,ref_p11,ref_p12,ref_p13,ref_p14 = (),(),(),(),(),(),(),(),(),(),(),(),(),()
    
    for i in range((-1*p1[0]), integral_img.shape[0]-p14[0]): #loop over rows(height)
        #if count == 1:
        #    break
        for j in range(-1*p1[1], integral_img.shape[1]-p8[1]): #loop over cols(width)
            #print((i,j))
            #if count == 1:
            #    break
            ref_p1 = (i + p1[0], j + p1[1])
            ref_p2 = (i + p2[0], j + p2[1])
            ref_p3 = (i + p3[0], j + p3[1])
            ref_p4 = (i + p4[0], j + p4[1])
            ref_p5 = (i + p5[0], j + p5[1])
            ref_p6 = (i + p6[0], j + p6[1])
            ref_p7 = (i + p7[0], j + p7[1])
            ref_p8 = (i + p8[0], j + p8[1])
            ref_p9 = (i + p9[0], j + p9[1])
            ref_p10 = (i + p10[0], j + p10[1])
            ref_p11 = (i + p11[0], j + p11[1])
            ref_p12 = (i + p12[0], j + p12[1])
            ref_p13 = (i + p13[0], j + p13[1])
            ref_p14 = (i + p14[0], j + p14[1])
            Ls1 = CalculateLocalSum(integral_img, ref_p1, ref_p2)
            Ls2 = (-1) * (CalculateLocalSum(integral_img, ref_p3, ref_p4))
            Ls3 = CalculateLocalSum(integral_img, ref_p5, ref_p6)
            Ls4 = (-1) * (CalculateLocalSum(integral_img, ref_p7, ref_p8))
            Ls5 = (-1) * (CalculateLocalSum(integral_img, ref_p9, ref_p10))
            Ls6 = CalculateLocalSum(integral_img, ref_p11, ref_p12)
            Ls7 = (-1) * (CalculateLocalSum(integral_img, ref_p13, ref_p14))
            score = Ls1 + Ls2 + Ls3 + Ls4 + Ls5 + Ls6 + Ls7
            if score > max:
                max = score
                max_pos = (i,j)
           
    return max_pos

def ExtractDetectedEye(image_array, max_pos, n):
    m = 0.15 * n
    top_left_y = max_pos[0] + round(-0.5*m)
    bottom_right_y = max_pos[0] + round(2*m)
    top_left_x = max_pos[1] + round(-0.5*n)
    bottom_right_x = max_pos[1] + round(0.5*n)
    result = np.empty((image_array.shape[0],image_array.shape[1]))
    print(top_left_y, bottom_right_y, top_left_x, bottom_right_x)
    result[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = image_array[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    return result    


integral_img = CalculateIntegral(image_array)
max_position = DetectEye(integral_img, n)
Extracted_area = ExtractDetectedEye(image_array, max_position, n)
plt.imshow(Extracted_area, cmap = 'gray')
plt.show()
#CalculateIntegral(image_array) (2,3) (row no., col no.) (0,3)
#print(integral_img.shape)
#print(max_position)