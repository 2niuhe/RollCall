from win32com.client import Dispatch
import time
import datetime


def txt2speech(name, repeat_times, pause_time=1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Rate = -3  # range -10(slow) - 10(fast)
    speak.Volume = 100  # range 0(low) - 100(loud)
    for i in range(repeat_times):
        speak.Speak(name)
        time.sleep(pause_time)


def load_students(filename='./students.txt'):
    students_list = []
    with open(filename, 'rt', encoding='utf-8') as f:
        for line in f:
            line = line[:-1].split('\t')
            students_list.append(line)
    return students_list


def add_selected(name, grade, filename='./selected.txt'):
    with open(filename, 'a') as f:
        f.writelines('%s\n' % name)


def add_log(category, name, grade, filename='./点名记录.log'):
    create_time = datetime.datetime.now().strftime("%m-%d")
    with open(filename, 'a') as f:
        f.writelines('%s\t%s\t%s\t%s\n' % (create_time, category, name, grade))


def reset_selected(filename='./selected.txt'):
    try:
        with open(filename, 'w+') as f:
            f.truncate()
        return True
    except Exception:
        return False

def load_selected(filename='./selected.txt'):
    selected_list = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line[:-1].split('\t')
                selected_list.append(line)
    except Exception:
        return None
    return selected_list


if __name__ == '__main__':
    s = load_students()
    for item in s:
        txt2speech(item[1] ,1)
