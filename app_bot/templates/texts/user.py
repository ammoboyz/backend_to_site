START = '''
<b>👨‍💻 Привет, это бот CodeMates от команды <a href="https://t.me/+nfztgdgHlChkOGZi">XOR</a>.</b>

Чтобы начать пользоваться ботом переходи по кнопке ниже и начинай знакомиться с новыми людьми из сферы IT.
'''


NOT_ENTER = '''
<b>🎓❌ Вы не состоите в белом листе нашего бота.</b>

<i>✍️ Чтобы получить доступ, обратитесь к @{}</i>
'''


VIEW = '''
<b>🔭 Чтобы начать просматривать анкеты переходи по кнопке снизу.</b>
'''


WELCOME = '''
<b>{full_name}, добро пожаловать в бота CodeMates by XOR. 👋</b>

☺️ Ваш профиль уже был получен ранее, регистрация не требуется.
'''


JOIN_TO_CHANNEL = '''
<b>👨‍💻 Также советуем подписаться на наш канал по программированию <a href="https://t.me/+i8wHsexRjLdmYTFi">XOR</a></b>
'''


NONE_PHOTO = '''
<b>🖼 Пришлите фотографию своего профиля. Присылать фото можно, как и картинкой, так и файлом.</b>

Вы также можете пропустить этот этап, тогда добавится фото с вашего телеграм-профиля.
'''


PHOTO_DONE = '''
<b>🖼 Ваше фото успешно загружено!</b>
'''


PHOTO_ERROR = '''
<b>🖼 Пожалуйста, отправьте картинку форматом .jpg</b>
'''


PROFILE_STUDENT = '''
<b>👨‍💻 Профиль студента:</b>

<b>🖼 Фото:</b> <code>прикреплено к сообщению</code>

<b>👨‍🦱 Полное имя:</b> <code>{full_name}</code>
<b>✏️ Описание профиля:</b> <code>{description}</code>
<b>🎓 Курс:</b> <code>{course}</code>
'''


PROFILE_MENTOR = '''
<b>👨‍💻 Профиль ментора:</b>

<b>🖼 Фото:</b> <code>прикреплено к сообщению</code>

<b>👨‍🦱 Полное имя:</b> <code>{full_name}</code>
<b>✏️ Описание профиля:</b> <code>{description}</code>
<b>👔 Текущая должность:</b> <code>{position}</code>
<b>💼 Сферы компетенций:</b> <code>{skills}</code>
<b>🎓 Экспертиза:</b> <code>{expertise}</code>
<b>🕘 Часовой пояс:</b> <code>GMT {time_zone}</code>
'''


CHANGE_PROFILE = '''
{}
<i>🛠 Выбери по кнопкам ниже что хочешь изменить:</i>
'''


CHANGE_FULL_NAME = '''
<b>👨‍🦱 Введите новое полное имя:</b>
'''


CHANGE_FULL_NAME_DONE = '''
<b>👨‍🦱 Полное имя изменено на <code>{}</code>!</b>
'''


CHANGE_DESCRIPTION = '''
<b>✏️ Введите новое oписание профиля:</b>
'''


CHANGE_DESCRIPTION_DONE = '''
<b>✏️ Описание профиля изменено на <code>{}</code></b>
'''


CHANGE_PIC = '''
<b>🖼 Отправьте новое фото:</b>
'''


CHANGE_PIC_DONE = '''
<b>🖼 Фото успешно обновлено!</b>
'''


CHANGE_COURSE = '''
🎓 Выберите курсы из списка ниже:
'''


CHANGE_POSITION = '''
<b>👔 Введите новую должность:</b>
'''


CHANGE_POSITION_DONE = '''
<b>👔 Должность заменена на <code>{}</code>!</b>
'''


CHANGE_SKILLS = '''
<b>💼 Выберите сферы компетенции:</b>
'''


CHANGE_SKILLS_DONE = '''
<b>💼 Сфера компетенций успешно изменена на <code>{}</code></b>
'''


