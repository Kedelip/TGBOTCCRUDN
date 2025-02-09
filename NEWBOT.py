from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime, timedelta
import pytz
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "7605263373:AAG6E5GLsYHM-qVnYnSoAq0L1m-Oi5iwY14"
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

ALLOWED_USERS = {
    5564290879: "12345",
    1022394597: "16022023",
    951251041: "16022023",
    1830701380: "16022023",
    1088855818: "16022023",
    879395121: "16022023",
    1013590555: "16022023",
    1063647108: "16022023"
}

BIRTHDAY_NOTIFICATION_ADMINS = [1022394597, 5564290879,1063647108]

SOCIAL_LINKS = {
    'case_club': {
        'VK': 'https://vk.com/case_club_rudn',
        'Telegram': 'https://t.me/case_club_rudn'
    },
    'studbeacon': {
        'VK': 'https://vk.com/studmayak_rudn',
        'Telegram': 'https://t.me/studmayak_rudn'
    }
}

CONTENT_LINK = "https://golnk.ru/J5dgD"
CALENDAR_LINK = "https://golnk.ru/bdMzB"
CERTIFICATES_LINK = "https://disk.yandex.ru/d/DnaR6RObRYywwQ"

BIRTHDAYS = {
    'January': [
        {'date': '11', 'name': 'Артемьева Анна'},
        {'date': '19', 'name': 'Укуматшоева Шахина'},
        {'date': '20', 'name': 'Розин Роман'}
    ],
    'February': [
        {'date': '07', 'name': 'Минченко Софья'},
        {'date': '07', 'name': 'Пегова Алина'}
    ],
    'March': [
        {'date': '05', 'name': 'Храмов Владислав'},
        {'date': '08', 'name': 'Киселев Петр'},
        {'date': '28', 'name': 'Юнусова Алина'}
    ],
    'April': [
        {'date': '04', 'name': 'Семчук Валерия'},
        {'date': '13', 'name': 'Галкин Никита'},
        {'date': '17', 'name': 'Расгидо Себастьян'},
        {'date': '19', 'name': 'Карасева Александра'}
    ],
    'May': [
        {'date': '13', 'name': 'Логачева Ольга'},
        {'date': '15', 'name': 'Бильданов Ян'},
        {'date': '28', 'name': 'Павлов Максим'},
        {'date': '29', 'name': 'Эебердыева Мая'}
    ],
    'June': [
        {'date': '02', 'name': 'Кулакова Полина'},
        {'date': '13', 'name': 'Пугачева Ирина'},
        {'date': '23', 'name': 'Кравченко Полина'},
        {'date': '24', 'name': 'Косолапова Анастасия'}
    ],
    'July': [
        {'date': '01', 'name': 'Неведомская Александра'},
        {'date': '01', 'name': 'Фролова Соня'},
        {'date': '05', 'name': 'Яхонтова Полина'},
        {'date': '13', 'name': 'Комиссарова Екатерина'},
        {'date': '23', 'name': 'Юдина Евгения'},
        {'date': '28', 'name': 'Рахимов Тимур'},
        {'date': '28', 'name': 'Туркиа Александр'}
    ],
    'August': [
        {'date': '05', 'name': 'Назармамадов Умед'},
        {'date': '16', 'name': 'Ложкомоев Никита'}
    ],
    'September': [
        {'date': '06', 'name': 'Третьякова Светлана'},
        {'date': '09', 'name': 'Никоненко Анастасия'},
        {'date': '09', 'name': 'Черкасова Юлия'},
        {'date': '23', 'name': 'Земцова Анастасия'},
        {'date': '27', 'name': 'Радько Алина'}
    ],
    'October': [
        {'date': '10', 'name': 'Карташов Владислав'},
        {'date': '11', 'name': 'Джангаров Артём'},
        {'date': '14', 'name': 'Суринова Полина'},
        {'date': '26', 'name': 'Щеренко Арина'}
    ],
    'November': [
        {'date': '15', 'name': 'Ларина Виктория'},
        {'date': '19', 'name': 'Лазырин Михаил'},
        {'date': '27', 'name': 'Садикова Екатерина'}
    ],
    'December': [
        {'date': '10', 'name': 'Хныкова Диана'},
        {'date': '15', 'name': 'Пассер Дарья'},
        {'date': '27', 'name': 'Гриб Екатерина'}
    ]
}

MONTH_TRANSLATION = {
    'January': 'Январь',
    'February': 'Февраль',
    'March': 'Март',
    'April': 'Апрель',
    'May': 'Май',
    'June': 'Июнь',
    'July': 'Июль',
    'August': 'Август',
    'September': 'Сентябрь',
    'October': 'Октябрь',
    'November': 'Ноябрь',
    'December': 'Декабрь'
}

class AuthState:
    def __init__(self):
        self.authenticated_users = set()

auth_state = AuthState()

