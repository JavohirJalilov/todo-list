from django.http import HttpRequest, JsonResponse
from .models import Task
from django.contrib.auth.models import User
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.contrib.auth import authenticate
from base64 import b64decode

def to_dict(task):
    data = {
        'id': task.id,
        'name': task.name,
        'completed': task.completed,
        'desciption': task.description,
        'created': task.created,
        'updated': task.updated,
        'user': task.user.username
    }
    return data

class Users(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        body = request.body
        # decode body
        decode = body.decode()
        data = json.loads(decode)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.create(
            username = username,
            password= password
        )
        user.save()
        return JsonResponse({"status": "created user!"})


class Tasks(View):
    def get(self, request: HttpRequest, id=None) -> JsonResponse:
        '''get all tasks'''
        try:
            auth = request.headers.get('Authorization').split()[1]
            username, password = b64decode(auth).decode().split(':')
            user = authenticate(username=username, password=password)
        except:
            user = None

        if user is not None:
            if id == None:
                tasks = Task.objects.filter(user=user)
                data = {'tasks': []}

                for task in tasks:
                    data['tasks'].append(to_dict(task))

                return JsonResponse(data)
            else:
                try:
                    task = Task.objects.get(id=id)
                    return JsonResponse(to_dict(task))
                except ObjectDoesNotExist:
                    return JsonResponse({"status": "does not exist"})
        else:
            return JsonResponse({"status": "You are not authorized!"})
        
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Creta todo task
        """
        try:
            auth = request.headers.get('Authorization').split()[1]
            username, password = b64decode(auth).decode().split(':')
            user = authenticate(username=username, password=password)
        except:
            user = None

        if user is not None:
            if request.method == 'POST':
                body = request.body
                # decode body
                decode = body.decode()
                data = json.loads(decode)
                name = data.get('name')
                completed = data.get('completed')
                description = data.get('description')
                user = data.get('user')

                if name == None:
                    return JsonResponse({"status": "name field is required."})
                if description == None:
                    return JsonResponse({"status": "description field is required."})
                
                task = Task.objects.create(
                    name = name,
                    completed = completed,
                    description = description,
                    user = user
                )
                task.save()
                return JsonResponse({"status": "Saccessfuly!"})
            else:
                return JsonResponse({"status": "You need POST request!"})
        else:
            return JsonResponse({"status": "You are not authorized!"})
    
class Delete(View):
    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        """
        delete task
        """
        try:
            auth = request.headers.get('Authorization').split()[1]
            username, password = b64decode(auth).decode().split(':')
            user = authenticate(username=username, password=password)
        except:
            user = None

        if user is not None:
            if request.method == "GET":
                try:
                    # get product from database by id
                    product = Task.objects.get(id=pk, user=user)
                    product.delete()
                    return JsonResponse(to_dict(product))
                except ObjectDoesNotExist:
                    return JsonResponse({"status": "object doesn't exist"})
        else:
            return JsonResponse({"status": "You are not authorized!"})

class Update(View):
    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            auth = request.headers.get('Authorization').split()[1]
            username, password = b64decode(auth).decode().split(':')
            user = authenticate(username=username, password=password)
        except:
            user = None

        if user is not None:
            if request.method == "POST":
                try:
                    task = Task.objects.get(id=pk, user=user)
                except:
                    return JsonResponse({"status": "Does not exist!"})
                
                body = request.body
                # decode body
                decode = body.decode()
                data = json.loads(decode)
                name = data.get('name')
                completed = data.get('completed')
                description = data.get('description')

                task.name = data['name']
                task.description = data['description']
                task.completed = data['completed']
                task.save()
                return JsonResponse({"status": "Saccessfuly updated!"})
        else:
            return JsonResponse({"status": "You are not authorized!"})

class CompletedTasks(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        try:
            auth = request.headers.get('Authorization').split()[1]
            username, password = b64decode(auth).decode().split(':')
            user = authenticate(username=username, password=password)
        except:
            user = None

        if user is not None:
            tasks = Task.objects.filter(completed=True, user=user)
            data = {
                'tasks': []
            }
            for task in tasks:
                data['tasks'].append(to_dict(task))

            return JsonResponse(data)
        else:
            return JsonResponse({"status": "You are not authorized!"})
    
class InCompletedTasks(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        try:
            auth = request.headers.get('Authorization').split()[1]
            username, password = b64decode(auth).decode().split(':')
            user = authenticate(username=username, password=password)
        except:
            user = None

        if user is not None:
            tasks = Task.objects.filter(completed=False)
            data = {
                'tasks': []
            }
            for task in tasks:
                data['tasks'].append(to_dict(task))
            return JsonResponse(data)
        else:
            return JsonResponse({"status": "You are not authorized!"})
