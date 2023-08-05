from rest_framework import viewsets
from rest_framework.response import Response
from .generator import OssPolicyAuth
from django.conf import settings


class PolicyAuthViewSet(viewsets.ViewSet):
    def create(self, request):
        access_key_id = settings.OSS_ACCESS_KEY
        access_key_secret = settings.OSS_ACCESS_SECRET
        timeout = getattr(settings, 'OSS_TIMEOUT', 60)
        max_size = getattr(settings, 'OSS_MAX_SIZE', 10)

        oss_policy_auth = OssPolicyAuth(access_key_id,
                                        access_key_secret,
                                        timeout,
                                        max_size)

        return Response(data=oss_policy_auth.get_token())
