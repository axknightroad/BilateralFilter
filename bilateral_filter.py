import Image
import math


FACTOR = -0.5
DS = 3.0
DR = 30.0
RADIUS = int(max(DS,DR))


class BilateralFilter:

    def __init__(self, factor, ds, rs, radiu, wight, height):
        self.factor = factor
        self.ds = ds
        self.rs = rs
        self.c_weight_table = []
        self.s_weight_table = []
        self.radius = radiu
        self.wight = wight
        self.height = height

    def build_distance_weight_table(self):
        size = 2 * self.radius + 1
        for semi_row in range(-self.radius,self.radius+1):
            self.c_weight_table.append([])
            for semi_col in range(-self.radius,self.radius+1):
                delta = math.sqrt(semi_row * semi_row + semi_col * semi_col) / self.ds
                delta_mult_delta = delta * delta
                self.c_weight_table[semi_row+self.radius].append(math.exp(delta_mult_delta * self.factor))
        #print self.c_weight_table

    def build_similarity_weight_table(self):
        for i in range(256):
            delta = math.sqrt(i * i) / self.rs
            delta_mult_delta = delta * delta
            self.s_weight_table.append(math.exp(delta_mult_delta * self.factor))
        #print self.s_weight_table

    def clamp(self,p):
        if p < 0:
            return 0
        elif p > 255:
            return 255
        else:
            return p

    def bilateral_filter(self, src):
        width = src.size[0]
        height = src.size[1]
        radius = int(max(self.ds,self.rs))
        self.build_distance_weight_table()
        self.build_similarity_weight_table()
        in_pixels = src.load()
        raw_data=[]    
        out_data=[]
        out_pixels = {}
        red_sum = green_sum = blue_sum = 0
        cs_sum_red_weight = cs_sum_green_weight = cs_sum_blue_weight = 0
        pixel_num = height * width 
        for row in range(height):
            for col in range(width):
                index = row * width +col
                #print in_pixels[index]
                tr = in_pixels[row,col][0]
                tg = in_pixels[row,col][1]
                tb = in_pixels[row,col][2]
                #print in_pixels[index],(tr,tg,tb)
                raw_data.append((tr, tg, tb))
                for semi_row in range(-radius, radius+1):
                    for semi_col in range(-radius, radius+1):
                        if row + semi_row >= 0 and row + semi_row < height:
                            row_offset = row + semi_row
                        else:
                            row_offset = 0
                        if semi_col + col >=0 and semi_col + col < width:
                            col_offset = col + semi_col
                        else:
                            col_offset = 0
                        index2 = row_offset * width + col_offset
                        tr2 = in_pixels[row_offset,col_offset][0]  
                        tg2 = in_pixels[row_offset,col_offset][1]
                        tb2 = in_pixels[row_offset,col_offset][2]
                        #print (float(tr2),tg2,tb2)
                        cs_red_weight = self.c_weight_table[semi_row+radius][semi_col+radius] * self.s_weight_table[(abs(tr2 - tr))]
                        cs_green_weight = self.c_weight_table[semi_row+radius][semi_col+radius]  * self.s_weight_table[(abs(tg2 - tg))]
                        cs_blue_weight = self.c_weight_table[semi_row+radius][semi_col+radius]  * self.s_weight_table[(abs(tb2 - tb))]

                            
                        cs_sum_red_weight += cs_red_weight
                        cs_sum_blue_weight += cs_blue_weight
                        cs_sum_green_weight += cs_green_weight

                        red_sum += cs_red_weight * float(tr2)
                        green_sum += cs_green_weight * float(tg2)
                        blue_sum += cs_blue_weight * float(tb2)

                #print "the", index, "pixel",red_sum,cs_sum_red_weight          
                tr = int(math.floor(red_sum / cs_sum_red_weight))
                tg = int(math.floor(green_sum  / cs_sum_green_weight))
                tb = int(math.floor(blue_sum  / cs_sum_blue_weight))
                temp_rgb=(self.clamp(tr), self.clamp(tg), self.clamp(tb))
                #print temp_rgb
                out_data.append(temp_rgb)
                out_pixels[row,col] = temp_rgb
                percent = ("%.3f" %(float(index+1) * 100 / pixel_num))
                print "proceseeing", index+1, "of", pixel_num, "pixels, finished",percent, "%"
                #print "processing", index, "of", pixel_num,"pixels"

                red_sum = green_sum = blue_sum = 0
                cs_red_weight = cs_green_weight = cs_blue_weight = 0
                cs_sum_red_weight =cs_sum_blue_weight =cs_sum_green_weight = 0

        f0 = open('raw_data','w')
        f1 = open('out_data','w')
        f0.write(str(raw_data))
        f1.write(str(out_data))
        print "finish write"
        f1.close()
        f0.close()
        dest = src.copy()
        for row in range(height):
            for col in range(width):
                dest.putpixel((row,col),out_pixels[row,col])
        
        return dest



img0 = Image.open('lena.bmp')
#img0.show()        
width = img0.size[0]
height = img0.size[1]
print width,height
bf = BilateralFilter(FACTOR,DS,DR,RADIUS,width,height)
dest = bf.bilateral_filter(img0)
dest.save('out.bmp')
dest.show()
