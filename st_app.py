import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Название приложения
# Описание
st.title('Заполни пропуски')
st.write('Загрузи CSV файл и заполни пропуски')


# Шаг 1. Загрузка данных (CSV файл)
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(5))
else:
    st.info('Upload a CSV file with the first column as the index')
    st.stop()

# Шаг 2. Просмотр пропусков в загруженном датасете
missing_values = df.isna().sum()
missing_values = missing_values[missing_values > 0]

if missing_values is not None:
    fig, ax = plt.subplots()
    sns.barplot(x=missing_values.index, y=missing_values.values, ax=ax)
    ax.set_title('Missing Values')
    ax.set_xlabel('Columns')
    ax.set_ylabel('Count')
    st.pyplot(fig)
else:
    st.write('No missing values found')
    st.stop()

# Шаг 3. Заполнение пропусков по нажатию кнопки

button = st.button('Заполнить пропуски')

if button:
    df_filled = df[missing_values.index]
    for col in df_filled.columns:
        if df[col].dtype == 'object':
            df_filled[col] = df_filled[col].fillna(df[col].mode()[0])
        else:
            df_filled[col] = df_filled[col].fillna(df[col].median())

    st.dataframe(df_filled.head(5))

else:
    st.stop()

# Шаг 4. Выгрузка заполненного от пропусков датасета

button = st.download_button(label='Скачать заполненный датасет', 
                   data=df_filled.to_csv(index=False, sep=',', encoding='utf-8'), 
                   file_name='filled.csv'
                   )


