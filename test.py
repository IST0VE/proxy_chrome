import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Заголовок приложения
st.title('Парсер данных из таблицы')

# Ввод URL пользователем
url = st.text_input('Введите URL веб-страницы с таблицей', '')

# Функция для парсинга данных из таблицы
def parse_table(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'id': 'proxy_list'})
        if not table:
            return None

        # Получаем заголовки столбцов таблицы
        headers = [header.text.strip() for header in table.find_all('th')]

        # Получаем строки таблицы
        rows = []
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                rows.append([col.text.strip() for col in columns])

        # Создаем DataFrame из полученных данных
        return pd.DataFrame(rows, columns=headers)

    except Exception as e:
        return None

# Парсинг и отображение данных
if st.button('Парсить таблицу'):
    if url:
        table_data = parse_table(url)
        if table_data is not None:
            st.write('Данные из таблицы:')
            st.dataframe(table_data)
        else:
            st.write('Не удалось найти таблицу или ошибка при парсинге.')
    else:
        st.write('Введите URL.')

st.write('Это приложение парсит и отображает данные из таблицы на указанной веб-странице.')
