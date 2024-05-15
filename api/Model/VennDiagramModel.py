from django.db import models

from django.contrib.auth.models import User

class VennDiagram(models.Model):
    field1 = models.TextField()
    field2 = models.TextField()
    filter = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class TwoVennDiagram(VennDiagram):
    pass
    def __str__(self):
        return f"{self.field1} | {self.field2}"

class ThreeVennDiagram(VennDiagram):
    field3 = models.TextField()
    def __str__(self):
        return f"{self.field1} | {self.field2} | {self.field3}"