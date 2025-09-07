import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from logic import GradeSystemLogic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import datetime
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io
import numpy as np

class GradeSystemGUI:
    def __init__(self):
        self.logic = GradeSystemLogic()
        self.current_user = None
        self.captcha_text = ""
        self.root = tk.Tk()
        self.root.title("智能学生成绩管理系统")
        self.root.geometry("1200x800")
        self.setup_login_gui()

    def generate_captcha(self):
        """生成验证码"""
        # 生成4位随机字符（数字和字母）
        characters = string.ascii_letters + string.digits
        self.captcha_text = ''.join(random.choice(characters) for _ in range(4))
        
        # 创建验证码图片
        width, height = 120, 40
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 添加干扰线
        for _ in range(5):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line([(x1, y1), (x2, y2)], fill='gray', width=1)
        
        # 添加干扰点
        for _ in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill='gray')
        
        # 绘制验证码文字
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            # 如果找不到字体，使用默认字体
            font = ImageFont.load_default()
        
        # 计算文字位置
        text_width = draw.textlength(self.captcha_text, font=font)
        text_height = 20
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # 绘制文字
        draw.text((x, y), self.captcha_text, fill='black', font=font)
        
        # 转换为PhotoImage
        photo = ImageTk.PhotoImage(image)
        return photo

    def setup_login_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        login_frame = ttk.Frame(self.root)
        login_frame.pack(expand=True)
        title_label = ttk.Label(login_frame, text="智能学生成绩管理系统", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        form_frame = ttk.LabelFrame(login_frame, text="用户登录")
        form_frame.pack(pady=20, padx=50)
        ttk.Label(form_frame, text="用户名:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(form_frame, text="密码:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.password_entry = ttk.Entry(form_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # 验证码部分
        ttk.Label(form_frame, text="验证码:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        captcha_frame = ttk.Frame(form_frame)
        captcha_frame.grid(row=2, column=1, padx=10, pady=10)
        
        self.captcha_entry = ttk.Entry(captcha_frame, width=15)
        self.captcha_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # 生成并显示验证码
        self.captcha_photo = self.generate_captcha()
        self.captcha_label = ttk.Label(captcha_frame, image=self.captcha_photo)
        self.captcha_label.pack(side=tk.LEFT, padx=5)
        
        # 刷新验证码按钮
        ttk.Button(captcha_frame, text="刷新", command=self.refresh_captcha).pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="登录", command=self.login).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="教师注册", command=self.show_register).pack(side=tk.LEFT, padx=10)
        self.root.bind('<Return>', lambda e: self.login())

    def refresh_captcha(self):
        """刷新验证码"""
        self.captcha_photo = self.generate_captcha()
        self.captcha_label.configure(image=self.captcha_photo)
        self.captcha_entry.delete(0, tk.END)

    def show_register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("教师注册")
        register_window.geometry("400x500")
        register_window.transient(self.root)
        register_window.grab_set()
        form_frame = ttk.LabelFrame(register_window, text="教师注册")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        fields = [
            ("用户名:", "username"),
            ("密码:", "password", True),
            ("确认密码:", "confirm_password", True),
            ("真实姓名:", "real_name"),
            ("邮箱:", "email"),
            ("电话:", "phone")
        ]
        entries = {}
        for i, field in enumerate(fields):
            ttk.Label(form_frame, text=field[0]).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(form_frame, width=30, show="*" if len(field) > 2 and field[2] else "")
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field[1]] = entry
        def register():
            if entries["password"].get() != entries["confirm_password"].get():
                messagebox.showerror("错误", "两次输入的密码不一致")
                return
            success, message = self.logic.register_teacher(
                entries["username"].get(),
                entries["password"].get(),
                entries["real_name"].get(),
                entries["email"].get(),
                entries["phone"].get()
            )
            if success:
                messagebox.showinfo("成功", message)
                register_window.destroy()
            else:
                messagebox.showerror("错误", message)
        ttk.Button(form_frame, text="注册", command=register).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        captcha = self.captcha_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("警告", "请输入用户名和密码")
            return
        
        if not captcha:
            messagebox.showwarning("警告", "请输入验证码")
            return
        
        # 验证验证码
        if captcha.lower() != self.captcha_text.lower():
            messagebox.showerror("错误", "验证码错误，请重新输入")
            self.refresh_captcha()
            return
        
        success, message, user = self.logic.login(username, password)
        if success:
            self.current_user = user
            messagebox.showinfo("成功", f"欢迎, {user.real_name}!")
            self.setup_main_gui()
        else:
            messagebox.showerror("错误", message)
            self.refresh_captcha()

    def setup_main_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部信息栏
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(info_frame, text=f"当前用户: {self.current_user.real_name} ({self.current_user.role})").pack(side=tk.LEFT)
        ttk.Button(info_frame, text="退出登录", command=self.logout).pack(side=tk.RIGHT)
        
        # 主内容区域
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        self.setup_student_tab(notebook)
        self.setup_grade_tab(notebook)
        self.setup_analysis_tab(notebook)
        self.setup_subject_tab(notebook)
        self.setup_import_export_tab(notebook)
        
        # 底部状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        self.status_label = ttk.Label(status_frame, text=f"系统就绪 | 学生: {len(self.logic.students)} | 成绩: {len(self.logic.grades)}")
        self.status_label.pack(side=tk.LEFT)
        
        # 更新时间显示
        self.time_label = ttk.Label(status_frame, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.time_label.pack(side=tk.RIGHT)
        
        # 定期更新时间
        self.update_time()

    def update_time(self):
        try:
            self.time_label.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.root.after(1000, self.update_time)  # 每秒更新一次
        except Exception:
            pass  # 控件被销毁时自动忽略

    def setup_student_tab(self, notebook):
        student_frame = ttk.Frame(notebook)
        notebook.add(student_frame, text="学生管理")
        left_frame = ttk.LabelFrame(student_frame, text="添加学生")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        fields = [
            ("学号:", "student_id"),
            ("姓名:", "name"),
            ("班级:", "class_name"),
            ("性别:", "gender"),
            ("电话:", "phone"),
            ("邮箱:", "email")
        ]
        self.student_entries = {}
        for i, field in enumerate(fields):
            ttk.Label(left_frame, text=field[0]).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            if field[1] == "gender":
                var = tk.StringVar(value="男")
                entry = ttk.Combobox(left_frame, textvariable=var, values=["男", "女"])
            else:
                entry = ttk.Entry(left_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.student_entries[field[1]] = entry
        ttk.Button(left_frame, text="添加学生", command=self.add_student).grid(row=len(fields), column=0, columnspan=2, pady=10)
        right_frame = ttk.LabelFrame(student_frame, text="学生列表")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # 搜索框架
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.student_search_entry = ttk.Entry(search_frame, width=20)
        self.student_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_students).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="刷新", command=self.refresh_student_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="修改选中", command=self.edit_selected_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="删除选中", command=self.delete_selected_student).pack(side=tk.LEFT, padx=5)
        columns = ("学号", "姓名", "班级", "性别", "电话", "邮箱")
        self.student_tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        self.student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.refresh_student_list()

    def setup_grade_tab(self, notebook):
        grade_frame = ttk.Frame(notebook)
        notebook.add(grade_frame, text="成绩管理")
        left_frame = ttk.LabelFrame(grade_frame, text="添加成绩")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(left_frame, text="学号:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.grade_student_id_entry = ttk.Entry(left_frame)
        self.grade_student_id_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(left_frame, text="科目:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(left_frame, textvariable=self.subject_var, values=self.logic.subjects)
        self.subject_combo.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(left_frame, text="成绩:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.score_entry = ttk.Entry(left_frame)
        self.score_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(left_frame, text="考试日期:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.exam_date_entry = ttk.Entry(left_frame)
        self.exam_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.exam_date_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(left_frame, text="考试类型:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.exam_type_var = tk.StringVar(value=self.logic.exam_types[0])
        self.exam_type_combo = ttk.Combobox(left_frame, textvariable=self.exam_type_var, values=self.logic.exam_types)
        self.exam_type_combo.grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(left_frame, text="添加成绩", command=self.add_grade).grid(row=5, column=0, columnspan=2, pady=10)
        right_frame = ttk.LabelFrame(grade_frame, text="成绩列表")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Button(right_frame, text="删除选中", command=self.delete_selected_grade).pack(anchor=tk.NW, padx=5, pady=5)
        columns = ("学号", "科目", "成绩", "考试日期", "考试类型", "录入教师")
        self.grade_tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        for col in columns:
            self.grade_tree.heading(col, text=col)
            self.grade_tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.grade_tree.yview)
        self.grade_tree.configure(yscrollcommand=scrollbar.set)
        self.grade_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.refresh_grade_list()

    def setup_analysis_tab(self, notebook):
        """设置成绩分析标签页"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="成绩分析")
        
        # 左侧控制面板
        control_frame = ttk.LabelFrame(analysis_frame, text="分析条件")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # 班级选择
        ttk.Label(control_frame, text="班级:").pack(anchor=tk.W, padx=5, pady=2)
        self.analysis_class_var = tk.StringVar(value="全部")
        class_names = ["全部"] + list(set([s.class_name for s in self.logic.students.values()]))
        self.analysis_class_combo = ttk.Combobox(control_frame, textvariable=self.analysis_class_var, 
                                                values=class_names, width=15)
        self.analysis_class_combo.pack(anchor=tk.W, padx=5, pady=2)
        
        # 科目选择
        ttk.Label(control_frame, text="科目:").pack(anchor=tk.W, padx=5, pady=2)
        self.analysis_subject_var = tk.StringVar(value="全部")
        subject_names = ["全部"] + self.logic.subjects
        self.analysis_subject_combo = ttk.Combobox(control_frame, textvariable=self.analysis_subject_var, 
                                                  values=subject_names, width=15)
        self.analysis_subject_combo.pack(anchor=tk.W, padx=5, pady=2)
        
        # 考试类型选择
        ttk.Label(control_frame, text="考试类型:").pack(anchor=tk.W, padx=5, pady=2)
        self.analysis_exam_type_var = tk.StringVar(value="全部")
        exam_type_names = ["全部"] + self.logic.exam_types
        self.analysis_exam_type_combo = ttk.Combobox(control_frame, textvariable=self.analysis_exam_type_var, 
                                                    values=exam_type_names, width=15)
        self.analysis_exam_type_combo.pack(anchor=tk.W, padx=5, pady=2)
        
        # 对比考试类型选择
        ttk.Label(control_frame, text="对比起始考试类型:").pack(anchor=tk.W, padx=5, pady=2)
        self.start_exam_type_var = tk.StringVar(value=self.logic.exam_types[0] if self.logic.exam_types else "")
        self.start_exam_type_combo = ttk.Combobox(control_frame, textvariable=self.start_exam_type_var, values=self.logic.exam_types, width=15)
        self.start_exam_type_combo.pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(control_frame, text="对比结束考试类型:").pack(anchor=tk.W, padx=5, pady=2)
        self.end_exam_type_var = tk.StringVar(value=self.logic.exam_types[-1] if self.logic.exam_types else "")
        self.end_exam_type_combo = ttk.Combobox(control_frame, textvariable=self.end_exam_type_var, values=self.logic.exam_types, width=15)
        self.end_exam_type_combo.pack(anchor=tk.W, padx=5, pady=2)
        
        # 图表类型选择
        ttk.Label(control_frame, text="图表类型:").pack(anchor=tk.W, padx=5, pady=2)
        self.chart_type_var = tk.StringVar(value="直方图+饼图")
        chart_types = ["直方图+饼图", "历次均分折线图", "分数段堆叠柱状图"]
        self.chart_type_combo = ttk.Combobox(control_frame, textvariable=self.chart_type_var, values=chart_types, width=18)
        self.chart_type_combo.pack(anchor=tk.W, padx=5, pady=2)
        
        # 分析按钮
        ttk.Button(control_frame, text="统计分析", command=self.analyze_grades).pack(pady=10)
        ttk.Button(control_frame, text="生成图表", command=self.generate_charts).pack(pady=5)
        ttk.Button(control_frame, text="查看排名", command=self.show_rankings).pack(pady=5)
        ttk.Button(control_frame, text="教学情况分析", command=self.show_teaching_analysis).pack(pady=5)
        
        # 右侧结果显示区域
        result_frame = ttk.Frame(analysis_frame)
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 统计结果显示
        self.stats_frame = ttk.LabelFrame(result_frame, text="统计结果")
        self.stats_frame.pack(fill=tk.X, pady=5)
        self.stats_text = tk.Text(self.stats_frame, height=8, width=50)
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建Notebook来管理图表和排名
        self.analysis_notebook = ttk.Notebook(result_frame)
        self.analysis_notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 图表显示区域
        self.chart_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(self.chart_frame, text="图表展示")
        
        # 排名显示
        self.ranking_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(self.ranking_frame, text="成绩排名")
        
        columns = ("排名", "学号", "姓名", "班级", "成绩", "科目", "考试类型")
        self.ranking_tree = ttk.Treeview(self.ranking_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.ranking_tree.heading(col, text=col)
            self.ranking_tree.column(col, width=80)
        scrollbar = ttk.Scrollbar(self.ranking_frame, orient=tk.VERTICAL, command=self.ranking_tree.yview)
        self.ranking_tree.configure(yscrollcommand=scrollbar.set)
        self.ranking_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def analyze_grades(self):
        """统计分析成绩"""
        class_name = self.analysis_class_var.get()
        subject = self.analysis_subject_var.get()
        exam_type = self.analysis_exam_type_var.get()
        
        # 获取符合条件的成绩
        grades = self.logic.search_grades(
            class_name=class_name if class_name != "全部" else None,
            subject=subject if subject != "全部" else None,
            exam_type=exam_type if exam_type != "全部" else None
        )
        
        if not grades:
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, "没有找到符合条件的成绩数据")
            return
        
        # 计算统计信息
        stats = self.logic.calculate_statistics(grades)
        
        # 教学情况分析
        teaching_analysis = self.logic.analyze_teaching(grades)
        
        # 进步/退步学生
        start_exam_type = self.start_exam_type_var.get()
        end_exam_type = self.end_exam_type_var.get()
        improved, declined = self.logic.get_progress_students(grades, start_exam_type, end_exam_type)
        improved_str = "，".join([f"{self.logic.students.get(sid).name}({diff:+.1f})" for sid, diff in improved if sid in self.logic.students])
        declined_str = "，".join([f"{self.logic.students.get(sid).name}({diff:+.1f})" for sid, diff in declined if sid in self.logic.students])
        # 分数段分布
        dist = self.logic.get_score_distribution(grades)
        dist_labels = ["0-59", "60-69", "70-79", "80-89", "90-100"]
        dist_str = ", ".join([f"{label}:{num}人" for label, num in zip(dist_labels, dist)])
        
        # 显示统计结果
        self.stats_text.delete(1.0, tk.END)
        stats_text = (
            f"""
成绩统计分析结果：
{'='*50}
数据范围：{class_name if class_name != '全部' else '所有班级'} - {subject if subject != '全部' else '所有科目'} - {exam_type if exam_type != '全部' else '所有考试类型'}

基本统计：
• 总人数：{stats['count']} 人
• 平均分：{stats['average']} 分
• 中位数：{stats['median']} 分
• 最高分：{stats['max']} 分
• 最低分：{stats['min']} 分
• 标准差：{stats['std']} 分
• 方差：{stats['variance']} 分²

成绩分布：
• 及格率：{stats['pass_rate']}% (≥60分)
• 优秀率：{stats['excellent_rate']}% (≥90分)

成绩等级分布：
• 优秀 (90-100分)：{len([g for g in grades if g.score >= 90])} 人
• 良好 (80-89分)：{len([g for g in grades if 80 <= g.score < 90])} 人
• 中等 (70-79分)：{len([g for g in grades if 70 <= g.score < 80])} 人
• 及格 (60-69分)：{len([g for g in grades if 60 <= g.score < 70])} 人
• 不及格 (<60分)：{len([g for g in grades if g.score < 60])} 人
"""
            f"\n教学情况分析：\n{teaching_analysis.get('message', '')}\n"
            f"\n进步最大: {improved_str if improved_str else '无'}\n退步最大: {declined_str if declined_str else '无'}\n分数段分布: {dist_str}\n"
        )
        self.stats_text.insert(tk.END, stats_text)

        # 如果只选了一个学生，显示其学习情况分析
        if class_name == "全部" and subject == "全部" and exam_type == "全部" and len(grades) > 0:
            student_ids = set([g.student_id for g in grades])
            if len(student_ids) == 1:
                student_id = list(student_ids)[0]
                learning_analysis = self.logic.analyze_student_learning(student_id)
                self.stats_text.insert(tk.END, f"\n学生学习情况分析：\n{learning_analysis.get('message', '')}\n")
                if 'subject_avg' in learning_analysis:
                    self.stats_text.insert(tk.END, f"各科均分：\n")
                    for sub, avg in learning_analysis['subject_avg'].items():
                        self.stats_text.insert(tk.END, f"  {sub}: {avg} 分\n")

    def generate_charts(self):
        """生成图表"""
        class_name = self.analysis_class_var.get()
        subject = self.analysis_subject_var.get()
        exam_type = self.analysis_exam_type_var.get()
        grades = self.logic.search_grades(
            class_name=class_name if class_name != "全部" else None,
            subject=subject if subject != "全部" else None,
            exam_type=exam_type if exam_type != "全部" else None
        )
        if not grades:
            messagebox.showwarning("警告", "没有找到符合条件的成绩数据")
            return
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        chart_type = self.chart_type_var.get()
        if chart_type == "直方图+饼图":
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            scores = [g.score for g in grades]
            ax1.hist(scores, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
            ax1.set_xlabel('成绩')
            ax1.set_ylabel('人数')
            ax1.set_title('成绩分布直方图')
            ax1.grid(True, alpha=0.3)
            excellent = len([s for s in scores if s >= 90])
            good = len([s for s in scores if 80 <= s < 90])
            medium = len([s for s in scores if 70 <= s < 80])
            pass_grade = len([s for s in scores if 60 <= s < 70])
            fail = len([s for s in scores if s < 60])
            labels = ['优秀', '良好', '中等', '及格', '不及格']
            sizes = [excellent, good, medium, pass_grade, fail]
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('成绩等级分布')
            plt.tight_layout()
        elif chart_type == "历次均分折线图":
            trend = self.logic.get_exam_trend(grades)
            if not trend:
                messagebox.showinfo("提示", "数据不足，无法生成趋势图")
                return
            dates = [t['date'] for t in trend]
            avg = [t['avg'] for t in trend]
            maxs = [t['max'] for t in trend]
            mins = [t['min'] for t in trend]
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(dates, avg, marker='o', label='均分')
            ax.plot(dates, maxs, marker='^', label='最高分')
            ax.plot(dates, mins, marker='v', label='最低分')
            ax.set_xlabel('考试日期')
            ax.set_ylabel('分数')
            ax.set_title('历次考试分数趋势')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
        elif chart_type == "分数段堆叠柱状图":
            trend = self.logic.get_exam_trend(grades)
            if not trend:
                messagebox.showinfo("提示", "数据不足，无法生成柱状图")
                return
            # 按考试日期分组统计分数段
            from collections import defaultdict
            exam_dict = defaultdict(list)
            for g in grades:
                exam_dict[g.exam_date].append(g)
            dates = sorted(exam_dict.keys())
            bins = [0, 60, 70, 80, 90, 100]
            dist_labels = ["0-59", "60-69", "70-79", "80-89", "90-100"]
            data = {label: [] for label in dist_labels}
            for date in dates:
                dist = [0] * (len(bins) - 1)
                for g in exam_dict[date]:
                    for i in range(len(bins)-1):
                        if bins[i] <= g.score < bins[i+1]:
                            dist[i] += 1
                            break
                for i, label in enumerate(dist_labels):
                    data[label].append(dist[i])
            fig, ax = plt.subplots(figsize=(10, 6))
            bottom = np.zeros(len(dates))
            for label in dist_labels:
                ax.bar(dates, data[label], bottom=bottom, label=label)
                bottom += np.array(data[label])
            ax.set_xlabel('考试日期')
            ax.set_ylabel('人数')
            ax.set_title('分数段堆叠柱状图')
            ax.legend()
            plt.tight_layout()
        else:
            messagebox.showinfo("提示", "暂不支持该图表类型")
            return
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # 切换到图表标签页
        self.analysis_notebook.select(0)

    def show_rankings(self):
        """显示成绩排名"""
        class_name = self.analysis_class_var.get()
        subject = self.analysis_subject_var.get()
        exam_type = self.analysis_exam_type_var.get()
        
        # 获取符合条件的成绩
        grades = self.logic.search_grades(
            class_name=class_name if class_name != "全部" else None,
            subject=subject if subject != "全部" else None,
            exam_type=exam_type if exam_type != "全部" else None
        )
        
        if not grades:
            messagebox.showwarning("警告", "没有找到符合条件的成绩数据")
            return
        
        # 按成绩排序
        sorted_grades = sorted(grades, key=lambda x: x.score, reverse=True)
        
        # 清空排名列表
        for item in self.ranking_tree.get_children():
            self.ranking_tree.delete(item)
        
        # 显示排名
        for i, grade in enumerate(sorted_grades, 1):
            student = self.logic.students.get(grade.student_id)
            if student:
                self.ranking_tree.insert("", tk.END, values=(
                    i,
                    grade.student_id,
                    student.name,
                    student.class_name,
                    f"{grade.score:.1f}",
                    grade.subject,
                    grade.exam_type
                ))
        
        # 切换到排名标签页
        self.analysis_notebook.select(1)

    def setup_subject_tab(self, notebook):
        subject_frame = ttk.Frame(notebook)
        notebook.add(subject_frame, text="自定义科目/考试类型")
        # 添加科目
        add_subject_frame = ttk.LabelFrame(subject_frame, text="添加科目")
        add_subject_frame.pack(fill=tk.X, padx=10, pady=10)
        self.new_subject_entry = ttk.Entry(add_subject_frame, width=20)
        self.new_subject_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(add_subject_frame, text="添加科目", command=self.add_subject).pack(side=tk.LEFT, padx=5)
        # 删除科目
        delete_subject_frame = ttk.LabelFrame(subject_frame, text="删除科目")
        delete_subject_frame.pack(fill=tk.X, padx=10, pady=10)
        self.delete_subject_var = tk.StringVar()
        self.delete_subject_combo = ttk.Combobox(delete_subject_frame, textvariable=self.delete_subject_var, values=self.logic.subjects, width=20)
        self.delete_subject_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(delete_subject_frame, text="删除科目", command=self.delete_subject).pack(side=tk.LEFT, padx=5)
        # 添加考试类型
        add_exam_type_frame = ttk.LabelFrame(subject_frame, text="添加考试类型")
        add_exam_type_frame.pack(fill=tk.X, padx=10, pady=10)
        self.new_exam_type_entry = ttk.Entry(add_exam_type_frame, width=20)
        self.new_exam_type_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(add_exam_type_frame, text="添加考试类型", command=self.add_exam_type).pack(side=tk.LEFT, padx=5)
        # 删除考试类型
        delete_exam_type_frame = ttk.LabelFrame(subject_frame, text="删除考试类型")
        delete_exam_type_frame.pack(fill=tk.X, padx=10, pady=10)
        self.delete_exam_type_var = tk.StringVar()
        self.delete_exam_type_combo = ttk.Combobox(delete_exam_type_frame, textvariable=self.delete_exam_type_var, values=self.logic.exam_types, width=20)
        self.delete_exam_type_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(delete_exam_type_frame, text="删除考试类型", command=self.delete_exam_type).pack(side=tk.LEFT, padx=5)
        # 当前科目和考试类型列表
        ttk.Label(subject_frame, text="当前科目:").pack(anchor=tk.W, padx=10, pady=5)
        self.subjects_label = ttk.Label(subject_frame, text=", ".join(self.logic.subjects))
        self.subjects_label.pack(anchor=tk.W, padx=20)
        ttk.Label(subject_frame, text="当前考试类型:").pack(anchor=tk.W, padx=10, pady=5)
        self.exam_types_label = ttk.Label(subject_frame, text=", ".join(self.logic.exam_types))
        self.exam_types_label.pack(anchor=tk.W, padx=20)

    def setup_import_export_tab(self, notebook):
        import_export_frame = ttk.Frame(notebook)
        notebook.add(import_export_frame, text="导入导出")
        # 导出功能
        export_frame = ttk.LabelFrame(import_export_frame, text="导出数据")
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(export_frame, text="导出内容:").pack(side=tk.LEFT, padx=5)
        self.export_type_var = tk.StringVar(value="all")
        export_type_combo = ttk.Combobox(export_frame, textvariable=self.export_type_var, 
                                       values=[("all", "所有数据"), ("students", "学生信息"), ("grades", "成绩信息")], width=15)
        export_type_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="导出数据", command=self.export_data).pack(side=tk.LEFT, padx=10)
        # 导入功能
        import_frame = ttk.LabelFrame(import_export_frame, text="导入数据")
        import_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(import_frame, text="导入类型:").pack(side=tk.LEFT, padx=5)
        self.import_type_var = tk.StringVar(value="students")
        import_type_combo = ttk.Combobox(import_frame, textvariable=self.import_type_var, 
                                       values=[("students", "学生信息"), ("grades", "成绩信息")], width=15)
        import_type_combo.pack(side=tk.LEFT, padx=5)
        ttk.Button(import_frame, text="导入数据", command=self.import_data).pack(side=tk.LEFT, padx=10)
        # 说明
        info_frame = ttk.LabelFrame(import_export_frame, text="使用说明")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        info_text = """
导入学生信息Excel文件需要包含以下列：
学号、姓名、班级、性别、电话、邮箱

导入成绩信息Excel文件需要包含以下列：
学号、科目、成绩、考试日期、考试类型

导出文件将保存为Excel格式(.xlsx)
        """
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.NW, padx=10, pady=10)

    def add_student(self):
        student_id = self.student_entries["student_id"].get().strip()
        name = self.student_entries["name"].get().strip()
        class_name = self.student_entries["class_name"].get().strip()
        gender = self.student_entries["gender"].get()
        phone = self.student_entries["phone"].get().strip()
        email = self.student_entries["email"].get().strip()
        
        # 输入验证
        if not all([student_id, name, class_name]):
            messagebox.showwarning("警告", "学号、姓名、班级为必填项")
            return
        
        # 验证学号格式（假设学号为数字）
        if not student_id.isdigit():
            messagebox.showwarning("警告", "学号必须为数字")
            return
        
        # 验证邮箱格式
        if email and not self.logic._validate_email(email):
            messagebox.showwarning("警告", "邮箱格式不正确")
            return
        
        # 验证性别
        if gender not in ["男", "女"]:
            messagebox.showwarning("警告", "请选择正确的性别")
            return
        
        success, message = self.logic.add_student(student_id, name, class_name, gender, phone, email)
        if success:
            messagebox.showinfo("成功", message)
            self.refresh_student_list()
            # 清空输入框
            for entry in self.student_entries.values():
                if hasattr(entry, 'delete'):
                    entry.delete(0, tk.END)
                elif hasattr(entry, 'set'):
                    entry.set("男")
            # 更新状态栏
            self.status_label.config(text=f"系统就绪 | 学生: {len(self.logic.students)} | 成绩: {len(self.logic.grades)}")
        else:
            messagebox.showerror("错误", message)

    def delete_selected_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的学生")
            return
        item = self.student_tree.item(selected[0])
        student_id = str(item['values'][0]).strip()
        if messagebox.askyesno("确认", f"确定要删除学号为 {student_id} 的学生吗？\n这将同时删除该学生的所有成绩记录。"):
            success, message = self.logic.delete_student(student_id)
            if success:
                messagebox.showinfo("成功", message)
                self.refresh_student_list()
                self.refresh_grade_list()
            else:
                messagebox.showerror("错误", message)

    def edit_selected_student(self):
        """修改选中的学生信息"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的学生")
            return
        
        item = self.student_tree.item(selected[0])
        values = item['values']
        student_id = str(values[0]).strip()
        
        # 获取学生信息
        student = self.logic.get_student_by_id(student_id)
        if not student:
            messagebox.showerror("错误", "学生信息不存在")
            return
        
        # 创建修改窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"修改学生信息 - {student_id}")
        edit_window.geometry("400x350")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        form_frame = ttk.LabelFrame(edit_window, text="学生信息")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # 学号显示（不可修改）
        ttk.Label(form_frame, text="学号:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Label(form_frame, text=student_id, foreground="gray").grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # 其他字段
        fields = [
            ("姓名:", "name", student.name),
            ("班级:", "class_name", student.class_name),
            ("性别:", "gender", student.gender),
            ("电话:", "phone", student.phone),
            ("邮箱:", "email", student.email)
        ]
        
        entries = {}
        for i, field in enumerate(fields, 1):
            ttk.Label(form_frame, text=field[0]).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            if field[1] == "gender":
                var = tk.StringVar(value=field[2])
                entry = ttk.Combobox(form_frame, textvariable=var, values=["男", "女"], width=30)
            else:
                entry = ttk.Entry(form_frame, width=30)
                entry.insert(0, field[2])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field[1]] = entry
        
        def save_changes():
            # 获取修改后的值
            name = entries["name"].get().strip()
            class_name = entries["class_name"].get().strip()
            gender = entries["gender"].get()
            phone = entries["phone"].get().strip()
            email = entries["email"].get().strip()
            
            # 调用逻辑层更新学生信息
            success, message = self.logic.update_student(student_id, name, class_name, gender, phone, email)
            if success:
                messagebox.showinfo("成功", message)
                self.refresh_student_list()
                edit_window.destroy()
            else:
                messagebox.showerror("错误", message)
        
        # 按钮框架
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="保存", command=save_changes).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=edit_window.destroy).pack(side=tk.LEFT, padx=10)

    def search_students(self):
        keyword = self.student_search_entry.get().strip()
        students = self.logic.search_students(keyword)
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for student in students:
            self.student_tree.insert("", tk.END, values=(
                student.student_id, student.name, student.class_name,
                student.gender, student.phone, student.email
            ))

    def add_grade(self):
        student_id = self.grade_student_id_entry.get().strip()
        subject = self.subject_var.get()
        score_str = self.score_entry.get().strip()
        exam_date = self.exam_date_entry.get().strip()
        exam_type = self.exam_type_var.get()
        if not all([student_id, subject, score_str, exam_date, exam_type]):
            messagebox.showwarning("警告", "请填写所有字段")
            return
        try:
            score = float(score_str)
        except ValueError:
            messagebox.showerror("错误", "成绩必须是数字")
            return
        success, message = self.logic.add_grade(student_id, subject, score, exam_date, exam_type, self.current_user.username)
        if success:
            messagebox.showinfo("成功", message)
            self.refresh_grade_list()
        else:
            messagebox.showerror("错误", message)

    def delete_selected_grade(self):
        selected = self.grade_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的成绩")
            return
        
        # 获取选中的项目索引
        selected_index = self.grade_tree.index(selected[0])
        item = self.grade_tree.item(selected[0])
        values = item['values']
        student_id, subject, score, exam_date, exam_type = values[0], values[1], values[2], values[3], values[4]
        
        if messagebox.askyesno("确认", f"确定要删除学号 {student_id} 的 {subject} 成绩吗？"):
            # 使用索引删除
            success, message = self.logic.delete_grade_by_index(selected_index)
            if success:
                messagebox.showinfo("成功", message)
                self.refresh_grade_list()
            else:
                messagebox.showerror("错误", message)

    def add_subject(self):
        subject = self.new_subject_entry.get().strip()
        if not subject:
            messagebox.showwarning("警告", "请输入科目名称")
            return
        success, message = self.logic.add_subject(subject)
        if success:
            messagebox.showinfo("成功", message)
            self.subject_combo['values'] = self.logic.subjects
            self.delete_subject_combo['values'] = self.logic.subjects
            self.subjects_label.config(text=", ".join(self.logic.subjects))
            self.new_subject_entry.delete(0, tk.END)
        else:
            messagebox.showerror("错误", message)

    def delete_subject(self):
        subject = self.delete_subject_var.get()
        if not subject:
            messagebox.showwarning("警告", "请选择要删除的科目")
            return
        if messagebox.askyesno("确认", f"确定要删除科目 '{subject}' 吗？"):
            success, message = self.logic.delete_subject(subject)
            if success:
                messagebox.showinfo("成功", message)
                self.subject_combo['values'] = self.logic.subjects
                self.delete_subject_combo['values'] = self.logic.subjects
                self.subjects_label.config(text=", ".join(self.logic.subjects))
            else:
                messagebox.showerror("错误", message)

    def add_exam_type(self):
        exam_type = self.new_exam_type_entry.get().strip()
        if not exam_type:
            messagebox.showwarning("警告", "请输入考试类型名称")
            return
        success, message = self.logic.add_exam_type(exam_type)
        if success:
            messagebox.showinfo("成功", message)
            self.exam_type_combo['values'] = self.logic.exam_types
            self.delete_exam_type_combo['values'] = self.logic.exam_types
            self.exam_types_label.config(text=", ".join(self.logic.exam_types))
            self.new_exam_type_entry.delete(0, tk.END)
        else:
            messagebox.showerror("错误", message)

    def delete_exam_type(self):
        exam_type = self.delete_exam_type_var.get()
        if not exam_type:
            messagebox.showwarning("警告", "请选择要删除的考试类型")
            return
        if messagebox.askyesno("确认", f"确定要删除考试类型 '{exam_type}' 吗？"):
            success, message = self.logic.delete_exam_type(exam_type)
            if success:
                messagebox.showinfo("成功", message)
                self.exam_type_combo['values'] = self.logic.exam_types
                self.delete_exam_type_combo['values'] = self.logic.exam_types
                self.exam_types_label.config(text=", ".join(self.logic.exam_types))
            else:
                messagebox.showerror("错误", message)

    def export_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            export_type = self.export_type_var.get()
            success, message = self.logic.export_data(filename, export_type)
            if success:
                messagebox.showinfo("成功", message)
            else:
                messagebox.showerror("错误", message)

    def import_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            import_type = self.import_type_var.get()
            if import_type == "students":
                success, message = self.logic.import_students_from_excel(filename)
            else:
                success, message = self.logic.import_grades_from_excel(filename)
            
            if success:
                messagebox.showinfo("成功", message)
                self.refresh_student_list()
                self.refresh_grade_list()
            else:
                messagebox.showerror("错误", message)

    def refresh_student_list(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for student in self.logic.students.values():
            self.student_tree.insert("", tk.END, values=(
                student.student_id, student.name, student.class_name,
                student.gender, student.phone, student.email
            ))

    def refresh_grade_list(self):
        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)
        for grade in self.logic.grades:
            self.grade_tree.insert("", tk.END, values=(
                grade.student_id, grade.subject, grade.score, grade.exam_date, grade.exam_type, grade.teacher_id
            ))

    def logout(self):
        self.current_user = None
        self.setup_login_gui()

    def show_teaching_analysis(self):
        class_name = self.analysis_class_var.get()
        subject = self.analysis_subject_var.get()
        exam_type = self.analysis_exam_type_var.get()
        grades = self.logic.search_grades(
            class_name=class_name if class_name != "全部" else None,
            subject=subject if subject != "全部" else None,
            exam_type=exam_type if exam_type != "全部" else None
        )
        if not grades:
            messagebox.showwarning("警告", "没有找到符合条件的成绩数据")
            return
        teaching_analysis = self.logic.analyze_teaching(grades)
        start_exam_type = self.start_exam_type_var.get()
        end_exam_type = self.end_exam_type_var.get()
        improved, declined = self.logic.get_progress_students(grades, start_exam_type, end_exam_type)
        improved_str = "，".join([f"{self.logic.students.get(sid).name}({diff:+.1f})" for sid, diff in improved if sid in self.logic.students])
        declined_str = "，".join([f"{self.logic.students.get(sid).name}({diff:+.1f})" for sid, diff in declined if sid in self.logic.students])
        dist = self.logic.get_score_distribution(grades)
        dist_labels = ["0-59", "60-69", "70-79", "80-89", "90-100"]
        dist_str = ", ".join([f"{label}:{num}人" for label, num in zip(dist_labels, dist)])
        # 各分数段学生名单
        bins = [0, 60, 70, 80, 90, 100]
        seg_students = {label: [] for label in dist_labels}
        for g in grades:
            for i in range(len(bins)-1):
                if bins[i] <= g.score < bins[i+1]:
                    name = self.logic.students.get(g.student_id).name if g.student_id in self.logic.students else g.student_id
                    seg_students[dist_labels[i]].append(name)
                    break
        # 弹窗显示
        win = tk.Toplevel(self.root)
        win.title("教学情况分析")
        win.geometry("500x600")
        text = tk.Text(win, height=18)
        text.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        text.insert(tk.END, f"{teaching_analysis.get('message', '')}\n\n进步最大: {improved_str if improved_str else '无'}\n退步最大: {declined_str if declined_str else '无'}\n分数段分布: {dist_str}\n\n")
        for label in dist_labels:
            text.insert(tk.END, f"{label}分段学生({len(seg_students[label])}人): {', '.join(seg_students[label])}\n")
        text.config(state=tk.DISABLED)
        # 学生分析输入
        frame = ttk.Frame(win)
        frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(frame, text="输入学生姓名: ").pack(side=tk.LEFT)
        name_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=name_var, width=20)
        entry.pack(side=tk.LEFT, padx=5)
        result_text = tk.Text(win, height=8)
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        def analyze_student():
            name = name_var.get().strip()
            sid = None
            for s in self.logic.students.values():
                if s.name == name:
                    sid = s.student_id
                    break
            result_text.delete(1.0, tk.END)
            if not sid:
                result_text.insert(tk.END, "未找到该学生")
                return
            analysis = self.logic.analyze_student_learning(sid)
            result_text.insert(tk.END, f"学生学习情况分析：\n{analysis.get('message', '')}\n")
            if 'subject_avg' in analysis:
                result_text.insert(tk.END, f"各科均分：\n")
                for sub, avg in analysis['subject_avg'].items():
                    result_text.insert(tk.END, f"  {sub}: {avg} 分\n")
        ttk.Button(frame, text="分析该生", command=analyze_student).pack(side=tk.LEFT, padx=5)

    def run(self):
        self.root.mainloop() 