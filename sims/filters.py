import django_filters
from django_filters import CharFilter

from .models import *


class SimFilter(django_filters.FilterSet):
    iccid_filter = CharFilter(field_name='vsim_iccid',lookup_expr='icontains', label='ICCID')
    operator_filter = CharFilter(field_name='operator', lookup_expr='icontains', label='Operator')

    class Meta:
        model = VSIMData
        fields = '__all__'
        exclude = ['vsim_iccid',
                   'objects',
                    'vsim_imsi',
                    'rat',
                    'available',
                    'dispatch',
                    'online_country',
                    'activation',
                    'swapping',
                    'vsim_resource',
                    'in_pool',
                    'plmn_set',
                    'activation_type',
                    'msisdn',
                    'package1',
                    'package2',
                    'bam_status',
                    'bam_code',
                    'bam',
                    'bam_slot',
                    'apn1',
                    'apn2',
                    'apn_new',
                    'district',
                    'flow_type',
                    'cloud_imei',
                    'create_time',
                    'activate_time',
                    'expiry_time',
                    'last_out_time',
                    'certify',
                    'hplmn_support',
                    'grade',
                    'batch_number',
                    'owner',
                    'time_to_reshelve',
                    'remarks',
                    'reserved_area',
                    'reserved_country_or_region',
                    'limit_channel',
                    'number_of_replace_device',
                    'freeze_status',
                    'card_reg_domain',
                    'history']

