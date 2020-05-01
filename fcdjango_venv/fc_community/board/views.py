from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from fcuser.models import Fcuser
from tag.models import Tag
from .models import Board
from .forms import BoardForm

# Create your views here.

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')
    return render(request, 'board_detail.html', {'board' : board})

def board_write(request):
    if not request.session.get('user'):
        return redirect('/fcuser/login')
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            fcuser = Fcuser.objects.get(pk=user_id)

            tags = form.cleaned_data['tags'].split(',')

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = fcuser
            board.save()

            for tag in tags: # 태그가 있으면 가져오고 없으면 만든다
                if not tag:
                    continue
                # _tag, created = Tag.objects.get_or_create(name=tag) #name=tag 조건 일치하는게 있으면 가져오고 없으면 생성한다 #writer=writer : 작성자도 같은 사람 #_tag 에는 가져오거나 생성한 객체 반환, created에는 생성한건지 아닌지 여부
                _tag, _ = Tag.objects.get_or_create(name=tag.lstrip()) #두번째 반환값 필요없어서 underbar 처리(python 문법) #lstrip : 왼쪽 공백 제거
                board.tags.add(_tag)

            return redirect('/board/list/')
    else:
        form = BoardForm()
    return render(request, 'board_write.html', {'form' : form})

def board_list(request):
    # all_boards = Board.objects.all().order_by('-id') # - : 역순
    all_boards = Board.objects.all().order_by('id')
    page = int(request.GET.get('p', 1)) # 없으면 1 페이지
    paginator = Paginator(all_boards, 2) # 한페이지 2개씩 나오게 설정

    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards' : boards})