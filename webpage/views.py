from PIL.ImageStat import Global
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import pd_query, create_db_engine, insert_query
from juvel.settings import DATABASES
from sqlalchemy import Engine
from django.template import loader
import os
from django.views.generic import TemplateView, DetailView, ListView

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
            messages.success(request, "You are logged in!")
            # connect to database
            login_db(request)
            return redirect(next_url)
        # if user not valid
        else:
            messages.error(request, "Invalid system login")
            return redirect('login_user')
    # open page if not authenticated or not connected to db
    return render(request, 'login_user.html')


def logout_user(request):
    logout(request)
    if not request.user.is_authenticated:
        messages.success(request, "You Have Been Logged Out...")
    else:
        messages.success(request, f"User {request.user.username} Not Have Been Logged Out...")
    return redirect('login_user')

def home(request):
    # login to db in any view that uses pandas
    login_db(request)
    return render(request, 'home.html')


from .forms import CatalogListForm, ModelCategoryListForm, GenderListForm
from .models import Catalog
def catalog_custom(request):
    # login to db in any view that uses pandas
    login_db(request)

    # various select boxes
    cataloglistform = CatalogListForm()
    modelcategorylistform = ModelCategoryListForm()
    genderlistform = GenderListForm()

    if request.method == 'POST':
        # Filter post dict from empty values
        post_dict = {key:value for key, value in request.POST.dict().items() if value not in [None, '', 'None'] and key != 'na'}
        print(post_dict)
        if 'new_model_id' in post_dict:
            stat = f'INSERT INTO catalog (model_id) VALUES ({post_dict["new_model_id"]})'
            select_model_id = post_dict["new_model_id"]
        elif 'select_model_id' in post_dict:
            select_model_id = post_dict['select_model_id']
        elif 'model_id' in post_dict:
            select_model_id = post_dict['model_id']
        else:
            return redirect(request, 'catalog_custom.html')

        # get model and stones by model_id
        stat = f"""SELECT * FROM catalog WHERE model_id = '{select_model_id}'"""
        model = pd_query(stat, POSTGRESQL_ENGINE)
        stat = f"""SELECT * FROM catalog_stones WHERE model_id = '{select_model_id}'"""
        stones = pd_query(stat, POSTGRESQL_ENGINE)
        # if model is not empty get the first and the only element
        # also define selected value for ModelCategoryListForm and GenderListForm
        if len(model):
            model = model[0]
            modelcategorylistform = ModelCategoryListForm(initial={'model_category': model.model_category})
            genderlistform = GenderListForm(initial={'gender': model.gender})
        else:
            model = dict()
        new_model = {key:value for key, value in request.POST.dict().items() if key in model}
        return render(request, 'catalog_custom.html', { 'cataloglistform': cataloglistform,
                                                  'modelcategorylistform':modelcategorylistform,
                                                  'genderlistform': genderlistform,
                                                  'model': model, 'stones': stones, } )

    return render(request, 'catalog_custom.html', {'cataloglistform': cataloglistform,
                                            'modelcategorylistform': modelcategorylistform,
                                            'genderlistform': genderlistform, } )



def admin_catalog(request):
    return redirect('juveladmin/webpage/catalog/')


def catalog_list(request):
    login_db(request)
    catalogs = Catalog.objects.all()
    stat = """SELECT cs.model_id, cs.stone_full_name, 
                                s.weight * cs.quantity::integer AS total_weight,
                                s.weight, cs.quantity,
                                CONCAT(cs.quantity::integer::text, ' ', cs.quantity_unit) AS quantity_unit
                                FROM catalog AS c
                                LEFT JOIN catalog_stones AS cs ON c.model_id = cs.model_id
                                LEFT JOIN stones AS s on cs.stone_full_name = s.stone_full_name"""
    catalog_stones = pd_query(stat, POSTGRESQL_ENGINE)
    return render(request, 'catalog_list.html', {'catalogs': catalogs, 'catalog_stones': catalog_stones})

from .forms import CatalogForm
def catalog_create(request):
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catalog entry created successfully.')
            return redirect('catalog_list')
    else:
        form = CatalogForm()
    return render(request, 'catalog_form.html', {'form': form, 'action': 'Create'})

def catalog_update(request, model_id):
    catalog = get_object_or_404(Catalog, model_id=model_id)
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES, instance=catalog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catalog entry updated successfully.')
            return redirect('catalog_list')
    else:
        form = CatalogForm(instance=catalog)
    return render(request, 'catalog_form.html', {'form': form, 'action': 'Update'})

def catalog_delete(request, model_id):
    catalog = get_object_or_404(Catalog, model_id=model_id)
    if request.method == 'POST':
        catalog.delete()
        messages.success(request, 'Catalog entry deleted successfully.')
        return redirect('catalog_list')
    return render(request, 'catalog_confirm_delete.html', {'catalog': catalog})


def delete_record(request, record):
    if not (request.user.is_authenticated and isinstance(POSTGRESQL_ENGINE, Engine)):
        messages.success(request, "Logg In to systemc or database")
        return redirect('home')
    else:
        print(record)
        # stat = f'DELETE FROM catalog_stones WHERE model_id={model_id} AND stone_full_name={stone_full_name}'
        # if crt_query(stat, POSTGRESQL_ENGINE):
        # 	messages.success(request, "Record Deleted Successfully...")
        # else:
        # 	messages.success(request, "Record was not deleted...")
        return redirect('home')

def test(request):
    # login to db in any view that uses pandas
    return render(request, 'home.html')
