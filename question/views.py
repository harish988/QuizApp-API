from django.shortcuts import render
from django.http import JsonResponse
from .models import Quiz, Question, Answer
from score.models import UserAnswer, UserScore
from user.models import UserProfile
from rest_framework import status
import json
from rest_framework.decorators import api_view


@api_view(['GET'])
def quiz(request, user_id):
    if(request.method == 'GET'):
        quizzes = Quiz.objects.all()
        response = {}
        body = list()
        for quiz in quizzes:
            scores_present = UserScore.objects.filter(user=user_id, quiz_id=quiz.id).count() > 0
            resume_quiz = UserAnswer.objects.filter(user=user_id, quiz_id=quiz.id).count() < quiz.no_of_question_to_display
            s = {'id': quiz.id, 'name': quiz.name, 'description': quiz.description, 'domain_name': quiz.domain_id.name, 'no_of_questions': quiz.no_of_questions, 'no_of_answers_to_display': quiz.no_of_question_to_display, 'pass_mark': quiz.pass_mark, 'time': quiz.time_in_minutes, 'hardness': quiz.hardness, "attended": scores_present, "resume": resume_quiz}
            body.append(s)
        response['quiz'] = body
        return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def questions_with_answers(request, user_id, quiz_id, question_id=None):
    if(request.method == 'GET'):
        answered_questions = None
        answered_questions_ids = set()
        answered_questions = UserAnswer.objects.filter(user=user_id, quiz_id=quiz_id)
        for answered_question in answered_questions:
            answered_questions_ids.add(answered_question.question_id)
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
                ans = {'id': answer.id,'answer_text': answer.answer_text}
                before_adding_answers.append(ans)
                question_answers[answer.question_id] = before_adding_answers
            else:
                if(answered_questions_ids is not None and answer.question_id in answered_questions_ids):
                    continue
                ans = {'id': answer.id, 'answer_text': answer.answer_text}
                question_answers[answer.question_id] = [ans]
                question_properties[answer.question_id] = {'id': answer.question_id.id, 'question_text': answer.question_id.question_text, 'mark': answer.question_id.mark, 'question_type': answer.question_id.question_type, 'no_of_answers': answer.question_id.no_of_answers}
                question_ids.append(answer.question_id)
        questions = list()
        answered_questions_count = 0
        if(len(answered_questions_ids) > 0):
            answered_questions_count = len(answered_questions_ids)
        response['answered_questions_count'] = answered_questions_count
        for id in question_ids:
            question_properties[id]['answers'] = question_answers[id]
            questions.append(question_properties[id])
        response['question'] = questions
        return JsonResponse(response, status=status.HTTP_200_OK)