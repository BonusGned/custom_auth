from django.contrib import admin

from users.models import CustomUser, Person


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass