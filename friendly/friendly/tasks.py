import json
import os
from datetime import datetime

import requests
from api.models import User
from api.serializers import UserSerializer

from friendly import celery_app


@celery_app.task
def set_user_metadata(user_id, ip):
    geo_data = get_geo_data(ip)
    if geo_data:
        country_code = geo_data["country_code"]
        holiday_data = get_holiday_data(country_code)
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(
            user,
            data={"geo_data": geo_data, "created_on_holiday": holiday_data},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
