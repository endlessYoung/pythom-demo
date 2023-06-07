# 导入两个标准库，as的意思是起一个别名，as后面的是别名;
# 其中subprocess库是用来用于在程序中创建和管理子进程的，tkinter库是用来创建图形化窗口的。
import subprocess as sp
import tkinter as tk

# 构建ADBTool类，符合面向对象编程
class ADBTool:
    def __init__(self):
        # 创建一个窗口
        self.window = tk.Tk()
        # 创建窗口的名称为ADB Tool
        self.window.title("ADB Tool")

        # 创建一个滑动框
        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建一个文本框
        self.window.text = tk.Text(self.window, yscrollcommand=scrollbar.set)
        self.window.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 关联滑动条和文本框
        scrollbar.config(command=self.window.text.yview)

        # 在窗口上添加Resolution的文本，后面类似，pack是一种布局的形式
        # self.resolution_label = tk.Label(self.window, text="Resolution", font=("Arial", 11))
        # self.resolution_label.pack()
        # 获取屏幕宽度和高度
        # screen_width = self.window.winfo_screenwidth()
        # screen_height = self.window.winfo_screenheight()

        # 指定窗口大小为800x500，注意一定为x，不能为*
        # self.window.geometry(f"{screen_width}x{screen_height}")
        self.window.geometry("950x650")
        # 更新标签文本
        # self.resolution_label.config(text=f"Resolution: {screen_width}x{screen_height}")

        # self.active_label = tk.Label(self.window, text="Active:")
        # self.active_label.pack()

        # self.active_label.config(text=f"")

        # self.view_label = tk.Label(self.window, text="View:")
        # self.view_label.pack()

        # self.system_label = tk.Label(self.window, text="System Info:")
        # self.system_label.pack()

        self.get_resolution_button = tk.Button(self.window, text="Get Resolution", command=self.get_resolution)
        self.get_resolution_button.pack()

        self.get_active_button = tk.Button(self.window, text="Get Active", command=self.get_active)
        self.get_active_button.pack()

        self.get_view_button = tk.Button(self.window, text="Get View", command=self.get_view)
        self.get_view_button.pack()

        self.get_system_info_button = tk.Button(self.window, text="Get System Info", command=self.get_system_info)
        self.get_system_info_button.pack(padx=10)

        # 开始窗口的事件循环
        self.window.mainloop()

    def get_resolution(self):
        # 获取当前设备屏幕的分辨率（宽度和高度）信息
        result = self.execute_adb_command("shell wm size")
        # 调用插入文本方法
        self.text_insert("Resolution：", result.strip())

    def get_active(self):
        # shell dumpsys window windows 命令会向设备发送一个命令，请求返回当前窗口系统的详细信息。执行该命令后，设备会返回一个包含窗口系统信息的文本
        result = self.execute_adb_command("shell dumpsys window windows | grep mCurrentFocus")

        # 调用插入文本方法
        self.text_insert("Active：", result.strip())

    def get_view(self):
        # uiautomator dump 命令会执行设备上的 UI 自动化脚本，将当前屏幕布局的信息转储到一个 XML 文件中。/dev/tty 是指将输出重定向到设备的终端（tty）设备
        result = self.execute_adb_command("shell uiautomator dump /dev/tty")
        # 调用插入文本方法
        self.text_insert("View：", result.strip())

    def get_system_info(self):
        # 输出系统信息的键值对
        result = self.execute_adb_command("shell getprop")
        # 调用插入文本方法
        self.text_insert("System Info: ", result.strip())

    # 首行信息头加粗
    def text_insert(self, title, content):
        # 将数据插入文本框
        self.window.text.insert(tk.END, title + "\n", "bold")
        if content == "":
            self.window.text.insert(tk.END, "出错啦，找不到此项配置信息~~~" + "\n")
        else:
            self.window.text.insert(tk.END,  content + '\n')

        # if result.strip().returncode == 1:
        #     self.window.text.insert(tk.END, "出错啦，找不到此项配置信息~~~")

        # # 配置标签加粗样式
        self.window.text.tag_configure("bold", font=("Arial", 11, "bold"))

    def execute_adb_command(self, command):
        # 拼接指令
        adb_command = ["adb"] + command.split()
        '''
        通过 subprocess.run()，你可以执行外部命令，并捕获其输出结果、获取返回代码等。
        subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, text=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, env=None, universal_newlines=None)

subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, text=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, env=None, universal_newlines=None)
其中，一些常用的参数包括：

args：要执行的命令及其参数，可以是一个字符串或字符串列表。
capture_output：设置为 True，可以捕获命令的标准输出和错误输出。
text：设置为 True，可以将输出解码为文本字符串。
shell：设置为 True，可以在系统的 shell 中执行命令。
timeout：设置命令的超时时间，超过指定时间后会抛出 TimeoutExpired 异常。
check：设置为 True，如果命令返回非零状态码，则会抛出 CalledProcessError 异常。
在你的代码中，使用了 subprocess.run() 来执行 ADB 命令。capture_output=True 参数用于捕获命令的输出结果，text=True 参数用于将输出解码为文本字符串。通过 result.stdout 获取命令的标准输出部分。
        '''
        result = sp.run(adb_command, capture_output=True, text=True, encoding="UTF-8")
        # 判断returncode或者直接判断result.strip()的值

        # 返回该进程的输出结果
        return result.stdout


ADBTool()
