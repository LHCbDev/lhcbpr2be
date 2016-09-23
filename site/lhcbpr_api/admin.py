from django.contrib import admin
from lhcbpr_api import models


class ApplicationAdmin(admin.ModelAdmin):
    pass

class OptionAdmin(admin.ModelAdmin):
    pass

class ExecutableAdmin(admin.ModelAdmin):
    pass

# class ApplicationVersionAdmin(admin.ModelAdmin):
#     pass

admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.Option, OptionAdmin)
admin.site.register(models.Executable, ExecutableAdmin)
#admin.site.register(models.ApplicationVersion, ApplicationVersionAdmin)