def create_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Социальные сети", callback_data="socials")],
        [InlineKeyboardButton("Календарь событий", callback_data="calendar")],
        [InlineKeyboardButton("Контент-План", callback_data="content")],
        [InlineKeyboardButton("Дни рождения в этом месяце", callback_data="birthdays")],
        [InlineKeyboardButton("Сертификаты", callback_data="certificates")]
    ])

def create_socials_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Case Club", callback_data="case_club_links")],
        [InlineKeyboardButton("СтудМаяк", callback_data="studbeacon_links")],
        [InlineKeyboardButton("Назад в меню", callback_data="main")]
    ])

def create_organization_links_keyboard(org_type):
    org_links = SOCIAL_LINKS[org_type]
    keyboard = [
        [InlineKeyboardButton(platform, url=link)] 
        for platform, link in org_links.items()
    ]
    keyboard.append([InlineKeyboardButton("Назад к соц. сетям", callback_data="socials")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return
    
    if user_id in auth_state.authenticated_users:
        await update.message.reply_text("Главное меню:", reply_markup=create_main_keyboard())
    else:
        await update.message.reply_text("Пожалуйста, введите ваш пароль:")
        context.user_data['awaiting_password'] = True

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        return
    
    if context.user_data.get('awaiting_password'):
        if update.message.text == ALLOWED_USERS[user_id]:
            auth_state.authenticated_users.add(user_id)
            context.user_data['awaiting_password'] = False
            await update.message.reply_text("Главное меню:", reply_markup=create_main_keyboard())
        else:
            await update.message.reply_text("Неверный пароль. Попробуйте еще раз:")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    print(f"User ID: {query.from_user.id}")
    await query.answer()

    if query.data == "socials":
        await query.edit_message_text(
            "Выберите организацию:",
            reply_markup=create_socials_keyboard()
        )

    elif query.data == "case_club_links":
        await query.edit_message_text(
            "Ссылки Case Club:",
            reply_markup=create_organization_links_keyboard('case_club')
        )

    elif query.data == "studbeacon_links":
        await query.edit_message_text(
            "Ссылки СтудМаяк:",
            reply_markup=create_organization_links_keyboard('studbeacon')
        )

    elif query.data == "content":
        keyboard = [
            [InlineKeyboardButton("Открыть", url=CONTENT_LINK)],
            [InlineKeyboardButton("Назад в меню", callback_data="main")]
        ]
        await query.edit_message_text(
            "Контент-План:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "birthdays":
        current_month = datetime.now(MOSCOW_TZ).strftime('%B')
        month_birthdays = BIRTHDAYS[current_month]
        
        response = f"Дни рождения в {MONTH_TRANSLATION[current_month]}:\n\n"
        for birthday in sorted(month_birthdays, key=lambda x: int(x['date'])):
            response += f"{birthday['date']} - {birthday['name']}\n"
        
        keyboard = [[InlineKeyboardButton("Назад в меню", callback_data="main")]]
        await query.edit_message_text(text=response, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "calendar":
        keyboard = [
            [InlineKeyboardButton("Открыть календарь", url=CALENDAR_LINK)],
            [InlineKeyboardButton("Назад в меню", callback_data="main")]
        ]
        await query.edit_message_text(
            "Календарь событий:", 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "certificates":
        keyboard = [
            [InlineKeyboardButton("Открыть сертификаты", url=CERTIFICATES_LINK)],
            [InlineKeyboardButton("Назад в меню", callback_data="main")]
        ]
        await query.edit_message_text(
            "Сертификаты:", 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "main":
        await query.edit_message_text("Главное меню:", reply_markup=create_main_keyboard())

async def check_birthdays(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(MOSCOW_TZ)
    month = now.strftime('%B')
    day = now.strftime('%d')
    
    today_birthdays = [b for b in BIRTHDAYS[month] if b['date'] == day]
    for birthday in today_birthdays:
        message = f"🎉 Сегодня день рождения у {birthday['name']}! 🎂"
        for user_id in auth_state.authenticated_users:
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
            except Exception as e:
                logger.error(f"Failed to send birthday notification to {user_id}: {e}")
    
    for days, future_date in [(3, now + timedelta(days=3)), (1, now + timedelta(days=1))]:
        future_birthdays = [b for b in BIRTHDAYS[future_date.strftime('%B')] 
                          if b['date'] == future_date.strftime('%d')]
        
        for birthday in future_birthdays:
            message = (f"⏰ Напоминание: через {days} {'день' if days == 1 else 'дня'} "
                     f"день рождения у {birthday['name']}!")
            for admin_id in BIRTHDAY_NOTIFICATION_ADMINS:
                try:
                    await context.bot.send_message(chat_id=admin_id, text=message)
                except Exception as e:
                    logger.error(f"Failed to send admin notification to {admin_id}: {e}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    job_queue = application.job_queue
    moscow_time = datetime.now(MOSCOW_TZ).replace(hour=8, minute=0, second=0, microsecond=0)
    job_queue.run_daily(check_birthdays, moscow_time.timetz())
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
