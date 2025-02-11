from django.urls import path
from triggers.views import (
    trigger_create,
    trigger_delete,
    trigger_list,
    trigger_test,
    trigger_update,
)

urlpatterns = [
    path("", trigger_list, name="trigger_list"),
    path("create/", trigger_create, name="trigger_create"),
    path("<int:pk>/update/", trigger_update, name="trigger_update"),
    path("<int:pk>/delete/", trigger_delete, name="trigger_delete"),
    path("<int:pk>/test/", trigger_test, name="trigger_test"),
]
