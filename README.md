# atomic_habits
**Трекер полезных привычек**

Контекст
В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и 
искоренению старых плохих привычек. Заказчик прочитал книгу, впечатлился и 
обратился с запросом реализовать трекер полезных привычек.

Этот проект представляет собой Django-приложение, развернутое с использованием Docker и Docker Compose.
Реализован бэкенд-сервер для SPA веб-приложения трекер полезных привычек "atomic_habits".

Для запуска проекта (используется Poetry):
клонировать файлы из репозитория,
заполнить данными файл .env.sample переименовав его в .env,
собрать и запустить контейнеры:
для сборки и запуска Docker-контейнеров выполните команду:
docker-compose up --build,
создайте суперпользователя:
в новом терминале создайте суперпользователя для доступа к панели администратора Django:
docker-compose exec app python manage.py createsuperuser
следуйте инструкциям для ввода имени пользователя, email и пароля, 
доступ к приложению: после успешного запуска приложение будет доступно по адресу http://localhost:8001
для доступа к панели администратора перейдите по http://localhost:8001/admin и войдите с учетными данными 
суперпользователя, созданного на предыдущем шаге.

Команды для управления проектом:
    Остановить контейнеры:
        docker-compose down
    Выполнить миграции базы данных:
        docker-compose exec app python manage.py migrate
    Запуск Django Shell:
        docker-compose exec app python manage.py shell

Зависимости
Все зависимости управляются через Poetry. 
Для обновления зависимостей, установите Poetry и выполните: poetry update

Примечания
Убедитесь, что у вас установлен Docker и Docker Compose.
Переменные окружения в файле .env могут быть изменены для ваших нужд.
Все команды выполняются из корневой директории проекта.

Настроен CORS.
Настроена интеграция с Телеграмом.
Реализована пагинацию.
Использованы переменные окружения.
Все необходимые модели описаны или переопределены.
Все необходимые эндпоинты реализованы.
Настроены все необходимые валидаторы.
Описанные права доступа заложены.
Настроена отложенная задача через Celery.
Проект покрыт тестами как минимум на 80%.
Имеется список зависимостей.
Результат проверки Flake8 равен 100%, при исключении миграций.

Описание задач
Добавьте необходимые модели привычек.
Реализуйте эндпоинты для работы с фронтендом.
Создайте приложение для работы с Telegram и рассылками напоминаний.
Модели
В книге хороший пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку необходимо себя вознаграждать или сразу после делать приятную привычку. 
Но при этом привычка не должна расходовать на выполнение больше двух минут. 
Исходя из этого получаем первую модель — «Привычка».

Привычка:
Пользователь — создатель привычки.
Место — место, в котором необходимо выполнять привычку.
Время — время, когда необходимо выполнять привычку.
Действие — действие, которое представляет собой привычка.
Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, 
но не для приятных.
Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
Признак публичности — привычки можно публиковать в общий доступ, 
чтобы другие пользователи могли брать в пример чужие привычки.
Обратите внимание, что в проекте у вас может быть больше, чем одна описанная здесь модель.

Чем отличается полезная привычка от приятной и связанной?
Полезная привычка — это само действие, которое пользователь будет совершать и получать за его выполнение 
определенное вознаграждение (приятная привычка или любое другое вознаграждение).
Приятная привычка — это способ вознаградить себя за выполнение полезной привычки. Приятная привычка указывается 
в качестве связанной для полезной привычки (в поле «Связанная привычка»).

Например: в качестве полезной привычки вы будете выходить на прогулку вокруг квартала сразу же после ужина. 
Вашим вознаграждением за это будет приятная привычка — принять ванну с пеной. То есть такая полезная привычка 
будет иметь связанную привычку.

Рассмотрим другой пример: полезная привычка — «я буду не опаздывать на еженедельную встречу с друзьями в ресторан». 
В качестве вознаграждения вы заказываете себе десерт. В таком случае полезная привычка имеет вознаграждение, 
но не приятную привычку.

Признак приятной привычки — булево поле, которые указывает на то, что привычка является приятной, а не полезной.

Валидаторы
Исключить одновременный выбор связанной привычки и указания вознаграждения.
В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить 
только одно из двух полей.

Время выполнения должно быть не больше 120 секунд.
В связанные привычки могут попадать только привычки с признаком приятной привычки.
У приятной привычки не может быть вознаграждения или связанной привычки.
Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
Нельзя не выполнять привычку более 7 дней. Например, привычка может повторяться раз в неделю, но не раз в 2 недели. 
За одну неделю необходимо выполнить привычку хотя бы один раз.

Пагинация
Для вывода списка привычек реализовать пагинацию с выводом по 5 привычек на страницу.

Права доступа
Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.
Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.
Эндпоинты
Регистрация.
Авторизация.
Список привычек текущего пользователя с пагинацией.
Список публичных привычек.
Создание привычки.
Редактирование привычки.
Удаление привычки.
Интеграция
Для полноценной работы сервиса реализована работа с отложенными задачами для напоминания о том, 
в какое время какие привычки необходимо выполнять.
Для этого сервис интегрирован с мессенджером Телеграм, который занимается рассылкой уведомлений.

Безопасность
Для проекта настроен CORS, чтобы фронтенд мог подключаться к проекту на развернутом сервере.