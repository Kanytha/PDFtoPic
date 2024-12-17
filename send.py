import telebot
import pandas as pd

BOT_TOKEN = 'your token'
bot = telebot.TeleBot(BOT_TOKEN)

chat_data = pd.read_excel('user_data.xlsx')

for user_id in chat_data['user_id']:
    print(user_id)
    bot.send_message(user_id, "Hello, I'm here to help you.")
    
# bot.send_photo(id, open('img/lala.jpg', 'rb'), caption = 'This is a photo from this bot.')