from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from business.models import Tag, Task, Done, User
from django.db.models import Q


# Create your views here.


def DoneList(request):
    if request.method == 'GET':
        currentDepartment = request.GET.get('currentDepartment')
        DoneLists = Done.objects.filter(
            Q(task__startDep=int(currentDepartment)) | Q(task__receiveDep=int(currentDepartment)),
            Q(task__status=1))
        print(DoneLists)
        businessDoneList = []
        for done in DoneLists:
            ID = done.task.id
            content = done.task.tag.content
            color = done.task.tag.color
            status = done.task.status
            startTime = done.task.startTime
            acceptTime = done.task.acceptTime
            deadLine = done.task.deadLine
            startDep = done.task.startDep
            receiveDep = done.task.receiveDep
            introduce = done.task.introduce
            fileAddress = done.task.fileAddress
            fileName = done.task.fileName
            message = done.message
            doneTime = done.doneTime
            doneFileAddress = done.doneFileAddress
            data = {"id": str(ID), "Tag": {"content": content, "color": color}, "status": status,
                    "startTime": startTime, "acceptTime": acceptTime, "deadLine": deadLine,
                    "startDep": startDep, "receiveDep": receiveDep, "introduce": introduce, "fileAddress": fileAddress,
                    "fileName": fileName, "message": message, "doneTime": doneTime, "doneFileAddress": doneFileAddress
                    }
            businessDoneList.append(data)
        return JsonResponse(businessDoneList, safe=False)


def IngList(request):
    return None


def ShowList(request):
    return None


def Accept(request):
    return None


def WithDraw(request):
    return None


def Submit(request):
    return None


def Zan(request):
    return None


def Start(request):
    return None


def Upload(request):
    return None
