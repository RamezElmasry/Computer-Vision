import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

original_img = Image.open('Test Image.jpg')


def CalculateColorMap(original_img):    
    color_map = {}
    data_mat = np.ones((original_img.size[1], original_img.size[0]), dtype= int)
    #print(data_mat.shape)
    count = 1
    for i in range(0, original_img.size[0]): #loop over columns(width) 700
        for j in range(0, original_img.size[1]): #loop over rows(height) 600
            r, g, b = original_img.getpixel((i,j))
            # if color exists in the colormap, get the value of the key and put it in the 
            # data matrix
            if (r,g,b) in color_map:
                data_mat[j,i] = color_map[(r,g,b)] # j: loops on the rows in the data matrix
                continue
            else:
                color_map[(r,g,b)] = count
                data_mat[j,i] = color_map[(r,g,b)] 
                count += 1

    return data_mat, color_map

def QuantizationLevels(color_map, range):
    new_color_map = {}
    removed_colors = {}
    # Take every color from the original color map and compare it with all new color map values
    for key, value in color_map.items():
        if len(new_color_map) == 0:
            new_color_map[key] = value
            continue
        similar = False
        # Get the difference between original color and all new color map values  
        for key2, value2 in new_color_map.items():    
            diff_R = abs(key[0] - key2[0])
            diff_G = abs(key[1] - key2[1])
            diff_B = abs(key[2] - key2[2])
            # If the difference is greater than the range, then the two colors are different
            # we continue until we find something thats similar that we can quantize at, if
            # that did not happen, its considered as a new value we can quantize at and add it to
            # the new color map.
            if diff_R > range or diff_G > range or diff_B > range:
                continue
            else:
                removed_colors[value] = value2
                similar = True
                break
        if not similar:
            new_color_map[key] = value

    return new_color_map, removed_colors
                        
def AdjustIndex(data_matrix, removed_colors):
    data_mat = data_matrix.copy()
    for i in range(data_mat.shape[0]):
        for j in range(data_mat.shape[1]):
            if data_mat[i,j] in removed_colors:
                data_mat[i,j] = removed_colors[data_mat[i,j]]
            else:
                continue

    return data_mat

def ReverseColorMap(new_color_map):
    reversed_color_map = {value : key for key, value in new_color_map.items()}
    return reversed_color_map


def ColorMapToImage(new_data_matrix, new_color_map):
    reconstructed_img = original_img.copy()
    for i in range(0, reconstructed_img.size[0]): #loop over columns(width) 700
        for j in range(0, reconstructed_img.size[1]): #loop over rows(height) 600
            key = new_data_matrix[j,i]
            color = new_color_map[key]
            reconstructed_img.putpixel((i,j), (color[0], color[1], color[2]))
    
    return reconstructed_img

print("Inside CalculateColorMap ")
data_matrix, color_map = CalculateColorMap(original_img)
print(len(color_map))
print("Inside QuantizationLevels ")
new_color_map, removed_colors = QuantizationLevels(color_map, 30)
print("Inside AdjustIndex ")
new_data_matrix = AdjustIndex(data_matrix, removed_colors)
print("Inside ReverseColorMap for new color map ")
rev_new_color_map = ReverseColorMap(new_color_map)
print("Inside ReverseColorMap for original color Map ")
rev_color_map = ReverseColorMap(color_map)
print("Inside original ColorMapToImage ")
reconstructed_img = ColorMapToImage(data_matrix, rev_color_map)
print("Inside ColorMapToImage after quantization ")
after_reconstructed_img = ColorMapToImage(new_data_matrix, rev_new_color_map)
print(len(rev_new_color_map))

#original image reconstructed from indexed image
plt.subplot(2,2,1)
plt.imshow(reconstructed_img)
#indexed image of the original image
plt.subplot(2,2,2)
plt.imshow(data_matrix, cmap = 'gray')
#image reconstructed after quantization by certain range
plt.subplot(2,2,3)
plt.imshow(after_reconstructed_img)
#indexed image of the quantized image by certain range
plt.subplot(2,2,4)
plt.imshow(new_data_matrix, cmap = 'gray')
#plt.savefig('Test_img_with_R30.jpg')
plt.show()         