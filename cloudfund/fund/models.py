from django.db import models


# A person who joins the chit fund
class Participant(models.Model):
    name = models.CharField(max_length=100)
    wallet_address = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)  # becomes False once they win
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'active' if self.is_active else 'inactive'})"


# One round of the auction
class BiddingRound(models.Model):
    round_number = models.IntegerField()
    is_active = models.BooleanField(default=False)
    winner = models.ForeignKey(
        Participant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="won_rounds"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Round {self.round_number}"


# A single bid placed by a participant in a round
class Bid(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    bidding_round = models.ForeignKey(BiddingRound, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # one bid per participant per round
        unique_together = ('participant', 'bidding_round')

    def __str__(self):
        return f"{self.participant.name} bid {self.bid_amount} in Round {self.bidding_round.round_number}"
