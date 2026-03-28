from django.shortcuts import render, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment


def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course)
    questions = Question.objects.filter(course=course)

    return render(request, 'course_details_bootstrap.html', {
        'course': course,
        'lessons': lessons,
        'questions': questions
    })


def submit(request, course_id):
    course = Course.objects.get(id=course_id)

    # simple enrollment (dummy)
    enrollment = Enrollment.objects.first()
    if not enrollment:
        enrollment = Enrollment.objects.create(user="TestUser", course=course)

    selected_choices = request.POST.getlist('choice')

    submission = Submission.objects.create(enrollment=enrollment)

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    submission = Submission.objects.get(id=submission_id)

    choices = submission.choices.all()
    total = choices.count()
    correct = choices.filter(is_correct=True).count()

    possible = total   # ⭐ required
    grade = (correct / total) * 100 if total > 0 else 0

    return render(request, 'course_details_bootstrap.html', {
        'score': grade,
        'correct': correct,
        'total': total,
        'possible': possible,   # ⭐ required
        'selected_ids': [c.id for c in choices]
    })
