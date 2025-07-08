from django.contrib import admin
from webpage.models import Currencies

from webpage.models import *

# Register your models here.

#########Simplest  lookup tables############

@admin.register(Units)
class UnitsAdmin(admin.ModelAdmin):
    list_display = ["label", "note"]

@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ["label", "note"]

@admin.register(StoneNames)
class StoneNamesAdmin(admin.ModelAdmin):
    list_display = ["label", "note"]

@admin.register(StoneQualities)
class StoneQualitiesAdmin(admin.ModelAdmin):
    list_display = ["label", "note"]

@admin.register(Genders)
class GendersAdmin(admin.ModelAdmin):
    list_display = ["label", "note"]


@admin.register(ModelCategories)
class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ["label", "note"]

#########Complicated  lookup tables that needs additional id############

@admin.register(Metals)
class MetalsAdmin(admin.ModelAdmin):
    list_display = ['full_name', "metal_name", "sinji", "note"]

    def full_name(self, obj):
        return f"{obj.metal_name}-{obj.sinji}"
    full_name.short_description = "full_name"

@admin.register(Stones)
class StonesAdmin(admin.ModelAdmin):
    list_display = ['full_name', "stone_name", "size", 'size_unit', 'weight', 'weight_unit', "note"]

    def full_name(self, obj):
        return f"{obj.stone_name}-{obj.size}"
    full_name.short_description = "full_name"


######################functional tables#################

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['model_id', "creation_date", "peaces", 'model_name', 'model_category', 'gender', 'image_location', 'note']

# @admin.register(CatalogStones)
# class CatalogStonesAdmin(admin.ModelAdmin):
#     list_display = ['model_id', "stone_full_name", "quantity", 'quantity_unit', 'note']
admin.site.register(CatalogStones)

# @admin.register(Stones)
# class StonesAdmin(admin.ModelAdmin):
#     # list_display = ["stone_name", "size", "size_unit", "weight", "weight_unit"]
#     list_display = ["stone_name", "size", "size_unit", "weight", "weight_unit", "c_stone_full_name"]
#     # readonly_fields = ["stone_full_name"]
#
#     def c_stone_full_name(self, obj):
#         return getattr(obj, 'stone_full_name', None)
#
#     c_stone_full_name.short_description = "stone_full_name"


#################testing
@admin.register(test_table)
class test_tableAdmin(admin.ModelAdmin):
    list_display = ["id", "image"]