class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def _average_grade(self):
        grades_list = [grade for grades in self.grades.values() for grade in grades]
        return sum(grades_list) / len(grades_list) if grades_list else 0

    def __str__(self):
        avg_grade = self._average_grade()
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress_str}\n"
                f"Завершенные курсы: {finished_courses_str}")

    def __lt__(self, other):
        return self._average_grade() < other._average_grade()

    def __gt__(self, other):
        return self._average_grade() > other._average_grade()

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self):
        grades_list = [grade for grades in self.grades.values() for grade in grades]
        return sum(grades_list) / len(grades_list) if grades_list else 0

    def __str__(self):
        avg_grade = self._average_grade()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_grade:.1f}")

    def __lt__(self, other):
        return self._average_grade() < other._average_grade()

    def __gt__(self, other):
        return self._average_grade() > other._average_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}")

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

# Функция подсчёта среднего балла студентов за определённый курс
def average_student_grades(students, course_name):
    total_sum = 0
    count = 0

    for student in students:
        if course_name in student.grades:
            total_sum += sum(student.grades.get(course_name))
            count += len(student.grades.get(course_name))

    return round(total_sum / count, 1) if count != 0 else None


# Функция подсчёта среднего балла лекторов за определённый курс
def average_lecturers_grades(lecturers, course_name):
    total_sum = 0
    count = 0

    for lecturer in lecturers:
        if course_name in lecturer.grades:
            total_sum += sum(lecturer.grades.get(course_name))
            count += len(lecturer.grades.get(course_name))

    return round(total_sum / count, 1) if count != 0 else None

# Создаем экземпляры студентов
student1 = Student("Иван", "Иванов", "Мужской")
student2 = Student("Анна", "Петрова", "Женский")

# Создаем экземпляры лекторов
lecturer1 = Lecturer("Сергей", "Сергеев")
lecturer2 = Lecturer("Ольга", "Васильева")

# Создаем экземпляры рецензентов
reviewer1 = Reviewer("Михаил", "Кузнецов")
reviewer2 = Reviewer("Елена", "Смирнова")

# Настройка курсов для студентов
student1.courses_in_progress.extend(["Python", "Java"])
student1.finished_courses.append("C++")

student2.courses_in_progress.extend(["Python", "Kotlin"])
student2.finished_courses.append("HTML/CSS")

# Настройка курсов для лекторов
lecturer1.courses_attached.extend(["Python", "Java"])
lecturer2.courses_attached.extend(["Python", "Kotlin"])

# Проставление курсов для рецензентов
reviewer1.courses_attached.extend(["Python", "Java"])
reviewer2.courses_attached.extend(["Python"])

# ОЦЕНКИ СТУДЕНТОВ ЛЕКТОРАМ
student1.rate_lecture(lecturer1, "Python", 9)
student2.rate_lecture(lecturer1, "Python", 8)

student2.rate_lecture(lecturer2, "Kotlin", 7)

# РЕВЬЮЕРЫ ПРОВЕРЯЮТ РАБОТУ СТУДЕНТОВ
reviewer1.rate_hw(student1, "Python", 10)
reviewer1.rate_hw(student2, "Python", 9)

reviewer2.rate_hw(student1, "Python", 9)

# Проверка магических методов сравнения (__lt__, __gt__)
if student1 > student2:
    print(f"\nСтудент {student1.name} имеет большую среднюю оценку, чем {student2.name}.")
else:
    print(f"\nСтудент {student2.name} имеет большую среднюю оценку, чем {student1.name}.")

if lecturer1 < lecturer2:
    print(f"Преподаватель {lecturer2.name} имеет лучшую среднюю оценку, чем {lecturer1.name}.")
else:
    print(f"Преподаватель {lecturer1.name} имеет лучшую среднюю оценку, чем {lecturer2.name}.")

# Тестируем все методы и выводим информацию
print("\nИнформация о студентах:")
print(student1, "\n")
print(student2)

print("\nИнформация о преподавателях:")
print(lecturer1, "\n")
print(lecturer2)

print("\nИнформация о проверяющих:")
print(reviewer1, "\n")
print(reviewer2)

print("\nСредняя оценка за курс Python среди студентов:",
      average_student_grades([student1, student2], "Python"))

print("Средняя оценка за курс Python среди лекторов:",
      average_lecturers_grades([lecturer1, lecturer2], "Python"))