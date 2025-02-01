import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from BotCredentials import bot_cred, cnpj

bot = telebot.TeleBot(bot_cred)

def mcexp():
    chrservice = Service(r'C:\Program Files (x86)\ChromeDriver\chromedriver.exe')
    driver = webdriver.Chrome(service=chrservice)
    
    driver.get('https://mcexperienciasurvey.com/bra');

    elem = driver.find_element(By.ID, "InputCNPJ")
    elem.send_keys(cnpj)

    button = driver.find_element(By.CLASS_NAME, "ui-datepicker-trigger")
    button.click()
    button = driver.find_elements(By.CLASS_NAME, "ui-datepicker-week-end")
    button[3].click()

    for pepe in ['Hour','Minute']:
        elem = driver.find_element(By.ID, f"Input{pepe}")
        elem.send_keys(Keys.ARROW_DOWN)
        elem.send_keys(Keys.ENTER)

    elem = driver.find_element(By.CLASS_NAME, "checkboxSimpleInput")
    elem.click()

    button = driver.find_element(By.ID, "NextButton")
    button.click()

    try:
        while button:
            elem = driver.find_elements(By.CLASS_NAME, "radioSimpleInput")
            for j in range(len(elem)):
                if j % 5 == 0:
                    elem[0].click()
            button = driver.find_element(By.ID, "NextButton")
            button.click()
    except:
        button = False

    for i in ['28','33','34','35','36']:
        elem = driver.find_element(By.ID, f"S0000{i}")
        elem.send_keys('a@b.c')
    button = driver.find_element(By.ID, "NextButton")
    button.click()

    elem = driver.find_elements(By.CLASS_NAME, "radioSimpleInput")
    elem[0].click()
    button = driver.find_element(By.ID, "NextButton")
    button.click()

    cod = driver.find_element(By.ID, 'FinishIncentiveCodeBox')
    dateexp = driver.find_element(By.ID, 'FinishExpirationDateBox')

    a=f'Seu código é {cod.text} válido até {dateexp.text}'
    driver.quit()
    
    return a

@bot.message_handler(commands=['sorvetinhu'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Seu código está sendo gerado. Isso leva alguns segundos.')
	bot.send_message(message.chat.id, mcexp())

@bot.message_handler(func=lambda message: True)
def send_reply(message):
	bot.send_message(message.chat.id, "Se você quiser um código de 2 por 1 para o McFlurry de Ovomaltine Rocks digite /sorvetinhu.")

bot.infinity_polling()