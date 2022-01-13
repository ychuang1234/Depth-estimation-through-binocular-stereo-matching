
<h1 align="left">Depth estimation through binocular stereo matching </h1>
<h2 align="center"> 
  
  ## Goal
Use Normalized cross correlation to match binoclar stereo vision and calculate depth according to the disparity from each pixel.
 
  ## Introduction

 Stereo Matching is one of the core technologies in computer vision, which recovers 3D structures of real world from 2D images. Given a pair of rectified stereo images, the goal of Stereo Matching is to compute the disparity for each pixel in the reference image, where disparity is defined as the horizontal displacement between a pair of corresponding pixels in the left and right images.

 <p align="center">
 <img src="https://github.com/ychuang1234/Depth-estimation-through-binocular-image/blob/7247ad144e94d91a7121cc30df743684809ec436/stereo-matching.JPG" height="80%">
 </p>
 
  ## Description
 
 ### (1) Rectify images to make epipolar line horizontal
 
 ### (2) For each pixel, scan along epipolar line for best matching in predefined kernel window and compute depth from disparity from the formula in the following 
![](http://latex.codecogs.com/svg.latex?Similarity:=NCC=\frac{\sum_{(i,j)\in{w}}I_{1}(i,j)\cdot{I_{2}(x+i.y+j)}}{\sqrt{\sum_{(i,j)\in_w}I_{1}^{2}(i,j)\cdot{\sum_{(i,j)\in{w}}}I_{2}^{2}(x+i,y+j)}})
 
 
![](http://latex.codecogs.com/svg.latex?Z=\frac{bf}{d})
 

 

 ### (3) Contraint energy (optional) : In this project, I used random gaussian noise as the contraint energy 
 ![](http://latex.codecogs.com/svg.latex?E_{constraint}=G(\mu,\sigma))
 
 ### (4-1) Optimization step (thereoretically): Gradient decent
 

  ### (4-2) Optimization step (in this project): trust region optimization
 Search in pre-defined range to find if there is any new position that could lower snake energy and update. 


## Experiment and Result
This is the procedure in experiment but **not yet adjust the weights** of each designated energy term.


