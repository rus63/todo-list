from django.contrib import admin
from django.urls import path, include, re_path

from todo.routers import router as todo_router

from core.swagger import SchemaView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger/", SchemaView.with_ui("swagger", cache_timeout=0), name="swagger_ui"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("", include(todo_router.urls)),
]
