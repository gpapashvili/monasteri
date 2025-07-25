from django.contrib import admin
from webpage.models import *

# admin sites customization
admin.site.site_title = "Juvel admin page"
admin.site.site_header = "Juvel administration"
admin.site.index_title = "Site administration"

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


@admin.register(Masters)
class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ["master_full_name", "note"]

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

@admin.register(Lots)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['lot_id', "lot_date", "metal_full_name", 'master_full_name', 'note']

@admin.register(LotModels)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['lot_id', "model_id", "production_timestamp", 'weight', 'weight_unit', 'note']

##########################not yet determined###########################
