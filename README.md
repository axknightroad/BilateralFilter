Bilateral Filter
==========

###运⾏环境

* Python 2.7
* PIL

###使用说明
程序会默认读取同一目录下的 ’lena1.bmp’ ⽂件并进⾏行双边滤波,最后将滤波后的图⽚保存为 ’out.bmp’ 并显⽰。

###参数说明

* ds: 计算卷积核内空间高斯权重时的sigma distance,默认为3
* dr: 计算卷积核内像素值之间的相似程度的权重时的sigma range,默认为30
* radius: ⾼斯卷积核半径
* source image: 在main函数中修改,默认为’lena1.bmp’