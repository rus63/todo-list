from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.swagger import SchemaView
from todo.admin import todo_list_admin_site
from todo.routers import router as todo_router


urlpatterns = [
    path("admin/", todo_list_admin_site.urls),
    path("swagger/", SchemaView.with_ui("swagger", cache_timeout=0), name="swagger_ui"),
    re_path(
        r"^swagger(?P<format>json|yaml)$",
        SchemaView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(todo_router.urls)),
]