CHANGE_EXPERTISE = '''
<b>🎓 Введите свою основную экспертизу.</b>
'''


CHANGE_EXPERTISE_DONE = '''
<b>🎓 Экспертиза успешно изменена на <code>{}</code></b>
'''


CHANGE_TIME_ZONE = '''
<b>🕘 Выберите свой часовой пояс в формате <code>GMT + </code></b>
'''


CHANGE_TIME_ZONE_DONE = '''
<b>🕘 Часовой пояс успешно установлен <code>GMT {}</code></b>
'''


FAVOURITE_MENU = '''
<b>❤️ Меню избранных.</b>
'''


lIKE_ADDED = '''
<b>❤️ Вам пришёл лайк!</b>

<b>Имя:</b> <code>{full_name}</code>
<b>Описание профиля:</b> <code>{description}</code>
<b>Курс:</b> <code>{course}</code>

<b>Сообщение:</b> <code>{message}</code>

<b>Чтобы ответить на лайк, перейди в приложение по кнопке ниже.<b>
'''


LIKE_APPROVED = '''
<b>🎓 Ментор <a href="https://t.me/{username}">{full_name}</a> принял Вашу заявку на консультацию!</b>

Переходите в приложение и выберите подходящую для Вас дату.
'''


LIKE_NOT_APPROVED = '''
<b>Ментор <a href="https://t.me/{username}">{full_name}</a> к сожалению отклонил Вашу заявку на консультацию.</b>
'''


MEETING_ADD = '''
<b>🎓 Студент <a href="https://t.me/{username}">{full_name}</a> успешно записался к Вам на консультацию!</b>

Переходите в приложение по кнопке ниже и изучите новую заявку.
'''


FEEDBACK_ADD = '''
<b>🎓 Студент <a href="https://t.me/{username}">{full_name}</a> поставил вам отзыв!</b>

<b>⭐️ Оценка:</b> {score}

<b>✏️ Описание:</b> {description}
'''


MEETING_CONTACT = '''
<b>📩 Чтобы написать пользователю, перейдите по кнопке ниже.</b>
'''


SEND_REMINDER = '''
<b>🔔 Напоминание о консультации!</b>

🧑‍💻 Консультация с <a href="https://t.me/{username}">{full_name}</a>

🕘 Назначена на <code>{appoint_date}</code>

⌛️ Начнётся через <code>{time}</code> минут по МСК.
'''


CONSULTATION_STARTED = '''
<b>⚠️ Консультация уже началась, не пропустите!</b>

🧑‍💻 Консультация с <a href="https://t.me/{username}">{full_name}</a>

🕘 Назначена на <code>{appoint_date}</code> по МСК.
'''


CONSULTATION_ENDED = '''
<b>🔥 Консультация завершена!</b>

⭐️ Оцените Вашу консультацию с <a href="https://t.me/{username}">{full_name}</a>
'''


FAVOURITE_MENTOR = '''
<b>👨‍🏫 Ментор <a href="https://t.me/{username}">{full_name}</a></b>

<b>👨‍🦱 Полное имя:</b> <code>{full_name}</code>
<b>✏️ Описание профиля:</b> <code>{description}</code>

<b>👔 Текущая должность:</b> <code>{position}</code>
<b>💼 Сферы компетенций:</b> <code>{skills}</code>
<b>🎓 Экспертиза:</b> <code>{expertise}</code>

<b>🕘 Часовой пояс:</b> <code>GMT {time_zone}</code>
'''


FAVOURITE_APPROVE_DELETE = '''
<b>🚮 Подтверждение удаления фаворита.</b>

Вы действительно хотите удалить ментора <a href="https://t.me/{username}">{full_name}</a> из своего списка избранных?
'''


FAVOURITE_DELETE = '''
<b>🚮 Фаворит <a href="https://t.me/{username}">{full_name}</a> успешно удалён.</b>
'''