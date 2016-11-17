from django.db import models


class Lcc(models.Model):
    value = models.CharField(max_length=100)
    main_class_start = models.IntegerField(db_index=True)
    sub_class_start = models.IntegerField(db_index=True, null=True)
    main_class_end = models.IntegerField(db_index=True)
    sub_class_end = models.IntegerField(db_index=True, null=True)

    year = models.CharField(max_length=6, null=True, blank=True)
    author = models.CharField(max_length=10, null=True, blank=True)
    regal = models.IntegerField(null=True, blank=True)
