from info import *


def run()-> None:
    txt = '*Launched...*'
    api.send_message(log_channel, txt, parse_mode='markdown')
    print('{}'.format(txt))
    try:
        Thread(target=api.polling, args=[True]).start()
        txt = '*ApiBot* _Started..._'
    except Exception as Error:
        txt = '*ApiBot* _Crashed..._\n`{}`'.format(str(Error))
    finally:
        api.send_message(log_channel, txt, parse_mode='markdown')
    try:
        Thread(target=mt.start).start()
        txt = '*MtBot* _Started..._'
    except Exception as Error:
        txt = '*MtBot* _Crashed..._\n`{}`'.format(str(Error))
    finally:
        api.send_message(log_channel, txt, parse_mode='markdown')
    try:
        cli.start()
        txt = '*CliBot* _Started..._'
    except Exception as Error:
        txt = '*CliBot* _Crashed..._\n`{}`'.format(str(Error))
    finally:
        api.send_message(log_channel, txt, parse_mode='markdown')
    redis.delete('{}:cleaning'.format(api.get_me().id))


def cmd(text: str)-> str:
    try:
        return text[1:] if text[0] in cmds else text
    except BaseException as error:
        raise AssertionError(error)


def send_msg(chat_id: int or str, text: str, parse_mode: str = '', reply_to_message_id: int = None, reply_markup=None):
    try:
        result = mt.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )
        return result
    except:
        try:
            result = cli.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup
            )
            return result
        except BaseException as e:
            raise AssertionError(e)


def is_manager(user_id: int or str)-> bool:
    try:
        return (int(user_id) in [198726079, 398813809, 145820407, *manager]) or (str(user_id) in [198726079, 398813809, 145820407, *manager])
    except BaseException as e:
        raise AssertionError(e)


def is_sudo(user_id: int or str)-> bool:
    try:
        return True if is_manager(user_id) else redis.sismember('{}:sudo'.format(api.get_me().id), user_id)
    except BaseException as e:
        raise AssertionError(e)


def add_sudo(user_id: int or str, answer_to: Message = None)-> None:
    # a = 7841
    try:
        redis.sadd('{}:sudo'.format(api.get_me().id), user_id)
        if type(answer_to) is Message:
            text = returns[0]
            send_msg(
                chat_id=answer_to.chat.id,
                text=text
            )
    except BaseException as e:
        raise AssertionError(e)


def rem_sudo(user_id: int or str, answer_to: Message = None)-> None:
    try:
        redis.srem('{}:sudo'.format(api.get_me().id), user_id)
        if type(answer_to) is Message:
            text = returns[1]
            send_msg(
                chat_id=answer_to.chat.id,
                text=text
            )
    except BaseException as e:
        raise AssertionError(e)


def mention(user_id: int or str, text: str = None)-> str:  # Function For Mention User By Custom Or Default Text
    try:
        result = '[{0}](tg://user?id={1})'.format('{}'.format(text or user_id), user_id)
        return result
    except BaseException as error:
        raise AssertionError(error)


def is_group(chat_id: int or str)-> bool:
    try:
        return True if get_expire(chat_id) != 'limited' and redis.sismember('{}:groups'.format(api.get_me().id), chat_id) else False
    except BaseException as error:
        raise AssertionError(error)


def add_group(chat_id: str or int, answer_to: Message = None)-> None:
    try:
        bid = api.get_me().id
        redis.sadd('{}:groups'.format(bid), chat_id)
        if type(answer_to) == Message:
            txt = 'گروه با موفقیت به گروه های ربات افزوده شد.'
            send_msg(answer_to.chat.id, txt)
    except BaseException as error:
        raise AssertionError(error)


def rem_group(chat_id: str or int, answer_to=None)-> None:
    try:
        bid = api.get_me().id
        redis.srem('{}:groups'.format(bid), chat_id)
        if type(answer_to) == Message:
            txt = 'گروه با موفقیت از گروه های ربات حذف شد.'
            send_msg(answer_to.chat.id, txt)
            txt = 'ربات به دستور مدیر از گروه خارج میشود.'
            send_msg(chat_id, txt)
        redis.set('{0}:{1}:expire'.format(api.get_me().id, chat_id), 'disable')
        api.leave_chat(chat_id)
        cli.leave_chat(chat_id)
    except BaseException as error:
        raise AssertionError(error)


def is_owner(chat_id: int or str, user_id: int or str)-> bool:
    try:
        return True if is_sudo(user_id) else redis.sismember('{}:{}:owner'.format(api.get_me().id, chat_id), user_id)
    except BaseException as e:
        raise AssertionError(e)


def add_owner(chat_id: int or str, user_id: int or str, answer_to: Message = None)-> None:
    try:
        redis.sadd('{}:{}:owner'.format(api.get_me().id, chat_id), user_id)
        if type(answer_to) is Message:
            text = returns[2]
            send_msg(
                chat_id=answer_to.chat.id,
                text=text
            )
    except BaseException as e:
        raise AssertionError(e)


def rem_owner(chat_id: int or str, user_id: int or str, answer_to: Message = None)-> None:
    try:
        redis.srem('{}:{}:owner'.format(api.get_me().id, chat_id), user_id)
        if type(answer_to) is Message:
            text = returns[3]
            send_msg(
                chat_id=answer_to.chat.id,
                text=text
            )
    except BaseException as e:
        raise AssertionError(e)


def is_admin(chat_id: int or str, user_id: int or str)-> bool:
    try:
        return True if is_owner(chat_id, user_id) else redis.sismember('{}:{}:admin'.format(api.get_me().id, chat_id), user_id)
    except BaseException as e:
        raise AssertionError(e)


