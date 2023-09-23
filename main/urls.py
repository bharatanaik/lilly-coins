from audioop import add
from unicodedata import name
from django.urls import path
from main.views import *


json_patterns = [
    path('json/blockchain', get_blockchain)
]

urlpatterns = [

    path('', IndexView.as_view(), name="index"),
    path('signup', RegisterView.as_view(), name="signup"),
    path('account', account, name="account"),
    path('transaction/<str:recv_address>', transaction, name="transaction"),
    path('mining', mining , name="mining"),
    path('blockchain', blockchain, name="blockchain"),
    path('block/<str:block_hash>', blockview, name="block"),
    path('node', TemplateView.as_view(template_name = "main/menu/node.html"), name="node"),
    path('blockchain/add-block', add_block, name="add-block"),
    path('share', TemplateView.as_view(template_name= "main/menu/share.html"), name="share")

]+json_patterns

