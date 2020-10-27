from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from simple_history.models import HistoricalRecords


class Carrier(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    country = models.CharField(max_length=2, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    countries_or_regions = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=250, blank=True, db_index=True)
    end_time = models.DateField(max_length=200, null=True)
    sum = models.IntegerField(null=True)
    available_sum = models.IntegerField(null=True)
    free_vsim_sum = models.IntegerField(null=True)
    pending_sum = models.IntegerField(null=True)
    reblock_up_sim_sum = models.IntegerField(null=True)
    block_up_sum = models.IntegerField(null=True)
    not_flow_sum = models.IntegerField(null=True)
    unactivate_sum = models.IntegerField(null=True)
    not_service_time_sum = models.IntegerField(null=True)
    package_status_ex_sum = models.IntegerField(null=True)
    used_traffic_gb = models.FloatField(null=True)
    remaining_traffic_gb = models.FloatField(null=True)
    residue_rate = models.FloatField(null=True)
    residue_flow = models.FloatField(null=True)
    near_threshold_sum = models.IntegerField(null=True)
    res_flow_sum = models.CharField(max_length=2, null=True)
    unique_id = models.CharField(max_length=250, null=True, unique=True)
    total_data = models.FloatField(null=True)
    daily_average_use = models.FloatField(null=True)
    days_left = models.FloatField(null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Sims(models.Model):
    carrier = models.ForeignKey(Carrier, null=True, on_delete=models.SET_NULL)
    package_name = models.ForeignKey(Package, null=True, on_delete=models.SET_NULL)
    iccid = models.CharField(max_length=20, unique=True, db_index=True)
    imsi = models.CharField(max_length=20, unique=True)
    country_code = models.CharField(max_length=2)
    country_assigned = models.CharField(max_length=30)
    last_modified = models.DateField(auto_now=True)
    issues = models.CharField(max_length=250, blank=True)
    gb_amount = models.IntegerField()
    cost_per_gb = models.FloatField()
    history = HistoricalRecords()

    choices = (
        ('Enabled', 'Enabled - Online'),
        ('Disabled', 'Disabled - Issue with SIM'),
        ('Pre-Disabled', 'Pre-disabled'),
        ('Blank', 'Blank'),
        ('Cancelled', "Cancelled"),
        ('In Transit', "In Transit")
    )

    status = models.CharField(max_length=20, choices=choices, default="Enabled")

    def __str__(self):
        return self.iccid


class VSIMData(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    country_or_region = models.CharField(max_length=250, blank=True)
    operator = models.CharField(max_length=50, blank=True)
    vsim_imsi = models.CharField(max_length=20, blank=True, unique=True)
    vsim_iccid = models.CharField(max_length=20, blank=True, unique=True, primary_key=True, db_index=True)
    plmn = models.CharField(max_length=250, blank=True)
    rat = models.CharField(max_length=250, blank=True)
    available = models.CharField(max_length=50, blank=True)
    dispatch = models.CharField(max_length=50, blank=True)
    online_country = models.CharField(max_length=2, blank=True)
    sim_status = models.CharField(max_length=50, blank=True)
    activation = models.CharField(max_length=50, blank=True)
    swapping = models.CharField(max_length=5, blank=True)
    vsim_resource = models.CharField(max_length=250, blank=True)
    in_pool = models.CharField(max_length=5, blank=True)
    plmn_set = models.CharField(max_length=250, blank=True)
    activation_type = models.CharField(max_length=250, blank=True)
    msisdn = models.CharField(max_length=20, blank=True)
    package1 = models.CharField(max_length=250, blank=True)
    package2 = models.CharField(max_length=250, blank=True)
    bam_status = models.CharField(max_length=50, blank=True)
    bam_code = models.CharField(max_length=50, blank=True)
    bam = models.CharField(max_length=50, blank=True)
    bam_slot = models.CharField(max_length=50, blank=True)
    apn1 = models.CharField(max_length=50, blank=True)
    apn2 = models.CharField(max_length=50, blank=True)
    apn_new = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    flow_type = models.CharField(max_length=50, blank=True)
    cloud_imei = models.CharField(max_length=50, blank=True)
    create_time = models.DateField(blank=True, null=True)
    activate_time = models.DateField(blank=True, null=True)
    expiry_time = models.DateField(blank=True, null=True)
    last_out_time = models.DateField(blank=True, null=True)
    certify = models.CharField(max_length=50, blank=True)
    hplmn_support = models.CharField(max_length=50, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    owner = models.CharField(max_length=50, blank=True)
    time_to_reshelve = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=50, blank=True)
    reserved_area = models.CharField(max_length=50, blank=True)
    reserved_country_or_region = models.CharField(max_length=50, blank=True)
    limit_channel = models.CharField(max_length=50, blank=True)
    number_of_replace_device = models.CharField(max_length=50, blank=True, null=True)
    freeze_status = models.CharField(max_length=50, blank=True, null=True)
    card_reg_domain = models.CharField(max_length=50, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.vsim_iccid


class SingleVSIMData(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    s_id = models.CharField(max_length=250, blank=True)
    countries_or_region = models.CharField(max_length=250, blank=True)
    svsim_imsi = models.CharField(max_length=20, blank=True, db_index=True)
    package = models.ForeignKey(Package, null=True, on_delete=models.SET_NULL)
    package_type = models.CharField(max_length=50, blank=True)
    initial_flow = models.FloatField(null=True,blank=True)
    remaining_flow = models.FloatField(null=True,blank=True)
    data_plan_threshold = models.IntegerField(null=True,blank=True)
    used_flow = models.FloatField(null=True,blank=True)
    remaining_validity = models.CharField(max_length=20, blank=True)
    limit_speed = models.FloatField(null=True)
    package_status = models.CharField(max_length=20, blank=True)
    expired = models.CharField(max_length=20, blank=True)
    activation_time = models.DateField(blank=True, null=True)
    due_time = models.DateField(blank=True, null=True)
    service_time_zone = models.CharField(max_length=20, blank=True, null=True)
    last_renewed_time = models.DateField(blank=True, null=True)
    next_renewal_time = models.DateField(blank=True, null=True)
    svsim_iccid = models.ForeignKey(VSIMData, null=True, on_delete=models.SET_NULL, db_index=True)
    svsim_msisdn = models.CharField(max_length=20, blank=True)
    renewal_time = models.DateField(blank=True, null=True)
    remark = models.CharField(max_length=20, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.svsim_imsi


class Csv(models.Model):
    file_name = models.FileField(upload_to='sims')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File ID: {self.id}"







