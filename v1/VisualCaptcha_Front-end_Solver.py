'''

 __     ___                 _  ____            _       _                        
 \ \   / (_)___ _   _  __ _| |/ ___|__ _ _ __ | |_ ___| |__   __ _              
  \ \ / /| / __| | | |/ _` | | |   / _` | '_ \| __/ __| '_ \ / _` |             
   \ V / | \__ \ |_| | (_| | | |__| (_| | |_) | || (__| | | | (_| |             
  __\_/  |_|___/\__,_|\__,_|_|\____\__,_| .__/ \__\___|_| |_|\__,_|             
 |  ___| __ ___  _ __ | |_       ___ _ _|_| __| | / ___|  ___ | |_   _____ _ __ 
 | |_ | '__/ _ \| '_ \| __|____ / _ \ '_ \ / _` | \___ \ / _ \| \ \ / / _ \ '__|
 |  _|| | | (_) | | | | ||_____|  __/ | | | (_| |  ___) | (_) | |\ V /  __/ |   
 |_|  |_|  \___/|_| |_|\__|     \___|_| |_|\__,_| |____/ \___/|_| \_/ \___|_|   
                                                                                


Title:                  VisualCaptcha_Front-end_Solver.py
Author:                 Arnaud BOURHIS
Email:                  arnaud.bourhis@free.fr
Source:                 github.com/bourhisa
Description:            Breaking Visual Captchas by browser emulation through Selenium
Pre-requisites:         All used Python libraries (including Selenium with all dependencies), and usable drivers
                        for the use of a browser thourgh Selenium (eg Gecko driver for Firefox)
                        (see http://selenium-python.readthedocs.io/api.html)

* Pre-requisites:         
  * All used Python libraries (including Selenium with all dependencies)
  * Browsers drivers must be installed for the use through Selenium (eg Gecko driver for Firefox) (see http://selenium-python.readthedocs.io/api.html)

### Details

This is a tool to break VisualCaptcha with a front-end approach.
It works using Selenium to generate a browser and make user-like interactions with it on the target page.

The selection of the icon to click relies on image comparison between a database of images previously loaded and
the icon to be selected.

The images are obtained through the cropping of a screenshot captured from the emulated browser (Firefox and PhantomJS implemented here)

At every refresh, this captures the label of the icon to be click, loads the expected image from the preloaded db, and compares it
with the images displayed.

It then picks the most resembling picture and generate the clicks to validate the VisualCaptcha


### WARNING : Please note
* This implementation success relies on your computation capacity, as image comparison is used  at every iteration.
  * The approach uses image treatment, which requires a considerable amount of operations.

* It has originally been developed for a coding challenge, where 10 submissions within 10 seconds were required to succeed.
  * This tool is therefore set to make multiple tries until success, any mistake made will result in another try in a new browser window.

* Intended for IDE use only in v.1

'''

__version__ = "Version: 1.0.0"

import os
import io
import imgcompare
import sys
import base64
import time
import StringIO
import json
from PIL import Image

# Selenium imports
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

target = "http://url_of_target_website" # Url of target
icons_folder = 'icons_captcha/'
browser_is_visible = True # Switches between either Firefox or PhantomJS
nb_iteration_until_success = 10 # Number of clicks to be made to solve the captcha, originally set to 10 to solve a challenge

# Path to the drivers, can be set in PATH
gecko_exec_path = r'path/to/geckodriver.exe'
phantomjs_exec_path = r'path/to/phantomjs.exe'

### Generates a new browser window and attempts to beat dat captcha ###
class Attempt:

    def __init__(self):
        self.driver = self.connect()
        self.nb_clicks = 0

    ### Generates a new Firefox window using Selenium and sets the window to maximum size ###
    def connect(self):
        if browser_is_visible:
            driver = webdriver.Firefox(executable_path=gecko_exec_path)
        else:
            driver = webdriver.PhantomJS(executable_path=phantomjs_exec_path)
        driver.maximize_window()
        driver.get(target)
        return driver

    def generate_new_click(self):
        self.get_cipher_icons()
        self.get_image_label()
        self.guess_and_click()
        self.let_page_load()
        return self.get_result()

    ### Return list of icons of the current screen in PIL images ####
    # 1. Gets the size of the displayed webpage
    # 2. Fetches the DOM elements of the icons, their position and size on the webpage
    # 3. Takes screenshot of the webpage, formats it at the size of the webpage
    # 4. Crops the screenshot according to each icon location and size to generate the images

    def get_cipher_icons(self):
        body = self.driver.find_element_by_xpath('/html/body')
        webpage_size = (int(body.size['width']), int(body.size['height']))
        elements_coordinates = [{'x1': int(e.location['x']),
                                 'y1': int(e.location['y']),
                                 'x2': int(e.location['x'] + e.size['width']),
                                 'y2': int(e.location['y'] + e.size['height'])} \
                                for e in
                                [self.driver.find_element_by_id('visualCaptcha-img-' + str(i)) for i in range(14)]]

        webpage_screenshot = Image.open(io.BytesIO(base64.b64decode(self.driver.get_screenshot_as_base64())))
        formatted = webpage_screenshot.convert('RGB').resize((webpage_size))
        self.cipher_icons = [formatted.crop((c['x1'], c['y1'], c['x2'], c['y2'])) for c in elements_coordinates]

    ### Fetch the image fitting the label from the local files ###
    def get_image_label(self):
        label = self.driver.find_element_by_class_name('visualCaptcha-explanation').text.lower().replace(
            'click or touch the ', '').replace(' ', '_')

        t = Image.open(icons_folder + label + '.png').convert('RGB')
        width, height = t.size
        for x in range(width):
            for y in range(height):
                if t.getpixel((x, y)) == (0, 0, 0):
                    t.putpixel((x, y), (255, 255, 255))

        self.img_of_label = t.convert('RGB').resize((32, 32))

    ### Determines which icon is the closest to the image corresponding to the label ###
    # Uses imgcompare to determine which icon is the most resembling with the one expected
    def guess_and_click(self):
        guesses = []
        for i in self.cipher_icons:
            ratio = imgcompare.image_diff_percent(self.img_of_label, i)
            # If the ratio is below 5, we can reasonably accept that the image is the good one
            if ratio < 5:
                index_to_click = self.cipher_icons.index(i)
                break
            else:
                guesses.append(ratio)

        index_to_click = guesses.index(min(guesses))

        # Generate the clicks
        self.driver.find_element_by_id('visualCaptcha-img-' + str(index_to_click)).click()
        self.driver.find_element_by_name('submit-bt').click()


    ### Ensures the images are loaded into the browser <=> All ajax calls are over ###
    def let_page_load(self):
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.ID, "visualCaptcha-img-13")))

    def get_result(self):
        response_text = self.driver.find_element_by_tag_name('body').text.lower()
        if ('image was not valid' in response_text) or ('reset' in response_text):
            return False
        else:
            self.nb_clicks += 1
            return True

    def __del__(self):
        self.nb_clicks = 0
        self.driver.close()

if __name__ == '__main__':

    success = False
    a = Attempt()

    while not success:
        if a.nb_clicks < nb_iteration_until_success:
            try:
                is_valid = a.generate_new_click()
                if not is_valid:
                    del a
                    a = Attempt()

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno, e)
                del a
                a = Attempt()

        else:
            success = True
            response = a.driver.get_screenshot_as_png()
            Image.open(StringIO.StringIO(response)).show()
            response.show()
