import random
import webbrowser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import os
import time

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

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1920,1080)

coords = [48.025754,-124.246594]
zoom = 10
zoom_pos = zoom

amount = 100

last_perc = 0
prog_bar = ""

for i in range(amount):
	url = "https://zoom.earth/#" + str(coords[0]) + "," + str(coords[1]) + "," + str(zoom) + "z,sat"
	driver.get(url);

	delay = 3  # seconds
	try:
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'map')))
		remove_html(driver)
		driver.save_screenshot("images/" + str("{:04}".format(i)) + ".jpg")
		
		#clear console
		os.system('cls') 
		
		print(str("{:04}".format(i+1)) + " / " + str(amount))
		
		if i / amount * 25 > last_perc:
			last_perc += 1
			prog_bar = last_perc * "|"
		
		
		print("0% " + prog_bar.ljust(24) + " 100%")
	except TimeoutException:
		print("Loading took too much time!")
driver.close()