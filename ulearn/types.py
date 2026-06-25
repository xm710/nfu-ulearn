from datetime import datetime
from enum import Enum

class Todo:
    def __init__(self, data:dict):
        self.courseCode = data.get("course_code") # course 以後應該也要刻一個類型出來
        self.courseId   = data.get("course_id")
        self.courseName = data.get("course_name")
        self.courseType = data.get("course_type") # 這邊的type有意義 需要拉一個type出來 跟 course 一起刻

        endTime = data.get("end_time")
        self.endTime = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y.%m.%d %H.%M")

        self.Id = data.get("id")
        self.isLocked = data.get("is_locked")
        self.isStudent = data.get("is_student")
        self.prerequisites = data.get("prerequisites")
        self.title = data.get("title")

        type_ = data.get("type")
        self.type = TodoType[type_.upper()]

    def __str__(self):
        string = (
            "{:<9}：{}\n"
            "{:<9}：{}\n"
            "{:<11}：{}\n"
            "{:<9}：{}\n"
            "{:<11}：{}\n"
            "{:<11}：{}\n"
            "{:<13}：{}\n"
            "{:<9}：{}\n"
            "{:<13}：{}\n"
            "{:<13}：{}\n"
            "{:<13}：{}"
        ).format(
            "課程名稱", self.courseName,
            "課程代碼", self.courseCode,
            "課程Id", self.courseId,
            "課程類型", self.courseType,
            "類型", self.type.name,
            "名稱", self.title,
            "Id", self.Id,
            "截止時間", self.endTime,
            "isLocked", self.isLocked,
            "isStudent", self.isStudent,
            "prerequisites", self.prerequisites
        )

        return string


class TodoType(Enum):
    HOMEWORK = 1
    EXAM = 2
    QUESTIONNAIRE = 3
    EVALUATION = 4