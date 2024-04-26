from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from handlers.base_handler import BaseHandler

FOREST, TENT, HUNTING, BERRIES, TEMPLE, ENDING, PASTKA, IDIVOIN = range(8)


class GameConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('game', cls.game)],
            states={
                FOREST: [MessageHandler(filters.Regex('^(Так|Ні)$'), cls.forest)],
                TENT: [MessageHandler(filters.Regex('^(Плисти|Здатись)$'), cls.tent)],
                HUNTING: [MessageHandler(filters.Regex('^(Полювати|Відпочити)$'), cls.hunting)],
                BERRIES: [MessageHandler(filters.Regex("^(З'їсти|Стриматись|Жерти!)$"), cls.berries)],
                TEMPLE: [MessageHandler(filters.Regex("^(Зайти|Стояти)$"), cls.temple)],
                ENDING: [MessageHandler(filters.Regex("^(Так|Ні)$"), cls.ending)],
                PASTKA: [MessageHandler(filters.Regex("^(Ухилитись|Пригнутись)$"), cls.pastkajokera)],
                IDIVOIN: [CallbackQueryHandler(cls.idivoin)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Так'), KeyboardButton('Ні')],
        ]

        reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(f"Здарова {update.effective_user.first_name}! Чи бажаєте ви зіграти у гру?",reply_markup=reply_text)

        return FOREST

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з історії :^(')

        return ConversationHandler.END

    @staticmethod
    async def forest(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [KeyboardButton('Плисти'), KeyboardButton('Здатись')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
            f"""
            Ви мандрівник, який перетинав океан але на вас напали пірати, які захопили ваш корабель і викинули вас за борт.\nАле ви побачили острів і почали плисти до нього.    
            """, reply_markup=reply_text)

            return TENT
        elif answer == 'Ні':
            await update.message.reply_text(f'Ви обрали не грати в захопливу гру.')
            return ENDING
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def tent(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Плисти':
            keyboard = [
                [KeyboardButton('Відпочити'), KeyboardButton('Полювати')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
            f"""
            Ви ледве-ледве доплили до острова, і побачили покинутий намет.\nВи були настільки знесилені що зайшли у намет і лягли спати.\n Ви проснулись, був ранок, ви були дуже голодні і зневоднені. Що будете робити?     
            """, reply_markup=reply_text)
            return HUNTING
        elif answer == 'Здатись':
            await update.message.reply_text(f'Ви потонули і вашим тілом наїлись акули.')
            return ENDING
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def hunting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == 'Полювати':
            keyboard = [
                [KeyboardButton("З'їсти"), KeyboardButton('Стриматись'),KeyboardButton('Жерти!')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                f"""
             Ви пішли у ліс. Ви довго блукали по лісі і знайшли дивні ягоди. Будете їсти їх?        
             """, reply_markup=reply_text)
            return BERRIES
        elif answer == 'Відпочити':
            await update.message.reply_text(f'Ви були зневоднені і висохли зі середини.')
            return ENDING
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def berries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == "З'їсти" or "Жерти!":
            keyboard = [
                [KeyboardButton("Зайти"), KeyboardButton('Стояти')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                f"""
             Ви почали збирати ягоди і поглинати їх.\n Ви наситились ягодами і трохи поповнили запаси води.\n Трохи пройшовшись лісом ви побачили старовинний храм, зайдете у нього?       
             """, reply_markup=reply_text)
            return TEMPLE
        elif answer == 'Стриматись':
            await update.message.reply_text(f'У вас закрутилась голова через голод і ви впали з обриву і розбились.')
            return ENDING
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def temple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == "Зайти":
            keyboard = [
                [KeyboardButton("Ухилитись"), KeyboardButton('Пригнутись')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                f"""
             Ви зайшли у храм і ненароком встали на нажимну плиту і у вас полетіла стріла. Що будете робити?       
             """, reply_markup=reply_text)
            return PASTKA
        elif answer == 'Стояти':
            await update.message.reply_text(f'Ви стояли і втикали на храм, потім до вас прийшов вовк і загриз вас.')
            return ENDING
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def pastkajokera(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == "Ухилитись":
            keyboard = [
                [InlineKeyboardButton("Йти", callback_data='Йти')],
                [InlineKeyboardButton("Втекти", callback_data='Втекти')]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"""
             Ви ухилились але стріла зачепила вас і ви зрозуміло що вона була отруйна. У вас закрутилась голова будете продовжувати йти?.    
             """, reply_markup=reply_markup)
            return IDIVOIN
        elif answer == 'Пригнутись':
            await update.message.reply_text(f'Ви пригнулись але стріла попала вам в голову. (Смерть)\n Бажаєте почати гру спочатку? ')
            return ENDING
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def idivoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        data = query.data
        if data == "Йти":
            await query.edit_message_text(
                f"""
             Ви продовжували йти як справжній воїн. Ви прийшли у велику залу і... \nПЕРЕМОГА!Ви зайшли у храм і знайшли золотий чобіток який коштує 300$.\n Бажаєте почати гру спочатку?       
             """)
            return ENDING
        elif data == 'Втекти':
            await query.edit_message_text(f'Ви вибігли але довго бігти не змогли, ви впали і померли.\n Бажаєте почати гру спочатку? ')
            return ENDING
        else:
            await query.edit_message_text(f'Ви написало щоcь не те.')

    @staticmethod
    async def ending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == "Так":
            await update.message.reply_text(
                f"""Гра починається ЗАНОВО!""")
            return FOREST
        elif answer == 'Ні':
            await update.message.reply_text(f'Ви вибрали не розпочинати гру заново.')
            return exit()
        else:
            await update.message.reply_text(f'Ви написало щоcь не те.')