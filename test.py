from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import argparse

parser = argparse.ArgumentParser(add_help=False, description="Write -f or --func ['req', 'send'] to change the use of the script")
parser.add_argument('-f', '--func', type=str, choices=['req', 'send'], required=True, help="Option to know if you want to collect questions(req) or send requests(send)")
parser.add_argument('-n', '--num', type=int, required=False, help="Number of questions you want for the script(if you dont say any number, in defect will be 10)\nIn case of option req you must put a longer number if you want get more questions like(500, 1000, 1500...)")
parser.add_argument('-L', '--login', required=False, action='store_true', help="argument to log in manually (to bypass captha manually) ")
parser.add_argument('-h', '--help', action='help', help="Write -f or --func ['req', 'send'] to change the use of the script\nExample: python .\\test.py -f send\nIf Login returns Captcha error put -L to login manually")
args = parser.parse_args()

def iniciar_sesion(driver):
    credentials = cred_return()
    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(credentials["email"])

    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(credentials["password"])

    if args.login:
        time.sleep(20)
    else:
        time.sleep(1)
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

  # Toma el tiempo de inicio
  start_time = time.perf_counter()
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
  driver.get('https://es.quora.com/profile/Lzarusss/questions')

  scroll_amount = 150

  # Número de veces que se va a hacer scroll
  preventiveNegativeQuestions = lambda num: 50 if num <= 0 else num
  try:
    num_scrolls = args.num
    num_scrolls = preventiveNegativeQuestions(num_scrolls)
  except:
    num_scrolls = 50
  print(f"The script will take approximately {num_scrolls*0.4/60:.1f} minutes")
  # Hacer scroll hasta el final de la página
  for i in range(num_scrolls):
    # Ejecutar código JavaScript para hacer scroll
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    # Esperar unos segundos entre cada iteración
    time.sleep(0.4)
    percent_complete = (i + 1) / num_scrolls * 100
    print(f"\rProgress: [{'#' * int(percent_complete // 2):50}] {percent_complete:.1f}%", end="")

  print("\nGenerating questions...\n")
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
  elapsed_time = (end_time - start_time) / 60

  # Muestra el tiempo transcurrido
  print(f"\nTime past: {elapsed_time:.2f} minutes")
  exit()

def request_question():
  start_time = time.perf_counter()
  options = webdriver.ChromeOptions() 
  options.add_experimental_option("excludeSwitches", ["enable-logging"])
  driver = webdriver.Chrome(options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')
  driver.get("https://es.quora.com/")

  iniciar_sesion(driver)

  try:
    num = args.num
    preventiveNegativeQuestions = lambda num: 20 if num <= 0 else num
    num = preventiveNegativeQuestions(num)
  except:
    num = 20
  print(f'Questions -> {num}')

  try:
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
  except:
    pass

  while num != 0:
    print(f'\rQuestion number: {num} ', end="")
    try:
      time.sleep(2)
      url = str(f'https://es.quora.com/{get_question()}')
      time.sleep(1)
      driver.get(url)
      time.sleep(1.4)
      
      driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div/div/div/div[2]/div/div/div[1]/button[3]').click()

      time.sleep(4)
      for i in range(1, 19):
        driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div/div/div/div/div[1]/div[2]/div[{i}]/div/div/div/div[3]/div/div/div').click()
        time.sleep(0.15)
    except Exception as e:
      pass
    num -= 1

  end_time = time.perf_counter()
  elapsed_time = (end_time - start_time) / 60
  time.sleep(2)
  # Muestra el tiempo transcurrido
  print(f"\nTime past: {elapsed_time:.2f}  minutes")
  driver.close()
  exit()

if args.func == 'req':
    return_questions()
elif args.func == 'send':
    request_question()
