from django.shortcuts import render
from django.http import JsonResponse
from .models import UserAnswer, UserScore
from user.models import UserProfile
from question.models import Question, Answer, Quiz
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import traceback

@csrf_exempt
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
            return JsonResponse(response)
        except Exception as e:
            traceback.print_exc()
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            response["mesaage"] = traceback.print_exc()
            return JsonResponse(response)
            

@csrf_exempt
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
            score = UserScore(user=user[0], quiz_id=quiz[0], score=total_marks)
            score.save()
            body = {'id': score.id, 'created_time': datetime.datetime.now(), 'score': total_marks}
            response["details"] = body
            response["status"] = 201
            response["code"] = "SUCCESS"
            response["message"] = "Score(s) Calculated Succesfully"
            return JsonResponse(response)
        except Exception as e:
            traceback.print_exc()
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            response["mesaage"] = traceback.print_exc()
            return JsonResponse(response)