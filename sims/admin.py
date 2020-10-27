from django.contrib import admin
from . models import Sims, Carrier, Package, VSIMData, Csv, SingleVSIMData
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin


class SimsAdmin(SimpleHistoryAdmin):
    list_display = ("carrier",
                    "country_code",
                    "country_assigned",
                    "iccid",
                    "imsi",
                    "last_modified",
                    "package_name",
                    "status",
                    "issues",
                    "cost_per_gb",
                    "gb_amount"
                    )


class CarrierAdmin(ImportExportModelAdmin):
    list_display = ("name",
                    "email",
                    "phone",
                    "country",
                    "date_created"
                    )


class PackageAdmin(SimpleHistoryAdmin):
    list_display = ("name",
                    "total_data",
                    "daily_average_use",
                    "days_left",
                    )


class VSIMDataAdmin(SimpleHistoryAdmin):
    list_display = ("vsim_iccid",
                    "vsim_imsi",
                    "country_or_region",
                    "operator",
                    "plmn",
                    "online_country",
                    "sim_status",
                    "plmn_set",
                    "package1",
                    "package2",
                    )

class SingleVSIMDataAdmin(SimpleHistoryAdmin):
    list_display = ("svsim_iccid",
                    "svsim_imsi",
                    "countries_or_region",
                    )


class ViewAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Sims, SimsAdmin)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(VSIMData, VSIMDataAdmin)
admin.site.register(SingleVSIMData, SingleVSIMDataAdmin)
admin.site.register(Csv)


