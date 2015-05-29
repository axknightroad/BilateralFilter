#!/usr/bin/python
# -*- coding:utf-8 -*-

# bilateral filter for python
# code by HanJianan
# 2015.5

import Image
import math
from time import clock

FACTOR = -0.5    #defualt factor
DS = 3.0    #defualt distance sigma
DR = 30.0    #defualt range sigma  
RADIUS = int(max(DS,DR))    #defualt radius
time0 = clock()    #start time


class BilateralFilter(object):
    """ the bilateral filter class here.

It can build distance weight table and similarity weight table,
load image, and filting it with these two table, then return the filted image.

Attributes:
    factor: the factor of power of e.
    ds: distance sigma, which denominator of delta in c.
    rs: range sigma, which denominator of delta in s.
    c_weight_table: the gaussian weight table of Euclidean distance, 
which namly c.
    s_weight_table: the gaussian weight table of The similarity function, 
which namly s.
    radius: half length of Gaussian kernel.
"""

    def __init__(self, factor, ds, rs, radiu):
        """init the bilateral filter class with the input args"""
        self.factor = factor
        self.ds = ds
        self.rs = rs
        self.c_weight_table = []
        self.s_weight_table = []
        self.radius = radiu

    def build_distance_weight_table(self):
        """bulid the c_weight_table with radius and ds"""
        size = 2 * self.radius + 1
        for semi_row in range(-self.radius,self.radius+1):
            self.c_weight_table.append([])
            for semi_col in range(-self.radius,self.radius+1):
                # calculate Euclidean distance between center point and close pixels
                delta = (math.sqrt(semi_row * semi_row + semi_col * semi_col)
                         / self.ds)
                delta_mult_delta = delta * delta
                self.c_weight_table[semi_row+self.radius].append(
                    math.exp(delta_mult_delta * self.factor))

    def build_similarity_weight_table(self):
        """build the s_weight_table with rs"""
        for i in range(256): # since the color scope is 0 ~ 255
            delta = math.sqrt(i * i) / self.rs
            delta_mult_delta = delta * delta
            self.s_weight_table.append(math.exp(delta_mult_delta * self.factor))

    def clamp(self,p):
        """return RGB color between 0 and 255"""
        if p < 0:
            return 0
        elif p > 255:
            return 255
        else:
            return p

    def bilateral_filter(self, src):
        """ the bilateral filter method.

It can load image and filting it with bilateral filter, then return the destination image.

Args:
        src: source image

Returns:
        dest: destination image after filting."""
        
        width = src.size[0]
        height = src.size[1]
        radius = self.radius
        self.build_distance_weight_table()
        self.build_similarity_weight_table()
        in_pixels = src.load()
        raw_data=[]    
        out_data=[]
        out_pixels = {}
        red_sum = green_sum = blue_sum = 0    # result of convolution before normalization
        cs_sum_red_weight = cs_sum_green_weight = cs_sum_blue_weight = 0    # normalization
        pixel_num = height * width

        for row in range(height):
            for col in range(width):
                # calculate for each pixel
                tr = in_pixels[row, col][0]
                tg = in_pixels[row, col][1]
                tb = in_pixels[row, col][2]
                raw_data.append((tr, tg, tb))
                for semi_row in range(-radius, radius+1):
                    for semi_col in range(-radius, radius+1):
                        # calculate the convolution by traversing each close pixel within radius
                        if row + semi_row >= 0 and row + semi_row < height:
                            row_offset = row + semi_row
                        else:
                            row_offset = 0
                        if semi_col + col >=0 and semi_col + col < width:
                            col_offset = col + semi_col
                        else:
                            col_offset = 0
                        tr2 = in_pixels[row_offset, col_offset][0]  
                        tg2 = in_pixels[row_offset, col_offset][1]
                        tb2 = in_pixels[row_offset, col_offset][2]

                        cs_red_weight = (
                            self.c_weight_table[semi_row+radius][semi_col+radius]
                            * self.s_weight_table[(abs(tr2 - tr))]
                        )
                        cs_green_weight = (
                            self.c_weight_table[semi_row+radius][semi_col+radius]
                            * self.s_weight_table[(abs(tg2 - tg))]
                        )
                        cs_blue_weight = (
                            self.c_weight_table[semi_row+radius][semi_col+radius]
                            * self.s_weight_table[(abs(tb2 - tb))]
                        )
                        
                        cs_sum_red_weight += cs_red_weight
                        cs_sum_blue_weight += cs_blue_weight
                        cs_sum_green_weight += cs_green_weight
                        
                        red_sum += cs_red_weight * float(tr2)
                        green_sum += cs_green_weight * float(tg2)
                        blue_sum += cs_blue_weight * float(tb2)

                # normalization
                tr = int(math.floor(red_sum / cs_sum_red_weight))
                tg = int(math.floor(green_sum  / cs_sum_green_weight))
                tb = int(math.floor(blue_sum  / cs_sum_blue_weight))

                temp_rgb=(self.clamp(tr), self.clamp(tg), self.clamp(tb))
                out_data.append(temp_rgb)
                out_pixels[row, col] = temp_rgb

                index = row * width + col + 1
                percent = float(index) * 100 / pixel_num
                time1 = clock()
                used_time = time1 -time0
                format = "proceseeing %d of %d pixels, finished %.2f%%, used %.2f second."
                print  format % (index, pixel_num, percent, used_time)

                # clean value for next time
                red_sum = green_sum = blue_sum = 0
                cs_red_weight = cs_green_weight = cs_blue_weight = 0
                cs_sum_red_weight =cs_sum_blue_weight =cs_sum_green_weight = 0

        # save the raw data and filted data for dubug
        f0 = open('raw_data','w')
        f1 = open('out_data','w')
        f0.write(str(raw_data))
        f1.write(str(out_data))
        print "finish writing"
        f1.close()
        f0.close()
        
        dest = src.copy()
        for row in range(height):
            for col in range(width):
                dest.putpixel((row,col),out_pixels[row,col])        
        return dest


def main():
    img0 = Image.open('lena1.bmp')
    bf = BilateralFilter(FACTOR,DS,DR,RADIUS)
    dest = bf.bilateral_filter(img0)
    dest.save('out.bmp')
    img0.show()
    dest.show()

if __name__ == '__main__':
    main()
