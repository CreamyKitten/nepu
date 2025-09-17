import json
import random
import datetime

# 标准班级、学生、学科、考试类型
classes = ["一班", "二班"]
# 自动生成每班15个不重复姓名
base_names = [
    "张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", "郑十一", "王十二", "冯十三", "陈十四", "褚十五", "卫十六", "蒋十七", "沈十八", "韩十九", "杨二十", "朱二一", "秦二二", "尤二三", "许二四", "何二五", "吕二六", "施二七", "张二八", "孔二九", "曹三十", "严三一", "华三二", "金三三"
]
students = {}
for idx, c in enumerate(classes):
    # 每班15人，取不同名字
    students[c] = [base_names[i+idx*15] for i in range(15)]
subjects = ["数学", "语文", "英语"]
exam_types = ["期中考试", "期末考试"]

# 生成学生信息
student_list = []
student_id_map = {}
for c in classes:
    for i, name in enumerate(students[c]):
        sid = f"202300{len(student_list)+1:03d}"
        student_list.append({
            "student_id": sid,
            "name": name,
            "class_name": c,
            "gender": "男" if i % 2 == 0 else "女",
            "phone": f"1380000{len(student_list)+1:04d}",
            "email": f"{name}@school.com",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        student_id_map[(c, name)] = sid

# 生成成绩（部分学生进步幅度大，部分退步幅度大，其余小幅波动）
grades = []
for c in classes:
    for idx, name in enumerate(students[c]):
        sid = student_id_map[(c, name)]
        for subject in subjects:
            if idx < 3:
                base1 = random.randint(65, 75)
                base2 = base1 + random.randint(15, 20)  # 最大进步
            elif idx >= 12:
                base2 = random.randint(65, 75)
                base1 = base2 + random.randint(15, 20)  # 最大退步
            else:
                base1 = random.randint(70, 85)
                base2 = base1 + random.randint(-5, 5)  # 小幅波动
            for j, exam_type in enumerate(exam_types):
                score = base1 if exam_type == "期中考试" else base2
                score += random.randint(-2, 2)
                score = min(100, max(60, score))
                exam_date = f"2024-0{6+j*5}-15"
                grades.append({
                    "student_id": sid,
                    "subject": subject,
                    "score": round(score, 1),
                    "exam_date": exam_date,
                    "exam_type": exam_type,
                    "teacher_id": "teacher01",
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

# 生成教师
teachers = {
    "teacher01": {
        "username": "teacher01",
        "password_hash": "e10adc3949ba59abbe56e057f20f883e",  # 123456
        "role": "teacher",
        "real_name": "张老师",
        "email": "zhang@school.com",
        "phone": "13800000000",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

# 汇总数据
out = {
    "users": teachers,
    "students": {s["student_id"]: s for s in student_list},
    "grades": grades,
    "subjects": subjects,
    "exam_types": exam_types
}

with open("grade_data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("标准数据已生成，文件为grade_data.json")
print("标准学科成绩数据已生成，文件名：grade_data.json") 