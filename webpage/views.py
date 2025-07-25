from PIL.ImageStat import Global
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import pd_query, create_db_engine, insert_query, crt_query
from juvel.settings import DATABASES
from sqlalchemy import Engine
from django.template import loader
import os
from django.views.generic import TemplateView, DetailView, ListView
from .forms import CatalogListForm, ModelCategoryListForm, GenderListForm

# Create your views here.

POSTGRESQL_ENGINE = None

def login_db(request):
    """Connect to database, required for pandas"""
    global POSTGRESQL_ENGINE

    if isinstance(POSTGRESQL_ENGINE, Engine):
        request.session['db_connected'] = True
    else:
        POSTGRESQL_ENGINE = create_db_engine(request.session.get('username'),  # or DATABASES['default']['USER'],
                                             request.session.get('password'),  # or DATABASES['default']['PASSWORD'],
                                             request.session.get('db_server') or DATABASES['default']['HOST'],
                                             request.session.get('db_name') or DATABASES['default']['NAME'], )
        if not isinstance(POSTGRESQL_ENGINE, Engine):
            request.session['db_connected'] = False
            messages.warning(request, POSTGRESQL_ENGINE)
            return redirect('login_user')
    return POSTGRESQL_ENGINE

def login_user(request):
    # to redirect to requested page after login
    next_url = request.GET.get('next', 'home')
    # create db engine
    login_db(request)
    # if authenticated and database is connected
    if request.user.is_authenticated and request.session.get('db_connected'):
        return redirect(next_url)
    # else if it is POST (you are trying to log in)
    elif request.method == 'POST':
        # for debugging make login automatic later remove DATABASE part
        request.session['username'] = request.POST['username'] #or DATABASES['default']['USER']
        request.session['password'] = request.POST['password'] #or DATABASES['default']['PASSWORD']
        request.session['db_server'] = request.POST['db_server'] or DATABASES['default']['HOST']
        request.session['db_name'] = request.POST['db_name'] or DATABASES['default']['NAME']
        # Authenticate
        user = authenticate(request, username=request.session.get('username'), password=request.session.get('password'))
        # if user is valid
        if user is not None:
            # connect to system
            login(request, user)
            messages.success(request, "ავტორიზაცია წარმატებით დასრულდა!")
            # connect to database
            login_db(request)
            return redirect(next_url)
        # if user not valid
        else:
            messages.error(request, "პრობლემა სისტემაში შესვლისას")
            return redirect('login_user')
    # open page if not authenticated or not connected to db
    return render(request, 'login_user.html')


def logout_user(request):
    logout(request)
    if not request.user.is_authenticated:
        messages.success(request, "სისტემიდან გამოსვლა წარმატებით დასრულდა")
    else:
        messages.success(request, f"მომხმარებელი {request.user.username} არ გამოსულა სისტემიდან")
    return redirect('login_user')

def home(request):
    # login to db in any view that uses pandas
    login_db(request)
    return render(request, 'home.html')


from .models import Catalog
def catalog(request):
    login_db(request)
    all_models = Catalog.objects.all()
    stat = """SELECT cs.model_id, cs.stone_full_name, 
                s.weight * cs.quantity::integer AS total_weight,
                s.weight, cs.quantity,
                CONCAT(cs.quantity::integer::text, ' ', cs.quantity_unit) AS quantity_unit
              FROM catalog AS c
                LEFT JOIN catalog_stones AS cs ON c.model_id = cs.model_id
                LEFT JOIN stones AS s on cs.stone_full_name = s.stone_full_name"""
    all_model_stones = pd_query(stat, POSTGRESQL_ENGINE)
    return render(request, 'model_list.html', {'all_models': all_models, 'all_model_stones': all_model_stones})


from .forms import CatalogForm
def model_create(request):
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'მოდელი წარმატებით დაემატა.')
            return redirect('catalog')
    else:
        form = CatalogForm()
    return render(request, 'model_form.html', {'form': form, 'action': 'Create'})


def model_update(request, model_id):
    model = get_object_or_404(Catalog, model_id=model_id)
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()
            messages.success(request, 'მოდელზე ინფორმაცია წარმატებით განახლდა.')
            return redirect('catalog')
    else:
        form = CatalogForm(instance=model)
    return render(request, 'model_form.html', {'form': form, 'action': 'Update'})


def model_delete(request, model_id):
    model = get_object_or_404(Catalog, model_id=model_id)
    if request.method == 'POST':
        model.delete()
        messages.success(request, 'მოდელი წარმატებით წაიშალა.')
        return redirect('catalog')
    return render(request, 'model_confirm_delete.html', {'model': model})


