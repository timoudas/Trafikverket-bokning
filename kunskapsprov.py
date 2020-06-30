import datetime
import schedule
import threading


from datetime import date

import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import PySimpleGUI as sg

from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def selenium_get_time(ort):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options, executable_path='/Users/andreas/.wdm/chromedriver/83.0.4103.39/mac64/chromedriver')

    # driver.get("https://fp.trafikverket.se/boka/#/search/SPHhISIPAfhPP/5/0/0/0")
    
    driver.get("https://fp.trafikverket.se/boka/#/search/dIccADaISRCIi/5/0/0/0")
    element = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "form-control")))
    driver.find_element_by_xpath("//select[@id='examination-type-select']/option[@value='3']").click()
    driver.find_element_by_xpath("//select[@id='language-select']/option[@value='13']").click()
    driver.find_element_by_id('id-control-searchText').clear()
    inputElement = driver.find_element_by_id("id-control-searchText")
    inputElement.send_keys(ort)
    inputElement.send_keys(Keys.ENTER)
    # time.sleep(10)
    
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='col-sm-3 text-center']/button[@data-bind='click:$parent.select']")))
        first_time = driver.find_element_by_xpath("//div[@class='col-xs-6']/strong")
        return first_time.text
    except (NoSuchElementException, TimeoutException) as e:
        driver.close()
        if NoSuchElementException:
            print('Nothing found for: ', ort, ' NoElemFound')
        else:
            print('Nothing found for: ', ort, ' TimedOut')

def convert_time(time_stamp):
    date_time_obj = datetime.datetime.strptime(time_stamp, '%Y-%m-%d %H:%M')
    return date_time_obj

def check_schedule(date, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    if start_date <= date <= end_date:
        return True
    else:
        return False

def send_email(first_availible, ort):
    gmailUser = 'noreplykorprov@gmail.com'
    gmailPassword = 'blomma12'
    recipient = 'andreas.timoudas@gmail.com'
    message=msg = 'Första lediga tid i'+' '+ str(ort) +' '+ str(first_availible) +' '+ 'https://fp.trafikverket.se/boka/#/search/SPHHISiPAfhpP/5/0/0/0'

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = "Ledig tid körkortsprov"
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()

def main(ort):
    first_availible = selenium_get_time(ort)
    if first_availible:
        date = convert_time(first_availible)
        if check_schedule(date, '2020-06-27', '2020-07-13'):
            print('FOUND: ', ort +' '+ first_availible)
            send_email(first_availible, ort)
        else:
            now = datetime.datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            print('Found Nothing for: ', ort, ' ', dt_string)

def selenium_get_orter():
    options = Options()
    driver = webdriver.Chrome(executable_path='/Users/andreas/.wdm/chromedriver/83.0.4103.39/mac64/chromedriver')
    driver.set_window_position(0, 0)
    driver.set_window_size(720, 900)
    driver.get("https://fp.trafikverket.se/boka/#/search/dIccADaISRCIi/5/0/0/0")
    time.sleep(25)
    driver.find_element_by_xpath("//button[@data-bind='click:selectLocation']").click()
    time.sleep(5)
    elems = driver.find_elements_by_xpath("//a[@class='list-group-item']/span[@class='list-group-item-heading']")
    driver.close()
    driver.quit()
    return elems

def run():
    ORTER = ['Södertälje', 'Stockholm', 'Järfälla', 'Sollentuna']
    for ort in ORTER:
        main(ort)




if __name__ == '__main__':


    schedule.every(1).minute.do(run)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)

        except Exception as e:
            schedule.run_pending()
            time.sleep(1)
    








