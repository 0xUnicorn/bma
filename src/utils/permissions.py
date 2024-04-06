from utils.schema import ApiMessageSchema, ApiResponseSchema, ObjectPermissionSchema
from guardian.shortcuts import get_user_perms, get_group_perms, get_perms
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission
from users.models import User
import logging

logger = logging.getLogger("bma")

def get_object_permissions_schema(obj, request):
    user = request.user
    user_perms = list(get_user_perms(user, obj))
    user_perms.sort()
    group_perms = list(get_group_perms(user, obj))
    group_perms.sort()
    effective_perms = list(get_perms(user, obj))
    effective_perms.sort()
    return ObjectPermissionSchema(
        user_permissions=user_perms,
        group_permissions=group_perms,
        effective_permissions=effective_perms,
    )


def get_all_user_object_permissions(obj):
    return UserObjectPermission.objects.filter(object_pk=obj.pk)

def get_all_group_object_permissions(obj):
    return GroupObjectPermission.objects.filter(object_pk=obj.pk)
