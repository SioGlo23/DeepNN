import streamlit as st
import requests
import json
import numpy as np
import pickle
import os

# Загрузка скейлера
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

st.title("Прогноз цены на жильё с использованием нейронной сети Keras")

# API для модели Keras
API_URL = "https://predict-cal-houses.onrender.com/predict"  # FastAPI URL


# Вводные данные
MedInc = st.number_input("Медианный доход", value=3.0)
HouseAge = st.number_input("Средний возраст жилья", value=3.0)
AveRooms = st.number_input("Среднее кол-во комнат", value=3.0)
AveBedrms = st.number_input("Среднее кол-во спален", value=3.0)
Population = st.number_input("Население", value=1500.0)
AveOccup = st.number_input("Среднее кол-во человек в доме", value=500.0)
Latitude = st.number_input("Широта", value=37.88)
Longitude = st.number_input("Долгота", value=-122.33)


if st.button("Получить прогноз"):
    # Подготовка данных для запроса
    data = {
        "MedInc": MedInc,
        "HouseAge": HouseAge,
        "AveRooms": AveRooms,
        "AveBedrms": AveBedrms,
        "Population": Population,
        "AveOccup": AveOccup,
        "Latitude": Latitude,
        "Longitude": Longitude
    }

     # Отправка запроса к API
    try:
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            result = response.json()
            prediction = result.get('prediction')
            st.success(f'Прогнозируемая цена: {prediction*100000:.2f}$')

            # Визуализация результата
            st.subheader('Визуализация прогноза')
            st.bar_chart({"Прогноз": [prediction]})
        else:
            st.error(f"Ошибка API: {response.status_code}")
    except Exception as e:
        st.error(f"Ошибка при отправке запроса: {str(e)}")   