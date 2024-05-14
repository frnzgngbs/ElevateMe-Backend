from django.db import models
from django.contrib.auth.models import User
from .VennDiagram import TwoVennDiagram, ThreeVennDiagram
class ProblemStatement(models.Model):
    statement = models.TextField()
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    def to_dict(self):
        return {
            'id': self.id,
            'statement': self.statement,
            'user_fk': self.user_fk.username  # Assuming you want the username, change it accordingly
        }
class TwoProblemStatement(ProblemStatement):
    venn_fk = models.ForeignKey(TwoVennDiagram, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.to_dict())

class ThreeProblemStatement(ProblemStatement):
    venn_fk = models.ForeignKey(ThreeVennDiagram, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.to_dict())