from django.shortcuts import render
from django.http import JsonResponse
from user.models import UserProfile
from question.models import Quiz
from .models import Rating
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import traceback

@csrf_exempt
def feedback(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        feedback = json_data["feedback"]
        response = {}
        body = list()
        try:
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            for data in feedback:
                user = UserProfile.objects.filter(id=data['user_id'])
                if(user.count() == 0):
                        response["message"] = "User with the given ID("+str(data['user_id'])+") not found"
                        return JsonResponse(response)
                quiz = Quiz.objects.filter(id=data['quiz_id'])
                if(quiz.count() == 0):
                        response["message"] = "Quiz with the given ID("+str(data['quiz_id'])+") not found"
                        return JsonResponse(response)
                rating = Rating.objects.create(user_id=user[0], quiz_id=quiz[0], site_or_quiz=data['site_or_quiz'], rating=data['rating'], comments=data['comments'])
                rating.save()
                body.append({'id': rating.id, 'created_time': datetime.datetime.now()})
            response["details"] = body
            response["message"] = "Rating(s) inserted Succesfully"
            response["status"] = 201
            response["code"] = "SUCCESS"
            return JsonResponse(response)
        except Exception as e:
            traceback.print_exc()
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            response["mesaage"] = traceback.print_exc()
            return JsonResponse(response)
