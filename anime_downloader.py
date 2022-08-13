import bs4 as bs
import requests
import re
import time
import winsound
import keyboard
import os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_extension('buster.crx')
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')
options.add_argument("--mute-audio")

def func(byPassUrl):
    z = []
    delayTime = 1
    driver.switch_to.default_content()
    driver.get(byPassUrl)
    time.sleep(delayTime)
    outeriframe = driver.find_element(By.TAG_NAME, 'iframe')
    outeriframe.click()
    allIframesLen = driver.find_elements(By.TAG_NAME, 'iframe')
    
    for index in range(len(allIframesLen)):
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(By.ID, 'recaptcha-audio-button') or driver.find_element(By.ID, 'recaptcha-anchor')
            ed = ActionChains(driver)
            ed.move_to_element(audioBtn).move_by_offset(50, 2).click().perform()
            time.sleep(delayTime)
        except Exception as e:
            pass
        
        
    time.sleep(delayTime + 1)
    driver.switch_to.default_content()
    frame = driver.find_element(By.ID, 'btn-submit')
    ed = ActionChains(driver)
    ed.move_to_element(frame).click().perform()
    time.sleep(delayTime + 2)
    driver.switch_to.window(driver.window_handles[0])
    so = bs.BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return so

def dwld_link(so):
    z = []
    lis = []
    download = []
    ls = so.find_all('div', id = 'content-download')
    lp = so.select('.mirror_link')
    ln = so.select('.dowload')
    for i in ln: 
        z.append(str(i))
    for i in z:
        if 'gogo-cdn.com/download' in i:  # take the href out from the list
            l = i[i.find('href=') + 6 : i.find('">Download')]
            download.append(l)
    for i in lp:
        if '(' in i.text:
            s = i.text.split('\n')
            for j in range(len(s)):
                if '(' in s[j]:
                    for v in s[j]:
                        lis.append(s[j][s[j].index('(') +1 : s[j].index(')')])
                        break
    return lis, download

choice = ''
eps = ''
name = ''
name = input('Enter the name of the anime here :\n') # Takes the input name
path = 'https://gogoanime.lu/search.html?keyword='
text = requests.get(path + name)
soup = bs.BeautifulSoup(text.content, 'html.parser')
links = soup.find_all('p', class_ = 'name')

ls = []                    #makes a list of all anime
for i in links:
    if i.find('a'):
        ls.append(i.find('a').get('href', ''))
    else:
        pass
names = [i.split('/')[-1] for i in ls]

for i,j in enumerate(names): # Print the names
    print(i +1 ,j)
if 'search' in path:
    path = path[:path.index('search')]
    
choice = input('Choose from the list :\n')
n = names[int(choice) - 1]
# print('https://gogoanime.lu/category/' + n)
tot = requests.get('https://gogoanime.lu/category/' + n)
no = bs.BeautifulSoup(tot.content, 'html.parser')
total_ep = no.select_one('.active').text.split('-')[-1]
print('Total episodes :- ', total_ep)

inp = input('Do you want to download episodes in bulk : (y/n)\n')
if inp == 'y':
    start = int(input('Start from :'))
    end = int(input('End on :'))
else:
    eps = int(input('Episode Number :\n'))
    start = eps
    end = start
try:    
    for i in range(start, end + 1):
        print('Downloading episode :',i)
        lin = requests.get(path + n + '-episode-' + str(i)) # provides the link to the downlaoder page
        soup = bs.BeautifulSoup(lin.content, 'html.parser')
        ep = soup.find('li', class_ = 'dowloads')
        link = ep.find('a')['href']
        print('LINK :- ', link)

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#         driver = webdriver.Chrome(r'C:\Users\Hemant\Downloads\chromedriver_win32\chromedriver.exe', options=options)
        driver.get(link)
        time.sleep(2)
        so = bs.BeautifulSoup(driver.page_source, 'html.parser')
        ls = so.find_all('div', id = 'content-download')

        if 'g-recaptcha-response' in str(ls[0]):
            sos = func(link)
            lis, download = dwld_link(sos)
            for i, j in enumerate(lis):
                print(i + 1, j)
            down = input('Quality of the downlaod :\n')

            print('DOWNLOADING STARTED ---------------->')
            r = requests.get(download[int(down) - 1])

            title = n + '-episode-' + str(i) + '(' + lis[int(down) - 1] + ')' + '.mp4'
            with open(title, 'wb') as fd:
                fd.write(r.content)
            print('DOWNLOADING COMPLETED ---------------->')
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

        else:
            driver.quit()
            lis, download = dwld_link(so)
            for i, j in enumerate(lis):
                print(i + 1, j)
            down = input('Quality of the downlaod :\n')

            print('DOWNLOADING STARTED ---------------->')
            r = requests.get(download[int(down) - 1])

            title = n + '-episode-' + str(i) + '(' + lis[int(down) - 1] + ')' + '.mp4'
            with open(title, 'wb') as fd:
                fd.write(r.content)
            print('DOWNLOADING COMPLETED ---------------->')
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
except:
    print('Try after some time!!!!!!!!!!!!!!!!!!')