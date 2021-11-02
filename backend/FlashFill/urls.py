from django.urls.conf import include
from rest_framework import routers
from django.urls import path
from .views import *
from django.conf.urls import url

router = routers.DefaultRouter()
                                  

#router.register(r'FlashExs',FlashFillExecutionList,basename='FlashExs')
router.register(r'FlashFreeLoopExs',FlashFillExecutionFreeLoopList,basename='FlashFreeLoopExs')



#urlpatterns = router.urls

urlpatterns = [
    #url(r'sessions/', FlashFillExecutionList.as_view()),
    url(r'sessions/', FlashFillExecutionFreeLoopList.as_view()),

]
urlpatterns += router.urls


