from django import forms
from .models import Catalog, Stones, ModelCategories, Genders


class CatalogListForm(forms.Form):
    select_model_id = forms.ModelChoiceField(
        queryset=Catalog.objects.all(),
        empty_label="აირჩიე მოდელი",
        widget=forms.Select,
        label='მოდელი',
        required=False,
    )


class ModelCategoryListForm(forms.Form):
    # ... your existing fields ...
    model_category = forms.ModelChoiceField(
        queryset=ModelCategories.objects.all(),
        empty_label="აირჩიე კატეგორია",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='კატეგორია',
        required=False,
    )


class GenderListForm(forms.Form):
    # ... your existing fields ...
    gender = forms.ModelChoiceField(
        queryset=Genders.objects.all(),
        empty_label="აირჩიე სქესი",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='სქესი',
        required=False,
    )


class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = [
            'model_id',
            'creation_date',
            'peaces',
            'model_name',
            'model_category',
            'gender',
            'image_location',
            'note'
        ]
        widgets = {
            'model_id': forms.TextInput(attrs={'class': 'form-control'}),
            'creation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peaces': forms.NumberInput(attrs={'class': 'form-control'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control'}),
            'model_category': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_location': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'model_id': 'Model ID',
            'creation_date': 'Creation Date',
            'peaces': 'Pieces',
            'model_name': 'Model Name',
            'model_category': 'Model Category',
            'gender': 'Gender',
            'image_location': 'Image',
            'note': 'Note'
        }