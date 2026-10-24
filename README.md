# 🛡️ End-to-End Spam Detection Microservice

Микросервис для бинарной классификации текстовых сообщений (Spam / Ham), обученный на [ruSpamModels/russian-spam-detection](https://huggingface.co/datasets/ruSpamModels/russian-spam-detection).
За основу взята комбинация **TF-IDF + Logistic Regression**
- Precision: 0.98
- Recall: 0.82
- F1-score: 0.9
  
## Результаты экспериментов

| Модель | Precision | Recall | F1-Score | FP | FN |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes (Baseline)** | 0.9612 | 0.8594 | 0.91 | 2 407 | 9 760 |
| **Logistic Regression** |  **0.9671** | **0.8976** | **0.93** | **2 121** | **7 107** |

### Анализ влияния порога уверенности (Logistic Regression)

| Порог  | Precision | Recall | FP | FN |
| :---: | :---: | :---: | :---: | :---: |
| 0.50 (Default) | 96.71% | 89.76% | 2 121 | 7 107 |
| 0.70 | 98.11% | 86.62% | 1 157 | 9 290 |
| **0.85** | **98.88%** | **82.52%** | **647** | **12 131** |
| 0.90 | 99.18% | 79.97% | 457 | 13 902 |



##  Быстрый запуск

### Запуск через Docker Compose

```bash
docker compose up --build
```

* **Web UI:** [http://localhost:8501](http://localhost:8501)
* **Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)


