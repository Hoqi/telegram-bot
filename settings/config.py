token = '' # Токен бота необходимый для получения запросов отправляемых на сервера телеграм

proxy = dict( # SOCKS5 прокси
    ip = '',
    port = ''
)


# состояния необходимые для поддержания конечного автомата 

userState = [
    'Anon',
    'StudentGroup',
    'AdminGroup'
]

dialogState = [
    'Main',
    'GroupChoice',
    'LessonsChoise',
    'LessonAdd',
    'LessonDelete'
]

states = dict(
    LessonsChoice = 'Расписание',
    GroupChoice = 'Выбрать группу',
    LecturerChoice = 'Расписание преподавателя',
    AuditChoice = 'Расписание аудиторий',
)

# Генерируемые кнопки для всех пользователей
keyboardMarkesDialog = dict(
    Main = [
        'Расписание аудиторий',
        'Выбрать группу',
        'Расписание преподавателя',
        'Найти аудиторию'
    ],
    LessonsChoice = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Назад',
    ],
    GroupChoice = [
        'Назад',
        ],
    LecturerChoice = [
        'Назад',
    ],
    AuditChoice = [
        'Назад',
    ],
)

botMessage = dict(
    Main = 'Выерите действие',
    LessonsChoice = 'Выберите день недели',
    GroupChoice = 'Введите название группы',
    LecturerChoice = 'Введите ФИО преподавателя ',
    AuditChoice = 'Введите номер аудитории',
)

inputStates = [
    'GroupChoice',
    'LecturerChoice',
    'AuditChoice'
]

inputStatesAdmin = [
    'AddLessons',
    'deleteLessons'
]

# Генерируесые кнопки конкретных пользователей
keyboardMarkesUser = dict(
    Anon = dict(
        Main = [],
        LessonsChoice = [],
        GroupChoice = [],
        LecturerChoice = [],
        AuditChoice = [],
    ),

    StudentGroup = dict(
        Main = [
            'Расписание'
        ],
        LessonsChoice = [],
        GroupChoice = [],
        LecturerChoice = [],
        AuditChoice = [],
    ),
    AdminGroup = dict(
        Main = [
            'Расписание',
            'Добавить пару',
            'Удалить пару'
        ],
        LessonsChoice = [],
        GroupChoice = [],
        LecturerChoice = [],
        AuditChoice = [],
    )
) 
