from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def wikipedia_search():
    # Инициализация браузера
    browser = webdriver.Chrome()  # ← Теперь используем понятное имя

    try:
        while True:
            query = input("\nВведите запрос (или 'выход'): ").strip()
            if query.lower() in ('выход', 'exit', 'quit'):
                break

            # Прямой переход к статье
            browser.get(f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}")
            time.sleep(1)

            try:
                # Получаем заголовок и содержание
                title = browser.find_element(By.ID, "firstHeading").text
                content = browser.find_element(By.CSS_SELECTOR, ".mw-parser-output p").text

                print(f"\n📖 {title}")
                print(f"\n{content[:500]}...")  # Вывод первых 500 символов

                action = input("\n1. Читать дальше\n2. Новый запрос\nВыбор: ").strip()
                if action == "1":
                    # Читаем следующие 2 параграфа
                    paragraphs = browser.find_elements(By.CSS_SELECTOR, ".mw-parser-output p")
                    for p in paragraphs[1:3]:
                        if p.text.strip():
                            print(f"\n{p.text}")

            except NoSuchElementException:
                print("Статья не найдена. Попробуйте другой запрос")

    finally:
        browser.quit()  # ← Соответствующее имя метода
        print("Программа завершена")


if __name__ == "__main__":
    wikipedia_search()