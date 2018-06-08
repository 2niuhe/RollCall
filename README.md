# RollCall
一个上课点名&amp;提问小程序

## Usage
功能：   

- 遍历列表并点名
- 随机抽人回答问题
- 将点名/回答情况记录到日志文档中


可以下载dist目录下的exe文件试用，需要在exe的当前目录放置students.txt文件。   
students.txt格式：   
> 序号+制表符+姓名+制表符+学号

可以使用excel打开`点名记录.log`，进行进一步数据统计。

## Compile
可以自行修改文件并编译
```bash
pyinstaller --onefile --windowed --icon=rollcall.ico roll_call.py
```


