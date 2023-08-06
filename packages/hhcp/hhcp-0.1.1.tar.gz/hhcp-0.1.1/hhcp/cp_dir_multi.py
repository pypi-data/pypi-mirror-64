"""
指定路径，将其中的所有文件复制到指定 path
"""

import multiprocessing
import os
import platform
import shutil
import threading

from hhcp.utils.chunks import get_chunks


def cp_dir(directory, destination, force):

    class myThread(threading.Thread):

        def __init__(self, threadID, filelist, overwrite):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.filelist = filelist
            self.overwrite = overwrite

        def run(self):
            print("开启线程： " + self.name)
            # 获取锁，用于线程同步
            # threadLock.acquire()
            i = 1
            for f in self.filelist:
                if platform.platform()[:7] == "Windows":
                    f = [x.replace("\\", "/") for x in f]

                if len(f) == 1:
                    if not os.path.exists(f[0]):
                        try:
                            os.makedirs(f[0])
                            print(
                                "thread ID {}, {}, create folder [{}]".format(
                                    self.threadID, i, f[0]))
                        except FileExistsError:
                            pass
                    else:
                        pass
                else:
                    if not os.path.exists(f[1]):
                        try:
                            os.makedirs(f[1])
                            print("thread ID {}, {}/{}, create folder [{}]".
                                  format(self.threadID, i, len(self.filelist),
                                         f[1]))
                        except FileExistsError:
                            pass
                    if self.overwrite:
                        shutil.copy(f[0], f[1])
                    else:
                        target_file = os.path.join(f[1], f[0].split("/")[-1])
                        if os.path.exists(target_file):
                            print(
                                "thread ID {}, {}/{}, File [{}] already exist."
                                .format(self.threadID, i, len(self.filelist),
                                        target_file))
                        else:
                            shutil.copy(f[0], f[1])
                            print("thread ID {}, {}/{}, copy [{}] to [{}]".
                                  format(self.threadID, i, len(self.filelist),
                                         f[0], f[1]))
                i += 1

    thread_num = multiprocessing.cpu_count()

    absp = os.path.abspath(directory)
    absp_prefix = os.path.split(absp)[0]
    absd = os.path.abspath(destination)

    filelist = []
    subs = os.walk(directory)
    for sub in subs:
        pre = sub[0]
        absd_suffix = os.path.relpath(os.path.abspath(pre), absp_prefix)
        files = sub[2]
        if len(files) != 0:
            """
            有文件的时候，filelist 里存为
            [原始文件绝对路径, 要 cp 到的文件夹的绝对路径]
            """
            for file in files:
                filelist.append([
                    os.path.join(os.path.abspath(pre), file),
                    os.path.join(absd, absd_suffix)
                ])
        else:
            """
            没有文件的时候，filelist 里存为
            [要 cp 成为的文件夹的绝对路径]
            """
            filelist.append([os.path.join(absd, absd_suffix)])

    filechunks = get_chunks(filelist, thread_num)
    thread_num = len(filechunks)

    # 线程锁
    # threadLock = threading.Lock()
    threads = []

    for i in range(thread_num):
        thread = myThread(i + 1, filechunks[i], force)
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("cp 结束，退出主线程")