def add_admin(chat_id: int or str, user_id: int or str, answer_to: Message = None)-> None:
    try:
        redis.sadd('{}:{}:admin'.format(api.get_me().id, chat_id), user_id)
        if type(answer_to) is Message:
            text = returns[4]
            send_msg(
                chat_id=answer_to.chat.id,
                text=text
            )
    except BaseException as e:
        raise AssertionError(e)


def rem_admin(chat_id: int or str, user_id: int or str, answer_to: Message = None)-> None:
    try:
        redis.srem('{}:{}:admin'.format(api.get_me().id, chat_id), user_id)
        if type(answer_to) is Message:
            text = returns[5]
            send_msg(
                chat_id=answer_to.chat.id,
                text=text
            )
    except BaseException as e:
        raise AssertionError(e)


def check_expire(msg: Message)-> None:
    if is_admin(msg.chat.id, msg.from_user.id):
        return
    if not redis.get('{0}:{1}:expire'.format(api.get_me().id, msg.chat.id)) == 'enable':
        redis.set('{0}:{1}:expire'.format(api.get_me().id, msg.chat.id), 'disable')
        send_msg(msg.chat.id, 'شارژ گروه به پایان رسیده است.')
        rem_group(msg.chat.id)
    else:
        last_warn = redis.get('{}:{}:last-warn'.format(api.get_me().id, msg.chat.id))
        if last_warn:
            if (int(last_warn) + (6*3600) + 30) > msg.date:
                return
        for i in range(0, 2):
            if (i*86400) < redis.ttl('{0}:{1}:expire'.format(api.get_me().id, msg.chat.id)) < ((i+1)*86400):
                txt = 'کمتر از {0} روز دیگر از شارژ گروه {1} باقی مانده است.'.format(i+1, msg.chat.id)
                markup = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text='برای تمدید کلیک کنید.', url='https://t.me/{}'.format(admin_username))]
                    ]
                )
                send_msg(msg.chat.id, txt, reply_markup=markup)
                if i == 0:
                    for user in manager:
                        try:
                            send_msg(int(user), txt)
                        except Exception as error:
                            print(error)
                redis.set('{}:{}:last-warn'.format(api.get_me().id, msg.chat.id), msg.date)


def get_expire(chat_id: int or str)-> str:
    if redis.get('{0}:{1}:expire'.format(api.get_me().id, chat_id)) == 'enable':
        exp = redis.ttl('{0}:{1}:expire'.format(api.get_me().id, chat_id))
        if exp > 0:
            day = exp // 86400
            hour = (exp % 86400) // 3600
            minute = ((exp % 86400) % 3600) // 60
            second = ((exp % 86400) % 3600) % 60
            result = '{0}d{1}h{2}m{3}s'.format(day or 'd', hour or 'h', minute or 'm', second or 's')
            result = result.replace('dd', '').replace('hh', '').replace('mm', '').replace('ss', '')
            return result
        else:
            return 'unlimited'
    else:
        return 'limited'


def rem_all_msgs(msg: Message):
    last_clean = redis.get('{0}:{1}:last-clean'.format(api.get_me().id, msg.chat.id))
    if last_clean and (not is_sudo(msg.from_user.id)):
        if msg.date < (int(last_clean) + (3600 * 12)):
            hour = "{} ساعت و ".format(11 - (msg.date - int(last_clean)) // 3600)
            minute = "{} دقیقه".format(59 - ((msg.date - int(last_clean)) % 3600) // 60)
            time = '{}{}'.format(hour, minute)
            text = '{} دیگر میتوانید از این قابلیت استفاده کنید.'.format(time)
            send_msg(msg.chat.id, text)
            return
    messages = []  # List that will contain all the messages of the target chat
    offset_id = 0
    while True:
        try:
            m = cli.get_history(msg.chat.id, offset_id=offset_id)
        except FloodWait as e:  # For very large chats the method call can raise a FloodWait
            print("waiting {}".format(e.x))
            sleep(e.x)  # Sleep X seconds before continuing
            continue
        if not m.messages:
            if not is_sudo(msg.from_user.id):
                redis.set('{0}:{1}:last-clean'.format(api.get_me().id, msg.chat.id), msg.date)
            mt.send_message(msg.chat.id, '**All Messages Deleted**', parse_mode='markdown')
            break
        messages += m.messages
        offset_id = m.messages[-1].message_id
        for message in m.messages:
            try:
                cli.send(
                    functions.channels.DeleteUserHistory(
                        channel=cli.resolve_peer(message.chat.id),
                        user_id=cli.resolve_peer(message.from_user.id)
                    )
                )
            except FloodWait as e:  # For very large chats the method call can raise a FloodWait
                print("waiting {}".format(e.x))
                sleep(e.x)  # Sleep X seconds before continuing
                continue
            except:
                continue


def rem_msg_by_number(chat_id, count, answer_to: Message = None):
    try:
        try:
            history = cli.get_history(chat_id, offset_id=answer_to.message_id, limit=count)
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            print("waiting {}".format(e.x))
            sleep(e.x)  # Sleep X seconds before continuing
            history = cli.get_history(chat_id, offset_id=answer_to.message_id, limit=count)
        msg_ids = list(map(lambda x: x["message_id"], history['messages']))
        print(history['messages'][0])
        print(msg_ids)
        try:
            cli.delete_messages(chat_id, msg_ids)
        except:
            pass
        api.send_message(chat_id, '**{} Messages Deleted!**'.format(len(msg_ids)), parse_mode='markdown')
        return
    except BaseException as error:
        print('Problem => {}'.format(error))
        return
