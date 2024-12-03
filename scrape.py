from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from tqdm import tqdm

#page = "file:///Users/christophebolduc/Documents/Registre des sanctions administratives pécuniaires.html"
page = "file:///Users/christophebolduc/Downloads/page.htm"


driver = webdriver.Chrome()

driver.get(page)

with open('sanctions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["date_imposition", "numero_sanction", "montant", "remarque"])
    
    trs = driver.find_elements(By.TAG_NAME, "tr")
    for tr in tqdm(trs):
        try:
            date_imposition = tr.find_element(By.XPATH, './/*[@title="Date de l\'imposition de la sanction administrative pécuniaire"]').text
        except:
            print("No date")
            continue
        
        numero_sanction = tr.find_element(By.XPATH, './/*[@title="Numéro de la sanction administrative pécuniaires"]').text
        montant = tr.find_element(By.XPATH, './/*[@title="Montant de la sanction"]').text
        
        remarque = tr.find_elements(By.TAG_NAME, "td")[-1].text
        remarque = remarque.replace('\n', ' ').replace('\r', '')
        
        writer.writerow([numero_sanction, date_imposition, montant, remarque])
        