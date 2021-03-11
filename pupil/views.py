from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views import generic
from .models import Visual
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from background_task import background
from django.core.files import File
from django.conf import settings
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from pupil.forms import CreateUserForm
from django.contrib import messages
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@background(schedule=0)
def convert(user_id,pk):
    from cv2 import cv2
    import os
    visual = Visual.objects.get(pk=pk)
    if(visual.visual_type=='1'):
        img = cv2.imread(visual.visual.url[1:])
        from tensorflow import keras
        from keras import models
        model = models.load_model("pupil/models/race.h5")
        model_gender = models.load_model("pupil/models/gender.h5")
        face_cascade = cv2.CascadeClassifier('pupil/models/haarcascade_frontalface_default.xml') 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
        import numpy as np
        converted_img = np.copy(img)
        for (x,y,w,h) in faces:
            roi_color = img[y:y+h, x:x+w] 
            roi_color = cv2.resize(roi_color,(250,250))
            roi_color = roi_color.reshape(1,250,250,3)
            pred = model.predict(roi_color)
            race = pred.argmax()
            if(race==4):
                cv2.putText(converted_img,"Others",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
            elif(race==3):
                cv2.putText(converted_img,"Indian",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
            elif(race==2):
                cv2.putText(converted_img,"Asian",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
            elif(race==1):
                cv2.putText(converted_img,"Black",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
            elif(race==0):
                cv2.putText(converted_img,"White",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
            
            roi_color = cv2.resize(img[y:y+h, x:x+w],(200,200))
            roi_color = roi_color.reshape(1,200,200,3)
            pred = model_gender.predict_classes(roi_color)
            if(pred[0][0]==0):
                cv2.putText(converted_img,"Male",(x+int(w/4),y+int(h/4)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
            elif(pred[0][0]==1):
                cv2.putText(converted_img,"Female",(x+int(w/4),y+int(h/4)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
        cv2.imwrite(settings.MEDIA_ROOT+'/converted/'+visual.name+"-converted.jpg",converted_img)
        visual.processes_visual.save(
            visual.name+"-converted.jpg",
            File(open(settings.MEDIA_ROOT+'/converted/'+visual.name+"-converted.jpg",'rb'))
        )
        visual.save()

    elif(visual.visual_type=='2'):
        cap = cv2.VideoCapture(visual.visual.url[1:]) 
        result = cv2.VideoWriter(settings.MEDIA_ROOT+'/converted/'+visual.name+"-converted.avi",  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, (250,250)) 
        while (cap.isOpened()): 
            _, frame = cap.read() 
            img = cv2.resize(frame, (250, 250), fx = 0, fy = 0, 
                                interpolation = cv2.INTER_CUBIC) 
            # img = cv2.imread(visual.visual.url[1:])
            from tensorflow import keras
            from keras import models
            model = models.load_model("pupil/models/race.h5")
            model_gender = models.load_model("pupil/models/gender.h5")
            face_cascade = cv2.CascadeClassifier('pupil/models/haarcascade_frontalface_default.xml') 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
            import numpy as np
            converted_img = np.copy(img)
            for (x,y,w,h) in faces:
                roi_color = img[y:y+h, x:x+w] 
                roi_color = cv2.resize(roi_color,(250,250))
                roi_color = roi_color.reshape(1,250,250,3)
                pred = model.predict(roi_color)
                race = pred.argmax()
                if(race==4):
                    cv2.putText(converted_img,"Others",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
                elif(race==3):
                    cv2.putText(converted_img,"Indian",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
                elif(race==2):
                    cv2.putText(converted_img,"Asian",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
                elif(race==1):
                    cv2.putText(converted_img,"Black",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
                elif(race==0):
                    cv2.putText(converted_img,"White",(x+int(w/4),y+int(h/2)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)

                roi_color = cv2.resize(img[y:y+h, x:x+w],(200,200))
                roi_color = roi_color.reshape(1,200,200,3)
                pred = model_gender.predict_classes(roi_color)
                if(pred[0][0]==0):
                    cv2.putText(converted_img,"Male",(x+int(w/4),y+int(h/4)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA)
                elif(pred[0][0]==1):
                    cv2.putText(converted_img,"Female",(x+int(w/4),y+int(h/4)),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,0),2,cv2.LINE_AA) 
            result.write(converted_img)
        visual.processes_visual.save(
            visual.name+"-converted.avi",
            File(open(settings.MEDIA_ROOT+'/converted/'+visual.name+"-converted.avi",'rb'))
        )
        visual.save()

    return

# @login_required(login_url='login')
class IndexView(View):
    def post(self,request):
        return render(request,'pupil/index.html')
    def get(self,request):
        return render(request,'pupil/index.html')
    
class NewVisual(CreateView):
    model = Visual
    fields = ['name','visual_type','visual']
    success_url = reverse_lazy('pupil:history')

class history(generic.ListView):
    template_name = 'pupil/history.html'
    def get_queryset(self):
        return Visual.objects.all()

class DeleteVisual(DeleteView):
    model = Visual
    success_url = reverse_lazy('pupil:history')

class download(View):
    def post(self,request):
        return redirect(request,'pupil:history')


class ConvertVisual(View):
    model = Visual
    def post(self,request,pk):
        convert(self.request.user.id,pk)
        return redirect('pupil:history')


class RegisterPage(View):
    
    form = CreateUserForm
    def post(self,request):
        # if request.user.is_authenticated:
        #     return redirect('pupil:index')
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created')
            return redirect('login')
        context = {'form':self.form()}
        return render(request,'home/register.html',context)
        
    def get(self,request):
        # if request.user.is_authenticated:
        #     return redirect('pupil:index')
        context = {'form':self.form()}
        return render(request,'home/register.html',context)

class LoginPage(View):

    def post(self,request):
        # if request.user.is_authenticated:
        #     return redirect('pupil:index')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('pupil:index')
        else:
            messages.info(request,'Username or password is Incorrect.')
        context = {}
        return render(request,'home/login.html',context)

    def get(self,request):
        # if request.user.is_authenticated:
        #     return redirect('pupil:index')
        context = {}
        return render(request,'home/login.html',context)