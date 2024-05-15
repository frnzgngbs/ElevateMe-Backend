from django.db import models
from django.contrib.auth.models import User
from .VennDiagramModel import TwoVennDiagram, ThreeVennDiagram
class ProblemStatementModel(models.Model):
    statement = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TwoVennProblemStatementModel(ProblemStatementModel):
    venn = models.ForeignKey(TwoVennDiagram, on_delete=models.CASCADE)


class ThreeVennProblemStatementModel(ProblemStatementModel):
    field3 = models.TextField(null=False)
    venn = models.ForeignKey(ThreeVennDiagram, on_delete=models.CASCADE)
