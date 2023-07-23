import telebot
from bs4 import BeautifulSoup as BS
import requests
from telebot import types
import calendar
from datetime import datetime
import locale
import schedule
import asyncio
import re

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def citata():
    url = 'https://finewords.ru/sluchajnaya?_=16'

    responce = requests.get(url)
    responce.raise_for_status()

    soup = BS(responce.text, 'lxml')

    text = soup.find('p').get_text()
    return text

def img():
    url = 'https://cataas.com/cat?html=true'
    
    responce = requests.get(url)
    responce.raise_for_status()

    soup = BS(responce.text, 'lxml')

    img = soup.find('img')['src']
    return 'https://cataas.com'+ img



bot = telebot.TeleBot('5657737695:AAEvQqZMdftPZVqivwcFTAqN2GMm2OMCJqo')

def downbuttons():
    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    citata = types.KeyboardButton('Цитата')
    deltime = types.KeyboardButton('Отменить запланированную цитату')
    settime = types.KeyboardButton('Установить время отправки')
    delinterval = types.KeyboardButton('Отменить интервальные сообщения')     
    markup.add(citata, settime, deltime, delinterval)
    return markup

@bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f'Привет <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=downbuttons())

current_datetime = datetime.now()
curm = current_datetime.month
cury = current_datetime.year
curh = current_datetime.hour
curm = current_datetime.minute
timehours = 0
timeminutes = 0
def settime():
    up1 = types.InlineKeyboardButton('+10', callback_data='up1')
    up2 = types.InlineKeyboardButton('+5', callback_data='up2')
    up3 = types.InlineKeyboardButton('+1', callback_data='up3')
    up4 = types.InlineKeyboardButton('+10', callback_data='up4')
    up5 = types.InlineKeyboardButton('+5', callback_data='up5')
    up6 = types.InlineKeyboardButton('+1', callback_data='up6')
    down1 = types.InlineKeyboardButton('-10', callback_data='down1')
    down2 = types.InlineKeyboardButton('-5', callback_data='down2')
    down3 = types.InlineKeyboardButton('-1', callback_data='down3')
    down4 = types.InlineKeyboardButton('-10', callback_data='down4')
    down5 = types.InlineKeyboardButton('-5', callback_data='down5')
    down6 = types.InlineKeyboardButton('-1', callback_data='down6')
    
    space = types.InlineKeyboardButton(' ', callback_data='n')
    bh1 = types.InlineKeyboardButton(str(timehours), callback_data='h1')
    space2 = types.InlineKeyboardButton(':', callback_data='n')
    bm1 = types.InlineKeyboardButton(str(timeminutes), callback_data='m1')
    conf = types.InlineKeyboardButton('OK', callback_data=f'confirm')
    settime = types.InlineKeyboardMarkup([[up1, up2, up3, space, up4, up5, up6], [bh1,space2,bm1], [down1, down2, down3, conf, down4, down5, down6]])
    return settime

def create(cury, curm):
    if cury != current_datetime.year or curm != current_datetime.month:
        curmonthnumber = 1
    else:
        curmonthnumber = current_datetime.day
    clndr = []
    name = types.InlineKeyboardButton(f'{calendar.month_name[curm]} {cury}', callback_data='fullyear')
    days = []
    for day in ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']:
        days.append(types.InlineKeyboardButton(day,callback_data='n'))
    clndr.append(days)
    for week in calendar.monthcalendar(cury, curm):
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(' ', callback_data='n'))
            elif curmonthnumber != 1:
                row.append(types.InlineKeyboardButton('🔒', callback_data='n'))
                curmonthnumber -= 1
            else:
                row.append(types.InlineKeyboardButton(str(day), callback_data=f'day {day} {curm} {cury}'))
        clndr.append(row)
    if curm == current_datetime.month:
        prev = types.InlineKeyboardButton('🔒', callback_data='n')
    else:
        prev = types.InlineKeyboardButton('🢀', callback_data='prev')
    next = types.InlineKeyboardButton('🢂', callback_data='next')
    line = [prev, name, next]
    clndr.append(line)
    markup = types.InlineKeyboardMarkup(clndr)
    return markup


def fullyear(cury):
    allyear = []
    if cury == current_datetime.year:
        prevyear = types.InlineKeyboardButton('🔒', callback_data='n')
    else:
        prevyear = types.InlineKeyboardButton('🢀', callback_data='prevyear')
    nextyear = types.InlineKeyboardButton('🢂', callback_data='nextyear')
    curyear = types.InlineKeyboardButton(str(cury), callback_data='n')
    allyear.append([prevyear, curyear, nextyear])
    line = []
    year = list(calendar.month_name)
    for month in year[1:]:
        indexmonth = year[1:].index(month) +1
        if indexmonth < current_datetime.month and cury == current_datetime.year:
            line.append(types.InlineKeyboardButton('🔒', callback_data='n'))
            indexmonth+=1
        else:
            line.append(types.InlineKeyboardButton(month, callback_data=f'month {month}'))
        if len(line) == 4:
            allyear.append(line)
            line = []
    markup = types.InlineKeyboardMarkup(allyear)
    return markup
    
            
