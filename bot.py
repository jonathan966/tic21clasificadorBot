import sys
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import requests
token = "1658087960:AAEobjhwQf3BLslH2y9FwI7zhFutts7Xjp0"

def start(bot, update):
    try:
        username = update.message.from_user.username
        message = "Hola "+ username
        update.message.reply_text(message)
    except Exception as error:
        print("Error 001{}".format(error.args[0]))

def echo(bot,update):
    try:
        respuesta = update.message.text

        def classify(text):
            key =  "6c145410-a196-11eb-921d-1bb481e93c2ba377c648-e5a7-4f4d-b8b9-cd4db3b9f8d4"
            url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

            response = requests.get(url, params={ "data" : text })

            if response.ok:
                responseData = response.json()
                topMatch = responseData[0]
                return topMatch
            else:
                response.raise_for_status()

        demo = classify(respuesta)

        label = demo["class_name"]
        confidence = demo["confidence"]
          
        if label == "Pug":
            respuesta1 = " Me parece que me estas hablando de un lindo Pug"
            update.message.reply_text(respuesta1)
        elif label == "Pastor_aleman":
            respuesta2 = " Me parece que me estas hablando de un genial Pastor Aleman"
            update.message.reply_text(respuesta2)
    except Exception as error:
       print("Error 002{}".format(error.args[0]))
       
def help(bot, update):
    try:
        message = "puedes enviar texto o imagen"
        update.message.reply_text(message)
    except Exception as error:
        print("Error 003{}".format(error.args[0]))

def error(bot, update):
    try:
        print(error)
    except Exception as e:
        print("Error 004{}".format(e.args[0]))

def getImage(bot, update):
    try:
        message = "Recibiendo imagen "
        update.message.reply_text(message)

        file = bot.getFile(update.message.photo[-1].file_id)
        id = file.file_id

        filename = os.path.join("descargas/","{}.jpg".format(id))
        file.download(filename)

        message = "imagen guardada"
        update.message.reply_text(message)

        prediction = clasificar(filename)
        print(prediction)
        
        update.message.reply_text(prediction)
    except Exception as e:
        print("Error 007{}".format(e.args[0]))


def clasificar(imagee):
       np.set_printoptions(suppress=True)
       model = tensorflow.keras.models.load_model('keras_model.h5')
       data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
       image = Image.open(imagee)
       size = (224, 224) 
       image = ImageOps.fit(image, size, Image.ANTIALIAS)
       image_array = np.asarray(image)
       normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
       data[0] = normalized_image_array

       prediction = model.predict(data)
       print(prediction)
       for i in prediction:
            if i [0] > 0.8:
                resultado = "es un Pastor aleman"
                return resultado
            
            elif i [1] > 0.8:
                resultado = "es un pug"
                return resultado
            
            elif i [2] > 0.8 :
                resultado = "es un Pitbull"
                return resultado

            elif i [3] > 0.8:
                resultado = " es un sanbernardo"
                return resultado
            elif i [4] > 0.8:
                resultado = " es un Golden retriver"
                return resultado
            elif i [5] > 0.8:
                resultado = " es un Chihuahua"
                return resultado
            
def main():
    try:
        updater = Updater(token)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start",start))
        dp.add_handler(CommandHandler("help",help))

        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_handler(MessageHandler(Filters.photo, getImage))

        dp.add_error_handler(error)

        updater.start_polling()
        updater.idle()
        print("Bot listo")
    except Exception as e:
        print("Error 005{}".format(e.args[0]))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error 006{}".format(error.args[0]))
