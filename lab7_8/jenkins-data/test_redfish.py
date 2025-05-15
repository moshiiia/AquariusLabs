import pytest
import requests
import logging

# Логирование 
logger = logging.getLogger(__name__) #логгер с именем текущ. модуля
logger.setLevel(logging.INFO) #записываются сообщения с уровнем инфо

file_handler = logging.FileHandler("test_redfish.log", mode="w")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)


BASE_URL = "https://localhost:2443/redfish/v1"
USERNAME = "root"
PASSWORD = "0penBmc"

# Фикстура для созданике сессии
@pytest.fixture(scope="module")
def session():
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    session.verify = False
    yield session
    session.close()



# Аутентификация
def test_authentication(session):
    auth_url = f"{BASE_URL}/SessionService/Sessions"

    auth_data ={
        "UserName": f"{USERNAME}",
        "Password": f"{PASSWORD}"
    }

    response = session.post(auth_url, json = auth_data) #преобразует словарь в JSON 
    assert response.status_code == 201, "Authentication error" # При выполнении post запрса возвращает 201 (Создано)
    session_info = response.json()
    assert "@odata.id" in session_info, "The Session token field is missing in the response"
    logger.info("The authentication test was completed successfuly")
    #print(session_info)


# Информация о системе
def test_get_system_info(session):
    system_url = f"{BASE_URL}/Systems/system"
    response = session.get(system_url)
    assert response.status_code == 200, "Error when receiving information about the system"
    system_info = response.json()
    assert "Status" in system_info, "The Status field is missing in the response"
    assert "PowerState" in system_info, "The PowerState field is missing in the response"
    logger.info("The system information acquisition test was completed successfully")



# Управление питанием 
def test_pover_on(session):
    pover_usl = f"{BASE_URL}/Systems/system/Actions/ComputerSystem.Reset"

    pover_data = {
        "ResetType": "On"
    }

    response = session.post(pover_usl, json = pover_data)
    assert response.status_code == 204, "Error when trying to turn on the server"

    # Проверка системы
    system_url = f"{BASE_URL}/Systems/system"
    response = session.get(system_url)
    system_info = response.json()

    assert system_info["PowerState"] == "On", "The server did not turn on" 
    logger.info("The power management test was completed successfully")