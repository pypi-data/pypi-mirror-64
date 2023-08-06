"""
指定 filelist，将其中的所有文件复制到指定 path
"""
import multiprocessing
import os
import platform
import shutil
import threading

from hhcp.utils.chunks import get_chunks


def cp_list(filelist, destination, prefix, overwrite):

    class myThread(threading.Thread):

        def __init__(self, threadID, filelist, destination, overwrite):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.filelist = filelist
            self.destination = destination
            self.overwrite = overwrite

        def run(self):
            print("开启线程： " + self.name)
            # 获取锁，用于线程同步
            # threadLock.acquire()

            for i, f in enumerate(self.filelist):
                if platform.platform()[:7] == "Windows":
                    f = [x.replace("\\", "/") for x in f]

                if self.overwrite:
                    shutil.copy(f, self.destination)
                    print("thread ID {}, {}/{}, copy [{}] to [{}]".format(
                        self.threadID, i, len(self.filelist), f,
                        self.destination))
                else:
                    target_file = os.path.join(self.destination,
                                               f.split("/")[-1])
                    if os.path.exists(target_file):
                        print("thread ID {}, {}/{}, File [{}] already exist.".
                              format(self.threadID, i, len(self.filelist),
                                     target_file))
                    else:
                        shutil.copy(f, self.destination)
                        print("thread ID {}, {}/{}, copy [{}] to [{}]".format(
                            self.threadID, i, len(self.filelist), f,
                            self.destination))

    thread_num = multiprocessing.cpu_count()

    files = []
    for l in open(filelist):
        files.append(os.path.join(prefix, l.strip("\n")))

    filechunks = get_chunks(files, thread_num)
    thread_num = len(filechunks)

    # 线程锁
    # threadLock = threading.Lock()
    threads = []

    for i in range(thread_num):
        thread = myThread(i, filechunks[i], destination, overwrite)
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("cp 结束，退出主线程")
