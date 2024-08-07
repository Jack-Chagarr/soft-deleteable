from django.db import models
from model_utils.managers import SoftDeletableQuerySetMixin
from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.db.models.query import QuerySet

class SchoolQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    def exclude_deleted(self):
        return self.filter(is_removed=False)
    
class SchoolManager(models.Manager["School"]):
    def get_queryset(self)-> SchoolQuerySet:
        return SchoolQuerySet(model=self.model, using=self._db).exclude_deleted()

class SchoolDefaultManager(models.Manager["School"]):
    def get_queryset(self)-> SchoolQuerySet:
        return SchoolQuerySet(model=self.model, using=self._db)  

class School(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    objects: SchoolManager = SchoolManager()
    all_objects: SchoolDefaultManager = SchoolDefaultManager()

    def __str__(self):
        return self.name




