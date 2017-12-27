# VisualCaptcha-Front-end-Solver

Breaking Visual Captchas by browser emulation through Selenium

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
    
Please give me feedback!
