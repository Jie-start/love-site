from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('M', '男'), ('F', '女')])
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    @property
    def relationship_status(self):
        """根据恋爱关系自动判断感情状态"""
        relationship = (Relationship.objects.filter(user1=self.user) | 
                      Relationship.objects.filter(user2=self.user)).first()
        if relationship:
            return relationship.status
        return 'single'

    def get_relationship_status_display(self):
        """获取状态的显示文本"""
        status = self.relationship_status
        status_dict = {
            'single': '单身',
            'dating': '恋爱中',
            'married': '已婚',
            'ended': '单身'
        }
        return status_dict.get(status, '单身')

class Relationship(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='relationship_as_user1')
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='relationship_as_user2')
    started_at = models.DateField(verbose_name='恋爱开始日期')
    status = models.CharField(
        max_length=20,
        choices=[
            ('dating', '恋爱中'),
            ('married', '已婚'),
            ('ended', '已结束')
        ],
        default='dating',
        verbose_name='关系状态'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '恋爱关系'
        verbose_name_plural = '恋爱关系'

    def __str__(self):
        return f"{self.user1.username} ❤ {self.user2.username}"

    def get_partner(self, user):
        """获取指定用户的伴侣"""
        return self.user2 if user == self.user1 else self.user1

class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    visit_date = models.DateField()
    description = models.TextField()
    photo = models.ImageField(upload_to='places/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.visit_date}"

    @classmethod
    def get_shared_places(cls, user):
        """获取用户和伴侣共享的所有地点"""
        try:
            relationship = (Relationship.objects.filter(user1=user) | 
                          Relationship.objects.filter(user2=user)).first()
            if relationship and relationship.status != 'ended':
                partner = relationship.get_partner(user)
                return cls.objects.filter(user__in=[user, partner]).order_by('-visit_date')
        except Relationship.DoesNotExist:
            pass
        return cls.objects.filter(user=user).order_by('-visit_date')

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    photo = models.ImageField(upload_to='activities/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_shared_activities(cls, user):
        try:
            relationship = (Relationship.objects.filter(user1=user) | 
                          Relationship.objects.filter(user2=user)).first()
            if relationship and relationship.status != 'ended':
                partner = relationship.get_partner(user)
                return cls.objects.filter(user__in=[user, partner]).order_by('-date')
        except Relationship.DoesNotExist:
            pass
        return cls.objects.filter(user=user).order_by('-date')

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待完成'),
            ('completed', '已完成')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_shared_wishes(cls, user):
        try:
            relationship = (Relationship.objects.filter(user1=user) | 
                          Relationship.objects.filter(user2=user)).first()
            if relationship and relationship.status != 'ended':
                partner = relationship.get_partner(user)
                return cls.objects.filter(user__in=[user, partner]).order_by('-created_at')
        except Relationship.DoesNotExist:
            pass
        return cls.objects.filter(user=user).order_by('-created_at')

class Anniversary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

class RelationshipRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    started_at = models.DateField(verbose_name='恋爱开始日期')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '等待确认'),
            ('accepted', '已接受'),
            ('rejected', '已拒绝')
        ],
        default='pending',
        verbose_name='申请状态'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '恋爱关系申请'
        verbose_name_plural = '恋爱关系申请'

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

    def accept(self):
        """接受恋爱关系申请"""
        if self.status == 'pending':
            # 创建恋爱关系
            relationship = Relationship.objects.create(
                user1=self.sender,
                user2=self.receiver,
                started_at=self.started_at
            )
            self.status = 'accepted'
            self.save()
            return relationship
        return None

    def reject(self):
        """拒绝恋爱关系申请"""
        self.status = 'rejected'
        self.save() 