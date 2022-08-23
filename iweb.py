#from selenium.webdriver.common.by import By
from selenium import webdriver

def telnet_link_7621(url):
    drive = webdriver.Chrome()
    drive.get(url)
    drive.close()
