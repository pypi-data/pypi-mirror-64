# hsvpicker
Finding HSV bounding values for tracking/masking an object 

## How to find HSV bounding values to track or mask an object?.
  This is the most common question as stated in opencv documentation. By using the hsvpicker we get a hsv bounding values by simply calling a function.
  
## Overview:
  We can get lower and upper bounding hsv values by clicking the left button of a mouse on an image for which object we want to track or mask.
  
## Usage:

### Getting it:

To download hsvpicker, either fork this github repo or simply use Pypi via pip.
```sh
    $ pip install hsvpicker
``` 

### Using it:

##### STEP 1: import hsvpicker package 
```python
from hsvpicker.hsv import HSV
```
##### STEP 2: Create an object
```python 
bound = HSV('pass the image url')
```
##### STEP 3: Getting a HSV value 
```python
bound.get_value()
```
Image will display here, you will choose color by simply double clicking the mouse's left button on an image and then it finds hsv values of the respected color .(i.e The color which we want to track or mask). PRESS ```q``` to quit the window.

##### STEP 4 : Getting a bounding values
```python
lower_bound,upper_bound = bound.get_boundings(h = 20,s = 50,v = 60)
```
You can fine tune color boundings by using h,s and v. Default values of h,s, and v are 20,50,60 respectively. This function returns numpy.ndarray.
