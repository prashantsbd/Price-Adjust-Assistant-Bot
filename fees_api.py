import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
option = webdriver.ChromeOptions()
option.add_argument("--window-size=1180,1180")
option.add_argument("--headless")
driver = webdriver.Chrome(options=option)
load_dotenv()
driver.get(os.getenv("li_url"))
driver.implicitly_wait(10)
driver.find_element(By.XPATH, "//input[1]").send_keys(os.getenv("ID"))
driver.find_element(By.ID, "password").send_keys(os.getenv("PW"))
driver.find_element(By.XPATH, "//button").click()
driver.implicitly_wait(7)
driver.find_element(By.XPATH, "//div[@class='dotm_action_card'][5]").click()
driver.find_element(By.ID, "disclaimer").click()
driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
driver.implicitly_wait(5)
# 2 vaneko bike 3 vaneko car
driver.find_element(By.XPATH, "//div[@class='dotm_category_wrapper']/div[2]/label").click()
driver.implicitly_wait(3)
driver.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()
driver.implicitly_wait(10)
y = 0
a = driver.find_elements(By.XPATH, "//div[@class='col-12 col-sm-6'][1]//option")
apidata = []
for i in range(len(a)-1):
    prov = driver.find_element(By.XPATH, f"//div[@class='col-12 col-sm-6'][1]//option[{i+2}]")
    prov.click()
    b = driver.find_elements(By.XPATH, "//div[@class='col-12 col-sm-6'][2]//option")
    for j in range(len(b)-1):
        off = driver.find_element(By.XPATH, f"//div[@class='col-12 col-sm-6'][2]//option[{j+2}]")
        rawdata2 = off.text
        arr_data2 = rawdata2.split(", ")
        try:
            data2 = arr_data2[1]
        except:
            arr_data2 = rawdata2.split(",")
            data2 = arr_data2[1]
        off.click()
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "//div[@class='input-group required']/input").click()
        driver.implicitly_wait(3)
        quota = driver.find_elements(By.CSS_SELECTOR, "td.nepDate")
        available = len(quota)
        match available:
            case 0:
                price = 999
            case 1:
                price = 949
            case 2:
                price = 900
            case 3:
                price = 799
            case 4:
                price = 640
            case 5:
                price = 600
            case 6:
                price = 499
            case 7:
                price = 499
            case 8:
                price = 399
            case 9:
                price = 350
            case _:
                print(available)
                price = 0
        datapkt = {"office":data2,"price":price}
        apidata.append(datapkt)
        driver.find_element(By.CSS_SELECTOR, ".btn-danger").click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='col-12 col-sm-6'][1]//option")))
mypacket = json.dumps(apidata)
liveurl = "http://www.nabinrekha.com.np/pricefed_api.php?API_KEY="+os.getenv("Api_key")
result = requests.post(liveurl, data=mypacket, timeout=40)
print(result)