import hashlib
import re
import statistics
import pandas as pd
from models import User, Student, Grade, UserRole
from storage import DataStorage

class GradeSystemLogic:
    def __init__(self):
        self.storage = DataStorage()
        self._cache = {}  # 添加缓存
        self.load_data()

    def _clear_cache(self):
        """清除缓存"""
        self._cache.clear()

    def load_data(self):
        try:
            data = self.storage.load()
            # 安全地加载数据，如果某个字段不存在则使用默认值
            self.users = {}
            if 'users' in data:
                for k, v in data['users'].items():
                    try:
                        self.users[k] = User(**v)
                    except Exception as e:
                        print(f"加载用户数据失败 {k}: {e}")
            
            self.students = {}
            if 'students' in data:
                for k, v in data['students'].items():
                    try:
                        student = Student(**v)
                        self.students[k] = student
                    except Exception as e:
                        print(f"加载学生数据失败 {k}: {e}")
            
            self.grades = []
            if 'grades' in data:
                for g in data['grades']:
                    try:
                        self.grades.append(Grade(**g))
                    except Exception as e:
                        print(f"加载成绩数据失败: {e}")
            
            self.subjects = data.get('subjects', ['数学', '语文', '英语', '物理', '化学', '生物'])
            self.exam_types = data.get('exam_types', ['期中考试', '期末考试', '月考', '小测验'])
            
        except Exception as e:
            print(f"加载数据时发生错误: {e}")
            # 使用默认值
            self.users = {}
            self.students = {}
            self.grades = []
            self.subjects = ['数学', '语文', '英语', '物理', '化学', '生物']
            self.exam_types = ['期中考试', '期末考试', '月考', '小测验']

    def save_data(self):
        try:
            data = {
                'users': {k: {**vars(v), 'role': v.role} for k, v in self.users.items()},
                'students': {k: vars(v) for k, v in self.students.items()},
                'grades': [vars(g) for g in self.grades],
                'subjects': self.subjects,
                'exam_types': self.exam_types
            }
            self.storage.save(data)
            self._clear_cache()  # 保存后清除缓存
        except Exception as e:
            print(f"保存数据时发生错误: {e}")

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def register_teacher(self, username, password, real_name, email, phone):
        if username in self.users:
            return False, "用户名已存在"
        if not self._validate_email(email):
            return False, "邮箱格式不正确"
        user = User(
            username=username,
            password_hash=self._hash_password(password),
            role=UserRole.TEACHER.value,
            real_name=real_name,
            email=email,
            phone=phone
        )
        self.users[username] = user
        self.save_data()
        return True, "教师注册成功"

    def login(self, username, password):
        if username not in self.users:
            return False, "用户不存在", None
        user = self.users[username]
        if user.password_hash != self._hash_password(password):
            return False, "密码错误", None
        return True, "登录成功", user

    def add_student(self, student_id, name, class_name, gender, phone, email):
        if student_id in self.students:
            return False, "学号已存在"
        student = Student(student_id, name, class_name, gender, phone, email)
        self.students[student_id] = student
        self.save_data()
        return True, "学生添加成功"

    def delete_student(self, student_id):
        if student_id not in self.students:
            return False, "学生不存在"
        # 删除学生相关的所有成绩
        self.grades = [g for g in self.grades if g.student_id != student_id]
        del self.students[student_id]
        self.save_data()
        return True, "学生删除成功"

    def update_student(self, student_id, name, class_name, gender, phone, email):
        """更新学生信息"""
        if student_id not in self.students:
            return False, "学生不存在"
        
        # 验证必填字段
        if not all([name, class_name, phone, email]):
            return False, "请填写所有必填字段"
        
        # 验证邮箱格式
        if not self._validate_email(email):
            return False, "邮箱格式不正确"
        
        # 更新学生信息
        student = self.students[student_id]
        student.name = name
        student.class_name = class_name
        student.gender = gender
        student.phone = phone
        student.email = email
        
        self.save_data()
        return True, "学生信息更新成功"

    def get_student_by_id(self, student_id):
        """根据学号获取学生信息"""
        return self.students.get(student_id)

    def add_grade(self, student_id, subject, score, exam_date, exam_type, teacher_id):
        if student_id not in self.students:
            return False, "学生不存在"
        if not (0 <= score <= 100):
            return False, "成绩必须在0-100之间"
        grade = Grade(student_id, subject, score, exam_date, exam_type, teacher_id)
        self.grades.append(grade)
        self.save_data()
        return True, "成绩添加成功"

    def delete_grade(self, student_id, subject, exam_date, exam_type):
        """删除指定的成绩记录"""
        original_count = len(self.grades)
        # 使用更精确的匹配条件
        self.grades = [g for g in self.grades if not (
            g.student_id == student_id and 
            g.subject == subject and 
            g.exam_date == exam_date and 
            g.exam_type == exam_type
        )]
        if len(self.grades) < original_count:
            self.save_data()
            return True, "成绩删除成功"
        return False, "未找到匹配的成绩记录"

    def delete_grade_by_index(self, grade_index):
        """通过索引删除成绩记录"""
        if 0 <= grade_index < len(self.grades):
            deleted_grade = self.grades.pop(grade_index)
            self.save_data()
            return True, f"成绩删除成功: {deleted_grade.student_id} {deleted_grade.subject}"
        return False, "成绩记录不存在"

    def add_subject(self, subject):
        if subject in self.subjects:
            return False, "科目已存在"
        self.subjects.append(subject)
        self.save_data()
        return True, "科目添加成功"

    def delete_subject(self, subject):
        if subject not in self.subjects:
            return False, "科目不存在"
        # 检查是否有成绩使用该科目
        if any(g.subject == subject for g in self.grades):
            return False, "该科目已被成绩记录使用，无法删除"
        self.subjects.remove(subject)
        self.save_data()
        return True, "科目删除成功"

    def add_exam_type(self, exam_type):
        if exam_type in self.exam_types:
            return False, "考试类型已存在"
        self.exam_types.append(exam_type)
        self.save_data()
        return True, "考试类型添加成功"

    def delete_exam_type(self, exam_type):
        if exam_type not in self.exam_types:
            return False, "考试类型不存在"
        # 检查是否有成绩使用该考试类型
        if any(g.exam_type == exam_type for g in self.grades):
            return False, "该考试类型已被成绩记录使用，无法删除"
        self.exam_types.remove(exam_type)
        self.save_data()
        return True, "考试类型删除成功"

    def search_students(self, keyword="", class_name=None):
        results = []
        for student in self.students.values():
            if (keyword.lower() in student.name.lower() or keyword.lower() in student.student_id.lower()):
                if class_name is None or student.class_name == class_name:
                    results.append(student)
        return results

    def search_grades(self, student_id=None, subject=None, class_name=None, exam_type=None, min_score=None, max_score=None):
        results = []
        for grade in self.grades:
            if student_id and grade.student_id != student_id:
                continue
            if subject and grade.subject != subject:
                continue
            if exam_type and grade.exam_type != exam_type:
                continue
            if min_score is not None and grade.score < min_score:
                continue
            if max_score is not None and grade.score > max_score:
                continue
            if class_name:
                student = self.students.get(grade.student_id)
                if not student or student.class_name != class_name:
                    continue
            results.append(grade)
        return results

    def get_student_grades(self, student_id):
        return [g for g in self.grades if g.student_id == student_id]

    def get_class_grades(self, class_name, subject=None):
        class_students = [s.student_id for s in self.students.values() if s.class_name == class_name]
        grades = [g for g in self.grades if g.student_id in class_students]
        if subject:
            grades = [g for g in grades if g.subject == subject]
        return grades

    def calculate_statistics(self, grades):
        if not grades:
            return {}
        scores = [g.score for g in grades]
        # 计算方差
        variance = round(statistics.variance(scores), 2) if len(scores) > 1 else 0
        return {
            'count': len(scores),
            'average': round(statistics.mean(scores), 2),
            'median': round(statistics.median(scores), 2),
            'max': max(scores),
            'min': min(scores),
            'std': round(statistics.stdev(scores), 2) if len(scores) > 1 else 0,
            'variance': variance,
            'pass_rate': round(len([s for s in scores if s >= 60]) / len(scores) * 100, 2),
            'excellent_rate': round(len([s for s in scores if s >= 90]) / len(scores) * 100, 2)
        }

    def analyze_teaching(self, grades):
        """
        教学情况分析：如班级整体进步、退步、分数波动、最高最低分变化等
        返回字典，包含教学建议、进步/退步学生、分数波动等
        """
        if not grades:
            return {}
        # 按考试时间排序
        grades_sorted = sorted(grades, key=lambda g: g.exam_date)
        scores = [g.score for g in grades_sorted]
        if len(scores) < 2:
            return {'message': '数据不足，无法分析教学变化'}
        # 进步/退步趋势
        trend = '上升' if scores[-1] > scores[0] else '下降' if scores[-1] < scores[0] else '持平'
        # 分数波动
        fluctuation = round(max(scores) - min(scores), 2)
        return {
            'trend': trend,
            'fluctuation': fluctuation,
            'first_score': scores[0],
            'last_score': scores[-1],
            'message': f"本组成绩整体{trend}，分数波动区间为{fluctuation}分。"
        }

    def analyze_student_learning(self, student_id):
        """
        分析单个学生的学习情况：如进步/退步、分数波动、各科均分、建议等。
        支持自动比较该学生所有考试类型的成绩，即使只选中一个考试类型。
        整体趋势优先用各考试类型均分对比。
        """
        grades = self.get_student_grades(student_id)
        if not grades:
            return {'message': '没有该学生的成绩数据'}
        # 按科目+考试类型分组
        from collections import defaultdict
        subject_exam_scores = defaultdict(list)
        exam_type_scores = defaultdict(list)
        for g in grades:
            key = (g.subject, g.exam_type)
            subject_exam_scores[key].append((g.exam_date, g.score))
            exam_type_scores[g.exam_type].append(g.score)
        # 自动比较同一科目不同考试类型的成绩
        progress_info = []
        for subject in set(g.subject for g in grades):
            # 按考试类型排序
            exam_types = sorted(set(g.exam_type for g in grades if g.subject == subject))
            scores_by_type = {}
            for et in exam_types:
                # 取该考试类型的最新成绩
                scores = [s for d, s in subject_exam_scores[(subject, et)]]
                if scores:
                    scores_by_type[et] = max(scores)
            if len(scores_by_type) >= 2:
                types_sorted = sorted(scores_by_type.keys())
                first, last = types_sorted[0], types_sorted[-1]
                diff = scores_by_type[last] - scores_by_type[first]
                trend = '上升' if diff > 0 else '下降' if diff < 0 else '持平'
                progress_info.append(f"{subject}: {first}→{last} {scores_by_type[first]}→{scores_by_type[last]}（{trend}{diff:+.1f}分）")
        # 整体趋势：优先用考试类型均分对比
        if len(exam_type_scores) >= 2:
            types_sorted = sorted(exam_type_scores.keys())
            first_type, last_type = types_sorted[0], types_sorted[-1]
            first_avg = sum(exam_type_scores[first_type]) / len(exam_type_scores[first_type])
            last_avg = sum(exam_type_scores[last_type]) / len(exam_type_scores[last_type])
            diff = last_avg - first_avg
            trend = '上升' if diff > 0 else '下降' if diff < 0 else '持平'
            fluctuation = round(max([max(v) for v in exam_type_scores.values()]) - min([min(v) for v in exam_type_scores.values()]), 2)
        else:
            # 只有一种考试类型，退回用所有成绩首末分数对比
            grades_sorted = sorted(grades, key=lambda g: g.exam_date)
            scores = [g.score for g in grades_sorted]
            if len(scores) < 2:
                return {'message': '数据不足，无法分析学习变化'}
            trend = '上升' if scores[-1] > scores[0] else '下降' if scores[-1] < scores[0] else '持平'
            fluctuation = round(max(scores) - min(scores), 2)
        # 各科均分
        subject_scores = {}
        for g in grades:
            subject_scores.setdefault(g.subject, []).append(g.score)
        subject_avg = {k: round(sum(v)/len(v), 2) for k, v in subject_scores.items()}
        msg = f"该生成绩整体{trend}，分数波动区间为{fluctuation}分。"
        if progress_info:
            msg += "\n各科考试类型成绩变化：\n" + "\n".join(progress_info)
        return {
            'trend': trend,
            'fluctuation': fluctuation,
            'first_score': None,
            'last_score': None,
            'subject_avg': subject_avg,
            'message': msg
        }

    def get_grade_rankings(self, class_name, subject):
        grades = self.get_class_grades(class_name, subject)
        if not grades:
            return []
        sorted_grades = sorted(grades, key=lambda x: x.score, reverse=True)
        rankings = []
        for i, grade in enumerate(sorted_grades, 1):
            student = self.students.get(grade.student_id)
            if student:
                rankings.append({
                    'rank': i,
                    'student_id': grade.student_id,
                    'name': student.name,
                    'score': grade.score,
                    'exam_date': grade.exam_date
                })
        return rankings

    def export_data(self, filename, data_type="all"):
        """导出数据到Excel"""
        try:
            if data_type == "students":
                # 导出学生信息
                students_data = []
                for student in self.students.values():
                    students_data.append({
                        '学号': student.student_id,
                        '姓名': student.name,
                        '班级': student.class_name,
                        '性别': student.gender,
                        '电话': student.phone,
                        '邮箱': student.email,
                        '创建时间': student.created_at
                    })
                df = pd.DataFrame(students_data)
            elif data_type == "grades":
                # 导出成绩信息
                grades_data = []
                for grade in self.grades:
                    student = self.students.get(grade.student_id)
                    if student:
                        grades_data.append({
                            '学号': grade.student_id,
                            '姓名': student.name,
                            '班级': student.class_name,
                            '科目': grade.subject,
                            '成绩': grade.score,
                            '考试日期': grade.exam_date,
                            '考试类型': grade.exam_type,
                            '录入教师': grade.teacher_id,
                            '创建时间': grade.created_at
                        })
                df = pd.DataFrame(grades_data)
            else:
                # 导出所有数据
                all_data = []
                for grade in self.grades:
                    student = self.students.get(grade.student_id)
                    if student:
                        all_data.append({
                            '学号': grade.student_id,
                            '姓名': student.name,
                            '班级': student.class_name,
                            '性别': student.gender,
                            '科目': grade.subject,
                            '成绩': grade.score,
                            '考试日期': grade.exam_date,
                            '考试类型': grade.exam_type,
                            '录入教师': grade.teacher_id,
                            '创建时间': grade.created_at
                        })
                df = pd.DataFrame(all_data)
            
            df.to_excel(filename, index=False)
            return True, "导出成功"
        except Exception as e:
            return False, f"导出失败: {str(e)}"

    def import_students_from_excel(self, filename):
        """从Excel导入学生信息"""
        try:
            df = pd.read_excel(filename)
            required_columns = ['学号', '姓名', '班级', '性别', '电话', '邮箱']
            
            # 检查必需的列
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return False, f"缺少必需的列: {', '.join(missing_columns)}"
            
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    student_id = str(row['学号']).strip()
                    name = str(row['姓名']).strip()
                    class_name = str(row['班级']).strip()
                    gender = str(row['性别']).strip()
                    phone = str(row['电话']).strip()
                    email = str(row['邮箱']).strip()
                    
                    if student_id and name and class_name:
                        success, _ = self.add_student(student_id, name, class_name, gender, phone, email)
                        if success:
                            success_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"导入学生数据失败: {e}")
            
            return True, f"导入完成: 成功 {success_count} 条，失败 {error_count} 条"
        except Exception as e:
            return False, f"导入失败: {str(e)}"

    def import_grades_from_excel(self, filename):
        """从Excel导入成绩信息"""
        try:
            df = pd.read_excel(filename)
            required_columns = ['学号', '科目', '成绩', '考试日期', '考试类型']
            
            # 检查必需的列
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return False, f"缺少必需的列: {', '.join(missing_columns)}"
            
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    student_id = str(row['学号']).strip()
                    subject = str(row['科目']).strip()
                    score = float(row['成绩'])
                    exam_date = str(row['考试日期']).strip()
                    exam_type = str(row['考试类型']).strip()
                    
                    if student_id and subject and exam_date and exam_type:
                        success, _ = self.add_grade(student_id, subject, score, exam_date, exam_type, self.current_user.username if hasattr(self, 'current_user') else 'system')
                        if success:
                            success_count += 1
                        else:
                            error_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"导入成绩数据失败: {e}")
            
            return True, f"导入完成: 成功 {success_count} 条，失败 {error_count} 条"
        except Exception as e:
            return False, f"导入失败: {str(e)}"

    def get_progress_students(self, grades, start_exam_type=None, end_exam_type=None):
        """
        返回进步最大和退步最大的学生（可指定对比的起始和结束考试类型）。
        """
        from collections import defaultdict
        # 先找出当前筛选下的学生ID
        student_ids = set(g.student_id for g in grades)
        # 构建学生所有成绩（不受当前考试类型筛选限制）
        all_grades = getattr(self, 'grades', [])
        student_scores = defaultdict(lambda: defaultdict(list))  # student_id -> exam_type -> [(date, score)]
        for g in all_grades:
            if g.student_id in student_ids:
                student_scores[g.student_id][g.exam_type].append((g.exam_date, g.score))
        progress = []
        for sid in student_scores:
            scores_by_type = student_scores[sid]
            # 只用指定考试类型
            if start_exam_type and end_exam_type and start_exam_type in scores_by_type and end_exam_type in scores_by_type:
                # 取每个类型的最新成绩
                start_score = max([s for d, s in scores_by_type[start_exam_type]])
                end_score = max([s for d, s in scores_by_type[end_exam_type]])
                diff = end_score - start_score
                progress.append((sid, diff))
            else:
                # 默认用所有成绩首末分数
                all_scores = []
                for v in scores_by_type.values():
                    all_scores.extend(v)
                all_scores.sort()
                if len(all_scores) > 1:
                    diff = all_scores[-1][1] - all_scores[0][1]
                    progress.append((sid, diff))
        improved = [(sid, diff) for sid, diff in progress if diff > 0]
        declined = [(sid, diff) for sid, diff in progress if diff < 0]
        improved.sort(key=lambda x: x[1], reverse=True)
        declined.sort(key=lambda x: x[1])
        return improved[:3], declined[:3]

    def get_score_distribution(self, grades):
        """
        返回各分数段人数分布（[0-60, 60-70, 70-80, 80-90, 90-100]）
        """
        bins = [0, 60, 70, 80, 90, 100]
        dist = [0] * (len(bins) - 1)
        for g in grades:
            for i in range(len(bins)-1):
                if bins[i] <= g.score < bins[i+1]:
                    dist[i] += 1
                    break
        return dist

    def get_exam_trend(self, grades):
        """
        返回历次考试的均分、最高分、最低分随时间变化（按exam_date分组）
        """
        from collections import defaultdict
        import datetime
        exam_dict = defaultdict(list)
        for g in grades:
            exam_dict[g.exam_date].append(g.score)
        trend = []
        for date in sorted(exam_dict.keys()):
            scores = exam_dict[date]
            avg = round(sum(scores)/len(scores), 2)
            max_score = max(scores)
            min_score = min(scores)
            trend.append({'date': date, 'avg': avg, 'max': max_score, 'min': min_score})
        return trend 