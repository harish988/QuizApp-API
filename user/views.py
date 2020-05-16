from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from user.models import UserProfile, Year, Department, Section
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import traceback

@csrf_exempt
def user(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        user = json_data["user"]
        response = {}
        body = list()
        try:
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            for data in user:
                user = User.objects.create_user(username=data["roll_no"], email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
                user.save()
                year = Year.objects.filter(name=data["year"])
                if(year.count() == 0):
                    response["message"] = "Year with the given Name("+str(data['year'])+") not found"
                    return JsonResponse(response)
                department = Department.objects.filter(name=data["department"])
                if(department.count() == 0):
                    response["message"] = "Department with the given Name("+str(data['department'])+") not found"
                    return JsonResponse(response)
                section = Section.objects.filter(name=data["section"])
                if(section.count() == 0):
                    response["message"] = "Section with the given Name("+str(data['section'])+") not found"
                    return JsonResponse(response)
                user_profile = UserProfile.objects.create(user=user, year=year[0], department=department[0], section=section[0])
                user_profile.save()
                body.append({"id": user_profile.id, "created_time": datetime.datetime.now()})
            response["details"] = body
            response["status"] = 201
            response["code"] = "SUCCESS"
            response["message"] = "User(s) Inserted Succesfully"
            return JsonResponse(response)
        except Exception as e:
            traceback.print_exc()
            response["details"] = {}
            response["status"] = 400
            response["code"] = "FAILED"
            response["mesaage"] = traceback.print_exc()
            return JsonResponse(response)

@csrf_exempt
def login(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        user_data = json_data["user"]
        response = {}
        user = User.objects.filter(username=user_data["username"])
        if(user.count() > 0):
            response["password"] = user[0].check_password(user_data["password"])
            if(response["password"]):
                response["message"] = "Password Matched"
            else:
                response["message"] = "Password Mismatched"
        else:
            response["password"] = False
            response["message"] = "Invalid UserName"
        return JsonResponse(response)

@csrf_exempt
def unique_username(request):
    if(request.method == 'POST'):
        json_data = json.loads(request.body)
        response = {"unique": True}
        count = User.objects.filter(username=json_data["roll_no"]).count()
        if(count > 0):
            response["unique"] = False
        return JsonResponse(response)