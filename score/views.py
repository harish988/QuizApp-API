from django.shortcuts import render
from django.http import JsonResponse
from .models import UserAnswer, UserScore
from user.models import UserProfile
from question.models import Question, Answer, Quiz
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import traceback
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Sum

@csrf_exempt
@api_view(['POST'])
def user_answer(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        answer = json_data["answer"]
        response = {}
        body = list()
        try:
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            for data in answer:
                user = UserProfile.objects.filter(id=data['user_id'])
                if(user.count() == 0):
                    response["message"] = "User with the given ID("+str(data['user_id'])+") not found"
                    return JsonResponse(response)
                quiz = Quiz.objects.filter(id=data['quiz_id'])
                if(user.count() == 0):
                    response["message"] = "Quiz with the given ID("+str(data['quiz_id'])+") not found"
                    return JsonResponse(response)
                question = Question.objects.filter(id=data['question_id'])
                if(question.count() == 0):
                    response["message"] = "Question with the given ID("+data['question_id']+") not found"
                    return JsonResponse(response)
                answer = Answer.objects.filter(id=data['answer_id'])
                if(answer.count() == 0):
                    response["message"] = "Answer with the given ID("+data['answer_id']+") not found"
                    return JsonResponse(response)
                score = UserAnswer.objects.create(user=user[0], quiz_id=quiz[0], question_id=question[0], answer_id=answer[0])
                score.save()
                body.append({"id": score.id, "created_time": datetime.datetime.now()})
            response["details"] = body
            response["status"] = 201
            response["code"] = "SUCCESS"
            response["message"] = "Answer(s) Submitted Succesfully"
            return JsonResponse(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            response["mesaage"] = traceback.print_exc()
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

@csrf_exempt
@api_view(['POST'])
def submit(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        data = json_data["answer"]
        response = {}
        body = list()
        try:
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            user = UserProfile.objects.filter(id=data['user_id'])
            if(user.count() == 0):
                response["message"] = "User with the given ID("+str(data['user_id'])+") not found"
                return JsonResponse(response)
            quiz = Quiz.objects.filter(id=data['quiz_id'])
            if(quiz.count() == 0):
                response["message"] = "Quiz with the given ID("+str(data['quiz_id'])+") not found"
                return JsonResponse(response)
            user_answers = UserAnswer.objects.filter(user=user[0], quiz_id=quiz[0])
            question_with_marks = {}
            for user_answer in user_answers:
                if(user_answer.question_id.question_type == 'SINGLECHOICE'):
                    if(user_answer.answer_id.is_correct_answer):
                        question_with_marks[user_answer.question_id.id] = user_answer.question_id.mark
                    else:
                        question_with_marks[user_answer.question_id.id] = 0
                elif(user_answer.question_id.question_type == 'MULTIPLECHOICE'):
                    if(user_answer.answer_id.is_correct_answer == 'TRUE'):
                        if(user_answer.question_id.id in question_with_marks):
                            before_insert = question_with_marks[user_answer.question_id.id]
                            before_insert.append(user_answer.question_id.mark)
                            question_with_marks[user_answer.question_id.id] = before_insert
                        else:
                            question_with_marks[user_answer.question_id.id] = [user_answer.question_id.mark]
            total_marks = 0
            for question in question_with_marks.keys():
                single_question_mark = question_with_marks[question]
                if(type(question_with_marks[question]) == type(list())):
                    no_of_correct_answers = Answer.objects.filter(question_id=Question.objects.filter(id=question)[0], is_correct_answer='TRUE').count()
                    single_question_mark = sum(question_with_marks[question])/no_of_correct_answers
                total_marks += single_question_mark
            score = UserScore(user=user[0], quiz_id=quiz[0], score=total_marks, is_pass=(total_marks >= quiz[0].pass_mark))
            score.save()
            body = {'id': score.id, 'created_time': datetime.datetime.now(), 'score': total_marks, 'is_pass': (total_marks >= quiz[0].pass_mark)}
            response["details"] = body
            response["status"] = 201
            response["code"] = "SUCCESS"
            response["message"] = "Score(s) Calculated Succesfully"
            return JsonResponse(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            response["mesaage"] = traceback.print_exc()
            return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def leaderboard(request, user_id, quiz_id, top=10):
    response = {}
    body = list()
    user_scores_count = UserScore.objects.filter(quiz_id=quiz_id).count()
    if(user_scores_count < top):
        top = user_scores_count
    user_scores = UserScore.objects.filter(quiz_id=quiz_id).order_by('-score')
    user_top_scores = user_scores[:top]
    user = None
    for i in range(len(user_scores)):
        if(user_scores[i].user.id == user_id):
            user = {'rank': i, 'first_name': user_scores[i].user.user.first_name, 'last_name': user_scores[i].user.user.last_name, 'year': user_scores[i].user.year.name, 'department': user_scores[i].user.department.name, 'section': user_scores[i].user.section.name, 'score': user_scores[i].score}
    for score in user_top_scores:
        is_current_user = (score.user.id == user_id)
        body.append({'first_name': score.user.user.first_name, 'last_name': score.user.user.last_name, 'year': score.user.year.name, 'department': score.user.department.name, 'section': score.user.section.name, 'score': score.score, 'is_current_user': is_current_user})
    response["leaderboard"] = body
    response["user"] = user
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def generic_leaderboard(request, user_id):
    response = {}
    body = list()
    current_user = None
    users = UserScore.objects.raw("SELECT 1 as id, user_id, SUM(score) as 'score', COUNT(quiz_id_id) as 'quizzes_attended' FROM score_userscore GROUP BY user_id ORDER BY -SUM(score)")
    i = 0
    for user in users:
        if(i == 10):
            break
        is_current_user = user.user_id
        user_spec = UserProfile.objects.filter(id=user.user_id)
        body.append({'first_name': user_spec[0].user.first_name, 'last_name': user_spec[0].user.last_name, 'year': user_spec[0].year.name, 'department': user_spec[0].department.name, 'section': user_spec[0].section.name, 'score': user.score, 'quizzes_attended': user.quizzes_attended, 'is_current_user': is_current_user})
    for user in users:
        i = i+1
        if(user.user_id == user_id):
            user_spec = UserProfile.objects.filter(id=user.user_id)
            current_user = {'rank': i, 'first_name': user_spec[0].user.first_name, 'last_name': user_spec[0].user.last_name, 'year': user_spec[0].year.name, 'department': user_spec[0].department.name, 'section': user_spec[0].section.name, 'score': user.score, 'quizzes_attended': user.quizzes_attended}
    response["leaderboard"] = body
    response["user"] = current_user
    return response
    return JsonResponse(response, status=status.HTTP_200_OK)