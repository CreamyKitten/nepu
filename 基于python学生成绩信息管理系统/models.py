import datetime
from dataclasses import dataclass
from enum import Enum

class UserRole(Enum):
    TEACHER = "teacher"
    ADMIN = "admin"

@dataclass
class User:
    username: str
    password_hash: str
    role: str  # 存储为字符串
    real_name: str
    email: str
    phone: str
    created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class Student:
    student_id: str
    name: str
    class_name: str
    gender: str
    phone: str
    email: str
    created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class Grade:
    student_id: str
    subject: str
    score: float
    exam_date: str
    exam_type: str
    teacher_id: str
    created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 