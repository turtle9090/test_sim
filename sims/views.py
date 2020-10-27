from django.shortcuts import render, redirect
from django.http import HttpResponse
from sims.models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .filters import SimFilter
from .tasks import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Func, OuterRef, Subquery, Count
from tqdm import tqdm
import numpy as np
import pandas as pd
from datetime import date

#def register(request):
    #form = CreateUserForm()
    #if request.method == "POST":
        #form = CreateUserForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect('login.html')
    #context = {'form': form}
    #return render(request, 'register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    sims_dash = Sims.objects.filter(status="Disabled")
    sims_count = Sims.objects.all()
    package_dash = Package.objects.all()
    carriers_dash = Carrier.objects.all()

    total_sims = sims_count.count()
    total_online = sims_count.filter(status="Enabled").count()
    total_pending = sims_count.filter(status="Disabled").count()

    context_dash = {
        'sims_dash': sims_dash,
        'sims_count': sims_count,
        'carriers_dash': carriers_dash,
        'package_dash': package_dash,
        'total_sims': total_sims,
        'total_online': total_online,
        'total_pending': total_pending
     }
    return render(request, 'dashboard.html', context_dash)


@login_required(login_url='login')
def issues(request):
    return render(request, 'issues.html')


@login_required(login_url='login')
def sims(request):
    simlists = VSIMData.objects.all()
    my_filter = SimFilter(request.GET, queryset=simlists)
    simlists = my_filter.qs
    context = {
        'simlists': simlists,
        'header': 'Sims',
        'my_filter': my_filter,
    }
    return render(request, 'sims.html', context)


@login_required(login_url='login')
def carriers(request, pk):
    carrier = Carrier.objects.get(id=pk)
    carrier_sims = carrier.sims_set.all()
    carrier_sim_count = carrier_sims.count()
    my_filter = SimFilter(request.GET, queryset=carrier_sims)
    carrier_sims = my_filter.qs
    context_carrier = {
        'my_filter': my_filter,
        'carrier': carrier,
        'carrier_sims': carrier_sims,
        'carrier_sim_count': carrier_sim_count,
    }
    return render(request, 'carriers.html', context_carrier)


@login_required(login_url='login')
def new_carrier(request):
    form = CarrierForm()
    if request.method == 'POST':
        form = CarrierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'new_carrier.html', context)


@login_required(login_url='login')
def update_carrier(request, pk):
    update = Carrier.objects.get(id=pk)
    form = CarrierForm(instance=update)
    if request.method == 'POST':
        form = CarrierForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
        'update': update
    }
    return render(request, 'new_carrier.html', context)


@login_required(login_url='login')
def delete_carrier(request, pk):
    delete = Carrier.objects.get(id=pk)
    if request.method == 'POST':
        delete.delete()
        return redirect('/')
    context = {
        'delete': delete
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def new_sim(request, pk):
    carrier = Carrier.objects.get(id=pk)
    #form = SimForm(Sims.objects.none(), instance=carrier)
    form = SimForm(initial={'carrier': carrier})
    if request.method == 'POST':
        form = SimForm(request.POST, instance=carrier)
        #form = SimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'new_sim.html', context)


@login_required(login_url='login')
def update_sim(request, pk):
    update = Sims.objects.get(id=pk)
    form = SimForm(instance=update)
    if request.method == 'POST':
        form = SimForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
        'update': update
    }
    return render(request, 'new_sim.html', context)


@login_required(login_url='login')
def delete_sim(request, pk):
    delete = Sims.objects.get(id=pk)
    if request.method == 'POST':
        delete.delete()
        return redirect('sims')
    context = {
        'delete': delete
    }
    return render(request, 'delete.html', context)


