#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import ttk
import random
from threading import Thread
from util import *

students_list = []
selected_list = []
cycle_index = 0
category = ''
c_name = ''


def fresh_listbox_selected(items):
    global students_list
    try:
        for item in items:
            index = students_list.index(item)
            listbox.selection_set(index)
    except Exception:
        reset_selected()

def fresh_log_view():
    text.delete(1.0, END)
    logs = load_log()
    if logs:
        for log in logs:
            text.insert(1.0, log+'\n')


def select_category_func():
    global students_list, selected_list, category
    category = chose_category.get()
    # 读取学员
    if category == '上课考勤':
        clear_selected()
    students_list = load_students()
    listbox.selection_clear(0, END)
    for student in students_list:
        listbox.insert(END, student)
    selected_list = load_selected()
    # 刷新界面
    fresh_listbox_selected(selected_list)
    fresh_log_view()
    child.withdraw()
    root.deiconify()


root = Tk()
root.title("课程点名系统")
root.geometry('650x500+100+100')
root.resizable(width=True, height=True)
# -----------主页选择子窗口---------------------------
child = Toplevel(bg='#15dbe7')
child.resizable(width=False, height=False)
child.geometry('250x150')
Label(child, text='选择点名类型', height=1,fg='white', bg='orange', font=("微软雅黑", 14)).pack(expand=YES, fill=X)
category_list = StringVar()
chose_category = ttk.Combobox(child, width=17,font=("微软雅黑", 14, "bold"), textvariable=category_list)
chose_category['values'] = ['上课考勤', '课堂提问']    # 设置下拉列表的值
chose_category.current(1)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
chose_category.pack(expand=YES)
but1 = Button(child, text="选择", width=5, font=("微软雅黑", 14), command=select_category_func)
but1.pack()
# 启动时只显示选择窗口
root.withdraw()
# -------------------主要工作窗口-----------------------
# 创建容器
frame = Frame(root, bg='#15dbe7')
labelname = Label(frame, text="这是一个点名小程序",height=1,width='52',font=("微软雅黑", 14, "bold"),fg='white', bg='orange')
labelname.pack(expand=NO,fill=X)
listbox = Listbox(frame,  selectmode=MULTIPLE,  bg='#15dbe7', height=15, width=22, font=('Arial', 12))
listbox.pack(side=LEFT,expand=NO,fill=Y)  # 将小部件放置到主窗口中
#添加列表的滚动条
sl = Scrollbar(frame)
sl.set(0, 0.5)
sl.pack(side=LEFT, fill=Y)
listbox['yscrollcommand'] = sl.set
sl['command'] = listbox.yview
# 文本框,显示已往的记录
v = StringVar()
text = Text(frame, width='40', height='10',font=("微软雅黑", 10), fg='blue')
text.pack(expand=YES, fill=BOTH)
# 显示被选学生标签
cur_selected = StringVar()
cur_label = Label(frame,width='40', height='1',textvariable=cur_selected,font=("微软雅黑", 22, "bold"))
cur_label.pack(expand=YES,fill=X)

fresh_listbox_selected(selected_list)
fresh_log_view()

def set_grade():
    return grade.get()

# 学生成绩单选框
grade = StringVar()
grade.set('合格')
r1 = Radiobutton(frame, text='优秀',font=("微软雅黑", 12, "bold"),
                    variable=grade, value='优秀',
                    command=set_grade)
r1.pack(side='top', fill=X, padx=10,pady=2)
r2 = Radiobutton(frame, text='合格',font=("微软雅黑", 12, "bold"),
                    variable=grade, value='合格',
                    command=set_grade)
r2.pack(side='top', fill=X, padx=10,pady=2)
r3 = Radiobutton(frame, text='没来',font=("微软雅黑", 12, "bold"),
                    variable=grade, value='没来',
                    command=set_grade)
r3.pack(side='top', fill=X, padx=10,pady=4)


def get_remaining_students():
    global students_list, selected_list
    result = []
    for student in students_list:
        if student not in selected_list:
            result.append(student)
    return result



def choose_func():
    global selected_list, c_name, category, cycle_index
    repeate_times = 1
    if category == '上课考勤':
        repeate_times = 1
        if cycle_index <= len(students_list)-1:
            c_name = students_list[cycle_index]
            cycle_index += 1
        else:
            messagebox.showinfo(title="点名结束", message='点名结束，重置后可重新点名')
            return None
    else:
        remaining_students = get_remaining_students()
        if len(remaining_students) == 0:
            listbox.selection_clear(0, END)
            reset_selected()
            selected_list = []
            messagebox.showinfo(title="开始新一轮选择", message='从头再来')
        else:
            random.seed()
            c_name = random.choice(remaining_students)
    cur_selected.set(c_name)
    #更新类文本
    selected_list.append(c_name)
    fresh_listbox_selected(selected_list)
    add_selected(c_name)
    t = Thread(target=txt2speech, args=(c_name[1],repeate_times))
    t.start()


def clear_selected():
    global selected_list, cycle_index
    cycle_index = 0
    listbox.selection_clear(0, END)
    selected_list = []
    reset_selected()


def add_grade_log(event=None):
    global category
    if c_name:
        name_str = '\t'.join(c_name)
        add_log(category, name_str, set_grade())
    fresh_log_view()
    if category == '上课考勤':
        choose_func()

def save_log(filename='./点名记录.log'):
    with open(filename, 'w') as fh:
        msg = text.get(1.0, END)
        fh.write(msg)


but8 = Button(frame, text="记录成绩", width=7, font=("微软雅黑", 14), command=add_grade_log)
but8.focus_set()
but8.bind('<Return>', add_grade_log)
but8.pack(side=LEFT, padx=6)
but6 = Button(frame, text="保存记录", width=7, font=("微软雅黑", 14), command=save_log)
but6.pack(side=LEFT, padx=6)
but5 = Button(frame, text="重置已选", width=7, font=("微软雅黑", 14), command=clear_selected)
but5.pack(side=LEFT, padx=6)
but7 = Button(frame, text="开始选择", width=7, font=("微软雅黑", 14), command=choose_func)
but7.pack(side=LEFT, padx=6)




frame.pack(expand=YES, fill=BOTH)
root.mainloop()
