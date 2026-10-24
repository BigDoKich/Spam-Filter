import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Spam Detector",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Детектор спама")
st.caption("Интерфейс для микросервиса на FastAPI (TF-IDF + Logistic Regression)")

try:
    health = requests.get(f"{API_URL}/health", timeout=2)
    backend_ready = health.status_code == 200 and health.json().get("model_loaded")
except Exception:
    backend_ready = False

if not backend_ready:
    st.error("⚠️ Бэкенд недоступен! Запустите сервис: `uvicorn app.main:app --port 8000`")
    st.stop()

st.subheader("⚙️ Настройки классификации")
threshold = st.slider(
    "Порог уверенности (Threshold):",
    min_value=0.0,
    max_value=1.0,
    value=0.85,
    step=0.05,
    help="Сообщение маркируется как СПАМ только если вероятность спама выше либо равна этому значению. Порог 0.85 снижает риск блокировки важных писем."
)

st.markdown("---")

st.subheader("✉️ Ввод сообщения")
message_text = st.text_area(
    "Введите текст для анализа:",
    height=140,
    placeholder="Вставьте сюда текст письма, сообщения или SMS..."
)

if st.button("Проверить сообщение", type="primary", use_container_width=True):
    clean_text = message_text.strip()
    if not clean_text:
        st.warning("Пожалуйста, введите текст сообщения перед отправкой.")
    else:
        with st.spinner("Отправка запроса в сервис..."):
            payload = {
                "text": clean_text,
                "threshold": threshold
            }
            try:
                response = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    is_spam = data["is_spam"]
                    prob = data["spam_probability"]

                    st.markdown("---")
                    st.subheader("📊 Результат анализа")
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if is_spam:
                            st.error("### 🛑 Вердикт: СПАМ")
                        else:
                            st.success("### ✅ Вердикт: НЕ СПАМ (Легитимное)")
                    
                    with col2:
                        st.metric(
                            label="Оценка вероятности спама",
                            value=f"{prob * 100:.1f}%"
                        )

                    st.progress(prob)
                    st.caption(f"Примененный порог отсечения: {data['threshold_used']}")

                else:
                    st.error(f"Ошибка бэкенда ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Не удалось связаться с сервером: {e}")