from pyrogram import Client, Filters, Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait
from re import search
from redis import StrictRedis
from time import sleep
from threading import Thread
from threading import Timer
from telebot import TeleBot
from multiprocessing import Process

Token = '000000000:AAAAAAAAAAAAAAAAAA-AAAAAAAAAAAA'
api_id = int('000000')
api_hash = '000000000000000000000000000'
log_channel = -1001111111111
manager = [198726079, ]
admin_username = 'uinxxxxxx'
redis = StrictRedis(decode_responses=True)
api = TeleBot(Token)
cli = Client('SubPyCleaner-{}'.format(api.get_me().id), api_id, api_hash, '0.1-SubPY', 'Python3.6', 'Ubuntu', 'fa')
mt = Client(Token, api_id, api_hash)
cmds = ['/', '!', '#']
returns = [
    'کاربر با موفقیت به مدیران ربات افزوده شد',
    'کاربر با موفقیت از مدیران ربات حذف شد',
    'کاربر با موفقیت به صاحبان گروه افزوده شد',
    'کاربر با موفقیت از صاحبان گروه حذف شد',
    'کاربر با موفقیت به مدیران گروه افزوده شد',
    'کاربر با موفقیت از مدیران گروه حذف شد',
    'این قابلیت بعدا اضافه خواهد شد.',
]
