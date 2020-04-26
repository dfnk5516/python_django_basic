from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser

def home(request):
    user_id = request.session.get('user')

    if user_id:
        fcuser = Fcuser.objects.get(pk=user_id)
        return HttpResponse(fcuser.username)
    return HttpResponse('Home!')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method =='POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}
        if not(username and password):
            res_data['error'] = '모든 값을 입력해야합니다'
        else:
            fcuser = Fcuser.objects.get(username=username)
            if check_password(password, fcuser.password):
                request.session['user'] = fcuser.id
                # 로그인 처리
                return redirect('/')
            else:
                res_data['error'] = '비밀번호가 틀렸습니다'


        return render(request, 'login.html', res_data)

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username', None) # 기본값 None
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not (username and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            # return HttpResponse('비밀번호가 일치하지 않습니다.')
            res_data['error'] = '비밀번호가 일치하지 않습니다.'
        else:
            fcuser = Fcuser(
                username = username,
                useremail = useremail,
                password = make_password(password)
            )
            fcuser.save()
        print('저장됨')
        return render(request, 'register.html', res_data)