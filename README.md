# Content Aware Scaler GUI (Repurposed from E E 440 Term Paper)

Instructions:
This program is run on Python and uses the following packages if they are not already added:
```pip install sys numpy scipy cv2 pyqt5 numba```

For trying to turn the included .ui file into a Python file yourself, you will need to add:
```pip install pyqt5-tools```
to have access to the method pyuic5 to perform the conversion:
```pyuic5 <filename>.ui -o <filename>.py```

To run the program itself, make sure you have the included programs in the same directory: cas.py, cas_runner.py, and your converted .ui file (we included one for you as contentawarescale.py) and run within the directory:
```python cas_runner.py```
to start the program.

To use the GUI, there is a prompt to upload your image, a reset button, and two sliders. 
* The Upload button will allow you to open any image as long as it's in the format of PNG, JPEG, or BMP. 
* The top slider will allow you to change the scaling in the vertical direction from a factor of 0.35 to 1, with the default set at the latter. 
* The bottom slider will allow you to change the scaling in the horizontal direction from a factor of 0.35 to 1, with the default set at the latter.
* The Reset button can be used to set the horizontal and vertical scaling back to 1, but will require you to upload the image after to see the changed effects.
* The Surprise checkmark will not be covered in this paper, but checking it will improve the appearance of your image. Viewer discretion is advised.

Implementation:
Editor’s Note: The image display for the conceptual demonstration is done using matplotlib. It is not something included in the actual GUI, but was utilized for testing purposes. 

Instead of removing data by rows and columns, a content-aware scaler develops a map of interconnected paths along the image that go along a corresponding energy map based on the result of an edge detection, as demonstrated below.

![Images/download (3).png](https://raw.githubusercontent.com/marcuschen001/cas/main/Images/download%20(3).png)

Moving backwards from the end of the row, or end of the column, the least mathematically significant seam – or the shortest path, is determined and is either copied for image expansion or removed for image compression; in our case, we are only compressing images. This process of finding and removing or adding seams is continued until the image reaches the desired image resolution. 

To find the edge detection of the image, I convoluted a Sobel-Feldman operator in both the vertical and horizontal direction, before taking the resulting magnitude of both.

![Images/download.png](https://raw.githubusercontent.com/marcuschen001/cas/main/Images/download.png)

To develop the energy map, dynamic programming (the process of storing sub-calculations to simplify the calculation of complex results) is used. To create the map, the top row contains the original energy values for each pixel; each pixel from the descending rows takes in their current energy value plus the smallest sum of the energy map value from one of the adjacent pixels in the previous row, as shown here:

![Images/Screenshot 2023-12-07 184824.png](https://raw.githubusercontent.com/marcuschen001/cas/main/Images/Screenshot%202023-12-07%20184824.png)

This is done until the bottom row is reached. An additional matrix called “backtrack” was also created to make calculations for finding the smallest seam easier.

![Images/download (1).png](https://raw.githubusercontent.com/marcuschen001/cas/main/Images/download%20(1).png)

To remove a single seam, the least important seam is found by finding the smallest energy value point in the bottom row and using the backtrack matrix to find the pixel to choose next for the seam until the seam reaches the top; this is removed from the image. 

To perform this multiple times, we will have to make an energy map of the modified image each time to ensure it is removing the least significant seam, but that can become computationally expensive. Python package numba is used to improve the efficiency, by converting the calculations of the energy map development and the seam finding process into fast machine code, encouraging more efficient seam carving. 

Carving in the vertical direction is simply done by taking the transpose of the image, and performing a transpose again after carving is finished.

![Images/download (2).png](https://raw.githubusercontent.com/marcuschen001/cas/main/Images/download%20(2).png)

For the sake of accommodating for every image, a ratio is used instead of a pixel threshold on the GUI, which is just then multiplied to the resolution of the image to determine the pixel resolution of the final product.

References:
1.	https://dl.acm.org/doi/10.1145/1275808.1276390
2.	https://cs.brown.edu/courses/cs129/results/proj3/taox/
3.	https://homepages.inf.ed.ac.uk/rbf/HIPR2/sobel.htm 
4.	https://avikdas.com/2019/05/14/real-world-dynamic-programming-seam-carving.html 
5.	https://numba.readthedocs.io/en/stable/index.html 
