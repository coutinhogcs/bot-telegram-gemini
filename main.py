import os
import time
import telebot as tb
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


client = genai.Client()


#   FALTAM ADICIONAR

#   LEITURA DE IMAGEM

#   LEITURA DE PDF

#   LEITURA DE VIDEO

#   LEITURA DE AUDIO

#   CRIAÇÃO DE IMAGEM

#   CRIAÇÃO DE VIDEO


BOT_KEY = os.getenv('BOT_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL')
PROMPT = os.getenv('PROMPT')
STARTER_MESSAGE = os.getenv('STARTER_MESSAGE')
bot = tb.TeleBot(BOT_KEY)


def message(message: tb.types.Message):
    return True

def send_long_message(bot, chat_id, text, max_length=4096):
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for chunk in chunks:
        bot.send_message(chat_id, chunk)
        time.sleep(0.5)

@bot.message_handler(commands=['imagem'])
def read_image(image_path):
    pass

@bot.message_handler(commands=['start'])
def start_serb(message:tb.types.Message):
    bot.reply_to(message, STARTER_MESSAGE)


@bot.message_handler(func=message)
def ask_serb(message:tb.types.Message):
    content = message.text
    try:
        response = client.models.generate_content(
            model = GEMINI_MODEL,
            contents = content,
            config= types.GenerateContentConfig(
                temperature=2.0,
                max_output_tokens=8000,
                top_p=0.95,
                system_instruction= PROMPT
            ),
            
        )
        if response.text:
            send_long_message(bot, message.chat.id, response.text)

    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")
        bot.reply_to(message, "Ocorreu um erro ao tentar processar sua solicitação.")
        return
    

while True:
    try:
        print("🤖 Bot iniciado e aguardando mensagens...")
        # O timeout=60 ajuda a evitar conexões "presas"
        bot.polling(non_stop=True, timeout=60) 
        
    except requests.exceptions.ConnectionError as e:
        # Erro de conexão específico (como o seu)
        print(f"⚠️ Erro de conexão detectado: {e}")
        print("Aguardando 10 segundos para reconectar...")
        time.sleep(10) # Aguarda 10s antes de tentar de novo
        
    except Exception as e:
        # Pega qualquer outro erro fatal que o bot.polling não pegou
        print(f"⚠️ Erro fatal no polling: {e}")
        print("Aguardando 5 segundos para reiniciar o polling...")
        time.sleep(5) # Aguarda 5s e o 'while True' vai tentar de novo