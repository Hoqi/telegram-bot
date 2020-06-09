import settings.config as config
import telebot as tb
from telebot import apihelper
from telebot import types
from contextlib import closing
import lib.db as database
import lib.user as u
import lib.preparedOut as prepareStr

apihelper.proxy = {
    'https': 'socks5://:@{}:{}'.format(config.proxy['ip'],config.proxy['port'])
}


bot = tb.TeleBot(config.token)


users = dict()


def initUsers():
     with closing(database.DataBase()) as db:
          temp = db.getUsers()
          for item in temp:
               user = u.User(item['chat_id'])
               user.setParam(item['Group_Name'],item['type'],item['state'])
               users[user.id] = user


initUsers()

@bot.message_handler(content_types=["text"])
def enter(message): 
     user = users.get(message.chat.id)
     if user == None:
          user = u.User(message.chat.id)
          users[message.chat.id] = user
          with closing(database.DataBase()) as db:
               db.saveNewUser(user.id)
     if (message.text == 'Назад'):
          user.state = 'Main'
          with closing(database.DataBase()) as db:
               db.updateDataUser(user)
          response(user,message,'Выбирите действие')
     elif (checkInputState(user.state)== True):
          inputHandler(user,message)
     elif checkAvailableCommand(user.state,user.type,message.text) == True:
          if (user.state == 'LessonsChoice'):
               findLessons(user,message)
          else:
               solveCommand(user,message)
     else:
          response(user,message,'Неизвестная команда')


def findLessons(user,message):
     res = ''
     with closing(database.DataBase()) as db:
          temp = db.getLessons(user.group,message.text)
          for item in temp:
               res = prepareStr.lessonResult.format(item['Time'],
                                                    item['Course'],
                                                    item['FIO_Lecturer'],
                                                    item['room'],
                                                    item['Type'])
               response(user,message,res)
     user.state = 'Main'
     with closing(database.DataBase()) as db:
               db.updateDataUser(user)
     response(user,message,'Выберите действие')



def checkInputState(state):
     for value in config.inputStates:
          if state == value:
               return True
     return False

def solveCommand(user,message):
     if message.text == 'Назад':
          user.state = 'Main'
     else:
          user.state = getKeyByValue(message.text,config.states)
     res = config.botMessage[user.state]

     with closing(database.DataBase()) as db:
               db.updateDataUser(user)

     response(user,message,res)


def notifyUsers(group,lesson,message):
     res = prepareStr.notifyStr.format(lesson['day'],
                                        lesson['time'],
                                        lesson['course'],
                                        lesson['lecturer'],
                                        lesson['room'],
                                        lesson['type'])
     for user in users:
          if (user.group == group):
               response(user,message,res)


def inputHandler(user,message):
     res = ''
     with closing(database.DataBase()) as db:
          if (user.state == 'GroupChoice'):
               tmp = db.getGroups(message.text)
               for item in tmp:
                    if (message.text == item['GroupName']):
                         res = 'Выбрана группа {0}'.format(message.text)
                         user.group = message.text
                         user.type = 'StudentGroup'
                         user.state = 'Main'                       
                         db.updateDataUser(user)
                         response(user,message,res)
                         break
               if (res == ''):
                    res = 'Неизвестная группа'
                    response(user,message,res)
          elif (user.state == 'LecturerChoice'):
               tmp = db.getLecturer(message.text)
               for item in tmp:
                    res = prepareStr.lecturerResult.format( item['day'],
                                                            item['Time'],
                                                            item['room'])
                    response(user,message,res)
               if (res == ''):
                    res = 'Неизвестный преподаватель'
                    response(user,message,res)
          else:
               tmp = db.getRoom(message.text)
               for item in tmp:
                    res = prepareStr.roomResult.format(item['day'],item['Time'],item['GroupName'])
                    response(user,message,res)
               if (res == ''):
                    res = 'Неизвестная аудитория'
                    response(user,message,res)



def response(user,message,res):
     bot.send_message(message.chat.id,
                    res,
                    reply_markup=generate_markup(user.state,user.type))


def checkAvailableCommand(state,typeUser,command):
     commonAction = any(i == command for i in config.keyboardMarkesDialog[state])
     userAction = 0
     action = 0
     if commonAction == False:
          userAction = any(i == command for i in config.keyboardMarkesUser[typeUser][state])
          if (userAction == False):              
               return False
          else:
               return True
     else:
          return True


def getKeyByValue(value,dict):
     for key in dict:
          if dict[key] == value:
               return key
     return None






def generate_markup(dialogState,userState):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in config.keyboardMarkesUser[userState][dialogState]:
         keyboard.add(item)
    for item in config.keyboardMarkesDialog[dialogState]:
         keyboard.add(item)
    return keyboard







if __name__ == '__main__':
     bot.infinity_polling()