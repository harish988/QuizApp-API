from django.shortcuts import render
from django.http import JsonResponse
from .models import UserAnswer, UserScore
from user.models import User
from question.models import Question, Answer
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
            for data in answer:
                user = User.objects.filter(id=data['user_id'])[0]
                question = Question.objects.filter(id=data['question_id'])[0]
                answer = Answer.objects.filter(id=data['answer_id'])[0]
                score = UserAnswer.objects.create(user_id=user, question_id=question, answer_id=answer)
                score.save()
                body.append({"id": score.id, "created_time": datetime.datetime.now()})
            response["answer"] = body
            response["status"] = 201
            response["code"] = "SUCCESS"
            return JsonResponse(response)
        except Exception as e:
            traceback.print_exc()
            response["answer"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            return JsonResponse(response)


