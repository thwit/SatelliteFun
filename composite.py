import random
import webbrowser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
from PIL import Image

### Removes html-overlays from zoom.earth ###
def remove_html(driver):
    driver.execute_script("var x = document.getElementsByClassName(\"controls overlay\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"date overlay\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"cookies\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"neave\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"title\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"notranslate\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"main-crosshairs\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"ol-zoom ol-unselectable ol-control\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"about-icon\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"ad\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByTagName(\"header\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"main-arrow left\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"main-arrow right\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")
    driver.execute_script("var x = document.getElementsByClassName(\"attribution\");var i;for (i = 0; i < x.length; i++) {  x[i].style.display = \"none\";}")

	
### Saves the 4 images that should be composited into 1, in your computer ###
def take_4_composite(driver, lat, long):
	
	# Don't change the odd decimal numbers. They work perfectly for a 10-level zoom
	lat_arr = [lat, lat + 0.115412]
	long_arr = [long, long + 0.328904]
	
	delay = 3
	
	counter = 0
	
	for i in range(2):
		for j in range(2):
			url = "https://zoom.earth/#" + str(lat_arr[i]) + "," + str(long_arr[j]) + "," + str(zoom) + "z,sat"
			driver.get(url)
			try:
				myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'map')))
				time.sleep(3)
				remove_html(driver)
				
				# Change 'images/' to your desired save-path
				driver.save_screenshot("images/" + str("{:04}".format(counter)) + ".jpg")
				print("Image #" + str("{:04}".format(counter+1)) + " of " + str(amount) + " saved.")
				counter += 1
			except TimeoutException:
				print("Loading took too much time!")
	driver.close()
	

### Function stolen from stackoverflow: https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python/46623632#46623632 ###
def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)

    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

### Small function that returns a list of 4 sequential images ###
def get_4_images(start):
	images = []
	for i in range(start,start+4):
		images.append(Image.open("images/" + str("{:04}".format(i)) + ".jpg"))
	return images

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920,1080)

coords = [48.025754,-124.246594]
zoom = 13

amount = 4

take_4_composite(driver, coords[0], coords[1])

images = get_4_images(0)

for i in range(1):
	img1 = append_images(images[:2], direction='horizontal')
	img2 = append_images(images[2:4], direction='horizontal')
	final = append_images([img2,img1], direction='vertical')
	final.save("images/composites/" + str("{:04}".format(i)) + ".jpg")
