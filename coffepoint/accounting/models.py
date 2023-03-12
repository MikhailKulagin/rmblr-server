from django.db import models
from django.contrib.auth.models import User


class Shelf(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    number = models.CharField(max_length=32)


class Cup(models.Model):
    """
    Если удаляем юзера, то кружка останется.
    Если удаляем полку, то кружки удаляются.
    """
    id = models.IntegerField(primary_key=True, unique=True)
    owner = models.ForeignKey(User, null=True, db_index=True, on_delete=models.SET_NULL, db_column='owner_id')
    shelf = models.ForeignKey(Shelf, db_index=True, on_delete=models.CASCADE, db_column='shelf_id')
    volume = models.IntegerField()

    def __str__(self):
        return f'{self.volume} мл.'


class Material(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=124)


class CupMaterials(models.Model):
    # Нельзя удалить материал, если есть кружки из него
    # Если кружка удаляется, то связь с материалом тоже удаляется, т.к. в ней не будет смысла и может породить баги
    id = models.IntegerField(primary_key=True, unique=True)
    material = models.ForeignKey(Material, db_index=True, on_delete=models.PROTECT, db_column='material_id')
    cup = models.ForeignKey(Cup, null=True, db_index=True, on_delete=models.CASCADE, db_column='cup_id')

    class Meta:
        db_table = "accounting_cup_materials"
