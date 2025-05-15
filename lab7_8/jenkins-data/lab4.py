import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # Ожидание перед поиском элементов
    driver.get("https://localhost:2443/?next=/login#/")
    return driver


# Проверка успешного входа по блоку пользователя root
def is_logged_in(wait):
    try:
        user_button = wait.until(EC.presence_of_element_located((By.ID, "app-header-user__BV_toggle_")))
        return user_button.is_displayed()
    except:
        return False


# Тест для успешной авторизации
def test_successful_login():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    print("[INFO] Тест успешного входа")

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))

    username_field.send_keys("root")
    password_field.send_keys("0penBmc")  
    login_button.click()

    if is_logged_in(wait):
        print("[PASSED] Авторизация прошла успешно.")
    else:
        print("[FAILED] Авторизация не удалась!")

    driver.quit()

# Тест для неверных данных
def test_invalid_login():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)

    print("[INFO] Тест входа с неверными данными")

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))

    username_field.send_keys("wrong_user")
    password_field.send_keys("wrong_password")
    login_button.click()

    # Проверяем, что вход не произошел
    if is_logged_in(wait):
        print("[FAILED] Прошла авторизация с неверными данными!")
    else:
        print("[PASSED] Авторизация не состоялась.")



# Тест для блокировки учетной записи
def test_block_user():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    def attempt_login(username_value, password_value):
        time.sleep(3)
        username = driver.find_element(By.ID, 'username')
        password = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.mt-3')
        username.send_keys(username_value)
        password.send_keys(password_value)
        login_button.click()

    print("[INFO] Тест блокировки пользователя")
    attempt_login('testuser', 'testpasswd1')  # Правильный пароль
    time.sleep(3)

    for _ in range(3):
        attempt_login('testuser', 'testpass')  # Неверный пароль
        time.sleep(3)

    attempt_login('testuser', 'testpasswd1')  # Правильный пароль
    time.sleep(3)

    if is_logged_in(wait):
        print("[FAILED] Блокировка не прошла!")
    else:
        print("[PASSED] Блокировка прошла успешно.")
    driver.quit()


# Запуск тестов
if __name__ == "__main__":
    test_successful_login()
    test_invalid_login()
    test_block_user()
    print("[INFO] Все тесты завершены.")
