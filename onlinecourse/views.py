from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    try:
        enrollment = Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        return redirect('onlinecourse:course_details', pk=course_id)
    
    if request.method == 'POST':
        selected_choice_ids = request.POST.getlist('choice')
        
        submission = Submission.objects.create(enrollment=enrollment)
        selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
        submission.choices.set(selected_choices)
        submission.save()
        
        return redirect('onlinecourse:exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    max_score = 0
    
    for question in course.question_set.all():
        max_score += question.grade
        selected_ids = [choice.id for choice in submission.choices.filter(question=question)]
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    context['course'] = course
    context['submission'] = submission
    context['total_score'] = total_score
    context['max_score'] = max_score
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
