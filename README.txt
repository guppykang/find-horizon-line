Create a new conda or python environment with the requirements.txt file given. 
Install requirements using pip install -r requirements.txt.

For conda users : 
conda create --name myenv
conda activate myenv
pip install -r requirements.txt


To run script run python horizon-detector.py
-i flag for input directory
-o flag for output directory 
-h for help

The give solution is naive and is overfit to the data given to me. In other words, 
there is a good chance that this will not work on other data since the hyperparameters were learned
imperically, and not learned in any sense. Average runtime per image was 0.84 seconds. THis
is probably not acceptable for a real time drone, and a once again a lower level language would 
perform better

I have used information from a research paper online from : http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.360.5951&rep=rep1&type=pdf#page=93

The research paper discusses several ways to get a horizon line in the applications from sailing, 
and images from the ocean (therefore a good reference and reliable source). The concluded that the 
"canny hough" method was the best to get the edges in the best runtime and results. Of course, 
this code would run better on a high performance low level language such as C, but I have created
a temporary prototype frankenstein solution as a proof of concept. 

Algorithm : 
1. Blurr the gray scale image for noise and impurities 

2. find the edges (in this case using canny). Edges are given values that are non zeros. 

3. give the edges captured to a probalisitic hough transformation to find the lines given edges 
in the image. Hyperparameters were chosen imperically. 

4. sort the lines, and get the longest one (this method could be changed), and use the line 
(elongated) across the entire image. 

5. save file and move on to next image  

p.s I will admit my algorithm doesn't find all the horizons. I did not have enought time to perfect the hyperparameters get a 100% success rate. 
Just a prototype that proves the concept and runtime. 

If there is a concern with the high use of libraries, I would be more than happy to explain how each filtering and algorithm works over Zoom!
