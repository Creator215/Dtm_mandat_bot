from threading import Thread
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,ContextTypes,filters
import sqlite3
from bot_params import bot_token
from Mandat import Mandat


class Dtm_Mandat_Bot:
    def __init__(self):
        self.bot_config = ApplicationBuilder().token(bot_token).build()

        self.year_db = sqlite3.connect("year_.db")
        self.user_db = sqlite3.connect("user_.db")

        self.create_year_formula = """CREATE TABLE year_d (
            year_value DATATYPE
        )"""

        self.create_user_formula = """CREATE TABLE user_d (
            user_id DATATYPE,
            message_value DATATYPE
        )"""

        self.select_year_formula = """SELECT * FROM year_d"""
        self.select_user_formula = """SELECT * FROM user_d"""

        self.year_cursor = self.year_db.cursor()
        self.user_cursor = self.user_db.cursor()

        try:
            self.year_cursor.execute(self.create_year_formula)
            self.year_db.commit()
            print("yil jadvali yaratildi !")
        except:
            print("yil jadvali yaratib bo'lingan")

        try:
            self.user_cursor.execute(self.create_user_formula)
            self.user_db.commit()
            print("foydalanuvchilar jadvali yaratildi !")

        except:
            print("foydalanuvchilar jadvali yaratib bo'lingan")


        self.buttons = ReplyKeyboardMarkup(keyboard=[[f"Bakalavr-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]}"],[f"O'qishni ko'chirish-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]}"]],resize_keyboard=True)
        self.back_btn = ReplyKeyboardMarkup(keyboard=[["Ortga"]],resize_keyboard=True)


        self.bot_config.add_handler(CommandHandler("start",self.start))
        self.bot_config.add_handler(CommandHandler("change", self.change_y))
        self.bot_config.add_handler(MessageHandler(filters=filters.TEXT,callback=self.user_messages))
        self.bot_config.run_polling()

    async def change_y(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
        user_text = update.message.text
        year_text = user_text.replace("/change","").replace(" ","")

        year_data = self.year_cursor.execute(self.select_year_formula).fetchall()
        insert_formula = f"""INSERT INTO year_d VALUES ("{year_text}")"""
        for i in year_data:
            delete_formula = f"""DELETE FROM year_d WHERE year_value="{i[0]}" """
            self.year_cursor.execute(delete_formula)
            self.year_db.commit()
        print("malumotlar tozalandi")

        self.year_cursor.execute(insert_formula)
        self.year_db.commit()
        print("malumot qo'shildi")

        user_list = self.user_cursor.execute(self.select_user_formula).fetchall()

        for i in user_list:
            await context.bot.send_message(chat_id=i[0],text="Bot sozlamalari o'zgartirildi.yangilanishni olish uchun /start ni bosing")

        print(user_list)

        print(year_text)

    async def start(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
        self.buttons = ReplyKeyboardMarkup(
            keyboard=[[f"Bakalavr-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]}"],
                      [f"O'qishni ko'chirish-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]}"]],
            resize_keyboard=True)
        user_list = self.user_cursor.execute(self.select_user_formula).fetchall()

        for i in user_list:
            delete_formula = f"""DELETE FROM user_d WHERE user_id="{i[0]}" """
            self.user_cursor.execute(delete_formula)
            self.user_db.commit()
        print("Barcha malumotlar tozalandi")

        await update.message.reply_text(text=f"Assalomu aleykum Mandat-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]} botiga xush kelibsiz",reply_markup=self.buttons)

    async def user_messages(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:

        user_message = update.message.text

        if(user_message == f"Bakalavr-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]}"):
            insert_formula = f"""INSERT INTO user_d VALUES ("{update.effective_user.id}","Home")"""
            self.user_cursor.execute(insert_formula)
            self.user_db.commit()
            print("ma'lummot kiritldi")
            await update.message.reply_text(text="Bakalavr belgilandi",reply_markup=self.back_btn)

        elif(user_message == f"O'qishni ko'chirish-{self.year_cursor.execute(self.select_year_formula).fetchall()[0][0]}"):
            insert_formula = f"""INSERT INTO user_d VALUES ("{update.effective_user.id}","Transfer")"""
            self.user_cursor.execute(insert_formula)
            self.user_db.commit()
            print("ma'lummot kiritldi")

            await update.message.reply_text(text="O'qishni ko'chirish belgilandi",reply_markup=self.back_btn)

        elif(user_message == "Ortga"):
            delete_formula = f"""DELETE FROM user_d WHERE user_id="{update.effective_user.id}" """
            self.user_cursor.execute(delete_formula)
            self.user_db.commit()
            print("malumot o'chirildi")
            await update.message.reply_text(text="Ortga qaytish",reply_markup=self.buttons)
        else:
            if(str(self.user_cursor.execute(self.select_user_formula).fetchall().copy()) == "[]"):
                await update.message.reply_text("Bot sozlamalari o'zgartirildi.Yangilanishni olish uchun /start ni bosing")
            else:
                select_formula = f"""SELECT * FROM user_d WHERE user_id="{update.effective_user.id}" """
                if(str(self.user_cursor.execute(select_formula).fetchone()[1]) == "Home"):

                    await update.message.reply_text(text="Kutib turing...")
                    th = Thread(target=await self.send_data(update,context))
                    th.start()
                elif(str(self.user_cursor.execute(select_formula).fetchone()[1]) == "Transfer"):

                    await update.message.reply_text(text="Kutib turing...")
                    th = Thread(target=await self.send_data2(update, context))
                    th.start()



    async def send_data(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
        dd = Mandat(str(self.year_cursor.execute(self.select_year_formula).fetchone()[0]),"Home",update.message.text)
        sstr = ""
        print(dd.get_data())
        print(int(len(dd.get_data())/2))
        for i in range(0,len(dd.get_data()),2):
            print(i)
            print(i + 1)
            sstr += dd.get_data()[i] +" : <b>"+ dd.get_data()[i+1]+"</b>\n"
        await update.message.reply_html(text=f"<b>Natija</b>\n\n{sstr}")
        dd.clear_all()

    async def send_data2(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
        dd = Mandat(str(self.year_cursor.execute(self.select_year_formula).fetchone()[0]),"Transfer",update.message.text)
        sstr = ""
        print(dd.get_data())
        print(int(len(dd.get_data())/2))
        for i in range(0,len(dd.get_data()),2):
            print(i)
            print(i + 1)
            sstr += dd.get_data()[i] +" : <b>"+ dd.get_data()[i+1]+"</b>\n"
        await update.message.reply_html(text=f"<b>Natija</b>\n\n{sstr}")
        dd.clear_all()


if __name__ == "__main__":
    Dtm_Mandat_Bot()