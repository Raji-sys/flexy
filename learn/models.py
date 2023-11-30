from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # photo=models.ImageField(upload_to='photos/',blank=True, null=True)
    dob=models.DateField(blank=True, null=True)
    phone=models.PositiveIntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.name])
    
    def __str__(self):
        return self.user


class Course(models.Model):
    name=models.CharField(max_length=200, blank=True, null=True)
    student=models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')
    description=models.TextField(blank=True, null=True)
    tutor=models.ForeignKey(User,on_delete=models.CASCADE, related_name='tutor_courses')
    duration=models.CharField(max_length=255, blank=True, null=True)
    date_created=models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('course_detail', args=[self.name])
    
    def __str__(self):
        return self.name

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=255,blank=True,null=True)


class Lesson(models.Model):
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    title=models.CharField(max_length=255,blank=True,null=True)
    text_content=models.TextField(blank=True,null=True)
    file_content=models.FileField(upload_to='lesson_files/',blank=True, null=True)
    # image_content=models.ImageField(upload_to='lesson_images/',blank=True, null=True)


class Enrollment(models.Model):
    student=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    enrollment_date=models.DateField(auto_now_add=True)


class Assessment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=255,blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    date=models.DateField()


class Question(models.Model):
    assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
    text=models.TextField()
    question_type=models.CharField(max_length=50)


class Answer(models.Model):
    question=models.ForeignKey(Assessment, on_delete=models.CASCADE)
    text=models.TextField()
    correct=models.BooleanField()


class Remark(models.Model):
    enrollment=models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
    grade=models.DecimalField(max_digits=5, decimal_places=2)
    comments=models.TextField()


class Certificate(models.Model):
    student=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date=models.DateField(auto_now_add=True)
