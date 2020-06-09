from django.shortcuts import render
from django.http import JsonResponse
from .models import Quiz, Question, Answer
from score.models import UserAnswer, UserScore
from user.models import UserProfile
from rest_framework import status
import json
from rest_framework.decorators import api_view
from itertools import chain
from django.utils import timezone
import pytz

@api_view(['GET'])
def quiz(request, user_id):
    if(request.method == 'GET'):
        current_time = timezone.now()
        quizzes = Quiz.objects.filter(quiz_start_time__lte=current_time, quiz_end_time__gte= current_time)
        quizzes_null_start_time = Quiz.objects.filter(quiz_start_time__isnull=True, quiz_end_time__gte= current_time)
        quizzes_null_end_time = Quiz.objects.filter(quiz_start_time__lte=current_time, quiz_end_time__isnull=True)
        quizzes_null_both = Quiz.objects.filter(quiz_start_time__isnull=True, quiz_end_time__isnull=True)
        quizzes_list = list(chain(quizzes, quizzes_null_start_time, quizzes_null_end_time, quizzes_null_both))
        response = {}
        body = list()
        to_be_resumed = list()
        completed = list()
        for quiz in quizzes_list:
            scores_present = UserScore.objects.filter(user=user_id, quiz_id=quiz.id).count() > 0
            questions_answered = UserAnswer.objects.filter(user=user_id, quiz_id=quiz.id).count()
            resume_quiz = False
            if(questions_answered < quiz.no_of_question_to_display and questions_answered != 0):
                resume_quiz =  True
            try:
                url = quiz.quiz_image.url
                splitted_url = url.split("/")
                image_name = splitted_url[-1]
            except:
                image_name = None
            s = {'id': quiz.id, 'name': quiz.name, 'description': quiz.description, 'domain_name': quiz.domain_id.name, 'no_of_questions': quiz.no_of_questions, 'no_of_answers_to_display': quiz.no_of_question_to_display, 'total_mark': quiz.total_marks, 'pass_mark': quiz.pass_mark, 'time': quiz.time_in_minutes, 'hardness': quiz.hardness, "attended": scores_present, "resume": resume_quiz, "image_url":image_name}
            if(scores_present):
                completed.append(s)
            elif(resume_quiz):
                to_be_resumed.append(s)
            else:
                body.append(s)
        response['quiz'] = to_be_resumed + body + completed
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
        questions_count = 0
        for answer in answers:
            try:
                answer_image_name = answer.answer_image.url.split("/")[-1]
            except:
                answer_image_name = None
            ans = {'id': answer.id,'answer_text': answer.answer_text, 'answer_image_name': answer_image_name}
            if(answer.question_id in question_answers):
                before_adding_answers = question_answers[answer.question_id]
                before_adding_answers.append(ans)
                question_answers[answer.question_id] = before_adding_answers
            else:
                questions_count = questions_count + 1
                if(answered_questions_ids is not None and answer.question_id in answered_questions_ids):
                    continue
                try:
                   question_image_name = answer.question_id.question_image.url.split("/")[-1]
                except:
                    question_image_name = None
                question_answers[answer.question_id] = [ans]
                question_properties[answer.question_id] = {'id': answer.question_id.id, 'question_text': answer.question_id.question_text, 'mark': answer.question_id.mark, 'question_type': answer.question_id.question_type, 'no_of_answers': answer.question_id.no_of_answers, 'question_image_name':question_image_name}
                question_ids.append(answer.question_id)
        questions = list()
        answered_questions_count = 0
        if(len(answered_questions_ids) > 0):
            answered_questions_count = len(answered_questions_ids)
        response['answered_questions_count'] = answered_questions_count
        response["count"] = questions_count
        for id in question_ids:
            question_properties[id]['answers'] = question_answers[id]
            questions.append(question_properties[id])
        response['question'] = questions
        return JsonResponse(response, status=status.HTTP_200_OK)