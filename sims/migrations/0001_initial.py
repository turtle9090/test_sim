# Generated by Django 3.1.2 on 2020-10-15 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=2, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='sims')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countries_or_regions', models.CharField(max_length=2, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=250)),
                ('end_time', models.DateField(max_length=200, null=True)),
                ('sum', models.IntegerField(null=True)),
                ('available_sum', models.IntegerField(null=True)),
                ('free_vsim_sum', models.IntegerField(null=True)),
                ('pending_sum', models.IntegerField(null=True)),
                ('reblock_up_sim_sum', models.IntegerField(null=True)),
                ('block_up_sum', models.IntegerField(null=True)),
                ('not_flow_sum', models.IntegerField(null=True)),
                ('unactivate_sum', models.IntegerField(null=True)),
                ('not_service_time_sum', models.IntegerField(null=True)),
                ('package_status_ex_sum', models.IntegerField(null=True)),
                ('used_traffic_gb', models.FloatField(null=True)),
                ('remaining_traffic_gb', models.FloatField(null=True)),
                ('residue_rate', models.FloatField(null=True)),
                ('residue_flow', models.FloatField(null=True)),
                ('near_threshold_sum', models.IntegerField(null=True)),
                ('res_flow_sum', models.CharField(max_length=2, null=True)),
                ('unique_id', models.CharField(max_length=250, null=True, unique=True)),
                ('total_data', models.FloatField(null=True)),
                ('daily_average_use', models.FloatField(null=True)),
                ('days_left', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VSIMData',
            fields=[
                ('country_or_region', models.CharField(blank=True, max_length=250)),
                ('operator', models.CharField(blank=True, max_length=50)),
                ('vsim_imsi', models.CharField(blank=True, max_length=20, unique=True)),
                ('vsim_iccid', models.CharField(blank=True, db_index=True, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('plmn', models.CharField(blank=True, max_length=250)),
                ('rat', models.CharField(blank=True, max_length=250)),
                ('available', models.CharField(blank=True, max_length=50)),
                ('dispatch', models.CharField(blank=True, max_length=50)),
                ('online_country', models.CharField(blank=True, max_length=2)),
                ('sim_status', models.CharField(blank=True, max_length=50)),
                ('activation', models.CharField(blank=True, max_length=50)),
                ('swapping', models.CharField(blank=True, max_length=5)),
                ('vsim_resource', models.CharField(blank=True, max_length=250)),
                ('in_pool', models.CharField(blank=True, max_length=5)),
                ('plmn_set', models.CharField(blank=True, max_length=250)),
                ('activation_type', models.CharField(blank=True, max_length=250)),
                ('msisdn', models.CharField(blank=True, max_length=20)),
                ('package1', models.CharField(blank=True, max_length=250)),
                ('package2', models.CharField(blank=True, max_length=250)),
                ('bam_status', models.CharField(blank=True, max_length=50)),
                ('bam_code', models.CharField(blank=True, max_length=50)),
                ('bam', models.CharField(blank=True, max_length=50)),
                ('bam_slot', models.CharField(blank=True, max_length=50)),
                ('apn1', models.CharField(blank=True, max_length=50)),
                ('apn2', models.CharField(blank=True, max_length=50)),
                ('apn_new', models.CharField(blank=True, max_length=50)),
                ('district', models.CharField(blank=True, max_length=50)),
                ('flow_type', models.CharField(blank=True, max_length=50)),
                ('cloud_imei', models.CharField(blank=True, max_length=50)),
                ('create_time', models.DateField(blank=True, null=True)),
                ('activate_time', models.DateField(blank=True, null=True)),
                ('expiry_time', models.DateField(blank=True, null=True)),
                ('last_out_time', models.DateField(blank=True, null=True)),
                ('certify', models.CharField(blank=True, max_length=50)),
                ('hplmn_support', models.CharField(blank=True, max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50)),
                ('batch_number', models.CharField(blank=True, max_length=50)),
                ('owner', models.CharField(blank=True, max_length=50)),
                ('time_to_reshelve', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50)),
                ('reserved_area', models.CharField(blank=True, max_length=50)),
                ('reserved_country_or_region', models.CharField(blank=True, max_length=50)),
                ('limit_channel', models.CharField(blank=True, max_length=50)),
                ('number_of_replace_device', models.CharField(blank=True, max_length=50, null=True)),
                ('freeze_status', models.CharField(blank=True, max_length=50, null=True)),
                ('card_reg_domain', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SingleVSIMData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.CharField(blank=True, max_length=250)),
                ('countries_or_region', models.CharField(blank=True, max_length=250)),
                ('svsim_imsi', models.CharField(blank=True, db_index=True, max_length=20)),
                ('package_type', models.CharField(blank=True, max_length=50)),
                ('initial_flow', models.FloatField(blank=True, null=True)),
                ('remaining_flow', models.FloatField(blank=True, null=True)),
                ('data_plan_threshold', models.IntegerField(blank=True, null=True)),
                ('used_flow', models.FloatField(blank=True, null=True)),
                ('remaining_validity', models.CharField(blank=True, max_length=20)),
                ('limit_speed', models.FloatField(null=True)),
                ('package_status', models.CharField(blank=True, max_length=20)),
                ('expired', models.CharField(blank=True, max_length=20)),
                ('activation_time', models.DateField(blank=True, null=True)),
                ('due_time', models.DateField(blank=True, null=True)),
                ('service_time_zone', models.CharField(blank=True, max_length=20, null=True)),
                ('last_renewed_time', models.DateField(blank=True, null=True)),
                ('next_renewal_time', models.DateField(blank=True, null=True)),
                ('svsim_msisdn', models.CharField(blank=True, max_length=20)),
                ('renewal_time', models.DateField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=20)),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sims.package')),
                ('svsim_iccid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sims.vsimdata')),
            ],
        ),
        migrations.CreateModel(
            name='Sims',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iccid', models.CharField(db_index=True, max_length=20, unique=True)),
                ('imsi', models.CharField(max_length=20, unique=True)),
                ('country_code', models.CharField(max_length=2)),
                ('country_assigned', models.CharField(max_length=30)),
                ('last_modified', models.DateField(auto_now=True)),
                ('issues', models.CharField(blank=True, max_length=250)),
                ('gb_amount', models.IntegerField()),
                ('cost_per_gb', models.FloatField()),
                ('status', models.CharField(choices=[('Enabled', 'Enabled - Online'), ('Disabled', 'Disabled - Issue with SIM'), ('Pre-Disabled', 'Pre-disabled'), ('Blank', 'Blank'), ('Cancelled', 'Cancelled'), ('In Transit', 'In Transit')], default='Enabled', max_length=20)),
                ('carrier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sims.carrier')),
                ('package_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sims.package')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalVSIMData',
            fields=[
                ('country_or_region', models.CharField(blank=True, max_length=250)),
                ('operator', models.CharField(blank=True, max_length=50)),
                ('vsim_imsi', models.CharField(blank=True, db_index=True, max_length=20)),
                ('vsim_iccid', models.CharField(blank=True, db_index=True, max_length=20)),
                ('plmn', models.CharField(blank=True, max_length=250)),
                ('rat', models.CharField(blank=True, max_length=250)),
                ('available', models.CharField(blank=True, max_length=50)),
                ('dispatch', models.CharField(blank=True, max_length=50)),
                ('online_country', models.CharField(blank=True, max_length=2)),
                ('sim_status', models.CharField(blank=True, max_length=50)),
                ('activation', models.CharField(blank=True, max_length=50)),
                ('swapping', models.CharField(blank=True, max_length=5)),
                ('vsim_resource', models.CharField(blank=True, max_length=250)),
                ('in_pool', models.CharField(blank=True, max_length=5)),
                ('plmn_set', models.CharField(blank=True, max_length=250)),
                ('activation_type', models.CharField(blank=True, max_length=250)),
                ('msisdn', models.CharField(blank=True, max_length=20)),
                ('package1', models.CharField(blank=True, max_length=250)),
                ('package2', models.CharField(blank=True, max_length=250)),
                ('bam_status', models.CharField(blank=True, max_length=50)),
                ('bam_code', models.CharField(blank=True, max_length=50)),
                ('bam', models.CharField(blank=True, max_length=50)),
                ('bam_slot', models.CharField(blank=True, max_length=50)),
                ('apn1', models.CharField(blank=True, max_length=50)),
                ('apn2', models.CharField(blank=True, max_length=50)),
                ('apn_new', models.CharField(blank=True, max_length=50)),
                ('district', models.CharField(blank=True, max_length=50)),
                ('flow_type', models.CharField(blank=True, max_length=50)),
                ('cloud_imei', models.CharField(blank=True, max_length=50)),
                ('create_time', models.DateField(blank=True, null=True)),
                ('activate_time', models.DateField(blank=True, null=True)),
                ('expiry_time', models.DateField(blank=True, null=True)),
                ('last_out_time', models.DateField(blank=True, null=True)),
                ('certify', models.CharField(blank=True, max_length=50)),
                ('hplmn_support', models.CharField(blank=True, max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50)),
                ('batch_number', models.CharField(blank=True, max_length=50)),
                ('owner', models.CharField(blank=True, max_length=50)),
                ('time_to_reshelve', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50)),
                ('reserved_area', models.CharField(blank=True, max_length=50)),
                ('reserved_country_or_region', models.CharField(blank=True, max_length=50)),
                ('limit_channel', models.CharField(blank=True, max_length=50)),
                ('number_of_replace_device', models.CharField(blank=True, max_length=50, null=True)),
                ('freeze_status', models.CharField(blank=True, max_length=50, null=True)),
                ('card_reg_domain', models.CharField(blank=True, max_length=50, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical vsim data',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSingleVSIMData',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('s_id', models.CharField(blank=True, max_length=250)),
                ('countries_or_region', models.CharField(blank=True, max_length=250)),
                ('svsim_imsi', models.CharField(blank=True, db_index=True, max_length=20)),
                ('package_type', models.CharField(blank=True, max_length=50)),
                ('initial_flow', models.FloatField(blank=True, null=True)),
                ('remaining_flow', models.FloatField(blank=True, null=True)),
                ('data_plan_threshold', models.IntegerField(blank=True, null=True)),
                ('used_flow', models.FloatField(blank=True, null=True)),
                ('remaining_validity', models.CharField(blank=True, max_length=20)),
                ('limit_speed', models.FloatField(null=True)),
                ('package_status', models.CharField(blank=True, max_length=20)),
                ('expired', models.CharField(blank=True, max_length=20)),
                ('activation_time', models.DateField(blank=True, null=True)),
                ('due_time', models.DateField(blank=True, null=True)),
                ('service_time_zone', models.CharField(blank=True, max_length=20, null=True)),
                ('last_renewed_time', models.DateField(blank=True, null=True)),
                ('next_renewal_time', models.DateField(blank=True, null=True)),
                ('svsim_msisdn', models.CharField(blank=True, max_length=20)),
                ('renewal_time', models.DateField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sims.package')),
                ('svsim_iccid', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sims.vsimdata')),
            ],
            options={
                'verbose_name': 'historical single vsim data',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSims',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('iccid', models.CharField(db_index=True, max_length=20)),
                ('imsi', models.CharField(db_index=True, max_length=20)),
                ('country_code', models.CharField(max_length=2)),
                ('country_assigned', models.CharField(max_length=30)),
                ('last_modified', models.DateField(blank=True, editable=False)),
                ('issues', models.CharField(blank=True, max_length=250)),
                ('gb_amount', models.IntegerField()),
                ('cost_per_gb', models.FloatField()),
                ('status', models.CharField(choices=[('Enabled', 'Enabled - Online'), ('Disabled', 'Disabled - Issue with SIM'), ('Pre-Disabled', 'Pre-disabled'), ('Blank', 'Blank'), ('Cancelled', 'Cancelled'), ('In Transit', 'In Transit')], default='Enabled', max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('carrier', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sims.carrier')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('package_name', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sims.package')),
            ],
            options={
                'verbose_name': 'historical sims',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPackage',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('countries_or_regions', models.CharField(max_length=2, null=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=250)),
                ('end_time', models.DateField(max_length=200, null=True)),
                ('sum', models.IntegerField(null=True)),
                ('available_sum', models.IntegerField(null=True)),
                ('free_vsim_sum', models.IntegerField(null=True)),
                ('pending_sum', models.IntegerField(null=True)),
                ('reblock_up_sim_sum', models.IntegerField(null=True)),
                ('block_up_sum', models.IntegerField(null=True)),
                ('not_flow_sum', models.IntegerField(null=True)),
                ('unactivate_sum', models.IntegerField(null=True)),
                ('not_service_time_sum', models.IntegerField(null=True)),
                ('package_status_ex_sum', models.IntegerField(null=True)),
                ('used_traffic_gb', models.FloatField(null=True)),
                ('remaining_traffic_gb', models.FloatField(null=True)),
                ('residue_rate', models.FloatField(null=True)),
                ('residue_flow', models.FloatField(null=True)),
                ('near_threshold_sum', models.IntegerField(null=True)),
                ('res_flow_sum', models.CharField(max_length=2, null=True)),
                ('unique_id', models.CharField(db_index=True, max_length=250, null=True)),
                ('total_data', models.FloatField(null=True)),
                ('daily_average_use', models.FloatField(null=True)),
                ('days_left', models.FloatField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical package',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
