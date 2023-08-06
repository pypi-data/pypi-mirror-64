from hsv import HSV

bound = HSV('/home/user_name/roi.jpg')
bound.get_value()
lower,upper = bound.get_boundings()
print(lower,upper)
