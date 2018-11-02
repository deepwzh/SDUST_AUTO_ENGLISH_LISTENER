from Tool import *
from ListenService import ListenService
from UserModel import UserModel

def delete_account(stu_id):
    data = read_list()
    for user in data["users"]:
        if user["stu_id"] == stu_id:
            user["status"] = -2
            # data["users"].remove(user)
            backup()
            write_list(data)
            return True

    return False

def add_account(stu_id, stu_password, unit_length, lessons, status = 1):
    data = read_list()
    for user in data["users"]:
        if user["stu_id"] == stu_id:
            print("error1")
            return False
    if not str(unit_length).isdigit() or int(unit_length) < -1:
        print("error2")
        return False
    stu = dict()
    stu["stu_id"] = stu_id
    stu["stu_password"] = stu_password
    stu["status"] = status
    stu["unit_length"] = int(unit_length) * 60
    stu["lessons"] = lessons
    info = get_account_info(UserModel(stu_id, stu_password, unit_length, lessons))
    if info == (-1, -1, -1):
        print("error3")
        return False
    stu["realname"] = info[0]
    stu["major"] = info[1]
    stu["class"] = info[2]
    data["users"].append(stu)
    backup()
    write_list(data)
    return True

def get_process_info(stu_id):
    data = read_list()
    for user in data["users"]:
        if user["stu_id"] == stu_id:
            user_obj = get_account_object(UserModel(user["stu_id"], user["stu_password"], user["unit_length"], user["lessons"]))
            statuses = user_obj.get_status_info()
            if user_obj:
                for status in statuses.values():
                    print("课程： %s" % status["lesson"])
                    print("单元   已挂时间  需挂时间")
                    for unit in status["units"]:
                        print(unit["id"], unit["start_time"], max(user["unit_length"], unit["end_time"]))
                return True
    return False
def get_account_object(user):
    service = ListenService()
    service.set_user(user)
    if service.login():
        return service
    else:
        return None


def get_account_info(user):
    if not get_account_object(user):
        return (-1, -1, -1)
    return (user.stu_realname, user.major, user.class_name)

def main():
    print("Welcome to SDUST English Listen System")
    while True:
        print("1:add a account")
        print("2.list all accounts")
        print("3.delete a account")
        print("4.query a process of account")
        print("5:exit")
        print("Please Choose Operator:")
        oper = int(input())
        if oper == 1:
            stu_id = input("学号：")
            stu_password = input("密码：")
            unit_length = input("每个单元挂的时长（分)：(不填默认为45分钟）")
            print("College_English_NEW_SecEdition_Integrated_3,College_English_NEW_SecEdition_Listening_3")
            lessons = input("需要挂的课程：(以逗号分隔，不填默认为全部）")
            if not unit_length:
                unit_length = 45
            if not lessons:
                lessons = []
            else:
                lessons = lessons.split(",")
            if add_account(stu_id, stu_password, unit_length, lessons):
                print("添加 %s 成功" % stu_id)
            else:
                print("添加 %s 失败，检查是否输入了重复或者错误的信息" % stu_id)

        elif oper == 2:
            print("Name s_id Major Class")
            cnt = 1
            for user in read_list()["users"]:
                print(cnt, user["stu_id"], user["realname"], user["major"], user["class"], user["status"], user["lessons"])
                cnt = cnt + 1
        elif oper == 3:
            stu_id = input("学号：")
            if delete_account(stu_id):
                print("删除 %s 成功" % stu_id)
            else:
                print("删除 %s 失败，检查是否输入了错误的信息" % stu_id)
        elif oper == 4:
            stu_id = input("学号：")
            if not get_process_info(stu_id):
                print("查询 %s 失败，检查是否输入了错误的信息" % stu_id)
        elif oper == 5:
            exit(0)


if __name__ == '__main__':
    main()