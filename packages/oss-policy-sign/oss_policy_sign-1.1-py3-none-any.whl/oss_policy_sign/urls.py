from rest_framework import routers

from oss_policy_sign.views import PolicyAuthViews

router = routers.DefaultRouter()
router.register('auth', PolicyAuthViews)
