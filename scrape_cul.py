from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from tqdm import tqdm

#page = "file:///Users/christophebolduc/Documents/Registre des sanctions administratives pécuniaires.html"
#page = "file:///Users/christophebolduc/Downloads/page.htm"
page = "file:///Users/christophebolduc/Documents/PickPick/Registre des déclarations de culpabilité.html"


driver = webdriver.Chrome()

driver.get(page)

with open('culpabilites.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["date_declaration", "loi"])
    
    trs = driver.find_elements(By.TAG_NAME, "tr")
    for tr in tqdm(trs):
        try:
            date_declaration = tr.find_element(By.XPATH, './/*[@title="Date de la déclaration de la culpabilité"]').text
        except:
            print("No date")
            continue
        
        loi = tr.find_element(By.XPATH, './/*[@title="Consultez la loi ou le règlement"]').text
        
        writer.writerow([date_declaration, loi])
        