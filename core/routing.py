from django.urls import re_path

from . import consumers
from student_core.consumers import StudentConsumer

websocket_urlpatterns = [
    re_path(r'ws/test_ws/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/teacher/$', consumers.TeacherConsumer.as_asgi()),
    re_path(r'ws/student/$', StudentConsumer.as_asgi()),
]
