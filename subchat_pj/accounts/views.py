from datetime import datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        # 회원가입에 필요한 코드
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            year = form.cleaned_data.get("year")
            month = form.cleaned_data.get("month")
            day = form.cleaned_data.get("day")
            birth = year + month + day
            birth = datetime.strptime(birth, "%Y%m%d")
            account = form.save(commit=False)
            account.birth = birth
            account.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/main')

    else:
        # 회원가입폼 리턴
        form = UserForm()

    return render(request, 'accounts/signup.html', {'form': form})
