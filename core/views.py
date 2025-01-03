from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User
from .models import (
    UserProfile, 
    Place, 
    Activity, 
    Wish, 
    Anniversary, 
    Relationship, 
    RelationshipRequest
)
from .forms import (
    UserProfileForm, 
    SignUpForm, 
    PlaceForm, 
    RelationshipForm, 
    ActivityForm, 
    WishForm
)

def home(request):
    """首页视图"""
    context = {}
    if request.user.is_authenticated:
        # 检查用户是否已经在恋爱关系中
        relationship = (Relationship.objects.filter(user1=request.user) | 
                      Relationship.objects.filter(user2=request.user)).first()
        
        if relationship:
            partner = relationship.get_partner(request.user)
            context.update({
                'relationship': relationship,
                'partner': partner
            })
        else:
            # 如果没有恋爱关系，传递表单用于创建
            if request.method == 'POST':
                form = RelationshipForm(request.POST, user=request.user)
                if form.is_valid():
                    partner = User.objects.get(email=form.cleaned_data['partner_email'])
                    # 创建申请而不是直接创建关系
                    RelationshipRequest.objects.create(
                        sender=request.user,
                        receiver=partner,
                        started_at=form.cleaned_data['started_at']
                    )
                    messages.success(request, '恋爱关系申请已发送，等待对方确认')
                    return redirect('home')
            else:
                form = RelationshipForm(user=request.user)
            context['form'] = form
            
    return render(request, 'core/home.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, '注册成功！欢迎加入恋爱记录')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'欢迎回来，{user.username}！')
            return redirect('home')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'core/login.html')

@login_required
def profile(request):
    """个人资料视图"""
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'nickname': request.user.username}
    )
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料已更新')
            return redirect('profile')
    else:
        form = UserProfileForm(
            instance=profile,
            initial={
                'email': request.user.email,
                'relationship_status': profile.get_relationship_status_display()
            }
        )
    
    return render(request, 'core/profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def place_list(request):
    """地点列表视图"""
    places = Place.get_shared_places(request.user)
    return render(request, 'core/place_list.html', {'places': places})

@login_required
def place_create(request):
    """创建地点记录"""
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            messages.success(request, '地点记录已创建')
            return redirect('place_list')
    else:
        form = PlaceForm()
    return render(request, 'core/place_form.html', {'form': form, 'title': '新增地点'})

@login_required
def place_detail(request, pk):
    """地点详情视图"""
    place = get_object_or_404(Place, pk=pk, user=request.user)
    return render(request, 'core/place_detail.html', {'place': place})

@login_required
def activity_list(request):
    """活动列表视图"""
    activities = Activity.get_shared_activities(request.user)
    return render(request, 'core/activity_list.html', {'activities': activities})

@login_required
def activity_create(request):
    """创建活动记录"""
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, '活动记录已创建')
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'core/activity_form.html', {'form': form, 'title': '新增活动'})

@login_required
def activity_detail(request, pk):
    """活动详情视图"""
    activity = get_object_or_404(Activity, pk=pk)
    # 检查是否有权限查看（自己或伴侣的活动）
    if activity.user != request.user:
        relationship = (Relationship.objects.filter(user1=request.user) | 
                      Relationship.objects.filter(user2=request.user)).first()
        if not relationship or relationship.status == 'ended' or \
           activity.user != relationship.get_partner(request.user):
            raise Http404("没有权限查看此活动")
    
    return render(request, 'core/activity_detail.html', {'activity': activity})

@login_required
def wish_list(request):
    """心愿清单视图"""
    wishes = Wish.get_shared_wishes(request.user)
    return render(request, 'core/wish_list.html', {'wishes': wishes})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, '您已成功退出登录')
    return redirect('home')

@login_required
def relationship_create(request):
    """创建恋爱关系"""
    if hasattr(request.user, 'relationship_as_user1') or hasattr(request.user, 'relationship_as_user2'):
        messages.error(request, '您已经在一段关系中了')
        return redirect('profile')

    if request.method == 'POST':
        form = RelationshipForm(request.POST)
        if form.is_valid():
            partner = User.objects.get(email=form.cleaned_data['partner_email'])
            relationship = form.save(commit=False)
            relationship.user1 = request.user
            relationship.user2 = partner
            relationship.save()
            messages.success(request, '恋爱关系已创建')
            return redirect('profile')
    else:
        form = RelationshipForm()
    
    return render(request, 'core/relationship_form.html', {'form': form})

@login_required
def relationship_request_create(request):
    """创建恋爱关系申请"""
    if hasattr(request.user, 'relationship_as_user1') or hasattr(request.user, 'relationship_as_user2'):
        messages.error(request, '您已经在一段关系中了')
        return redirect('home')

    if request.method == 'POST':
        form = RelationshipForm(request.POST, user=request.user)
        if form.is_valid():
            partner = User.objects.get(email=form.cleaned_data['partner_email'])
            # 创建申请而不是直接创建关系
            RelationshipRequest.objects.create(
                sender=request.user,
                receiver=partner,
                started_at=form.cleaned_data['started_at']
            )
            messages.success(request, '恋爱关系申请已发送，等待对方确认')
            return redirect('home')
    else:
        form = RelationshipForm(user=request.user)
    
    return render(request, 'core/relationship_form.html', {'form': form})

@login_required
def relationship_requests(request):
    """查看收到的恋爱关系申请"""
    pending_requests = RelationshipRequest.objects.filter(
        receiver=request.user,
        status='pending'
    )
    return render(request, 'core/relationship_requests.html', {
        'requests': pending_requests
    })

@login_required
def relationship_request_handle(request, request_id):
    """处理恋爱关系申请"""
    rel_request = get_object_or_404(
        RelationshipRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )
    
    action = request.POST.get('action')
    if action == 'accept':
        rel_request.accept()
        messages.success(request, '已接受恋爱关系申请')
    elif action == 'reject':
        rel_request.reject()
        messages.success(request, '已拒绝恋爱关系申请')
    
    return redirect('relationship_requests')

@login_required
def wish_create(request):
    """创建心愿"""
    if request.method == 'POST':
        form = WishForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.user = request.user
            wish.save()
            messages.success(request, '心愿已创建')
            return redirect('wish_list')
    else:
        form = WishForm()
    return render(request, 'core/wish_form.html', {'form': form, 'title': '新增心愿'})

@login_required
def wish_toggle_status(request, pk):
    """切换心愿状态（完成/未完成）"""
    wish = get_object_or_404(Wish, pk=pk)
    if wish.user != request.user:
        relationship = (Relationship.objects.filter(user1=request.user) | 
                      Relationship.objects.filter(user2=request.user)).first()
        if not relationship or relationship.status == 'ended' or \
           wish.user != relationship.get_partner(request.user):
            raise Http404("没有权限修改此心愿")
    
    wish.status = 'completed' if wish.status == 'pending' else 'pending'
    wish.save()
    return redirect('wish_list') 