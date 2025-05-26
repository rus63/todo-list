from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


SchemaView = get_schema_view(
    openapi.Info(title="ToDo List API", default_version="v1"),
    public=True,
    authentication_classes=(SessionAuthentication,),
    permission_classes=(permissions.IsAdminUser,),
)
