from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import datetime
driver = webdriver.Firefox(executable_path=r'C:\Users\Vishaal Sudarsan\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe')
driver.get('https://www.cowin.gov.in/')
driver.find_element_by_xpath("/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[1]/div/label/div").click()
driver.find_element_by_xpath("/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[1]/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span").click()
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/mat-option[13]/span").click()
statedata=pd.DataFrame()
for cityindex in range(1,23):
    driver.find_element_by_xpath("/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[2]/mat-form-field/div/div[1]/div/mat-select/div/div[2]").click()
    time.sleep(0.2)
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/mat-option["+ str(cityindex) +"]/span").click()
    time.sleep(0.2)
    driver.find_element_by_xpath("/html/body/app-root/div/app-home/div[2]/div/appointment-table/div/div/div/div/div/div/div/div/div/div/div[2]/form/div/div/div[2]/div/div[3]/button").click()
    time.sleep(0.2)
    citydata = list()
    soup = BeautifulSoup(driver.page_source)
    cityname = soup.find("span", class_="mat-select-min-line ng-tns-c64-3 ng-star-inserted").get_text()
    rows = soup.find_all('div', class_='row ng-star-inserted')
    for row in rows:
        hospital = (row.find("h5", class_ = "center-name-title")).get_text()
        address = row.find("p", class_ = "center-name-text").get_text()
        slots = row.find("ul", class_= "slot-available-wrap").find_all("li")
        avail_slots = list()
        date = datetime.datetime.today().date()
        for slot in slots:
            status = slot.find("a").get_text()
            vaccine = slot.find("h5").get_text()
            try:
                agelimit = slot.find("span").get_text()
            except:
                agelimit = ''
            citydata.append([ hospital, address, date, status, vaccine, agelimit ])
            date += datetime.timedelta(days=1)
    citydata = pd.DataFrame(data=citydata)
    citydata.columns =  ['Hospital', 'Address', 'Date', 'Status', 'Vaccine', 'AgeLimit' ]
    citydata["City"] = cityname
    statedata = statedata.append(citydata)

driver.close()
filename = os.getcwd() + r'\statedata.csv'
print(filename)
statedata.to_csv(filename, index=False)
os.startfile('c:\\Users\Vishaal Sudarsan\\Documents\\Python Files\\statedata.csv')
while(True):
    pass