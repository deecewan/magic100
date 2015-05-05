from Tkinter import *
import mysql.connector
from config import create_config

root = Tk()
configscreen = create_config()

# db connection

db = mysql.connector.connect(user="root", password="password", host="localhost",
                             database="magic100", buffered=True)

# globals
all_student_names = []
first_five = []
first_five_id = []
student_id = 0
# functions


def make_selection():
    global student_id, first_five
    next_words_box.delete(0, END)
    remaining_unknown_words_box.delete(0, END)
    first_five = []
    cur = name_list.curselection()
    student_id = int('%d' % cur) + 1
    student_name = all_student_names[student_id-1]
    student_name_title['text'] = student_name

    if student_id < 10:
        student_id_box['text'] = '0' + str(student_id)
    else:
        student_id_box['text'] = str(student_id)

    unknown_words = get_unknown_words(student_id)
    for unknown_word in unknown_words:
        remaining_unknown_words_box.insert(END, '  ' + unknown_word)

    for each_word in first_five:
        next_words_box.insert(END, '  ' + each_word)

# end functions

# mySQL Queries


def all_names():  # called at the beginning to populate student list

    global all_student_names

    query = "SELECT student_id, student_name FROM students"
    cursor = db.cursor()
    cursor.execute(query)

    for (student_id, student_name) in cursor:
        all_student_names.append('%s' % student_name)

    for name in all_student_names:
        name_list.insert(END, name)
    cursor.close()


def get_unknown_words(student_id):
    global first_five_id
    query = "SELECT word_id from known_words WHERE student_id = %s" % student_id
    cursor = db.cursor()
    cursor.execute(query)

    all_word_id = []
    first_five_id = []
    for word_id in cursor:
        all_word_id.append('%s' % word_id)

    for i in range(5):
        first_five_id.append('%s' % all_word_id[i])

    cursor.close()
    cursor = db.cursor()

    all_unknown_words = []

    for word_id in all_word_id:
        query = "SELECT word FROM word_list WHERE word_id = %s" % word_id
        cursor.execute(query)
        for each_word in cursor:
            all_unknown_words.append('%s' % each_word)
    for i in range(5):
        first_five.append(all_unknown_words[i])

    return all_unknown_words


def delete_first_five():
    global student_id
    cursor = db.cursor()
    for word_id in first_five_id:
        query = "DELETE FROM known_words WHERE student_id = %s and word_id = %s" % (student_id, word_id)
        cursor.execute(query)
    db.commit()
    cursor.close()
    make_selection()

# end mySQL Queries

name_list_frame = Frame(height=200, width=50)
name_list_scroll = Scrollbar(name_list_frame, orient=VERTICAL)
name_list = Listbox(name_list_frame, width=25, height=15, yscrollcommand=name_list_scroll.set)
name_list_scroll.config(command=name_list.yview)
name_list_frame.grid(row=0, column=0, rowspan=11, padx=5)
name_list_scroll.pack(side=RIGHT, fill=Y)
name_list_scroll.lift(name_list)
name_list.pack()
student_select = Button(name_list_frame, text='Select Student', command=make_selection)
student_select.pack()

middle_frame = Frame()
student_name_title = Label(middle_frame, text='Student', font=("Verdana", 14), width=15)
next_words_label = Label(middle_frame, text="Next 5 words", font=("Verdana", 12), wraplength=100)
next_words_box = Listbox(middle_frame, width=15, height=5)
next_words_button = Button(middle_frame, text='Remove Words', width=12, command=delete_first_five)
middle_frame.grid(row=0, column=1)
student_name_title.grid(row=0, column=0, sticky='n')
next_words_label.grid(row=1, column=0)
next_words_box.grid(row=2, column=0)
next_words_button.grid(row=3, column=0)

remaining_unknown_words_frame = Frame()
student_id_box = Label(remaining_unknown_words_frame, text='ID', font=("Verdana", 14), relief=GROOVE)
remaining_unknown_words_scroll = Scrollbar(remaining_unknown_words_frame, orient=VERTICAL)
remaining_unknown_words_label = Label(remaining_unknown_words_frame, text='Remaining Unknown Words',
                                      font=("Verdana", 12), wraplength = 100)
remaining_unknown_words_box = Listbox(remaining_unknown_words_frame, width=15, height=10,
                                      yscrollcommand=remaining_unknown_words_scroll)
remaining_unknown_words_scroll.config(command=remaining_unknown_words_box.yview)
remaining_unknown_words_frame.grid(row=0, column=2)
student_id_box.grid(row=0, column=0)
remaining_unknown_words_label.grid(row=1, column=0)
remaining_unknown_words_scroll.grid(row=2, column=1, sticky='e')
remaining_unknown_words_box.grid(row=2, column=0)

all_names()
root.mainloop()
configscreen.mainloop()
