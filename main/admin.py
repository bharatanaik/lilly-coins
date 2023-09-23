from django.contrib import admin
from main.models import Block, LillyUser, Transaction
from django.contrib.auth.admin import UserAdmin

from .forms import LillyUserCreationForm, LillyUserChangeForm

@admin.register(LillyUser)
class LillyUserAdmin(UserAdmin):
    add_form = LillyUserCreationForm
    form = LillyUserChangeForm
    model = LillyUser
    list_display = ['username','address', 'amount']
    fieldsets = UserAdmin.fieldsets + (
            ("Lilly Coins", {
                'fields': ('private_key', 'public_key', 'amount')
                    }),
                ) 


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender','reciever', 'amount')



@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("hash", "miner", "timestamp")


