from PIL import Image
import math

class BilateralFilter:

    def __init__(self, factor, ds, rs, raidus, wight, height, image):
        self.factor = factor
        self.ds = ds
        self.rs = rs
        self.c_weight_table = []
        self.s_weight_table = []
        self.radius =radius
        self.wight = wight
        self.height = height
        self.image = image

    def build_distance_weight_table():
        size = 2 * self.radius + 1
        for semi_row in range(-self.radius,self.radius+1):
            self.c_weight_table.append([])
            for semi_col in range(-self.radius,self.radius+1):
                delta = math.sqrt(semi_row * semi_row + semi_col * semi_col) / self.ds
                delta_mult_delta = delta * delta
                self.c_weight_table[semi_row+radius].append(math.exp(delta_mult_delta * self.factor))

    def build_similarity_weight_table():
        for i in range(256):
            delta = math.sqrt(i * i) / self.rs
            delta_mult_delta = delta * delta
            self.s_weight_table.append(math.exp(delta_mult_delta * self.factor))

    def bilateral_filter(src, dest)
                
