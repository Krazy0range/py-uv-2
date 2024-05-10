from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
import mutagen
import os
import shutil

spotify_urls_file = 'C:/Users/Teo/Desktop/spotify-links.txt'
spotify_urls = []
with open(spotify_urls_file, 'r') as file:
    spotify_urls = file.readlines()
    
spotify_urls = spotify_urls

spotify_converter = 'https://spotifydown.com'

with webdriver.Firefox() as driver:
    for i, spotify_url in enumerate(spotify_urls):
        # driver.execute_script(f'window.open(\'about:blank\', \'tabulation{i}\')')
        # driver.switch_to.window(f'tabulation{i}')
        driver.get(spotify_converter)
        sleep(0.5)
        url_input = driver.find_element(By.XPATH, '//input')
        url_input.send_keys(spotify_url)
        sleep(0.5)
        submit_button = driver.find_element(By.XPATH, '//button[contains(., \'Download\')]')
        submit_button.click()
        sleep(0.5)
        download_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[contains(., \'Download\')]')))
        driver.execute_script('arguments[0].click()', download_button);
        sleep(0.5)
        last_download_button = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//a[contains(., \' MP3\')]')))
        driver.execute_script('arguments[0].click()', last_download_button)
        sleep(2)
        
        filename = max(['C:/Users/Teo/Downloads/' + f for f in os.listdir('C:/Users/Teo/Downloads/')], key=os.path.getctime)
        audio = mutagen.File(filename, easy=True)
        filename_new = f'{audio['artist'][0]} - {audio['title'][0]}'
        filename_new = filename_new.replace('/', ' ')
        shutil.move(filename, f'C:/Users/Teo/Documents/uv-2/mp3s/{filename_new}.mp3')

# x TODO: change tab system; it crashes after 20 tabs