startloop = False
@bot.message_handler(content_types=['text'])
def oth(message):
    global startloop
    global breakinterval
    months = {1:'Января', 2:'Февраля', 3:'Марта', 4:'Апреля', 5:'Мая', 6:'Июня', 7:'Июля', 8:'Августа', 9:'Сентября', 10:'Октября', 11:'Ноября', 12:'Декабря'}
    if message.text == 'Цитата':
        bot.send_photo(message.chat.id, img(), caption=citata())

    elif message.text == 'Отменить запланированную цитату':
        if len(listofonetime)<1:
            bot.send_message(message.chat.id, 'Нет запланированных цитат')
        else:
            dates = []
            for i in listofonetime:
                text = f'{i[0] if i[0] != datetime.now().year else ""} {i[2]} {months[i[1]]} в {i[3]}:{i[4]}'
                dates.append([types.InlineKeyboardButton(text, callback_data=f'delete#{i}')])
            timedmarkup = types.InlineKeyboardMarkup(dates)
            bot.send_message(message.chat.id, 'Выберите что именно хотите отменить', reply_markup=timedmarkup)

    elif message.text == 'Установить время отправки':
        
        global curm
        global cury
        curm = current_datetime.month
        cury = current_datetime.year
        bot.send_message(message.chat.id, 'Выберите день', reply_markup=create(cury, curm))
        if not startloop:
            startloop = True
            asyncio.run(startasync(message))

    elif re.match(r'[0-9]+:[0-9]+',message.text) and len(listofintervals)==1:
        breakinterval = False
        text = (message.text).split(':')
        interval_number = int(text[0])*60 + int(text[1])
        date = listofintervals[0]
        year = date[0]
        month = date[1]
        day = date[2]
        hour = date[3]
        minute = date[4]
        if date[0]!= datetime.now().year:
            bot.send_message(message.chat.id, f'Цитата будет отправлена {year} {months[month]} {day} в {hour}:{minute}', reply_markup=downbuttons())
        else:
            bot.send_message(message.chat.id, f'Цитата будет отправлена {day} {months[month]} в {hour if len(str(hour))==2 else "0"+str(hour)}:{minute if len(str(minute))==2 else "0"+str(minute)}, и затем через каждые {text[0]} ч. и {text[1]} м.', reply_markup=downbuttons())
        intervallist[tuple(listofintervals.pop())] = interval_number

    elif message.text == 'Отменить интервальные сообщения':
        intervallist.clear()
    
    else:
        bot.send_message(message.chat.id, '123', reply_markup=settime())


@bot.callback_query_handler(func=lambda callback: callback.data == 'fullyear')
def year(data):
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=fullyear(cury))

@bot.callback_query_handler(func=lambda callback: callback.data == 'prevyear')
def prevyear(data):
    global cury
    cury -= 1
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=(fullyear(cury)))

@bot.callback_query_handler(func=lambda callback: callback.data == 'nextyear')
def prevyear(data):
    global cury
    cury += 1
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=(fullyear(cury)))

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('month'))
def month(data):
    monthname = data.data.split()[1]
    months = {'Январь':1, 'Февраль':2, 'Март':3, 'Апрель':4, 'Май':5, 'Июнь':6, 'Июль':7, 'Август':8, 'Сентябрь':9, 'Октябрь':10, 'Ноябрь':11, 'Декабрь':12}
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=create(cury, months[monthname]))


@bot.callback_query_handler(func=lambda callback: callback.data == 'next')
def get_next(data):
    global curm
    global cury
    if curm == 12:
        curm = 1
        cury += 1
    else:
        curm += 1
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=create(cury, curm))

@bot.callback_query_handler(func=lambda callback: callback.data == 'prev')
def get_next(data):
    global curm
    global cury
    if curm == 1:
        curm = 12
        cury -= 1
    else:
        curm -= 1
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=create(cury, curm))

@bot.callback_query_handler(func= lambda callback: callback.data.startswith('day'))
def printday(data):
    date = data.data.split()
    global chosenday
    chosenday = int(date[1])
    datestr = f'{date[1]} {calendar.month_name[int(date[2])]} {date[3]}' 
    bot.edit_message_text(f'Выбран день {datestr}. Выберите время', data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'up1')
def up1(data):
    global timehours
    timehours += 10
    if timehours > 23:
        timehours = timehours - 24
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'up2')
def up2(data):
    global timehours
    timehours += 5
    if timehours > 23:
        timehours = timehours - 24
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'up3')
def up3(data):
    global timehours
    timehours += 1
    if timehours > 23:
        timehours = 0
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'up4')
def up4(data):
    global timeminutes
    timeminutes += 10
    if timeminutes > 59:
        timeminutes = timeminutes - 60
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'up5')
def up4(data):
    global timeminutes
    timeminutes += 5
    if timeminutes > 59:
        timeminutes = timeminutes - 60
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'up6')
def up4(data):
    global timeminutes
    timeminutes += 1
    if timeminutes > 59:
        timeminutes = 0
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())


