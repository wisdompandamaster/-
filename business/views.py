from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Tag, Task, Done, User
from django.db.models import Q
from django.utils import timezone

# Create your views here.


def DoneList(request):
    if request.method == 'GET':
        currentDepartment = request.GET.get('currentDepartment')
        DoneLists = Done.objects.filter(
            Q(task__startDep=int(currentDepartment)) | Q(task__receiveDep=int(currentDepartment))
            )
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
            doneFileName = done.doneFileName
            data = {"id": str(ID), "Tag": {"content": content, "color": color}, "status": status,
                    "startTime": startTime, "acceptTime": acceptTime, "deadLine": deadLine,
                    "startDep": startDep, "receiveDep": receiveDep, "introduce": introduce, "fileAddress": fileAddress,
                    "fileName": fileName, "message": message, "doneTime": doneTime, "doneFileAddress": doneFileAddress,
                    "doneFileName": doneFileName}
            businessDoneList.append(data)
        return JsonResponse(businessDoneList, safe=False)


def IngList(request):
    if request.method == 'GET':
        currentDepartment = request.GET.get('currentDepartment')
        IngLists = Task.objects.filter(
            Q(startDep=int(currentDepartment)) | Q(receiveDep=int(currentDepartment)),
            status__in=[0, 1, 3]).order_by("deadLine")
        print(IngLists)
        businessIngList = []
        for task in IngLists:
            ID = task.id
            content = task.tag.content
            color = task.tag.color
            status = task.status
            startTime = task.startTime
            acceptTime = task.acceptTime
            deadLine = task.deadLine
            startDep = task.startDep
            receiveDep = task.receiveDep
            introduce = task.introduce
            fileAddress = task.fileAddress
            fileName = task.fileName
            data = {"id": str(ID), "Tag": {"content": content, "color": color}, "status": status,
                    "startTime": startTime, "acceptTime": acceptTime, "deadLine": deadLine,
                    "startDep": startDep, "receiveDep": receiveDep, "introduce": introduce, "fileAddress": fileAddress,
                    "fileName": fileName
                    }
            businessIngList.append(data)
        return JsonResponse(businessIngList, safe=False)


def ShowList(request):
    if request.method == 'GET':
        ShowLists = Done.objects.order_by("doneTime")
        print(ShowLists)
        businessShowList = []
        for done in ShowLists:
            ID = done.task.id
            content = done.task.tag.content
            color = done.task.tag.color
            startTime = done.task.startTime
            startDep = done.task.startDep
            receiveDep = done.task.receiveDep
            message = done.message
            doneTime = done.doneTime
            doneFileAddress = done.doneFileAddress
            doneFileName = done.doneFileName
            zanList = list(map(int, done.zanList.split(",")))
            print(zanList)

            data = {"id": str(ID), "Tag": {"content": content, "color": color},
                    "startTime": startTime, "doneTime": doneTime,
                    "startDep": startDep, "receiveDep": receiveDep, "message": message,
                    "doneFileAddress": doneFileAddress,
                    "doneFileName": doneFileName, "zanList": zanList
                    }
            businessShowList.append(data)
    return JsonResponse(businessShowList, safe=False)


def Accept(request):
    if request.method == "POST":
        ID = int(request.POST.get('id'))
        print(ID)
        task = Task.objects.filter(id=ID)
        print(task)
        task.update(status=1, acceptTime=timezone.now())
    return JsonResponse({"status": task[0].status})


def WithDraw(request):
    if request.method == "POST":
        ID = int(request.POST.get('id'))
        Task.objects.filter(id=ID).delete()
        Done.objects.filter(task__id=ID).delete()
        withdraw = {"msg": "成功撤销id="+str(ID)+"号事务"}
    return JsonResponse(withdraw)


def Submit(request):
    return None


def Zan(request):      # 先把zanList转化为int列表，检测是否部门id在其中，在就删除，不在就添加，再转为字符串
    if request.method == "POST":
        ID = int(request.POST.get('id'))
        department = request.POST.get('department')
        zan = Done.objects.filter(task__id=ID)[0]
        Zan = zan.zanList.split(',')
        print(Zan)
        if department in Zan:            # 赞过就取消，没赞过就点赞
            Zan.remove(department)
        else:
            Zan.append(department)
        zanList = ','.join(Zan)
        zan.zanList = zanList
        zan.save()
       # Zan.update(zanList=Zan[0].zanList + "," + str(department))
    return JsonResponse({"msg": "点赞成功"})


def Start(request):
    return None


def Upload(request):
    return None
