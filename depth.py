import numpy as np
import cv2
import os
import math
class conv(object):
   def __init__(self):
        pass
   def conv2d(self,image,kernel,padding=[0,0],strides=[1,1]):
        #kernel = np.flipud(np.fliplr(kernel))
        xKernelShape = kernel.shape[0]
        yKernelShape = kernel.shape[1]
        xImgShape = image.shape[0]
        yImgShape = image.shape[1]
        try:
            if xImgShape%strides[0] ==0 and yImgShape%strides[1]==0:
                pass
        except ValueError:
            print("x:%i or y%i cannot be divided by strides[0]:%i or strides[1]:%i"%(x,y,strides[0],strides[1]))
        xOutput = int (((xImgShape-xKernelShape +2*padding[0])/strides[0])+1)
        yOutput = int (((yImgShape-yKernelShape +2*padding[1])/strides[1])+1)
        #output = np.zeros((xOutput,yOutput))
        if padding != [0]*len(image.shape):
            imagePadded = np.zeros((image.shape[0]+padding[0]*2,image.shape[1]+padding[1]*2))
            imagePadded[int(padding[0]):int(-1*padding[0]),int(padding[1]):int(-1*padding[1])] = image
        else:        
            imagePadded = image
        for y in range(yKernelShape,2*yKernelShape,yKernelShape):
            for x in range(xKernelShape,2*xKernelShape,xKernelShape):
                #print("B:",kernel,imagePadded[x:x+xKernelShape,y:y+yKernelShape])
                output= (kernel*imagePadded[x:x+xKernelShape,y:y+yKernelShape]).sum()
        #print("output:",output)
        #print(b)
        return output
   def conv3d(self,image,kernel,padding=[0,0,0],strides=[1,1,1]):
        output = []
        for ch in image.shape[2]:
            output.append(self.conv2d(image[:,:,ch],kernel[:,:,ch],padding[:2],strides[:2]))
        output = np.array(output)
        return output
class NCC(conv):
    def __init__(self, win=None,ws=9):
        self.win = win
        self.ws = ws
        self.F = conv()
    def loss(self, y_left, y_right):
        I = np.double(y_left)
        J = np.double(y_right)
        #get dimension of volume
        ndims = len(list(I.shape))
        # set window size
        win = [self.ws] * ndims if self.win is None else self.win

        # compute filters
        sum_filter = np.ones([*win])
         
        #pad_no = math.floor(win[0]/2)
        pad_no = 0
        if ndims == 1:
            stride = (1)
            padding = [pad_no]
        elif ndims == 2:
            stride = (1,1)
            padding = [pad_no, pad_no]
        else:
            stride = (1,1,1)
            padding = [pad_no, pad_no, pad_no]

        # get convolution function
        conv_fn = getattr(self.F, 'conv%dd' % ndims)

        # compute CC squares
        I2 = I * I
        J2 = J * J
        IJ = I * J

        I_sum = conv_fn(I, sum_filter, strides=stride, padding=padding)
        J_sum = conv_fn(J, sum_filter, strides=stride, padding=padding)
        I2_sum = conv_fn(I2, sum_filter, strides=stride, padding=padding)
        J2_sum = conv_fn(J2, sum_filter, strides=stride, padding=padding)
        IJ_sum = conv_fn(IJ, sum_filter, strides=stride, padding=padding)
        win_size = np.prod(win)
        u_I = I_sum / win_size
        u_J = J_sum / win_size

        cross = IJ_sum - u_J * I_sum - u_I * J_sum + u_I * u_J * win_size
        I_var = I2_sum - 2 * u_I * I_sum + u_I * u_I * win_size
        J_var = J2_sum - 2 * u_J * J_sum + u_J * u_J * win_size

        cc = cross / np.power((I_var * J_var + 1e-5),0.5)
        return cc
def main():
    left = cv2.imread("tmp1.jpg",cv2.IMREAD_GRAYSCALE)
    left = cv2.resize(left,(200,267))
    #print("size:",left.shape)
    #cv2.imshow("left",left)
    #cv2.waitKey(0)
    right = cv2.imread("tmp2.jpg",cv2.IMREAD_GRAYSCALE)
    right = cv2.resize(right,(200,267))
    #cv2.imshow("right",right)
    #cv2.waitKey(0)
    dmin = -20
    dmax = 60
    ws = 7
    ncc = NCC(ws=ws)
    im = np.zeros((left.shape[0],left.shape[1]))
    ncc_record = np.zeros((left.shape[0],left.shape[1],dmax-dmin))
    currMax = np.zeros((left.shape[0],left.shape[1]))
    ncc_tmp = np.zeros((left.shape[0],left.shape[1]))
    depth = np.zeros((left.shape[0],left.shape[1]))
    for i in range(ws,left.shape[0]-ws):
        for j in range(ws,left.shape[1]-ws):
            for d in range(dmin,dmax):
                if j+d+ws<right.shape[1] and j+d-ws>0:
                    ncc_record[i,j,d-dmin]= ncc.loss(left[i-ws:i+ws,j-ws:j+ws],right[i-ws:i+ws,j+d-ws:j+d+ws])
                #print("Ncc record[%i,%i]="%(i,j),ncc_record[i,j])
    for i in range(left.shape[0]):
        for j in range(left.shape[1]):
            currMax[i,j] = ncc_record[i,j,:].max()
            if (currMax[i,j]<0.5):
                ncc_tmp[i,j]=500
            else:
                ncc_tmp[i,j] = currMax[i,j]
            if ncc_tmp[i,j]>0:
                depth[i,j] = 2550/ncc_tmp[i,j]
            else:
                depth[i,j] = 0
            #print("C:",ncc_tmp[i,j],depth[i,j])
    cv2.imwrite("depth_w7.jpg",np.array(depth,dtype=np.uint8))
    cv2.imshow("Depth",np.array(depth,dtype=np.uint8))    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main()