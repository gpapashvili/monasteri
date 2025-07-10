# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.utils.timezone import now
from datetime import datetime


#########Simplest  lookup tables############
## this simple lookup tables don't need any database modifications
## do not need custom forms
## they will be controlled using django admin

class Units(models.Model):
    label = models.CharField(primary_key=True, max_length=15)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'units'
        ordering = ['label']

    def __str__(self):
        return f"{self.label}"


class Currencies(models.Model):
    label = models.CharField(primary_key=True, max_length=5)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'currencies'
        ordering = ['label']

    def __str__(self):
        return f"{self.label}"


class StoneNames(models.Model):
    label = models.CharField(primary_key=True, max_length=30)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stone_names'
        ordering = ['label']

    def __str__(self):
        return f"{self.label}"


class StoneQualities(models.Model):
    label = models.CharField(primary_key=True, max_length=10)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stone_qualities'
        ordering = ['label']

    def __str__(self):
        return f"{self.label}"


class Genders(models.Model):
    label = models.CharField(primary_key=True, max_length=10)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genders'
        ordering = ['label']

    def __str__(self):
        return f"{self.label}"


class ModelCategories(models.Model):
    label = models.CharField(primary_key=True, max_length=20)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'model_categories'

    def __str__(self):
        return f"{self.label}"


#########Complicated  lookup tables that needs additional id############
## those complicated lookup tables need addition of django_id in database
## do not need custom forms
## will be managed using django admin

class Metals(models.Model):
    metal_name = models.CharField(max_length=20)
    sinji = models.IntegerField()
    # metal_full_name = models.CharField(primary_key=True, max_length=25)
    note = models.TextField(blank=True, null=True)
    django_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'metals'
        ordering = ['metal_name', 'sinji']

    def __str__(self):
        return f"{self.metal_name}-{self.sinji}"


class Stones(models.Model):
    stone_name = models.ForeignKey(StoneNames, models.DO_NOTHING, db_column='stone_name')
    size = models.CharField(max_length=10)
    size_unit = models.ForeignKey('Units', models.DO_NOTHING, db_column='size_unit')
    weight = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    weight_unit = models.ForeignKey('Units', models.DO_NOTHING, db_column='weight_unit', related_name='stones_weight_unit_set', blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    django_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'stones'
        ordering = ['stone_name', 'size']

    def __str__(self):
        return f"{self.stone_name}-{str(self.size)}"


######################functional tables#################
## those functional tables do not need modification in database
## do not need custom forms
## will be managed using django admin

class Catalog(models.Model):
    def catalog_image_path(instance, filename):
        """Method to take model_id and file extension and return path to image file"""
        # Get the file extension
        ext = filename.split('.')[-1]
        # Generate filename as model_id.extension
        filename = f"{instance.model_id}.{ext}"
        # Return the complete path
        return f'catalog/{filename}'

    model_id = models.CharField(primary_key=True, max_length=30)
    creation_date = models.DateField(default=now)
    peaces = models.IntegerField(default=1)
    model_name = models.CharField(max_length=30, blank=True, null=True)
    model_category = models.ForeignKey('ModelCategories', models.DO_NOTHING, db_column='model_category', blank=True, null=True)
    gender = models.ForeignKey('Genders', models.DO_NOTHING, db_column='gender', blank=True, null=True)
    image_location = models.ImageField(upload_to=catalog_image_path, null=True, blank=True)

    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'catalog'
        ordering = ['model_id']

    def __str__(self):
        return f"{self.model_id}"


######################Needs Custom Form#################
## those tables can not be managed from django admin
## do not need database modification as thay will not be managed from django admin
## need custom forms
## can be deleted from here (models.py)

class CatalogStones(models.Model):
    model_id = models.ForeignKey('Catalog', models.CASCADE, db_column='model_id')
    stone_full_name = models.ForeignKey('Stones', models.DO_NOTHING, db_column='stone_full_name')
    quantity = models.DecimalField(max_digits=8, decimal_places=4)
    quantity_unit = models.CharField(max_length=15, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    django_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'catalog_stones'


##########################not yet determined###########################

class Lots(models.Model):
    lot_id = models.AutoField(primary_key=True)
    lot_date = models.DateField()
    metal_full_name = models.ForeignKey('Metals', models.DO_NOTHING, db_column='metal_full_name')
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lots'


class ProductionModels(models.Model):
    pk = models.CompositePrimaryKey('lot_id', 'model_id', 'production_timestamp')
    lot = models.ForeignKey(Lots, models.DO_NOTHING)
    model = models.ForeignKey(Catalog, models.DO_NOTHING)
    production_timestamp = models.DateTimeField()
    weight = models.DecimalField(max_digits=8, decimal_places=4)
    weight_unit = models.CharField(max_length=15, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'production_models'


#################testing

class test_table(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='static/')

    class Meta:
        managed = True
        db_table = 'test_table'