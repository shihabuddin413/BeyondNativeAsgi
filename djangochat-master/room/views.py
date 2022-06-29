from .models import Room, Chat
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


records = Chat.objects.all()
records.delete()

# bot_id = bot['bot_id']
#     name = bot['name']
#     slug = bot['name']
#     wellcome_msg = msg
#     Questions = bot['Questions']
#     Answers = bot['Answers']
#     updatebot = Room(
#         bot_id=bot_id,
#         name=name,
#         slug=slug,
#         wellcome_msg=wellcome_msg,
#         Questions=Questions,
#         Answers=Answers
#     )


def save_welcome_msg(bot, msg):
    updatebot = Room.objects.filter(
        bot_id=bot['bot_id']).update(wellcome_msg=msg)
    print(bot['wellcome_msg'])
    return True


def save_qns(bot, qns):
    ans_pre = "ans"
    qs_pre = "qs"

    j = 0
    qs = []
    ns = []

    for i in qns:
        ans_pre = ans_pre + str(j)
        qs_pre = qs_pre + str(j)
        v1 = qns.get(qs_pre, '')
        v2 = qns.get(ans_pre, '')
        if v1 == '' or v2 == '':
            break
        qs.append(v1)
        ns.append(v2)
        ans_pre = "ans"
        qs_pre = "qs"
        j += 1

    all_qs_str = ''
    all_ns_str = ''

    for k in qs:
        all_qs_str += k+','

    for n in ns:
        all_ns_str += n+','

    print(all_qs_str)
    print(all_ns_str)

    updatebot = Room.objects.filter(bot_id=bot['bot_id']).update(
        Questions='',
        Answers=''
    )

    updatebot = Room.objects.filter(bot_id=bot['bot_id']).update(
        Questions=all_qs_str,
        Answers=all_ns_str
    )

    return True


def create_new_bot(bot_name):
    bot_id = random.randint(1000, 1000000)
    name = bot_name
    slug = bot_name
    wellcome_msg = "Hello World ! i am a new bot"
    Questions = ""
    Answers = ""
    all_bot = Room.objects.values()
    for tmp_bot in all_bot:
        tmp_name = tmp_bot['name']
        if (tmp_name.lower() == bot_name):
            return [False, "Please Choose another name! this bot exist."]

    newbot = Room(
        bot_id=bot_id,
        name=name,
        slug=slug,
        wellcome_msg=wellcome_msg,
        Questions=Questions,
        Answers=Answers
    )
    newbot.save()
    return [True, "bot created"]


def get_new_update():
    return "The talent lab bot is in training mode please wait"


@login_required
def room_edit(request, slug):
    current_user = request.user
    crr_bot = Room.objects.values().filter(slug__icontains=slug)[0]
    qs_data = []
    qs_set = crr_bot['Questions'].split(',')
    ans_set = crr_bot['Answers'].split(',')

    for i in range(30):
        temp = {'serial_title': i+1, 'serial': i +
                1, 'qs_set': '', 'ans_set': ''}
        if(len(qs_set) > i or len(ans_set) > i):
            temp = {'serial_title': i+1, 'serial': i,
                    'qs_set': qs_set[i], 'ans_set': ans_set[i]}
        qs_data.append(temp)

    if request.method == "POST":
        try:
            if request.POST['content']:
                msg = request.POST['content']
                save_welcome_msg(crr_bot, msg)
                crr_bot = Room.objects.values().filter(slug__icontains=slug)[0]
                return render(request, 'room/edit.html', {'room': crr_bot, "qs_data": qs_data, 'numqs': len(qs_data), 'msg': "Welcome Message Saved"})
        except:
            save_qns(crr_bot, request.POST)
            qs_set = []
            ans_set = []
            crr_bot = Room.objects.values().filter(slug__icontains=slug)[0]
            qs_set = crr_bot['Questions'].split(',')
            ans_set = crr_bot['Answers'].split(',')
            qs_data = []
            for i in range(30):
                temp = {'serial': i+1, 'qs_set': '', 'ans_set': ''}
                if(len(qs_set) > i or len(ans_set) > i):
                    temp = {'serial': i,
                            'qs_set': qs_set[i], 'ans_set': ans_set[i]}
                qs_data.append(temp)

    return render(request, 'room/edit.html', {'room': crr_bot, "qs_data": qs_data, 'numqs': len(qs_data)})


