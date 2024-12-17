import telebot
import fitz  # PyMuPDF
from PIL import Image
import io

BOT_TOKEN = 'you token'  # Replace with your actual bot token
bot = telebot.TeleBot(BOT_TOKEN)

# Message handler for commands
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hello, please send me a PDF file.')

# Document handler
@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with io.BytesIO(downloaded_file) as pdf_file:
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Increase resolution using a zoom factor
                zoom = 2.0  # Increase for better quality; e.g., 2.0 means 200%
                mat = fitz.Matrix(zoom, zoom)  # Scaling matrix
                pix = page.get_pixmap(matrix=mat)  # Render page with scaling
                
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)

                bot.send_document(
                    message.chat.id,
                    img_byte_arr,
                    visible_file_name=f'page_{page_num + 1}.png'
                )

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

bot.infinity_polling()