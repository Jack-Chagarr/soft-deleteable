from django.db import models
from model_utils.managers import SoftDeletableQuerySetMixin
from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.db.models.query import QuerySet
from.school import School


class CourseQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    def exclude_deleted(self):
        return self.filter(is_removed=False)
    def exclude_deleted_schools(self):
        return self.filter(school__is_removed=False)
    
class CourseManager(models.Manager["Course"]):
    def get_queryset(self)-> CourseQuerySet:
        return CourseQuerySet(model=self.model, using=self._db).exclude_deleted().exclude_deleted_schools()

class CourseDefaultManager(models.Manager["Course"]):
    def get_queryset(self)-> CourseQuerySet:
        return CourseQuerySet(model=self.model, using=self._db)  

class Course(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='course_set')

    objects: CourseManager = CourseManager()
    all_objects: CourseDefaultManager = CourseDefaultManager()

    def __str__(self):
        return self.name