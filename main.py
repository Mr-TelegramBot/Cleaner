import method
mt = method.mt
client = method.cli


@client.on_message(method.Filters.group & method.Filters.text)
def _cli_process_msgs(cli: method.Client, msg: method.Message):
    cid = msg.chat.id
    uid = msg.from_user.id
    txt = method.cmd(msg.text.lower())
    method.Timer(120, method.check_expire, args=[msg]).start()
    try:
        if method.is_manager(uid):
            if method.search(r'^(add sudo)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$', txt):
                sudo_id = method.search(r'^(add sudo)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$',
                                        txt).group(3)
                if sudo_id:
                    if sudo_id.isnumeric():
                        try:
                            method.add_sudo(
                                user_id=sudo_id,
                                answer_to=msg
                            )
                        except Exception as error:
                            print('{}'.format(error))
                    else:
                        try:
                            method.send_msg(
                                msg.chat.id,
                                method.returns[6]
                            )
                        except Exception as error:
                            print('{}'.format(error))
                elif msg.reply_to_message:
                    try:
                        method.add_sudo(
                            user_id=msg.reply_to_message.from_user.id,
                            answer_to=msg
                        )
                    except Exception as error:
                        print('{}'.format(error))
            elif method.search(r'^(rem sudo)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$', txt):
                sudo_id = method.search(r'^(rem sudo)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$',
                                        txt).group(3)
                if sudo_id:
                    if sudo_id.isnumeric():
                        try:
                            method.rem_sudo(sudo_id, msg)
                        except Exception as error:
                            print('{}'.format(error))
                    else:
                        try:
                            method.send_msg(
                                msg.chat.id,
                                method.returns[6]
                            )
                        except Exception as error:
                            print('{}'.format(error))
                elif msg.reply_to_message:
                    try:
                        method.rem_sudo(msg.reply_to_message.from_user.id, msg)
                    except Exception as error:
                        print('{}'.format(error))
        if method.is_sudo(uid):
            if method.search(r'^sudo list$', txt):
                text = "\n".join(list(method.redis.smembers('{}:sudo'.format(
                    method.api.get_me().id)))) or 'List Is Empty.'
                method.send_msg(
                    chat_id=msg.chat.id,
                    text=text
                )
            elif method.search(r'^rem$', txt):
                method.rem_group(msg.chat.id, msg)
            elif method.search(r'^charge(\s(\d+)([smhd]))?$', txt):
                if not method.is_group(msg.chat.id):
                    method.add_group(msg.chat.id, msg)
                count = str(method.search(r'charge(\s(\d+)([smhd]))?', txt).group(2))
                mode = str(method.search(r'charge(\s(\d+)([smhd]))?', txt).group(3))
                if mode.lower() == 's':
                    exp = int(count)
                    method.redis.setex('{0}:{1}:expire'.format(method.api.get_me().id, cid), int(exp), 'enable')
                    txt = 'ربات به مدت {0} ثانیه برای گروه {1} فعال شد.'.format(count, msg.chat.id)
                elif mode.lower() == 'm':
                    exp = int(count) * 60
                    method.redis.setex('{0}:{1}:expire'.format(method.api.get_me().id, cid), int(exp), 'enable')
                    txt = 'ربات به مدت {0} دقیقه برای گروه {1} فعال شد.'.format(count, msg.chat.id)
                elif mode.lower() == 'h':
                    exp = int(count) * 60 * 60
                    method.redis.setex('{0}:{1}:expire'.format(method.api.get_me().id, cid), int(exp), 'enable')
                    txt = 'ربات به مدت {0} ساعت برای گروه {1} فعال شد.'.format(count, msg.chat.id)
                    for user in method.manager:
                        try:
                            method.send_msg(int(user), 'ربات به مدت {0} ساعت برای گروه {1} شارژ شد.'.format(
                                count, msg.chat.id))
                        except:
                            pass
                elif mode.lower() == 'd':
                    exp = int(count) * 60 * 60 * 24
                    method.redis.setex('{0}:{1}:expire'.format(method.api.get_me().id, cid), int(exp), 'enable')
                    txt = 'ربات به مدت {0} روز برای گروه {1} فعال شد.'.format(count, msg.chat.id)
                else:
                    method.redis.set('{0}:{1}:expire'.format(method.api.get_me().id, cid), 'enable')
                    txt = 'ربات برای همیشه برای گروه {1} فعال شد.'.format(count, msg.chat.id)
                method.send_msg(msg.chat.id, txt)
                for user in method.manager:
                    try:
                        method.send_msg(int(user), txt)
                    except:
                        pass
            elif method.search(r'^(add owner)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$', txt):
                sudo_id = method.search(r'^(add owner)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$',
                                        txt).group(3)
                if sudo_id:
                    if sudo_id.isnumeric():
                        try:
                            method.add_owner(
                                chat_id=msg.chat.id,
                                user_id=sudo_id,
                                answer_to=msg
                            )
                        except Exception as error:
                            print('{}'.format(error))
                    else:
                        try:
                            method.send_msg(
                                msg.chat.id,
                                method.returns[6]
                            )
                        except Exception as error:
                            print('{}'.format(error))
                elif msg.reply_to_message:
                    try:
                        method.add_owner(
                            chat_id=msg.chat.id,
                            user_id=msg.reply_to_message.from_user.id,
                            answer_to=msg
                        )
                    except Exception as error:
                        print('{}'.format(error))
            elif method.search(r'^(rem owner)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$', txt):
                sudo_id = method.search(r'^(rem owner)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$',
                                        txt).group(3)
                if sudo_id:
                    if sudo_id.isnumeric():
                        try:
                            method.rem_owner(
                                chat_id=msg.chat.id,
                                user_id=sudo_id,
                                answer_to=msg
                            )
                        except Exception as error:
                            print('{}'.format(error))
                    else:
                        try:
                            method.send_msg(
                                msg.chat.id,
                                method.returns[6]
                            )
                        except Exception as error:
                            print('{}'.format(error))
                elif msg.reply_to_message:
                    try:
                        method.rem_owner(
                            chat_id=msg.chat.id,
                            user_id=msg.reply_to_message.from_user.id,
                            answer_to=msg
                        )
                    except Exception as error:
                        print('{}'.format(error))
        if method.is_owner(cid, uid):
            if method.search(r'^(add admin)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$', txt):
                sudo_id = method.search(r'^(add admin)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$',
                                        txt).group(3)
                if sudo_id:
                    if sudo_id.isnumeric():
                        try:
                            method.add_admin(
                                chat_id=msg.chat.id,
                                user_id=sudo_id,
                                answer_to=msg
                            )
                        except Exception as error:
                            print('{}'.format(error))
                    else:
                        try:
                            method.send_msg(
                                msg.chat.id,
                                method.returns[6]
                            )
                        except Exception as error:
                            print('{}'.format(error))
                elif msg.reply_to_message:
                    try:
                        method.add_admin(
                            chat_id=msg.chat.id,
                            user_id=msg.reply_to_message.from_user.id,
                            answer_to=msg
                        )
                    except Exception as error:
                        print('{}'.format(error))
            elif method.search(r'^(rem admin)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$', txt):
                sudo_id = method.search(r'^(rem admin)(\s(\d+|@[a-zA-Z](?!.*[_]{2})[a-zA-Z0-9_]{3,30}[a-zA-Z0-9]))?$',
                                        txt).group(3)
                if sudo_id:
                    if sudo_id.isnumeric():
                        try:
                            method.rem_admin(
                                chat_id=msg.chat.id,
                                user_id=sudo_id,
                                answer_to=msg
                            )
                        except Exception as error:
                            print('{}'.format(error))
                    else:
                        try:
                            method.send_msg(
                                msg.chat.id,
                                method.returns[6]
                            )
                        except Exception as error:
                            print('{}'.format(error))
                elif msg.reply_to_message:
                    try:
                        method.rem_admin(
                            chat_id=msg.chat.id,
                            user_id=msg.reply_to_message.from_user.id,
                            answer_to=msg
                        )
                    except Exception as error:
                        print('{}'.format(error))
            elif method.search(r'^owner list$', txt):
                text = "\n".join(list(method.redis.smembers('{}:{}:owner'.format(method.api.get_me().id, cid))))
                method.send_msg(
                    chat_id=msg.chat.id,
                    text=text
                )
        if method.is_admin(cid, uid):
            if method.is_group(msg.chat.id):
                if method.search(r'^id$', txt):
                    txt = '**Group Id** **:** `{}`\n'.format(msg.chat.id)
                    txt += '**Personal Id** **:** `{}`\n'.format(msg.from_user.id)
                    if msg.forward_from:
                        txt += '**Fwd Personal Id** **:** `{}`\n'.format(msg.forward_from.id)
                    elif msg.forward_from_chat:
                        txt += '**Fwd Channel Id** **:** `{}`\n'.format(msg.forward_from_chat.id)
                    if msg.reply_to_message:
                        txt += '**Reply User Id** **:** `{}`\n'.format(msg.reply_to_message.from_user.id)
                        if msg.reply_to_message.forward_from:
                            txt += '**Reply Fwd Personal Id** **:** `{}`\n'.format(msg.reply_to_message.forward_from.id)
                        elif msg.reply_to_message.forward_from_chat:
                            txt += '**Reply Fwd Channel Id** **:** `{}`\n'.format(
                                msg.reply_to_message.forward_from_chat.id)
                    cli.send_message(
                        chat_id=msg.chat.id,
                        text=txt,
                        parse_mode='markdown'
                    )
                elif method.search(r'^admin list$', txt):
                    text = "\n".join(list(method.redis.smembers('{}:{}:admin'.format(method.api.get_me().id, cid))))
                    method.send_msg(
                        chat_id=msg.chat.id,
                        text=text
                    )
                elif method.search(r'^clean$', txt):
                    try:
                        th = method.Thread(target=method.rem_all_msgs, args=(msg,))
                        th.start()
                    except Exception as error:
                        method.send_msg(method.log_channel, '{}'.format(error))
                elif method.search(r'^del (\d+)$', txt):
                    try:
                        count = method.search(r'del (\d+)', txt).group(1)
                        if (not method.is_sudo(msg.from_user.id)) and (int(count) not in range(1, 101)):
                            text = 'لطفا عددی بین 0 تا 101 وارد نمایید.'
                            method.send_msg(msg.chat.id, text)
                            return
                        th = method.Thread(target=method.rem_msg_by_number, args=(cid, int(count), msg))
                        th.start()
                    except Exception as error:
                        method.send_msg(method.log_channel, '{}'.format(error))
                elif method.search(r'^del all', txt) and msg.reply_to_message:
                    reply_msg = client.get_messages(cid, msg.reply_to_message.message_id)
                    print('{}'.format(reply_msg))
                    try:
                        client.send(
                            method.functions.channels.DeleteUserHistory(
                                channel=client.resolve_peer(msg.chat.id),
                                user_id=client.resolve_peer(reply_msg.from_user.id)
                            )
                        )
                        txt = '**All Messages From** {0} **Has Been Deleted**'.format(
                            method.mention(reply_msg.from_user.id))
                        mt.send_message(msg.chat.id, txt, parse_mode='markdown')
                    except Exception as error:
                        print('{}'.format(error))
                elif method.search(r'^del$', txt) and msg.reply_to_message:
                    try:
                        cli.delete_messages(msg.chat.id, [msg.message_id, msg.reply_to_message.message_id])
                    except Exception as error:
                        method.send_msg(method.log_channel, '{}'.format(error))
                elif method.search(r'^ping$', txt):
                    method.send_msg(msg.chat.id, '**Pong**', parse_mode='markdown')
                elif method.search(r'^help$', txt):
                    text = """⚠️نکته⚠️
〽️مقام ها از بالا به پایین میباشد یعنی مقام بالا تمامی اختیارات مقام پایین تر را دارا میباشد.

🔰**manager (صاحبان ربات)**
`add sudo`
`rem sudo`

🔰**sudo (مدیران ربات)**
`sudo list`
`add`
`rem`
`charge (n)[d/h/m/s]`
`add owner`
`rem owner`

🔰**owner (صاحبان گروه)**
`add admin`
`rem admin`
`owner list`

🔰**admin (مدیران گروه)**
`admin list`
`clean`
`del (n)`
`del all`
`info`
`ping`
"""
                    method.send_msg(msg.chat.id, text)
                elif method.search(r'^info$', txt):
                    expire = method.get_expire(msg.chat.id)
                    if expire == 'limited':
                        method.check_expire(msg)
                        return
                    elif expire == 'unlimited':
                        expire = 'نامحدود'
                    else:
                        expire = expire.replace('d', ' روز و ').replace('h', ' ساعت و ').replace(
                            'm', ' دقیقه و ').replace('s', ' ثانیه ')
                    method.send_msg(cid, expire)
                elif method.search(r'clean delete', txt):
                    result = cli.get_chat_members(
                        msg.chat.id,
                        filter='kicked'
                    )
                    print(result)
    except Exception as error:
        print('{}'.format(error))


if __name__ == '__main__':
    method.run()
