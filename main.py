from dotenv import load_dotenv
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import telebot
import json

load_dotenv()

data = json.loads(open('training.json', 'r', encoding='utf-8').read())
conv = []

for row in data:
    for question in row['questions']:
        conv.append(question)
        conv.append(row['answer'])

print(conv)

# Função para inicializar e treinar o chatbot em uma thread separada
def initialize_chatbot():
    chatbot = ChatBot(
        'Chatbot',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Ainda não sei responder esta pergunta!',
            }
        ]
    )

    trainer = ListTrainer(chatbot)
    trainer.train(conv)

    return chatbot


# Inicialize o chatbot em uma thread separada
chatbot = initialize_chatbot()

# Chave de API do Telegram
TELEGRAM_API_KEY = os.environ['TELEGRAM_API_KEY']

bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Função para verificar se a mensagem deve ser respondida pelo bot
def verify(message):
    return True


@bot.message_handler(func=verify)
def respond(message):
    try:
        question = message.text
        response = chatbot.get_response(question)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        print(f"Erro ao responder à mensagem: {e}")


# Iniciando a escuta de novas mensagens pelo bot
bot.polling()
