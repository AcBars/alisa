# Информационная система "Алиса"

## Структура базы данных
![Структура БД](img/alisa.png)

## База данных состоит из четырёх основных таблиц

![](img/general_form.png)

* ### Students 
  * id (_Идентификационный номер записи_)
  * first_name (_Имя_)
  * last_name (_Фамилия_)
  * id_class (_Класс_)
* ### Classes 
  * id (_Идентификационный номер записи_)
  * level (_Класс_)
  * symbol (_Буква_)
* ### Subjects
  * id (_Идентификационный номер записи_)
  * subject (_Название урока_)
* ### Schedule
  * id (_Идентификационный номер записи_)
  * id_week (_День недели_)
  * time_start (_Время начала урока_)
  * id_class (_Класс_)
  * id_subject (_Урок_)
____

## Работа с информационной системой
В таблицах реализованы следующие операции:
* Добавление новых записей
  * Начало добавления:
  
    ![](img/add_button.png)

  * После добавления для записи новых строк в базу данных необходимо нажать кнопку `Submit`:
  
    ![](img/submit_button.png)


* Удаление записей.  
![](img/delete_button.png)


* Редактирование существующих записей. При редактировании ссылочных полей для пользователя отображается выпадающий 
  выпадающий список с читаемыми именами, при этом все поля хранятся и записываются в виде ключей.  
![](img/table_intersection.png)


* Каждая таблица представлены в виде отдельного окна приложения, можно изменять её размеры и разворачивать на
  полный экран  
![](img/full_screen_mode.png)

* При этом остаётся возможность переключения между таблицами
![](img/switching.jpg)
____

## Над проектом работали:

* ### Рафаэль: _**Создание и первичное заполнение базы данных, чтение и изменение записей**_
* ### Александр: _**Графический интерфейс**_
* ### Алексей: _**Добавление и удаление записей, инструкция**_
* ### Артём: _**Git-репозиторий, добавление и удаление записей**_