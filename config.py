from Tkinter import *
import mysql.connector
user = 'root'
password = 'password'
host = 'localhost'
db = mysql.connector.connect(user=user, password=password, host=host,
                             buffered=True)

list_words = ['a', 'and', 'be', 'I', 'in', 'is',
              'it', 'of', 'that', 'the', 'to', 'was',
              'all', 'as', 'are', 'at', 'but', 'for',
              'had', 'have', 'he', 'her', 'his', 'not',
              'on', 'one', 'said', 'so', 'they', 'we',
              'with', 'you', 'an', 'by', 'do', 'go', 'if',
              'me', 'my', 'no', 'up', 'or', 'big', 'can',
              'did', 'get', 'has', 'him', 'new', 'now',
              'off', 'old', 'our', 'out', 'see', 'she',
              'two', 'who', 'back', 'bee', 'came', 'down',
              'from', 'into', 'just', 'like', 'made',
              'much', 'over', 'them', 'this', 'well',
              'went', 'when', 'call', 'come', 'here',
              'make', 'must', 'only', 'some', 'then',
              'were', 'what', 'will', 'your', 'about',
              'before', 'could', 'first', 'little', 'look',
              'more', 'other', 'right', 'their', 'there',
              'want', 'where', 'which']

def start_screen():
    global welcome_text
    start = Tk()
    welcome_label = Label(start, text="Please enter your name:", font=("Comic Sans", 14))
    welcome_text = Text(start, width=20, height=1, font=("Helvetica", 14))
    welcome_button = Button(start, text='Enter', command=check_name)
    welcome_label.pack()
    welcome_text.pack()
    welcome_button.pack()
    return start

def check_name():
    name = welcome_text.get(1.0,END)
    try:
        db = mysql.connector.connect(user=user, password=password, host=host,
                                     database=name)
    except:
        create_config()
        name_entry.insert(1.0,name)
        start.withdraw()


def create_config():
    global name_label, name_entry, class_entry
    config_screen = Tk()
    name_label = Label(config_screen, text = 'Teacher Name')
    name_entry = Text(config_screen,width=15, height = 1)
    class_label = Label(config_screen, text="Student Names", font=("Helvetica",14))
    class_instructions = Label(config_screen, text="Enter each name on a new line.")
    class_entry = Text(config_screen, height=10, width=30)
    b = Button(config_screen,text="Press Me", command=create_schema)
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    class_label.grid(row=1, column=0)
    class_instructions.grid(row=2, column=0)
    class_entry.grid(row=3, column=0, columnspan=2)
    b.grid(row=3, column=2, sticky='s')

    return config_screen

def create_schema():
    global db
    db_name = str(name_entry.get(1.0,END)).strip()
    query = "CREATE SCHEMA IF NOT EXISTS %s" % db_name
    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    db = mysql.connector.connect(user=user, password=password, host=host,
                             buffered=True, database=db_name)
    class_names = class_entry.get(1.0,END).split()
    create_tables(db_name,class_names)


def create_tables(db_name,class_names):
    cursor = db.cursor()
    create_students = "CREATE TABLE IF NOT EXISTS students(student_id INT NOT NULL, student_name VARCHAR(45) NULL, PRIMARY KEY (student_id))"
    cursor.execute(create_students)
    for iden in range(len(class_names)):
        insert_students = "INSERT into students (student_id, student_name) VALUES (%d,'%s')" % (iden+1,class_names[iden])
        cursor.execute(insert_students)
    db.commit()
    create_word_list = "CREATE TABLE IF NOT EXISTS word_list(word_id INT NOT NULL, word VARCHAR(45) NULL, PRIMARY KEY (word_id))"
    cursor.execute(create_word_list)
    for index in range(len(list_words)):
        insert_words = "INSERT into word_list(word_id, word) VALUES (%d,'%s')" % (index+1, list_words[index])
        cursor.execute(insert_words)
    db.commit()
    create_unknown_words = "CREATE TABLE IF NOT EXISTS unknown_words(student_id INT NOT NULL, word_id INT NOT NULL)"
    cursor.execute(create_unknown_words)
    for name_index in range(1,len(class_names)+1):
        for word_index in range(1,len(list_words)+1):
            insert_unknown = "INSERT into unknown_words (student_id, word_id) VALUES (%d,%d)" % (name_index,word_index)
            cursor.execute(insert_unknown)
    db.commit()
    cursor.close()



start = start_screen()
start.mainloop()