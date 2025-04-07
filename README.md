# AMADEUS - TRL- BOT: MIDDLEWARE PARA LA IMPLEMENTACIÓN DEL CHATBOT INTELIGENTE
El desarrollo de mi tesis se basó en la implementación de LLMs (Modelos grandes de lenguaje) para la creación de un asistente virtual inteligente que sea experto en la evaluación de madurez de tecnologías en desarrollo, utilizando como marco de referencia de evaluación el TRL (Technology Readiness Level creado por la NASA). Además, asiste al usuario en como avanzar en su desarrollo tecnológico y es una fuente de conocimientos profunda especializada en información técnica sobre el TRL. Utilizando la metodología CRISP-ML(Q) se diseñó y desarrolló el proyecto en el que se realizaron las fases de:
- Entendimiento del negocio
- Ingeniería de datos (creación de dataset, limpieza del dataset, segmentación de conjunto de datos para entrenamiento y pruebas)
- Ingeniería de modelos (análisis de varios modelos y sus desempeños, e.g. Llama 2, GPT 3.5.turbo, OpenAssistant, Claude...)
- Evaluación de modelos (Fine-tuning y conjunto de pruebas de rendimiento a los modelos seleccionados)
- Despliegue (Diseño de la arquitectura y despliegue de la aplicación en funcionamiento)
![Image](https://github.com/user-attachments/assets/101ae4ad-aa7c-4d75-8092-34b016319d72)


Esta es una aplicación pensada para ser alojada en una máquina virtual que actúa como intermediario entre la API de Telegram y la API de OpenAI. Gestiona la lógica de negocio y las solicitudes/respuestas entre las dos APIs utilizando HTTP.Este script recibe los mensajes de los usuarios desde la API de Telegram, los envía a la API de OpenAI como prompt, y luego devuelve las respuestas generadas de vuelta a Telegram.


![1](https://github.com/user-attachments/assets/164f4d78-8de5-4ae8-8c84-b39030b5611a)

![Image](https://github.com/user-attachments/assets/a0eeb5c3-cdd3-4693-8aa0-42b034ab85b4)



This is an application designed to be hosted on a virtual machine that acts as an intermediary between the Telegram API and the OpenAI API. It manages the business logic and the requests/responses between the two APIs using HTTP.This script receives messages from users through the Telegram API, sends them to the OpenAI API as a prompt, and then returns the generated responses back to Telegram.


El conjunto de datos que se utilizó para entrenar el modelo que se implementó se encuentra en este repositorio:
The dataset used to train the implemented model is located in this repository:
https://github.com/Beta-sebas/dataset_1



