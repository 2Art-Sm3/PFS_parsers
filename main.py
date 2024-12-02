from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# === 1. Настройка папки для сохранения файлов ===
# Указываем директорию для скачивания
DOWNLOAD_FOLDER = "downloads"  # Имя папки, куда будут сохраняться файлы

# === 2. Настройка ChromeDriver для автоматического скачивания файлов ===
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),  # Путь для загрузки
    "download.prompt_for_download": False,  # Отключение всплывающего окна с запросом загрузки
    "download.directory_upgrade": True,  # Разрешение менять директорию загрузки
    "safebrowsing.enabled": True,  # Отключение предупреждений о безопасности
}
options.add_experimental_option("prefs", prefs)

# === 3. Создание экземпляра драйвера Chrome ===
driver = webdriver.Chrome(options=options)

try:
    # === 4. Переход на сайт с проектами ===
    driver.get("https://gisp.gov.ru/nmp/main/?recommended=0&search_terms=&search_terms=&search_terms=&search_terms=&event=&search_terms=&search_terms=&search_terms=&search_terms=&search_terms=&measureActive=1&searchstr=&csrftoken=1809ba1086ebed6939c64a68812d4a676b4f06aef49a6bf91c361e661bcaf32f5b54d4342bda65a1")
    wait = WebDriverWait(driver, 5)  # Явное ожидание элементов на странице (до 10 секунд)

    # === 5. Цикл для обработки всех страниц с проектами ===
    while True:
        # ШАГ 1: Находим ссылки на проекты на текущей странице


        project_links = driver.find_elements(By.CSS_SELECTOR, ".catalog__list-info a")
        print(project_links[0].get_attribute("href"))
        # ШАГ 2: Переходим в каждый проект
        for project in project_links:
            project_url = project.get_attribute("href")  # Получаем URL проекта
            driver.execute_script("window.open(arguments[0], '_blank');", project_url)  # Открываем проект в новой вкладке
            driver.switch_to.window(driver.window_handles[-1])  # Переключаемся на новую вкладку

            try:
                # ШАГ 3: Скачиваем файл "Скачать условия" на странице проекта
                download_button = wait.until(EC.element_to_be_clickable(
                    (By.LINK_TEXT, "Скачать условия")  # Кнопка "Скачать условия"
                ))
                download_button.click()  # Нажимаем кнопку для скачивания
                time.sleep(0.1)  # Задержка, чтобы файл успел сохраниться
            except Exception as e:
                print(f"Не удалось скачать файл: {e}")  # Логируем ошибки, если кнопка недоступна
            finally:
                driver.close()  # Закрываем вкладку
                driver.switch_to.window(driver.window_handles[0])  # Возвращаемся на страницу списка проектов

        # ШАГ 4: Проверяем, есть ли следующая страница
        try:
            # Ищем кнопку "Следующая страница" через селектор на основе атрибутов

            next_button = driver.find_elements(By.CSS_SELECTOR, "a[href*='/nmp/main/'] svg use")
            if len(next_button) == 1:
                # Если только один элемент (первая итерация), кликаем по нему
                print("Кликаем по единственному элементу")
                next_link = next_button[0].find_element(By.XPATH, "..")
                next_link.click()

            elif len(next_button) > 1:
                # Если два или больше, кликаем по второму
                print("Кликаем по второму элементу")
                next_link = next_button[1].find_element(By.XPATH, "..")
                next_link.click()
            # Кликаем по кнопке

            # Ждем, пока загрузится новая страница (пример: ждем появления контента карточек проектов)
            time.sleep(5)

        except TimeoutException:
            print("Следующей страницы не найдено.")
            break

finally:
    # === 6. Завершаем работу и закрываем браузер ===
    driver.quit()



