from django.contrib import admin
from .models import Participant, BiddingRound, Bid

# Register so you can view everything in /admin too
admin.site.register(Participant)
admin.site.register(BiddingRound)
admin.site.register(Bid)
