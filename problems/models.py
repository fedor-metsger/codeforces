
from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='название')

    def __str__(self):
        return f'Tag({self.name})'
        # return self.name

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'теги'


class Problem(models.Model):
    number = models.CharField(max_length=10, unique=True, verbose_name='номер')
    name = models.CharField(max_length=150, verbose_name='название')
    solutions = models.IntegerField(verbose_name='количество решений')
    difficulty = models.IntegerField(verbose_name='сложность')
    tags = models.ManyToManyField(Tag, related_name="теги")

    def __str__(self):
        return f'Problem({self.name})'
        # return self.name

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

class Belonging(models.Model):
    tag = models.ForeignKey(Tag,
                            related_name="belonging",
                            on_delete=models.CASCADE,
                            null=False,
                            blank=False,
                            verbose_name="тэг")
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,
                                verbose_name="задача")


    def __str__(self):
        return f'Belonging({self.name})'
        # return self.name

    class Meta:
        verbose_name = 'принадлежность'
        verbose_name_plural = 'принадлежности'