def upload_vsim_mgmt(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            df = pd.read_csv(f, encoding='latin1', error_bad_lines=False, index_col=False, dtype='unicode', sep=',').replace(np.nan, '', regex=True).replace("\t", '', regex=True)
            #print(df)
            row_iter = df.iterrows()

            #vsim_dict = {
               #SingleVSIMData.svsim_iccid: vsim_iccid for vsim_iccid in SingleVSIMData.objects.all()
            #}
            #print(vsim_dict)
            items = []
            for _, row in tqdm(row_iter, total=len(df.index)):
                vsim_data = VSIMData(
                    country_or_region=row['Country or Region	'],
                    operator=row['Operator	'],
                    vsim_imsi=row['IMSI	'],
                    vsim_iccid= row['ICCID	'],
                    online_country=row['Online Country or Region	'],
                    sim_status=row['SIM Status	'],
                    plmn_set=row['PLMN Set	'],
                    package1=row['Package 1	'],
                    package2=row['Package 2	'],

                )
                items.append(vsim_data)

            # vsim_iccids = [row['ICCID	'] for index, row in row_iter]
            # to_update = VSIMData.objects.filter(vsim_iccid__in=vsim_iccidss)
            # bulk_update(to_upate)
            # vsim_iccids = [id in vsim_iccids if id not in to_update]
            # bulk_create(vsim_iccids)
            with VSIMData.objects.bulk_update_or_create_context(['operator','country_or_region', 'vsim_imsi', 'online_country', 'sim_status', 'plmn_set','package1', 'package2'], match_field='vsim_iccid', batch_size=1000) as bulkit:
                for item in tqdm(items):
                    bulkit.queue(item)
            obj.activated = True
            obj.save()
            messages.success(request, 'File upload successful')

    context = {
        'form': form
    }
    return render(request, 'upload.html', context)

def upload_single_vsim_mgmt(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            df = pd.read_csv(f, encoding='latin1', error_bad_lines=False, index_col=False, dtype='unicode',
                             sep=',').replace(np.nan, '', regex=True).replace("\t", '', regex=True)
            df['Due Time\t'] = pd.to_datetime(df['Due Time\t'])
            df['Renewal Time\t'] = pd.to_datetime(df['Renewal Time\t'])
            # print(df)
            row_iter = df.iterrows()
            # for row in row_iter:
            # package_assign, _ = Package.objects.get(name=row[3])
            package_dict = {
                package.name: package for package in Package.objects.all()
            }
            items = []
            for _, row in tqdm(row_iter, total=len(df.index)):
                sing_vsim_data = SingleVSIMData(
                    countries_or_region=row['Countries or Regions	'],
                    svsim_imsi=row['IMSI	'],
                    svsim_iccid=VSIMData.objects.get(vsim_iccid=row['ICCID	']),
                    package=package_dict.get(row['Package	']),
                    remaining_flow=row['Remaining Flow	'],
                    initial_flow=row['Initial Flow	'],
                    used_flow=row['Used Flow	'],
                    due_time=row['Due Time	'],
                    renewal_time=row['Renewal Time	'],
                )
                items.append(sing_vsim_data)
            with SingleVSIMData.objects.bulk_update_or_create_context(
                    ['countries_or_region', 'svsim_imsi', 'package', 'initial_flow', 'remaining_flow', 'used_flow',
                     'due_time', 'renewal_time'], match_field='svsim_iccid', batch_size=1000) as bulkit:
                for item in tqdm(items):
                    bulkit.queue(item)
            obj.activated = True
            obj.save()
            messages.success(request, 'File upload successful')

    context = {
        'form': form
    }
    return render(request, 'upload_single_vsim.html', context)


def upload_package(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            df = pd.read_csv(f, encoding='latin1', error_bad_lines=False, index_col=False, dtype='unicode', sep=',').replace(np.nan,'', regex=True).replace("\t", '', regex=True)
            df['Unique_ID'] = np.where(df["Package name\t"].duplicated(keep=False), df["Package name\t"] + df.groupby("Package name\t").cumcount().add(1).astype(str), df["Package name\t"])
            t = date.today()
            tdiv = t.day
            df['Used traffic(GB)\t'] = df['Used traffic(GB)\t'].astype(float)
            df["Remaining Traffic(GB)\t"] = df["Remaining Traffic(GB)\t"].astype(float)
            df['Total_Data'] = df["Used traffic(GB)	"] + df["Remaining Traffic(GB)	"]
            df['Daily_Avg'] = df["Used traffic(GB)	"] / tdiv
            df['Days_Left'] = df["Remaining Traffic(GB)	"] / df['Daily_Avg']
            df['Days_Left'] = df['Days_Left'].replace(np.inf, 31).replace(np.nan, 31).astype(float).round(2)
            #df['Due Time\t'] = pd.to_datetime(df['Due Time\t'])
            #df['Renewal Time\t'] = pd.to_datetime(df['Renewal Time\t'])
            #print(df)
            row_iter = df.iterrows()
            items = [
                Package(
                    countries_or_regions =row['Countries or Regions	'],
                    name =row['Package name	'],
                    sum =row['sum	'],
                    available_sum =row['avaliableSum	'],
                    free_vsim_sum =row['free Vsim Sum	'],
                    pending_sum =row['pending Sum	'],
                    reblock_up_sim_sum =row['reBlockUpSum	'],
                    block_up_sum =row['reBlockUpSum	'],
                    not_flow_sum =row['notFlowSum	'],
                    unactivate_sum =row['unActivate Card	'],
                    not_service_time_sum =row['unActivate Card	'],
                    package_status_ex_sum =row['unActivate Card	'],
                    used_traffic_gb =row['Used traffic(GB)	'],
                    remaining_traffic_gb =row['Remaining Traffic(GB)	'],
                    unique_id = row['Unique_ID'],
                    total_data = row['Total_Data'],
                    daily_average_use = row['Daily_Avg'],
                    days_left = row['Days_Left'],
                )
                for index, row in row_iter
            ]
            with Package.objects.bulk_update_or_create_context(['name','countries_or_regions','sum','available_sum','free_vsim_sum','pending_sum','reblock_up_sim_sum','block_up_sum','not_flow_sum','unactivate_sum','not_service_time_sum','package_status_ex_sum','used_traffic_gb','remaining_traffic_gb','total_data','daily_average_use','days_left'], match_field='unique_id', batch_size=1000) as bulkit:
                for item in items:
                    bulkit.queue(item)
            obj.activated = True
            obj.save()
            messages.success(request, 'File upload successful')

    context = {
        'form': form
    }
    return render(request, 'upload_package.html', context)

# for index, item in enumerate(items):
#     if index == 0:
#         continue
#     else:

def analytics(request):
    single_vsim_data = SingleVSIMData.objects.all()
    vsim_data = VSIMData.objects.all()
    #package analytics
    package_data = Package.objects.exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month")
    #QA
    package_qa = Package.objects.filter(countries_or_regions='QA').exclude(name__contains='TEST').exclude(name__contains='¼')
    total_qa = Package.objects.filter(countries_or_regions='QA').exclude(name__contains='TEST').exclude(name__contains='¼').aggregate(Sum('total_data'))
    used_qa = Package.objects.filter(countries_or_regions='QA').exclude(name__contains='TEST').exclude(name__contains='¼').aggregate(Sum('used_traffic_gb'))
    remaining_qa = Package.objects.filter(countries_or_regions='QA').exclude(name__contains='TEST').exclude(name__contains='¼').aggregate(Sum('remaining_traffic_gb'))
    avg_qa = Package.objects.filter(countries_or_regions='QA').exclude(name__contains='TEST').exclude(name__contains='¼').aggregate(Sum('daily_average_use'))
    days_qa = Package.objects.filter(countries_or_regions='QA').exclude(name__contains='TEST').exclude(name__contains='¼').aggregate(Sum('days_left'))
    #RO
    package_ro = Package.objects.filter(countries_or_regions='RO').exclude(name__contains='TEST')
    total_ro = Package.objects.filter(countries_or_regions='RO').exclude(name__contains='TEST').aggregate(Sum('total_data'))
    used_ro = Package.objects.filter(countries_or_regions='RO').exclude(name__contains='TEST').aggregate(Sum('used_traffic_gb'))
    remaining_ro = Package.objects.filter(countries_or_regions='RO').exclude(name__contains='TEST').aggregate(Sum('remaining_traffic_gb'))
    avg_ro = Package.objects.filter(countries_or_regions='RO').exclude(name__contains='TEST').aggregate(Sum('daily_average_use'))
    days_ro = Package.objects.filter(countries_or_regions='RO').exclude(name__contains='TEST').aggregate(Sum('days_left'))
    #CL
    package_cl = Package.objects.filter(countries_or_regions='CL').exclude(name__contains='TEST')
    total_cl = Package.objects.filter(countries_or_regions='CL').exclude(name__contains='TEST').aggregate(Sum('total_data'))
    used_cl = Package.objects.filter(countries_or_regions='CL').exclude(name__contains='TEST').aggregate(Sum('used_traffic_gb'))
    remaining_cl = Package.objects.filter(countries_or_regions='CL').exclude(name__contains='TEST').aggregate(Sum('remaining_traffic_gb'))
    avg_cl = Package.objects.filter(countries_or_regions='CL').exclude(name__contains='TEST').aggregate(Sum('daily_average_use'))
    days_cl = Package.objects.filter(countries_or_regions='CL').exclude(name__contains='TEST').aggregate(Sum('days_left'))
    #AF
    package_af = Package.objects.filter(countries_or_regions='AF').exclude(name__contains='TEST')
    total_af = Package.objects.filter(countries_or_regions='AF').exclude(name__contains='TEST').aggregate(Sum('total_data'))
    used_af = Package.objects.filter(countries_or_regions='AF').exclude(name__contains='TEST').aggregate(Sum('used_traffic_gb'))
    remaining_af = Package.objects.filter(countries_or_regions='AF').exclude(name__contains='TEST').aggregate(Sum('remaining_traffic_gb'))
    avg_af = Package.objects.filter(countries_or_regions='AF').exclude(name__contains='TEST').aggregate(Sum('daily_average_use'))
    days_af = Package.objects.filter(countries_or_regions='AF').exclude(name__contains='TEST').aggregate(Sum('days_left'))
    #EU VDF
    package_vdf = Package.objects.filter(name__contains='DHI GB Vodafone EU Roaming')
    total_vdf = Package.objects.filter(name__contains='DHI GB Vodafone EU Roaming').aggregate(Sum('total_data'))
    used_vdf = Package.objects.filter(name__contains='DHI GB Vodafone EU Roaming').aggregate(Sum('used_traffic_gb'))
    remaining_vdf = Package.objects.filter(name__contains='DHI GB Vodafone EU Roaming').aggregate(Sum('remaining_traffic_gb'))
    avg_vdf = Package.objects.filter(name__contains='DHI GB Vodafone EU Roaming').aggregate(Sum('daily_average_use'))
    days_vdf = Package.objects.filter(name__contains='DHI GB Vodafone EU Roaming').exclude(name__contains='TEST').aggregate(Sum('days_left'))
    #EU BE
    package_be = Package.objects.filter(name__contains='DHI Belgium Orange EU Roaming')
    total_be = Package.objects.filter(name__contains='DHI Belgium Orange EU Roaming').aggregate(Sum('total_data'))
    used_be = Package.objects.filter(name__contains='DHI Belgium Orange EU Roaming').aggregate(Sum('used_traffic_gb'))
    remaining_be = Package.objects.filter(name__contains='DHI Belgium Orange EU Roaming').aggregate(Sum('remaining_traffic_gb'))
    avg_be = Package.objects.filter(name__contains='DHI Belgium Orange EU Roaming').aggregate(Sum('daily_average_use'))
    days_be = Package.objects.filter(name__contains='DHI Belgium Orange EU Roaming').aggregate(Sum('days_left'))
    #EU Total
    total_eu = {key: total_be.get(key,0)+total_vdf.get(key,0)
        for key in set(total_be) | set(total_vdf)}
    used_eu = {key: used_be.get(key,0)+used_vdf.get(key,0)
        for key in set(used_be) | set(used_vdf)}
    remaining_eu = {key: remaining_be.get(key,0)+remaining_vdf.get(key,0)
        for key in set(remaining_be) | set(remaining_vdf)}
    avg_eu = {key: avg_be.get(key,0)+avg_vdf.get(key,0)
        for key in set(avg_be) | set(avg_vdf)}
    days_eu = {key: days_be.get(key,0)+days_vdf.get(key,0)
        for key in set(days_be) | set(days_vdf)}
    #FR exclude(name="DHI FR Captive Bouygues-Unlimted/Month")
    package_fr = Package.objects.filter(countries_or_regions='FR').exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month").exclude(name="DHI FR Orange SKI-20GB/14days")
    total_fr = Package.objects.filter(countries_or_regions='FR').exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month").exclude(name="DHI FR Orange SKI-20GB/14days").aggregate(Sum('total_data'))
    used_fr = Package.objects.filter(countries_or_regions='FR').exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month").exclude(name="DHI FR Orange SKI-20GB/14days").aggregate(Sum('used_traffic_gb'))
    remaining_fr = Package.objects.filter(countries_or_regions='FR').exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month").exclude(name="DHI FR Orange SKI-20GB/14days").aggregate(Sum('remaining_traffic_gb'))
    avg_fr = Package.objects.filter(countries_or_regions='FR').exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month").exclude(name="DHI FR Orange SKI-20GB/14days").aggregate(Sum('daily_average_use'))
    days_fr = Package.objects.filter(countries_or_regions='FR').exclude(name__contains='TEST').exclude(name="DHI FR Captive Bouygues-Unlimted/Month").exclude(name="DHI FR Orange SKI-20GB/14days").aggregate(Sum('days_left'))

    #SG exclude
    package_sg = Package.objects.filter(countries_or_regions='SG').exclude(name__contains='TEST')
    total_sg = Package.objects.filter(countries_or_regions='SG').exclude(name__contains='TEST').aggregate(Sum('total_data'))
    used_sg = Package.objects.filter(countries_or_regions='SG').exclude(name__contains='TEST').aggregate(Sum('used_traffic_gb'))
    remaining_sg = Package.objects.filter(countries_or_regions='SG').exclude(name__contains='TEST').aggregate(Sum('remaining_traffic_gb'))
    avg_sg = Package.objects.filter(countries_or_regions='SG').exclude(name__contains='TEST').aggregate(Sum('daily_average_use'))
    days_sg = Package.objects.filter(countries_or_regions='SG').exclude(name__contains='TEST').aggregate(Sum('days_left'))

    context = {
        'package_data': package_data,
        'package_qa': package_qa,
        'total_qa': total_qa,
        'used_qa': used_qa,
        'remaining_qa':remaining_qa,
        'avg_qa': avg_qa,
        'days_qa': days_qa,
        'package_ro': package_ro,
        'total_ro': total_ro,
        'used_ro': used_ro,
        'remaining_ro': remaining_ro,
        'avg_ro': avg_ro,
        'days_ro': days_ro,
        'package_cl': package_cl,
        'total_cl': total_cl,
        'used_cl': used_cl,
        'remaining_cl': remaining_cl,
        'avg_cl': avg_cl,
        'days_cl': days_cl,
        'package_af': package_af,
        'total_af': total_af,
        'used_af': used_af,
        'remaining_af': remaining_af,
        'avg_af': avg_af,
        'days_af': days_af,
        'package_vdf': package_vdf,
        'total_vdf': total_vdf,
        'used_vdf': used_vdf,
        'remaining_vdf': remaining_vdf,
        'avg_vdf': avg_vdf,
        'days_vdf': days_vdf,
        'package_be': package_be,
        'total_be': total_be,
        'used_be': used_be,
        'remaining_be': remaining_be,
        'avg_be': avg_be,
        'days_be': days_be,
        'total_eu': total_eu,
        'used_eu': used_eu,
        'remaining_eu': remaining_eu,
        'avg_eu': avg_eu,
        'days_eu': days_eu,
        'package_fr':package_fr,
        'total_fr': total_fr,
        'used_fr': used_fr,
        'remaining_fr': remaining_fr,
        'avg_fr': avg_fr,
        'days_fr': days_fr,
        'package_sg': package_sg,
        'total_sg': total_sg,
        'used_sg': used_sg,
        'remaining_sg': remaining_sg,
        'avg_sg': avg_sg,
        'days_sg': days_sg,

    }
    return render(request, 'analytics.html', context)


def plmn_sets(request):
    t = date.today()
    tdiv = t.day

    test = [vsim_data['svsim_iccid__plmn_set'] for vsim_data in SingleVSIMData.objects.exclude(svsim_iccid__plmn_set__contains="Ó¢¹úVDF²âÊÔ-PL").filter(svsim_iccid__plmn_set__contains="VDF").values('svsim_iccid__plmn_set').annotate(Count('svsim_iccid__plmn_set'))]

    countries =  [vsim_data['svsim_iccid__plmn_set'] for vsim_data in SingleVSIMData.objects.exclude(svsim_iccid__plmn_set__contains="Ó¢¹úVDF²âÊÔ-PL").filter(svsim_iccid__plmn_set__contains="VDF").values('svsim_iccid__plmn_set').annotate(Count('svsim_iccid__plmn_set'))]
    querysets = []
    for country in countries:
        test1 = SingleVSIMData.objects.select_related('svsim_iccid').filter(svsim_iccid__plmn_set__contains=country)
        package_52 = SingleVSIMData.objects.select_related('svsim_iccid').filter(svsim_iccid__plmn_set__contains=country).filter(package=52)
        package_9 = SingleVSIMData.objects.select_related('svsim_iccid').filter(svsim_iccid__plmn_set__contains=country).filter(package=9)
        querysets.extend([
            {
                'country': country,
                'package': 'Total',
                'data': test1
            },
            {
                'country': country,
                'package': '100GB',
                'data': package_52
            },
            {
                'country': country,
                'package': '50GB',
                'data': package_9
            }
        ])

    items = []
    for queryset in querysets:
        country = queryset['country']
        package = queryset['package']
        queryset = queryset['data']
        intflow = queryset.aggregate(Sum('initial_flow'))['initial_flow__sum']
        intflow = intflow if intflow else 0
        rentflow = queryset.aggregate(Sum('remaining_flow'))['remaining_flow__sum']
        used = queryset.aggregate(Sum('used_flow'))['used_flow__sum']
        used = used if used else 0
        rentflow = rentflow if rentflow else 0
        avg = used / tdiv
        day_avg = rentflow / avg if avg != 0 else 0
        item = {
            'country': country,
            'package': package,
            'total': queryset.count(),
            'enable': queryset.filter(svsim_iccid__sim_status="Enable").count(),
            'disable': queryset.filter(svsim_iccid__sim_status="Disable").count(),
            'pending': queryset.filter(svsim_iccid__sim_status="Pending").count(),
            'pre_disable': queryset.filter(svsim_iccid__sim_status="Pre-Disable").count(),
            'intflow': intflow,
            'rentflow': rentflow,
            'used': used,
            'avg': avg,
            'day_avg': day_avg,
        }
        items.append(item)

    context = {
        'items': items,
    }
    return render(request, 'plmn_sets.html', context)





