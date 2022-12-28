from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


def iniciar_sesion(driver):
    credentials = cred_return()
    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(credentials["email"])

    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(credentials["password"])

    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[4]/button').click()

def cred_return():
    cred_file = open("./credentials.json", "r")
    credentials = cred_file.read()
    credentials = json.loads(credentials)
    cred_file.close
    return credentials


def add_question(question):
  with open("ask.txt", "a", encoding='utf-8') as f:
  # Escribir la nueva línea al final del archivo
    question = question.replace("?", "").replace("¿", "").replace(' ', "-")
    f.write(f"{question}\n")

def get_question():
    filename = 'ask.txt'
    f = open(filename, 'r+', encoding='utf-8')
    # Leemos todas las líneas del archivo
    lines = f.readlines()
    first_line =  lines[0]
    # Borramos la primera línea
    lines.pop(0)
    f = open(filename, "w", encoding='utf-8')
    f.writelines(lines)
    f.close

    f = open('askDone.txt', "a", encoding='utf-8')
    f.writelines(first_line)
    f.close
    return first_line


def return_questions():
  
  HEADERS = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate",
      "Accept":"*/*",
      "Keep-Alive": "300",
      "Connection": "keep-alive",
      "Upgrade-Insecure-Requests": "1",
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
  }
  # Toma el tiempo de inicio
  start_time = time.perf_counter()
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
  driver.get('https://es.quora.com/profile/Lzarusss/questions')

  scroll_amount = 150

  # Número de veces que se va a hacer scroll
  num_scrolls = 2000
  print(f"El script tardará aproximadamente {num_scrolls*0.4} segundos")
  # Hacer scroll hasta el final de la página
  for i in range(num_scrolls):
    # Ejecutar código JavaScript para hacer scroll
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    # Esperar unos segundos entre cada iteración
    time.sleep(0.4)
    percent_complete = (i + 1) / num_scrolls * 100
    print(f"\rProgreso: [{'#' * int(percent_complete // 2):50}] {percent_complete:.1f}%", end="")

  print("\nGenerando preguntas...\n")
  # Obtener el HTML de la página
  html = driver.page_source

  # Cerrar el navegador
  driver.close()

  soup = BeautifulSoup(html, "html.parser")

  num = 0

  for i in soup.find_all("span", class_="q-box"):
      for x in i.find_all("span"):
          add_question(x.text)
          num+=1
  print(f"Num of questions add to file: {num}")
  end_time = time.perf_counter()
  elapsed_time = end_time - start_time

  # Muestra el tiempo transcurrido
  print(f"Tiempo transcurrido: {elapsed_time:.6f} segundos")

def request_question():
  start_time = time.perf_counter()
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
  driver.get("https://es.quora.com/")

  iniciar_sesion(driver)
  time.sleep(2)
  num = 50
  while num != 0:
    print(f'\rPregunta número: {num} ', end="")
    try:
      time.sleep(2)
      url = str(f'https://es.quora.com/{get_question()}')
      time.sleep(1)
      driver.get(url)
      time.sleep(1.4)
      
      driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div/div/div/div[2]/div/div/div/div[1]/button[3]').click()

      time.sleep(4)
      for i in range(1, 19):
        driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div/div/div/div[1]/div[2]/div[{i}]/div/div/div/div[3]/div/div/div').click()
        time.sleep(0.15)
    except Exception as e:
      pass
    num -= 1

  end_time = time.perf_counter()
  elapsed_time = end_time - start_time
  # Muestra el tiempo transcurrido
  print(f"Tiempo transcurrido: {elapsed_time:.6f} segundos")
  driver.close()
request_question()