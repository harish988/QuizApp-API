from django.shortcuts import render
from django.http import JsonResponse
from .models import Quiz, Question, Answer

def quiz(request):
    if(request.method == 'GET'):
        quizzes = Quiz.objects.all()
        response = {}
        body = list()
        for quiz in quizzes:
            s = {'id': quiz.id, 'name': quiz.name, 'description': quiz.description, 'domain_name': quiz.domain_id.name, 'no_of_questions': quiz.no_of_questions, 'no_of_answers_to_display': quiz.no_of_question_to_display, 'pass_mark': quiz.pass_mark, 'time': quiz.time_in_minutes, 'hardness': quiz.hardness}
            body.append(s)
        response['quiz'] = body
        return JsonResponse(response)

def questions_with_answers(request, quiz_id, question_id=None):
    if(request.method == 'GET'):
        if(question_id is None):
            answers = Answer.objects.filter(quiz_id = quiz_id)
        else:
            answers = Answer.objects.filter(quiz_id = quiz_id, question_id=question_id)
        response = {}
        question_ids = list()
        question_answers = {}
        question_properties = {}
        for answer in answers:
            if(answer.question_id in question_answers):
                before_adding_answers = question_answers[answer.question_id]
                ans = {'id': answer.id,'answer_text': answer.answer_text, 'is_correct': answer.is_correct_answer}
                before_adding_answers.append(ans)
                question_answers[answer.question_id] = before_adding_answers
            else:
                ans = {'id': answer.id, 'answer_text': answer.answer_text, 'is_correct': answer.is_correct_answer}
                question_answers[answer.question_id] = [ans]
                question_properties[answer.question_id] = {'id': answer.question_id.id, 'question_text': answer.question_id.question_text, 'mark': answer.question_id.mark, 'question_type': answer.question_id.question_type, 'no_of_answers': answer.question_id.no_of_answers}
                question_ids.append(answer.question_id)
        questions = list()
        for id in question_ids:
            question_properties[id]['answers'] = question_answers[id]
            questions.append(question_properties[id])
        response['question'] = questions
        return JsonResponse(response)