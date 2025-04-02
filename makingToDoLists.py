from fastapi import FastAPI
import mysql.connector

# Создаём сайт
my_app = FastAPI()

# Функция для подключения к БД
def connect_to_my_database():
    # Подключаемся к MySQL
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ur password",
        database="tasks_db"
    )

    my_cursor = my_db.cursor()  

    # Делаем таблицу для задач
    my_cursor.execute("""
        CREATE TABLE IF NOT EXISTS my_tasks (
            # Номер задачи
            id INT AUTO_INCREMENT PRIMARY KEY,  
            # Текст задачи
            task_text VARCHAR(255),  
            # Сделана или нет - 0 or 1
            done INT  
        )
    """)

    my_db.commit()

    return my_db, my_cursor

# Функция для добавления задачи
def add_new_task(task_text, my_cursor, my_db):
    # Пишем задачу в БД
    my_cursor.execute("INSERT INTO my_tasks (task_text, done) VALUES (%s, %s)", (task_text, 0))
    
    my_db.commit()

    return {"message": "Задача добавлена!"}

# Функция для ввывода всех задач
def get_all_tasks(my_cursor):
    # Читаем все задачи из блокнота
    my_cursor.execute("SELECT id, task_text, done FROM my_tasks")

    # Берёт все задачи
    tasks = my_cursor.fetchall()  
    task_list = []
    
    # Делает список задач
    for task in tasks:
        task_list.append({"id": task[0], "text": task[1], "done": task[2]})

    return task_list

# Функция для корректировки задачи
def change_task(task_id, new_text, new_done, my_cursor, my_db):
    # Меняем задачу в БД
    my_cursor.execute("UPDATE my_tasks SET task_text = %s, done = %s WHERE id = %s", (new_text, new_done, task_id))
    
    my_db.commit()
    
    # Проверяем: нашли задачу?
    if my_cursor.rowcount > 0:  
        return {"message": "Задача изменена!"}
    else:
        return {"message": "Задача не найдена!"}

# Функция для удаления
def delete_task(task_id, my_cursor, my_db):
    # Удаляем задачу из БД
    my_cursor.execute("DELETE FROM my_tasks WHERE id = %s", (task_id,))
    
    my_db.commit()
    
    # Проверяем: удалили?
    if my_cursor.rowcount > 0:  
        return {"message": "Задача удалена!"}
    else:
        return {"message": "Задача не найдена!"}

# Подключаемся к БД
my_db, my_cursor = connect_to_my_database()

# Главная страница
@my_app.get("/")
def home_page():
    return {"message": "Привет! Это сайт для задач!"}

# Добавляем задачу
@my_app.post("/add_task")
def add_task_endpoint(task_text: str):
    result = add_new_task(task_text, my_cursor, my_db)
    return result

# Показываем все задачи
@my_app.get("/tasks")
def get_tasks_endpoint():
    tasks = get_all_tasks(my_cursor)
    return tasks

# Корректируем задачу
@my_app.put("/change_task")
def change_task_endpoint(task_id: int, new_text: str, new_done: int):
    result = change_task(task_id, new_text, new_done, my_cursor, my_db)
    return result

# Удаляем задачу
@my_app.delete("/delete_task")
def delete_task_endpoint(task_id: int):
    result = delete_task(task_id, my_cursor, my_db)
    return resul