from .forms import CatalogStonesForm
def model_add_stone(request, model_id):
    if request.method == 'POST':
        form = CatalogStonesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'მოდელზე ქვა წარმატებით დაემატა.')
            return redirect('catalog')
    else:
        form = CatalogStonesForm()
        # will add default value to form when rendered
        form.fields['model_id'].widget.attrs['value'] = model_id
    return render(request, 'model_add_stone.html', {'form': form, 'model_id': model_id, 'action': 'დაამატე'})


from .models import CatalogStones
def model_delete_stone(request, model_id, stone_full_name):
    catalogstones = get_object_or_404(CatalogStones, model_id=model_id, stone_full_name=stone_full_name)
    print(catalogstones)
    if request.method == 'POST':
        catalogstones.delete()
        messages.success(request, 'მოდელზე ქვა წარმატებით წაშლილია.')
        return redirect('catalog')
    return render(request, 'model_delete_stone_confirm.html', {'catalogstones': catalogstones})


from .forms import LotListForm
def model_add_2_lot(request, model_id):
    form = LotListForm()
    image_location = Catalog.objects.get(model_id=model_id).image_location
    if request.method == 'POST':
        login_db(request)
        lot_id = request.POST.get('select_lot_id')
        data = [ {"lot_id": lot_id, "model_id": model_id}, ]
        data_inserted = insert_query('lot_models', data, POSTGRESQL_ENGINE)
        if data_inserted == True:
            messages.success(request, 'მოდელზე ინფორმაცია წარმატებით განახლდა.')
        else:
            messages.error(request, "პრობლემა მოდელის პარტიაში დამატებისას")
        return redirect('catalog')
    return render(request, 'model_add_2_lot.html', {'form': form, 'model_id': model_id, 'image_location':image_location})


from .models import Lots, Metals, Masters
def lot_list(request):
    login_db(request)
    lots = Lots.objects.all()
    # stat = """SELECT l.lot_id, l.lot_date, l.metal_full_name, l.master_full_name, l.note,
    #             lot.model_quantity, lot.price, lot.cost
    #           FROM lots AS l
    #             LEFT JOIN production_models AS pm ON l.lot_id = pm.lot_id"""
    # catalog_stones = pd_query(stat, POSTGRESQL_ENGINE)
    return render(request, 'lot_list.html', {'lots': lots})


from .forms import LotForm
def lot_create(request):
    if request.method == 'POST':
        form = LotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'პარტია წარმატებით დაემატა.')
            return redirect('lot_list')
    else:
        form = LotForm()
    return render(request, 'lot_form.html', {'form': form, 'action': 'შექმენი'})


from .models import LotModels
from collections import Counter
def lot_update(request, lot_id):
    login_db(request)
    lot = get_object_or_404(Lots, lot_id=lot_id)
    stat = f"""SELECT c.image_location, lms.model_id, lms.stone_full_name, lms.quantity, lms.weight
               FROM lot_model_stones AS lms
                LEFT JOIN catalog AS c ON lms.model_id = c.model_id
               WHERE lms.lot_id = {lot_id}"""
    lot_stones = pd_query(stat, POSTGRESQL_ENGINE)
    print(lot_stones)
    # lotmodels = LotModels.objects.filter(lot_id=lot_id)
    lotmodels = get_list_or_404(LotModels, lot_id=lot_id)
    for each in lotmodels:
        model = get_object_or_404(Catalog, model_id=each.model_id)
        image = model.image_location
        each.__setattr__('image', image)
        print(each.image)
    if request.method == 'POST':
        form = LotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            messages.success(request, 'პარტიაზე ინფორმაცია წარმატებით განახლდა.')
            return redirect('lot_list')
    else:
        lotform = LotForm(instance=lot)
    return render(request, 'lot_form.html', {'lotform': lotform, 'action': 'შეცვალე'})


    all_models = Catalog.objects.all()
    stat = """SELECT cs.model_id, cs.stone_full_name, 
                s.weight * cs.quantity::integer AS total_weight,
                s.weight, cs.quantity,
                CONCAT(cs.quantity::integer::text, ' ', cs.quantity_unit) AS quantity_unit
              FROM catalog AS c
                LEFT JOIN catalog_stones AS cs ON c.model_id = cs.model_id
                LEFT JOIN stones AS s on cs.stone_full_name = s.stone_full_name"""
    all_model_stones = pd_query(stat, POSTGRESQL_ENGINE)
    return render(request, 'model_list.html', {'all_models': all_models, 'all_model_stones': all_model_stones})

def lot_delete(request, lot_id):
    lot = get_object_or_404(Lots, lot_id=lot_id)
    if request.method == 'POST':
        lot.delete()
        messages.success(request, 'პარტია წარმატებით წაიშალა.')
        return redirect('lot_list')
    return render(request, 'lot_confirm_delete.html', {'lot': lot})