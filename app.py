import streamlit as st
import random

# Инициализация состояния игры
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.record = None
    st.session_state.max_number = 100
    st.session_state.max_attempts = 7
    st.session_state.wins = 0      # счётчик побед
    st.session_state.losses = 0    # счётчик поражений

st.title("🎯 Проверь свой фарт 😂")

# Выбор уровня сложности (только в начале игры)
if st.session_state.game_over == False and st.session_state.attempts == 0:
    level = st.selectbox("Выбери уровень сложности:", 
                         ["Лёгкий (1-50, 10 попыток)", 
                          "Средний (1-100, 7 попыток)", 
                          "Сложный (1-200, 5 попыток)"])
    if level == "Лёгкий (1-50, 10 попыток)":
        st.session_state.max_number = 50
        st.session_state.max_attempts = 10
    elif level == "Средний (1-100, 7 попыток)":
        st.session_state.max_number = 100
        st.session_state.max_attempts = 7
    else:
        st.session_state.max_number = 200
        st.session_state.max_attempts = 5
    st.session_state.secret_number = random.randint(1, st.session_state.max_number)

st.write(f"Я загадал число от 1 до {st.session_state.max_number}.")
st.write(f"У тебя {st.session_state.max_attempts} попыток.")

# Основная игровая логика
if not st.session_state.game_over:
    guess = st.number_input("Введите число:", 
                            min_value=1, 
                            max_value=st.session_state.max_number, 
                            step=1, 
                            key="guess")
    if st.button("🔍 Проверить"):
        st.session_state.attempts += 1
        if guess < st.session_state.secret_number:
            st.warning("📈 Моё число БОЛЬШЕ!")
        elif guess > st.session_state.secret_number:
            st.warning("📉 Моё число МЕНЬШЕ!")
        else:
            # ПОБЕДА!
            st.session_state.wins += 1
            st.success(f"🎉 ПОБЕДА! Ты угадал за {st.session_state.attempts} попыток!")
            if st.session_state.record is None or st.session_state.attempts < st.session_state.record:
                st.session_state.record = st.session_state.attempts
                st.balloons()
            st.session_state.game_over = True
    # Проверка на исчерпание попыток
    if st.session_state.attempts >= st.session_state.max_attempts and not st.session_state.game_over:
        st.session_state.losses += 1
        st.error(f"😢 Ты исчерпал все попытки! Я загадал {st.session_state.secret_number}.")
        st.session_state.game_over = True

# Отображение статистики
st.write(f"Попыток: {st.session_state.attempts} из {st.session_state.max_attempts}")
if st.session_state.record is not None:
    st.write(f"🏆 Рекорд: {st.session_state.record} попыток")
# --- СЧЁТЧИК ПОБЕД И ПОРАЖЕНИЙ ---
col1, col2 = st.columns(2)
col1.metric("✅ Побед", st.session_state.wins)
col2.metric("❌ Поражений", st.session_state.losses)

# Кнопка "Новая игра"
if st.session_state.game_over:
    if st.button("🔄 Новая игра"):
        # Сброс параметров игры, но счётчики остаются
        st.session_state.secret_number = random.randint(1, st.session_state.max_number)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.rerun()