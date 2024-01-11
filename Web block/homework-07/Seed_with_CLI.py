import argparse

from dateutil import parser as date_parser

from src.db import session
from src.models import Student, Group, Teacher, Subject, Grade


def add_record(model_name, **data):
    try:
        record = model_name(**data)
        session.add(record)
        session.commit()
        print(f"{model_name.__name__} added successfully.")
    except Exception as e:
        print(f"No record has been added: {str(e)}")
        session.rollback()


def update_record(model_name, record_id, **kwargs):
    try:
        record = session.query(model_name).get(record_id)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            session.commit()
            print(f"{model_name.__name__} with ID {record_id} updated successfully.")
        else:
            print(f"{model_name} with ID {record_id} not found.")
    except Exception as e:
        print(f"This record has not been updated: {str(e)}")
        session.rollback()


def list_records(model_name):
    try:
        result = session.query(model_name).all()
        return result
    except Exception as e:
        print(f"No records available: {str(e)}")
        session.rollback()
        return None


def remove_record(model_name, record_id):
    try:
        record = session.query(model_name).get(record_id)
        if record:
            session.delete(record)
            session.commit()
            print(f"{model_name.__name__} with ID {record_id} removed.")
        else:
            print(f"{str(model_name)} with ID {record_id} not found.")
    except Exception as e:
        print(f"Error removing record: {str(e)}")
        session.rollback()

 
def main():
    parser = argparse.ArgumentParser(description='CLI for CRUD actions in the database')
    parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True,
                        help='Possible actions')
    parser.add_argument('--model', '-m', choices=['Student', 'Group', 'Teacher', 'Subject', 'Grade'], required=True)
    parser.add_argument('--id', type=int)
    parser.add_argument('--student_id', type=int)
    parser.add_argument('--group_id', type=int)
    parser.add_argument('--teacher_id', type=int)
    parser.add_argument('--subject_id', type=int)
    parser.add_argument('--date', type=lambda x: date_parser.parse(x).date())
    parser.add_argument('--name', '-n', required=False)
    parser.add_argument('--grade', '-g', type=int, required=False)

    args = parser.parse_args()

    match args.action:
        case 'create':
            match args.model:
                case 'Teacher':
                    add_record(Teacher, fullname=args.name)
                case 'Group':
                    add_record(Group, name=args.name)
                case 'Student':
                    add_record(Student, fullname=args.name, group_id=args.group_id)
                case 'Subject':
                    add_record(Subject, name=args.name, teacher_id=args.teacher_id)
                case 'Grade':
                    if 0 < args.grade < 101:
                        add_record(Grade, grade=args.grade, grade_date=args.date,
                                   student_id=args.student_id, subject_id=args.subject_id)
                    else:
                        print("Wrong grade")
        case 'list':
            match args.model:
                case 'Teacher':
                    print(list_records(Teacher))
                case 'Group':
                    print(list_records(Group))
                case 'Student':
                    print(list_records(Student))
                case 'Subject':
                    print(list_records(Subject))
                case 'Grade':
                    print(list_records(Grade))
        case 'update':
            match args.model:
                case 'Teacher':
                    update_record(Teacher, args.id, fullname=args.name)
                case 'Group':
                    update_record(Group, args.id, name=args.name)
                case 'Student':
                    update_record(Student, args.id, fullname=args.name, group_id=args.group_id)
                case 'Subject':
                    update_record(Subject, args.id, name=args.name, teacher_id=args.teacher_id)
                case 'Grade':
                    if 0 < args.grade < 101:
                        update_record(Grade, args.id, grade=args.grade, grade_date=args.date,
                                      student_id=args.student_id, subject_id=args.subject_id)
                    else:
                        print("Wrong grade")
        case 'remove':
            match args.model:
                case 'Teacher':
                    remove_record(Teacher, args.id)
                case 'Group':
                    remove_record(Group, args.id)
                case 'Student':
                    remove_record(Student, args.id)
                case 'Subject':
                    remove_record(Subject, args.id)
                case 'Grade':
                    remove_record(Grade, args.id)


if __name__ == '__main__':
    main()
