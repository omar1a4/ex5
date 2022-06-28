import json
import os



def get_json(input_json_path):
    with open(input_json_path, 'r') as input_file:
        return json.load(input_file)

def is_registered(course_name, student_dict):
    return course_name in student_dict["registered_courses"]

def update_dict(course_count_dict, student_dict):
    for course in student_dict["registered_courses"]:
        if course not in course_count_dict.keys():
            course_count_dict[course] = 0
        course_count_dict[course]+=1

def create_course_count_json(unsorted_dict,output_file_path):
    list=sorted([course for course in unsorted_dict.keys()])
    with open(output_file_path, 'w') as output_file:
        for course in list:
            output_file.write(' " ' + course + ' " ' + ' ' + str(unsorted_dict[course]) + '\n')


def update_course_for_lecturer(courses_for_lecturers_dict, course_dict):
    for lecturer in course_dict["lecturers"]:
        if (lecturer not in courses_for_lecturers_dict.keys()):
            courses_for_lecturers_dict[lecturer] = [course_dict["course_name"]]
        else:
            if(course_dict["course_name"] not in courses_for_lecturers_dict[lecturer]):
                courses_for_lecturers_dict[lecturer].append(course_dict["course_name"])


def update_courses_for_lecturers(semester_file_path, courses_for_lecturers_dict):
    with open(semester_file_path, 'r') as semester_file:
        semester_dict=json.load(semester_file)
    for course_data in semester_dict.values():
        update_course_for_lecturer(courses_for_lecturers_dict, course_data)
 
 

"""
This function returns a list of the names of the students who registered for
the course with the name "course_name".
:param input_json_path: Path of the students database json file.
:param course_name: The name of the course.
:return: List of the names of the students.
"""
def names_of_registered_students(input_json_path, course_name):
    loaded_dict = get_json(input_json_path)
    return [student_dict["student_name"] for student_dict in loaded_dict.values() if(is_registered(course_name, student_dict))]

"""
This function writes all the course names and the number of enrolled
student in ascending order to the output file in the given path.
:param input_json_path: Path of the students database json file.
:param output_file_path: Path of the output text file.
"""
def enrollment_numbers(input_json_path, output_file_path):
    loaded_dict = get_json(input_json_path)
    course_count = {}
    for student_dict in loaded_dict.values():
        update_dict(course_count_dict = course_count, student_dict = student_dict)
    create_course_count_json(course_count,output_file_path)


"""
This function writes the courses given by each lecturer in json format.
:param json_directory_path: Path of the semsters_data files.
:param output_json_path: Path of the output json file.
"""
def courses_for_lecturers(json_directory_path, output_json_path):
    json_file_names = [file_name for file_name in os.listdir(json_directory_path) if file_name.endswith(".json")]
    courses_for_lecturers_dict={}
    for file_name in json_file_names:
        json_file_path=os.path.join(json_directory_path,file_name)
        update_courses_for_lecturers(json_file_path, courses_for_lecturers_dict)
    with open(output_json_path, 'w') as output_file:
        json.dump(courses_for_lecturers_dict, output_file, indent=4)

#names_of_registered_students("D:/Varrock/technion/courses/sem_D/234124/ex5/students_database.json", "matam")
#print(names_of_registered_students( input_json_path = "D:/Varrock/technion/courses/sem_D/234124/ex5/students_database.json", course_name = "Introduction to Systems Programming"))
#enrollment_numbers(input_json_path = "D:/Varrock/technion/courses/sem_D/234124/ex5/students_database.json", output_file_path = "D:/Varrock/technion/courses/sem_D/234124/ex5/students_database_courses_count.txt")
courses_for_lecturers(json_directory_path="D:/Varrock/technion/courses/sem_D/234124/ex5/semesters_databases", output_json_path="D:/Varrock/technion/courses/sem_D/234124/ex5/courses_for_lecturers.json")