from dotenv import load_dotenv, find_dotenv
import requests
import openai
import json
import time
import os

class ChatBotMaker:
    
    def __init__(self, env_file):
        load_dotenv(find_dotenv(env_file))
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.telegram_token = os.getenv("TELEGRAM_API_KEY")
        self.model_engine = os.getenv("MODEL_ENGINE")
        self.chats = []
    
    
    def get_updates(self, offset: int):
        """
        Función para obtener los mensajes más recientes del Bot de telegram
        :param offset: se utiliza para indicar el identificador del último mensaje recibido por el bot. Este parámetro
        se usa junto con el método "getUpdates" para obtener solo los mensajes nuevos que han llegado desde el último
        mensaje procesado por el bot.
        :return:
        """
        url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
        params = {"timeout": 100, "offset": offset}
        response = requests.get(url, params=params)
        print(response)
        return response.json()["result"]
    
    
    def send_messages(self, chat_id, text: str):
        """
        Envía un mensaje del BOT al Usuario de Telegram
        :param chat_id: Id del chat al cual será enviado el mensaje
        :param text: texto a enviar
        :return:
        """
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        params = {"chat_id": chat_id, "text": text}
        print(params)
        response = requests.post(url, params=params)
        #print(response)
        return response
    
    
    def validate_chat(self, chat_id, user_message):
        """
        Valida si el mensaje de usuario de la actualización recibida pertenece a una conversación existente o nueva, luego almacena el mensaje dentro del contexto de la conversación.
        :param chat_id: id de la conversación en Telegram
        :user_message: mensaje escrito por el usuario en Telegram
        :return:
        """
        conversation_found = False
        
        if not self.chats:
            print(f"No existen conversaciones, creando conversación...")
            new_conversation = Conversation(chat_id, user_message)
            self.chats.append(new_conversation)
        else:    
            for conversation in self.chats:
                if chat_id == conversation.chat_id:
                    print(f"la conversación de id {chat_id} ya existe, se añadirá este mensaje de usuario a la conversación")
                    conversation_found = True
                    conversation.add_user_message(user_message)
                else:
                    conversation_found = False

            if conversation_found == False:
                print(f"la conversación de id {chat_id} no existe, creando conversación...")
                new_conversation = Conversation(chat_id, user_message)
                self.chats.append(new_conversation)
            
    
    def get_openai_response(self, chat_id):
        """
        Genera una respuesta a un prompt de entrada utilizando el modelo de ChatGPT fine-tuned
        :param chat_id: id de la conversación a la que se le quiere generar una respuesta por parte de GPT
        :return:
        """
        
        for conversation in self.chats:
            if chat_id == conversation.chat_id:
                messages = conversation.messages

        try:
            response = openai.ChatCompletion.create(
                model = self.model_engine, 
                messages = messages, 
                temperature = 0.5, 
                max_tokens = 500,
                #n = 1,
                #stop = None
            )
            
            new_answer = response["choices"][0]["message"]["content"]
            
            for conversation in self.chats:
                if chat_id == conversation.chat_id:
                    conversation.add_assistant_message(new_answer=new_answer)
                    
            return new_answer
        
        except openai.error.APIError as e:
            # Manejar error de API aquí, p. reintentar o iniciar sesión
            print(f"La API de OpenAI devolvió un error de API: {e}")
            pass  # Aprobar
        except openai.error.APIConnectionError as e:
            # Manejar error de conexión aquí
            print(f"Error al conectarse a la API de OpenAI: {e}")
            pass
        except openai.error.RateLimitError as e:
            # Manejar error de límite de tasa (recomendamos usar retroceso exponencial)
            print(f"La solicitud de API de OpenAI excedió el límite de frecuencia: {e}")
            pass

        return "Ocurrió un Error :("
    
    def save_conversations(self):
        
        conversations=[]
        for chat in self.chats:
            new_conversation={"chat_id": chat.chat_id, "messages": chat.messages}
            conversations.append(new_conversation)
        
        with open("saved_conversations.jsonl", 'w', encoding="utf8") as file:
            for conversation in conversations:
                json_line = json.dumps(conversation)
                file.write(json_line + '\n')    
        
    def run(self):
        print("Starting bot...")
        offset = 0
        
        while True:
            #Escucha nuevos mensajes en telegram
            updates = self.get_updates(offset)
            
            if updates:
                for update in updates:
                    
                    offset = update["update_id"] + 1
                    chat_id = update["message"]["chat"]['id']
                    user_message = update["message"]["text"]
                    print(f"Received message: {user_message}")
                    
                    #valida si la conversación es nueva o existente, y almacena el mensaje
                    self.validate_chat(chat_id, user_message)
                    
                    #Genera una respuesta del modelo GPT basado en el mensaje de telegram(prompt)
                    GPT_answer = self.get_openai_response(chat_id)
                    #Envía a telegram la respuesta del modelo para que se le imprima al usuario
                    self.send_messages(chat_id, GPT_answer)
                    
                    if user_message == "pushtohub":
                        self.save_conversations()
                        
                    
            else:
                time.sleep(1)
                
                
class Conversation:
    
    
    def __init__(self, chat_id, first_prompt):
        
        self.chat_id = chat_id
        self.messages = []
        
        #system_job = "Eres un asistente de Platzi, que es una plataforma de cursos de educaci\u00f3n en l\u00ednea. T\u00fa ayudas a sus estudiantes a resolver dudas sobre la plataforma y sus cursos"
        system_job = "Eres un asistente experto en medir el nivel de madurez de tecnologías utilizando la métrica de 9 niveles del TRL creada por la nasa, y eres capaz de preguntar a los usuarios sobre sus tecnologías para evaluar el nivel de madurez tecnológico que tienen, mientras resuelves sus dudas sobre el TRL."
        self.messages.append({"role": "system", "content": system_job})
        self.messages.append({"role": "user", "content": first_prompt})
        
        
    def add_user_message(self, new_prompt):
        self.messages.append({"role": "user", "content": new_prompt})
        
        
    def add_assistant_message(self, new_answer):
        self.messages.append({"role": "assistant", "content": new_answer})