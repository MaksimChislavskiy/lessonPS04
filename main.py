from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def wikipedia_search():
    # Инициализация браузера
    browser = webdriver.Chrome()

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

                while True:
                    action = input(
                        "\n1. Читать дальше\n2. Новый запрос\n3. Перейти на связанную страницу\nВыбор: ").strip()

                    if action == "1":
                        # Читаем следующие 2 параграфа
                        paragraphs = browser.find_elements(By.CSS_SELECTOR, ".mw-parser-output p")
                        for p in paragraphs[1:3]:
                            if p.text.strip():
                                print(f"\n{p.text}")

                    elif action == "2":
                        break  # Выход из внутреннего цикла для нового запроса

                    elif action == "3":
                        # Получаем все ссылки из основного содержимого
                        links = browser.find_elements(By.CSS_SELECTOR, ".mw-parser-output p a[href^='/wiki/']")
                        if not links:
                            print("Связанные страницы не найдены.")
                            continue

                        # Формируем список уникальных ссылок с их текстом
                        unique_links = []
                        seen_links = set()
                        for link in links:
                            href = link.get_attribute("href")
                            text = link.text.strip()
                            if href and text and href not in seen_links:
                                seen_links.add(href)
                                unique_links.append((text, href))

                        # Выводим список ссылок для выбора
                        if not unique_links:
                            print("Нет доступных связанных страниц.")
                            continue

                        print("\nДоступные связанные страницы:")
                        for i, (text, href) in enumerate(unique_links[:10], 1):  # Ограничиваем 10 ссылками
                            print(f"{i}. {text}")

                        choice = input("\nВыберите номер страницы (или 0 для отмены): ").strip()
                        try:
                            choice = int(choice)
                            if 1 <= choice <= len(unique_links):
                                selected_link = unique_links[choice - 1][1]
                                browser.get(selected_link)
                                # Обновляем заголовок и содержание после перехода
                                title = browser.find_element(By.ID, "firstHeading").text
                                content = browser.find_element(By.CSS_SELECTOR, ".mw-parser-output p").text
                                print(f"\n📖 {title}")
                                print(f"\n{content[:500]}...")
                            elif choice != 0:
                                print("Некорректный выбор.")
                        except ValueError:
                            print("Введите число.")

                    else:
                        print("Некорректный выбор. Попробуйте снова.")

            except NoSuchElementException:
                print("Статья не найдена. Попробуйте другой запрос")

    finally:
        browser.quit()
        print("Программа завершена")


if __name__ == "__main__":
    wikipedia_search()