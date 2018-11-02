class UserModel(object):

    class Lesson:
        pass

    class Unit:
        pass

    def __init__(self, stu_id, stu_pw, unit_length, lessons):
        self.stu_id = stu_id
        self.stu_pw = stu_pw
        self.stu_realname = ""
        self.name = ""
        self.is_finish = 1
        self.class_id = None
        self.major = None
        self.class_name = None
        self.lessons = lessons
        self.status = dict()
        self.unit = None
        self.lesson = None
        self.unit_length = unit_length


    def is_finish(self):
        return self.is_finish

    def set_finish_flag(self, flag):
        self.is_finish = flag

    def get_process_info(self):
        datas = self.get_status_info()
        for data in datas:
            print(data["lesson"])
            print(data["units"])

    def set_class_id(self, id):
        self.class_id = id

    def get_class_id(self):
        return self.class_id

    def set_class_info(self, major, no):
        self.major, self.class_name = major, no

    def get_class_info(self):
        return self.major, self.class_name

    def get_current_lesson(self):
        return self.lesson

    def get_current_unit(self):
        return self.unit

    def set_status_info(self, status):
        self.status = status

    def get_status_info(self):
        return self.status

    def set_current_lesson(self, lesson):
        self.lesson = lesson

    def set_current_unit(self, unit):
        self.unit = unit

    def set_current_task(self, lesson, unit):
        pass

    def updata_time(self):
        pass