@bot.callback_query_handler(func= lambda callback: callback.data == 'down1')
def down1(data):
    global timehours
    timehours -= 10
    if timehours < 0:
        timehours = 24 + timehours
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'down2')
def down2(data):
    global timehours
    timehours -= 5
    if timehours < 0:
        timehours = 24 + timehours
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'down3')
def down3(data):
    global timehours
    timehours -= 1
    if timehours < 0:
        timehours = 23
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'down4')
def down4(data):
    global timeminutes
    timeminutes -= 10
    if timeminutes < 0:
        timeminutes = 60 + timeminutes
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'down5')
def down4(data):
    global timeminutes
    timeminutes -= 5
    if timeminutes < 0:
        timeminutes = 60 + timeminutes
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'down6')
def down4(data):
    global timeminutes
    timeminutes -= 1
    if timeminutes < 0:
        timeminutes = 59
    bot.edit_message_reply_markup(data.message.chat.id, data.message.id, reply_markup=settime())

@bot.callback_query_handler(func= lambda callback: callback.data == 'confirm')
def conf(data):
    onetime = types.InlineKeyboardButton('1 раз', callback_data='onetime')
    interval = types.InlineKeyboardButton('Установить свой промежуток в формате часы:минуты', callback_data='interval')
    whattime = types.InlineKeyboardMarkup([[onetime], [interval]])
    bot.edit_message_text('Выберите частоту отправки', data.message.chat.id, data.message.id, reply_markup=whattime)



listofonetime = []

async def sendtimedmessage(message):
    while True:
        if len(listofonetime)>0:
            timenow = datetime.now().time()
            datenow = datetime.now().date()
            if [datenow.year, datenow.month, datenow.day, timenow.hour, timenow.minute] in listofonetime:
                listofonetime.remove([datenow.year, datenow.month, datenow.day, timenow.hour, timenow.minute])
                bot.send_photo(message.chat.id, img(), caption=citata(), reply_markup=downbuttons())
                
        await asyncio.sleep(1)

def sendcitata(message):
    bot.send_photo(message.chat.id, img(), caption=citata(), reply_markup=downbuttons())


async def sendintervalmessage(message):
    while True:      
        if len(intervallist)>0:
            schedule.run_pending()
            timenow = datetime.now().time()
            datenow = datetime.now().date()
            if (datenow.year, datenow.month, datenow.day, timenow.hour, timenow.minute) in intervallist:
                bot.send_photo(message.chat.id, img(), caption=citata(), reply_markup=downbuttons())
                d = (datenow.year, datenow.month, datenow.day, timenow.hour, timenow.minute)
                x = intervallist[d]
                schedule.every(x).minutes.do(sendcitata, message = message)
        await asyncio.sleep(60)

async def startasync(message):
    task1 = asyncio.create_task(sendtimedmessage(message))
    task2 = asyncio.create_task(sendintervalmessage(message))

    await asyncio.gather(task1, task2)

@bot.callback_query_handler(func=lambda callback: callback.data == 'onetime')
def onetime(data):
    global curm
    global cury
    chosenhour = timehours
    chosenmin = timeminutes
    chosenmonth = curm
    chosenyear = cury
    listofonetime.append([chosenyear,chosenmonth,chosenday,chosenhour,chosenmin])
    months = {1:'Января', 2:'Февраля', 3:'Марта', 4:'Апреля', 5:'Мая', 6:'Июня', 7:'Июля', 8:'Августа', 9:'Сентября', 10:'Октября', 11:'Ноября', 12:'Декабря'}
    if cury != datetime.now().year:
        bot.send_message(data.message.chat.id, f'Цитата будет отправлена {chosenday} {months[curm]} {cury} в {chosenhour}:{chosenmin}', reply_markup=downbuttons())
    else:
        bot.delete_message(data.message.chat.id, data.message.id)
        bot.send_message(data.message.chat.id, f'Цитата будет отправлена {chosenday} {months[curm]} в {chosenhour if len(str(chosenhour))==2 else "0"+str(chosenhour)}:{chosenmin if len(str(chosenmin))==2 else "0"+str(chosenmin)}', reply_markup=downbuttons())


listofintervals =  []
intervallist = {}
@bot.callback_query_handler(func=lambda callback: callback.data == 'interval')
def setinterval(data):
    if len(listofintervals)>0:
        listofintervals.pop()
    global cury
    global curm
    chosenhour = timehours
    chosenmin = timeminutes
    chosenmonth = curm
    chosenyear = cury
    listofintervals.append([chosenyear,chosenmonth,chosenday,chosenhour,chosenmin])
    bot.delete_message(data.message.chat.id, data.message.id)
    bot.send_message(data.message.chat.id, 'Укажите интервал отправки цитат в формате часы:минуты (например 2:1, чтобы цитата отправлялась каждые 2 часа и 1 минуту)')
   

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('delete'))
def deletedate(data):
    res = []
    z = ((data.data.split('#')[1])[1:-1]).split(',')
    for i in z:
        res.append(int(i))
    listofonetime.remove(res)
    bot.delete_message(data.message.chat.id, data.message.id)
    bot.send_message(data.message.chat.id, 'Запланированная цитата была отменена')

bot.infinity_polling()
