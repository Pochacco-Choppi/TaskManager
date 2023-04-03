from django.db import models


class Tag(models):
    title = models.CharField(max_length=255, unique=True)
