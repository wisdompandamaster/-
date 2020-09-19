from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Tag, Task, Done, User
from django.db.models import Q
import os
from django.utils import timezone
from lanzou.api import LanZouCloud
import zipfile
import shutil


# Create your views here.

# TODO fix the try_except
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


# TODO fix the try_except
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


# TODO fix the try_except
# TODO fix the announcement
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


# TODO fix the try_except
def Accept(request):
    task = []
    if request.method == "POST":
        ID = int(request.POST.get('id'))
        print(ID)
        task = Task.objects.filter(id=ID)
        print(task)
        task.update(status=1, acceptTime=timezone.now())
    return JsonResponse({"status": task[0].status})


# TODO fix the try_except
# TODO delete the file_address
def WithDraw(request):
    withdraw = {}
    if request.method == "POST":
        ID = int(request.POST.get('id'))
        file_address = Task.objects.filter(id=ID).fileAddress
        Task.objects.filter(id=ID).delete()
        Done.objects.filter(task__id=ID).delete()
        withdraw = {"msg": "成功撤销id=" + str(ID) + "号事务"}
    return JsonResponse(withdraw)


# TODO fix the try_except
def Zan(request):
    msg = ''
    if request.method == "POST":
        ID = int(request.POST.get('id'))
        department = request.POST.get('department')
        zan = Done.objects.filter(task__id=ID)[0]
        Zan = zan.zanList.split(',')
        print(Zan)
        if department in Zan:
            Zan.remove(department)
            msg = '取消点赞'
        else:
            Zan.append(department)
            msg = '点赞成功'
        zanList = ','.join(Zan)
        zan.zanList = zanList
        zan.save()
    return JsonResponse({"msg": msg})


def Submit(request):
    return None


# TODO fix the try_except
def Start(request):
    return None


def Upload(request):
    lzy = LanZouCloud()
    # !修改为对应的蓝奏云盘的cookies
    cookie_for_lzy = {'ylogin': '1639384',
                      'phpdisk_info': 'AjdXYwxtAzZUZVA4D2FUBwBkAQpZMVw%2BBD8CYQU2ADAENFNnUjYGOVRuBF1ZZVI%2FBjQCMFwzAW8GZgNgVDYENQIwV2IMOwM7VGNQOQ8zVG0AYQEwWTBcOAQ0AjcFZQBkBDRTaFIxBm9UYQRhWQpSOQZjAjhcNgFjBjcDZ1RkBDACNVdt'}
    if lzy.login_by_cookie(cookie_for_lzy) == LanZouCloud.FAILED:
        return JsonResponse({"filename": "蓝奏登录失败", "fileAddress": "上传失败"})
    if lzy.get_dir_list().find_by_name("飞扬人资文件") is None:
        lzy.mkdir(-1, 'fyhr_use', "飞扬人资文件")
    cloud_file_id = lzy.get_dir_list().name_id['fyhr_use']
    if request.method == 'POST':
        return_fileAddress_list = []
        return_fileName_list = []
        files = request.FILES.getlist('file')
        for file in files:
            file_path = os.path.join('test', file.name)
            f = open(file_path, mode='wb')
            for i in file.chunks():
                f.write(i)
            f.close()
            with zipfile.ZipFile(file_path + '.zip', 'w') as z:
                z.write(file_path)

            try:
                code = lzy.upload_file(file_path + '.zip', cloud_file_id,
                                       uploaded_handler=lambda fid, is_file: return_fileAddress_list.append(
                                           lzy.get_file_info_by_id(fid).durl))
                if code == LanZouCloud.FAILED:
                    return JsonResponse({"filename": "文件上传失败", "fileAddress": "上传失败"})
                return_fileName_list.append(file.name)
            except Exception as e:
                print(e)
            finally:
                shutil.rmtree('test')
                os.mkdir('test')
        return JsonResponse({"filename": return_fileName_list, "fileAddress": return_fileAddress_list})
