
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.google.com")
print("Заголовок страницы:", driver.title)

driver.quit()