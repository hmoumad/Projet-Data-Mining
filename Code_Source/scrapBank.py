from time import time,sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


driver = webdriver.Chrome('~/chromedriver')
wait = WebDriverWait(driver, 10)
root = 'https://www.google.com/maps/search/Banque/'
driver.get(root)

boot_start = time()
boot_finish = time()
while boot_finish - boot_start < 60:
    scroll = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
    sleep(3)
    boot_finish = time()

elements = [e.find_element(By.TAG_NAME,'a').get_attribute('href') for e in driver.find_elements(By.CSS_SELECTOR,'div[class^=Nv2PK]')]

stat = []

for element in elements:
    Bank = {'nom':'','adresse':'','rate':'','nombre_reaction':'','avis':[]}
    
    driver.get(element)
    
    # Wait for the element to be present
    nom_agence_element = wait.until(EC.presence_of_element_located((By.TAG_NAME,'h1')))
    Bank['nom'] = nom_agence_element.text
    
    try:
        adresse_element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div/div[3]/div[1]')))
        Bank['adresse'] = adresse_element.text
        
    except :
        pass
    try:
        rate_element = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]')
        Bank['rate'] = rate_element.text   
        
    except:
        pass
    try:
        nombre_avis_element = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span')
        Bank['nombre_reaction'] = re.sub('\(|\)','',nombre_avis_element.text)

    except:
        pass

    print(Bank['nom'])
    print(Bank['rate'])
    print(Bank['adresse'])
    print(Bank['nombre_reaction'])
    
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]')))
        
        print('existing reviews')
        
        driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]').click()
        print('get to reviews')
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"wiI7pd")))
        
        print('some comments there')
        start = time()
        finish = time()
        
        while finish - start < 10:
            scroll = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')
            print('scrolling')
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
            print('run scrolling')
            sleep(3)
            finish = time()
        
        Bank['avis'] = [avis.text for avis in driver.find_elements(By.CLASS_NAME,'wiI7pd')]
        
        print(Bank['avis'])

    except:
        print('no comments')

    stat.append(Bank) 
    driver.back()
    
driver.quit()


with open('/home/yassine/python_works/banque_info.json','w') as file:
    json.dump(stat,file)
    
