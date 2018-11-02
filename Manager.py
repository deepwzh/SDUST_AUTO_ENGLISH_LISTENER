import multiprocessing
import signal
import time
from UserModel import UserModel
from ListenService import ListenService
import json

from Tool import *

def run(queue):
    while True:
        user = queue.get()
        if isinstance(user, UserModel):
            print("系统侦测到新任务加入：%s" % user.stu_id)
            service = ListenService()
            service.set_user(user)
            service.listen(10)
        elif isinstance(user, int):
            print("由于用户被删除, %s 的进程终止" % user.stu_id)
            os.kill(int(user), signal.SIGKILL)


    # print("%s, %s" % (user, time.ctime()))
def listen(queue):
    vis = dict()
    while True:
        datas = read_list()
        for user in datas["users"]:
            if vis.get(user["stu_id"], None) and user["status"] == -2:
                user["status"] = -1
                backup()
                write_list(datas)
                queue.put(int(user["stu_id"]))

            if not vis.get(user["stu_id"], None) and user["status"] == 1:
                # print(user)
                vis[user["stu_id"]] = True
                user = UserModel(user["stu_id"],user["stu_password"], user["unit_length"], user["lessons"])
                queue.put(user)
        time.sleep(5)

def main():
    print("欢迎使用英语听力挂听力系统")
    users = read_list()["users"]
    max_size = 10
    queue = multiprocessing.Manager().Queue(max_size)
    writer = multiprocessing.Process(target=listen, args=(queue, ))
    ioLock = multiprocessing.Lock()
    pool = multiprocessing.Pool(processes=max_size)
    for i in range(max_size):
        pool.apply_async(run, args=(queue, ))
    pool.close()
    writer.daemon = True
    writer.start()

    writer.join()

    pool.join()
    print("系统关闭")
    # pool.join()
    # for i in range(2):
    # usermodels = []
    # for user in users:
    #     if user["status"]:
    #         usermodel = UserModel(user["stu_id"],user["stu_password"], user["unit_length"])
    #         usermodels.append(usermodel)
    #         pool.apply_async(run, (usermodel, ))

    # user = UserModel("201601060925","111111")
    # user.set_current_lesson("College_English_NEW_SecEdition_Integrated_3")
    # user.set_current_unit(1)
    # pool.apply_async(run, (user, ))
    # user = UserModel("201601060519","111111")
    # user.set_current_lesson("College_English_NEW_SecEdition_Integrated_3")
    # user.set_current_unit(1)
    # pool.apply_async(run, (user, ))
    print("ha!")

if __name__ == '__main__':
    main()