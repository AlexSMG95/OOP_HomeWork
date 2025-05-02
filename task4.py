from statistics import mean

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def calculate_average_grade(self):
        all_grades = [grade for grades_list in self.grades.values() for grade in grades_list]
        return round(mean(all_grades), 1) if all_grades else None

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self.calculate_average_grade()
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {avg_grade or 'Нет оценок'}\nКурсы в процессе изучения: {courses_in_progress_str}\nЗавершенные курсы: {finished_courses_str}"

    def __lt__(self, other):
        return self.calculate_average_grade() < other.calculate_average_grade()

    def __gt__(self, other):
        return self.calculate_average_grade() > other.calculate_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def calculate_average_grade(self):
        all_grades = [grade for grades_list in self.grades.values() for grade in grades_list]
        return round(mean(all_grades), 1) if all_grades else None

    def __str__(self):
        avg_grade = self.calculate_average_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade or 'Нет оценок'}"

    def __lt__(self, other):
        return self.calculate_average_grade() < other.calculate_average_grade()

    def __gt__(self, other):
        return self.calculate_average_grade() > other.calculate_average_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Создание экземпляров классов
student1 = Student('Иван', 'Иванов', 'Мужской')
student2 = Student('Анна', 'Петрова', 'Женский')

reviewer1 = Reviewer('Василий', 'Петров')
reviewer2 = Reviewer('Ольга', 'Кузнецова')

lecturer1 = Lecturer('Александр', 'Смирнов')
lecturer2 = Lecturer('Елена', 'Андреева')

# Назначение курсов
student1.courses_in_progress.extend(['Python', 'JavaScript'])
student2.courses_in_progress.extend(['Python', 'C++'])

reviewer1.courses_attached.extend(['Python', 'JavaScript'])
reviewer2.courses_attached.extend(['Python', 'C++'])

lecturer1.courses_attached.extend(['Python', 'JavaScript'])
lecturer2.courses_attached.extend(['Python', 'C++'])

# Первоначальные оценки
student1.grades['Python'] = [9, 8, 10]
student2.grades['Python'] = [7, 8]

lecturer1.grades['Python'] = [9, 9, 10]
lecturer2.grades['Python'] = [8, 7]

# Новые оценки (использование методов)
reviewer1.rate_hw(student1, 'Python', 9)           # Новая оценка студенту 1
reviewer2.rate_hw(student2, 'C++', 8)              # Новая оценка студенту 2
print(reviewer1.rate_hw(student2, 'Python', 7))    # Ошибка, студент2 не участвует в курсе Python у reviewer1

student1.rate_lecture(lecturer1, 'Python', 9)      # Новая оценка лектору 1
student2.rate_lecture(lecturer2, 'C++', 8)         # Новая оценка лектору 2
print(student1.rate_lecture(lecturer2, 'Python', 7))  # Ошибка, lecturer2 не ведёт Python

# Вспомогательные функции для расчёта средних оценок
def average_students_homework(students, course_name):
    total_sum = 0
    count = 0
    for student in students:
        if course_name in student.grades:
            total_sum += sum(student.grades.get(course_name, []))
            count += len(student.grades.get(course_name, []))
    return round(total_sum / count, 1) if count != 0 else 'Нет оценок'

def average_lecturers_course(lecturers, course_name):
    total_sum = 0
    count = 0
    for lecturer in lecturers:
        if course_name in lecturer.grades:
            total_sum += sum(lecturer.grades.get(course_name, []))
            count += len(lecturer.grades.get(course_name, []))
    return round(total_sum / count, 1) if count != 0 else 'Нет оценок'

# Списки студентов и лекторов
students = [student1, student2]
lecturers = [lecturer1, lecturer2]

# Средние оценки
print("\nСредний балл за домашние задания по курсу \"Python\":")
print(average_students_homework(students, 'Python'))  # Ожид.: ~8.5

print("\nСредний балл за лекции по курсу \"Python\":")
print(average_lecturers_course(lecturers, 'Python'))  # Ожид.: ~9.3