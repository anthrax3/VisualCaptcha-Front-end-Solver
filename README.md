# VisualCaptcha-Front-end-Solver

 __     ___                 _  ____            _       _                        
 \ \   / (_)___ _   _  __ _| |/ ___|__ _ _ __ | |_ ___| |__   __ _              
  \ \ / /| / __| | | |/ _` | | |   / _` | '_ \| __/ __| '_ \ / _` |             
   \ V / | \__ \ |_| | (_| | | |__| (_| | |_) | || (__| | | | (_| |             
  __\_/  |_|___/\__,_|\__,_|_|\____\__,_| .__/ \__\___|_| |_|\__,_|             
 |  ___| __ ___  _ __ | |_       ___ _ _|_| __| | / ___|  ___ | |_   _____ _ __ 
 | |_ | '__/ _ \| '_ \| __|____ / _ \ '_ \ / _` | \___ \ / _ \| \ \ / / _ \ '__|
 |  _|| | | (_) | | | | ||_____|  __/ | | | (_| |  ___) | (_) | |\ V /  __/ |   
 |_|  |_|  \___/|_| |_|\__|     \___|_| |_|\__,_| |____/ \___/|_| \_/ \___|_|   
                                                                                
                                                                               
*Title:                  VisualCaptcha_Front-end_Solver.py
*Author:                 Arnaud BOURHIS
*Email:                  arnaud.bourhis@free.fr
*Source:                 github.com/bourhisa
*Description:            Breaking Visual Captchas by browser emulation through Selenium
*Pre-requisites:         All used Python libraries (including Selenium with all dependencies), and usable drivers
                        for the use of a browser thourgh Selenium (eg Gecko driver for Firefox)
                        (see http://selenium-python.readthedocs.io/api.html)


    - This is a tool to break VisualCaptcha with a front-end approach.
    It works using Selenium to generate a browser and make user-like interactions with it on the target page.
    - The selection of the icon to click relies on image comparison between a database of images previously loaded and
    the icon to be selected.
    - The images are obtained through cropping of a screenshot captured from the emulated browser (Firefox and PhantomJS implemented here)
    - At every refresh, this captures the label of the icon to be click, loads the expected image from the preloaded db, and compares it
     with the images displayed.
    - It then picks the most resembling picture and generate the clicks to validate the VisualCaptcha

    WARNING : This implementation success relies on your computation capacity, as image comparison is used  at every iteration.
    The approach uses image treatment, which required a considerable amount of operations.

    It has originally been developed for a coding challenge, where 10 submissions within 10 seconds were required to succeed.
    This tool is therefore set to make multiple tries until success, any mistake made will result in another try in a new browser window.

    Intended for IDE use only in this version.


Title:                  VisualCaptcha_Front-end_Solver.py
Author:                 Arnaud BOURHIS
Email:                  arnaud.bourhis@free.fr
Source:                 github.com/bourhisa
Description:            Breaking Visual Captchas by browser emulation through Selenium
Pre-requisites:         All used Python libraries (including Selenium with all dependencies), and usable drivers
                        for the use of a browser thourgh Selenium (eg Gecko driver for Firefox)
                        (see http://selenium-python.readthedocs.io/api.html)


    - This is a tool to break VisualCaptcha with a front-end approach.
    It works using Selenium to generate a browser and make user-like interactions with it on the target page.
    - The selection of the icon to click relies on image comparison between a database of images previously loaded and
    the icon to be selected.
    - The images are obtained through cropping of a screenshot captured from the emulated browser (Firefox and PhantomJS implemented here)
    - At every refresh, this captures the label of the icon to be click, loads the expected image from the preloaded db, and compares it
     with the images displayed.
    - It then picks the most resembling picture and generate the clicks to validate the VisualCaptcha

    WARNING : This implementation success relies on your computation capacity, as image comparison is used  at every iteration.
    The approach uses image treatment, which required a considerable amount of operations.

    It has originally been developed for a coding challenge, where 10 submissions within 10 seconds were required to succeed.
    This tool is therefore set to make multiple tries until success, any mistake made will result in another try in a new browser window.

    Intended for IDE use only in version 1.
