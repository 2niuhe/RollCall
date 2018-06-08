#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter.messagebox as messagebox
from tkinter import ttk
import random
import datetime
from util import *

#共同变量或函数
create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
students_list = []
selected_students = []


def select_category_func():
    global students_list, selected_students, selected_category

    selected_category = chose_category.get()
    # 改变主窗口label
    # 读取学员
    listbox.selection_clear(0, END)
    selected_students = load_selected()
    #for selected_student in selected_students[1:-1]:
     #   index = students_list[:-1].index(selected_student[1:-1])
      #  listbox.selection_set(index)

        #读取log日志
    text.delete(1.0, END)
    logs = ['hello','hellolll']
    for log in logs:
        text.insert(1.0, log+'\n')
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
Label(child, text='选择点名类型', height=1,fg='white',bg='orange', font=("微软雅黑", 14)).pack(expand=YES, fill=X)
category_list = StringVar()
chose_category = ttk.Combobox(child, width=17,font=("微软雅黑", 14, "bold"), textvariable=category_list)
chose_category['values'] = ['上课考勤', '课堂提问']    # 设置下拉列表的值
chose_category.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
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
#学员列表
students_list = load_students()
listbox = Listbox(frame,  selectmode=MULTIPLE,  bg='#15dbe7', height=15, width=22, font=('Arial', 12))
listbox.pack(side=LEFT,expand=NO,fill=Y)  # 将小部件放置到主窗口中
for item in students_list:
    listbox.insert(END, item)
#列表上的鼠标点击对选择框的影响
def click_list(event):
    global selected_students
    for selected_student in selected_students[1:-1]:
        index = students_list.index(selected_student)
        listbox.selection_set(index)

listbox.bind('<Button-1>', click_list)

#列表中显示已选过的学员
for selected_student in selected_students[1:]:
    index = students_list.index(selected_student)
    listbox.selection_set(index)

#添加列表的滚动条
sl = Scrollbar(frame)
sl.set(0, 0.5)
sl.pack(side=LEFT, fill=Y)
listbox['yscrollcommand'] = sl.set
sl['command'] = listbox.yview


# 文本框,显示已往的记录
v = StringVar()
text = Text(frame, width='40', height='20', fg='blue')
text.pack(expand=YES, fill=BOTH)
# 显示被选学生标签
cur_selected = StringVar()
cur_label = Label(frame,width='40', height='1',textvariable=cur_selected,font=("微软雅黑", 22, "bold"))
cur_label.pack(expand=YES,fill=X)

def set_grade():
    print(grade.get())

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


def choose_func():
    global students_list, selected_list
    # len(selected_students)
    if  1 == len(students_list):
        listbox.selection_clear(0, END)
        reset_selected()
        selected_list = []
        messagebox.showinfo(title="开始新一轮选择", message='从头再来')
    else:
        random.seed()
        c_name = random.choice(students_list)
        cur_selected.set(c_name)
        #更新类文本
        # selected_list.append(c_name)
        #更新列表
        index = students_list.index(c_name)
        listbox.selection_set(index)


def reset_selected():
    global selected_list
    listbox.selection_clear(0, END)
    with open('./selected.txt', 'w+')as f:
        f.truncate()
    # 清空所有日志信息
    text.delete(1.0, END)

def add_grade_log():
    set_grade()
    print('hhhhhhhhh')


but8 = Button(frame, text="记录成绩", width=7, font=("微软雅黑", 14), command=set_grade)
but8.bind("<Return>", set_grade)
but8.pack(side=LEFT, padx=6)
but8 = Button(frame, text="重置已选", width=7, font=("微软雅黑", 14), command=reset_selected)
but8.pack(side=LEFT, padx=6)
but7 = Button(frame, text="开始选择", width=7, font=("微软雅黑", 14), command=choose_func)
but7.pack(side=LEFT, padx=6)



frame.pack(expand=YES, fill=BOTH)
root.mainloop()
