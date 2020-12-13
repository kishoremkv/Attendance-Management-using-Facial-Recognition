from django.urls import path
from . import views

app_name = "attendance"   
urlpatterns = [
    path('', views.index, name = "index"),
    path('train', views.train_model, name = "train" ),
    path('add_student', views.add_student, name = "add_student"),
    path('start_streaming', views.start_streaming, name = "start_streaming"),
    # path('video_streaming', qviews.video_streaming, name = "video_streaming"),
    path('display',views.display, name = "display"),

]