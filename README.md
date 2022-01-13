
<h1 align="left">Depth estimation through binocular stereo matching </h1>
<h2 align="center"> 
  
  ## Goal
Use Normalized cross correlation (NCC) to match binoclar stereo vision and calculate depth according to the disparity from each pixel.
 
  ## Introduction

 Stereo Matching is one of the core technologies in computer vision, which recovers 3D structures of real world from 2D images. Given a pair of rectified stereo images, the goal of Stereo Matching is to compute the disparity for each pixel in the reference image, where disparity is defined as the horizontal displacement between a pair of corresponding pixels in the left and right images.

 <p align="center">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/7247ad144e94d91a7121cc30df743684809ec436/stereo-matching.JPG" height="80%">
 </p>
 
  ## Procedure in this project
 
 ### (1) Rectify images to make epipolar line horizontal
 
 ### (2) For each pixel, scan along epipolar line for best matching in predefined kernel window. In this project, I used NCC as the indicator measuring similarity between two image blocks:
![](http://latex.codecogs.com/svg.latex?Similarity:=NCC=\frac{\sum_{(i,j)\in{w}}I_{1}(i,j)\cdot{I_{2}(x+i.y+j)}}{\sqrt{\sum_{(i,j)\in_w}I_{1}^{2}(i,j)\cdot{\sum_{(i,j)\in{w}}}I_{2}^{2}(x+i,y+j)}})
 
 ### (3) Compute depth from disparity from the formula in the following:
![](http://latex.codecogs.com/svg.latex?Depth:=Z=\frac{bf}{d})

  In order to avoid depth estimation calculated from matches which are **not considered as good matches**, I set **0.5 as threashold** empirically. That is to say, matches with NCC value <0.5 would not be calculated its corresponding depth.

## Experiment and Result
In this project, I use two sets of picture as binocular vision. In each set of experiment, first from left one is reference image, and second from left is used as matching image. The depth map is calculated from **window size 7\*7 and 10\*10 pixels**, which are the second from the right and first from the right respectively.
 <p align="center">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/d64f216c0fc5b02d15e83a356501369eb8eb8dab/tmp1_1.jpg" width="20%" height="30%">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/7247ad144e94d91a7121cc30df743684809ec436/tmp1_2.jpg" width="20%" height="30%">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/89716ceb200a5ee9b08de66ffbfd632801e53d77/depth1_w7.jpg" width="20%" height="30%">  
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/ac56e2ce584b81bcb8b4c7651596fdd3ecd3d4af/depth1_10.jpg" width="20%" height="30%">
  
 </p>
  
  
 <p align="center">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/d64f216c0fc5b02d15e83a356501369eb8eb8dab/tmp1.jpg" width="20%" height="30%">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/7247ad144e94d91a7121cc30df743684809ec436/tmp2.jpg" width="20%" height="30%">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/89716ceb200a5ee9b08de66ffbfd632801e53d77/depth_w7.jpg" width="20%" height="30%">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/ec30ead83d2ba52fcfb92981626d991a64dd11a6/depth_10.jpg" width="20%" height="30%">
 </p>
