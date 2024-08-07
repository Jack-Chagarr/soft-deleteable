from django.db import models
from model_utils.managers import SoftDeletableQuerySetMixin
from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.db.models.query import QuerySet
from .course import Course

class AssignmentQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    def exclude_deleted(self):
        return self.filter(is_removed=False)
    def exclude_deleted_courses(self):
        return self.filter(course__is_removed=False)
    def exclude_deleted_schools(self):
        return self.filter(course__school__is_removed=False)
    
class AssignmentManager(models.Manager["Assignment"]):
    def get_queryset(self)-> AssignmentQuerySet:
        return AssignmentQuerySet(model=self.model, using=self._db).exclude_deleted().exclude_deleted_courses().exclude_deleted_schools()

class AssignmentDefaultManager(models.Manager["Assignment"]):
    def get_queryset(self)-> AssignmentQuerySet:
        return AssignmentQuerySet(model=self.model, using=self._db)  

class Assignment(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment_set')


    objects: AssignmentManager = AssignmentManager()
    all_objects: AssignmentDefaultManager = AssignmentDefaultManager()

    def __str__(self):
        return self.name
