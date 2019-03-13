
# coding: utf-8

# In[165]:


from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


# In[183]:


import PIL
from PIL import Image
from pytesseract import image_to_string
import pytesseract
import numpy as np, matplotlib.pyplot as plt, pandas as pd


# ### Load Firefox and get the Lakport Schedule page

# In[167]:


opts = Options()
opts.headless=True
browser = Firefox(options=opts)
browser.get('http://lakport.nic.in/ship_online_programme.aspx')


# ### Select All Passenger Ships option

# In[168]:


#Select All Passenger Ships in drop down selection
ship_selector=Select(browser.find_element_by_id("ContentPlaceHolder1_ship_dlist"))
ship_selector.select_by_visible_text("All Passenger Ships")
ship_selector=Select(browser.find_element_by_id("ContentPlaceHolder1_ship_dlist"))
print(ship_selector.all_selected_options[0].text)


# ### Defining all required methods to extract and solve captcha

# In[184]:


def extract_capcha(browser):
    """Extract the captcha from browser and return
    """
    img=browser.find_element_by_css_selector('img')
    import os, random
    os.makedirs('captcha', exist_ok=True) # Serialize the captchas
    captchas=[int(filename.split('.')[0].split('_')[1]) for filename 
              in os.listdir('captcha') if 'cap' in filename]
    # New name = old name + 1
    if len(captchas)==0: captchas=[-1]
    cap_name = 'captcha/cap_'+ str(max(captchas)+1) +'.png'
    img.screenshot(cap_name)
    return Image.open(cap_name)

def display_captcha(browser):
    plt.imshow(extract_capcha(browser))
    print("OCR Prediction: ", image_to_string(extract_capcha(browser)))
    plt.show(block=False)


# In[185]:


def solve_captcha(browser):
    """Solve the captcha using teserract and press Enter/Return
    """
    captcha_inp=browser.find_element_by_id('ContentPlaceHolder1_txtimage')
    captcha_inp.clear()
    captcha_inp.send_keys(image_to_string(extract_capcha(browser)))
    captcha_inp.send_keys(Keys.RETURN)


# In[186]:


def solve_captcha_again(browser, display=True):
    """Get New Captcha and solve it again
    """
    # Button to refresh the captcha
    refresh_button=browser.find_element_by_id('ContentPlaceHolder1_ImageButton')
    refresh_button.click()
    if display: display_captcha(browser)
    solve_captcha(browser)


# In[187]:


def is_captcha_valid(browser):
    """Check if the page contains the required table
    If solve_captcha worked, it will or else need to solve new captcha
    """
    from selenium.common.exceptions import NoSuchElementException
    try: 
        _ = browser.find_element_by_id('ContentPlaceHolder1_progallships_dgrid')
        #Schedule has been found in page without error
        return True
    except NoSuchElementException: return False    


# ### Keep Solving Captcha until correct

# In[182]:


# Try new captchas untill correct prediction ;)
for i in range(100):
    if is_captcha_valid(browser): break #break out of for loop
    solve_captcha_again(browser, display=True)
    from time import sleep
    sleep(1)


# ### Save the page to html

# In[177]:


with open('../Lakport_schedule.html', 'w') as f:
    f.write(browser.page_source)


# ### Showing the read timetable from saved html

# In[181]:


pd.read_html('../Lakport_schedule.html', header=0)[0]
print(pd)
print('\n\nDone!!!!')

