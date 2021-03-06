from django import forms
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .froms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    # request:インターネットを介してユーザーから受け取ったすべての情報
    # {}:この中に指定した情報をテンプレートが表示してくれる

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        #instance：代入値と考えればよくinstanceのみはそのオブジェクトでフォームを作成
        # instanceの前に引数がある場合はそのデータを使ってフォームに値を設定する
        # ちなみにこの地点ではまだセーブはしていない
        # instanceがなければ元のものと一緒という事がわからない
        # フォームを保存するとき
        if form.is_valid():
            post = form.save(commit=False)
            # formの時点ではタイトルとテキストしかいじれないため
            # ここで一度セーブをしないでモデルオブジェクトを呼ぶ必要あり
            post.author = request.user
            post.publiished_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
        # このポストを編集するためにただフォームを開く場合
    return render(request,'blog/post_edit.html',{'form':form})