@ login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms, })


def save_msg(chat_room, message, message_from):
    message = message
    chat_room = chat_room['bot_id']
    message_from = message_from.username
    if (len(message.strip()) == 0):
        return
    new_chat = Chat(chat_room=chat_room, message=message,
                    message_from=message_from)
    try:
        new_chat.save()
        return True
    except:
        return False


@ login_required
def room(request, slug):
    current_user = request.user
    crr_bot = Room.objects.values().filter(slug__icontains=slug)[0]
    chats = []
    if crr_bot['bot_id'] == '1' or crr_bot['bot_id'] == '2':
        first_qs = crr_bot['Questions'].split(',')[0]
        chats.append(
            {
                'chat_room': crr_bot['name'],
                'message': first_qs,
                'message_from': 'bot'
            }
        )
    else:
        qs = crr_bot['Questions'].split(',')
        idx = 1
        options = []
        for i in qs:
            if (len(i.strip()) == 0):
                break
            options.append({'data': i, "num": idx})
            idx += 1
        prompt = "Please Enter A Question Number To Get An Answer! " if len(
            options) > 0 else "Plese Go to menu and edit your bot set answers & Questions Accordingly! Thank you"
        chats.append(
            {
                'chat_room': crr_bot['name'],
                'message': prompt,
                'message_from': 'bot',
                'options': options
            }
        )

    if request.method == "POST":
        msg = request.POST.get('content')
        print(msg)
        save_msg(crr_bot, msg, current_user)
        if crr_bot['bot_id'] == '1' or crr_bot['bot_id'] == '2':
            if (crr_bot['bot_id'] == '1'):
                if (len(msg.strip()) > 1):
                    response = crr_bot['Answers'].split(',')[0].split('|')
                    result = create_new_bot(msg)
                    for m in response:
                        if (result[0]):
                            save_msg(crr_bot, m, FakeObj('bot'))
                        else:
                            save_msg(crr_bot, result[1], FakeObj('bot'))
                            break
                else:
                    response = crr_bot['Answers'].split(',')[-1].split('|')
                    for m in response:
                        save_msg(crr_bot, m, FakeObj('bot'))

            elif(crr_bot['bot_id'] == '2'):
                if(msg.lower() == "yes"):
                    data = get_new_update()
                    save_msg(crr_bot, data, FakeObj('bot'))
                else:
                    response = crr_bot['Answers'].split(',')[-1].split('|')
                    for m in response:
                        save_msg(crr_bot, m, FakeObj('bot'))

            chats.extend(Chat.objects.values().filter(
                chat_room__icontains=crr_bot['bot_id']))
        else:
            try:
                msg = int(msg)
                print(msg, "in int")
                answer = crr_bot['Answers'].split(',')[msg-1]
                print(answer)
                if len(answer.strip()) == 0:
                    save_msg(
                        crr_bot, f"Sorry! i can't recognize your response ! please enter number only", FakeObj('bot'))
                else:
                    save_msg(crr_bot, answer, FakeObj('bot'))
            except:
                print("unkown")
                save_msg(
                    crr_bot, f"Sorry! i can't recognize your response ! please enter number only", FakeObj('bot'))
            chats.extend(Chat.objects.values().filter(
                chat_room__icontains=crr_bot['bot_id']))

    return render(request, 'room/room.html',
                  {'room': crr_bot, 'chats': chats, 'welcome_msg': crr_bot['wellcome_msg']})


class FakeObj:
    def __init__(self, username):
        self.username = username
