from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Participant, BiddingRound, Bid


def home(request):
    # show a summary: total participants, current round, past rounds
    active_participants = Participant.objects.filter(is_active=True)
    current_round = BiddingRound.objects.filter(is_active=True).first()
    past_rounds = BiddingRound.objects.filter(is_active=False).order_by('-round_number')

    return render(request, 'fund/home.html', {
        'active_participants': active_participants,
        'current_round': current_round,
        'past_rounds': past_rounds,
    })


def join_fund(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        wallet = request.POST.get('wallet_address', '').strip()

        # basic validation
        if not name or not wallet:
            messages.error(request, "Please fill in all fields.")
            return redirect('join')

        # check for duplicate wallet
        if Participant.objects.filter(wallet_address=wallet).exists():
            messages.error(request, "This wallet address is already registered!")
            return redirect('join')

        Participant.objects.create(name=name, wallet_address=wallet)
        messages.success(request, f"Welcome, {name}! You've joined the fund.")
        return redirect('participants')

    return render(request, 'fund/join.html')


def participants(request):
    all_participants = Participant.objects.all().order_by('-joined_at')
    return render(request, 'fund/participants.html', {'participants': all_participants})


def start_round(request):
    if request.method == 'POST':

        # check no round is already running
        if BiddingRound.objects.filter(is_active=True).exists():
            messages.error(request, "A round is already in progress!")
            return redirect('bidding')

        # check there are at least 2 active participants
        active_count = Participant.objects.filter(is_active=True).count()
        if active_count < 2:
            messages.error(request, "Need at least 2 active participants to start a round.")
            return redirect('home')

        # next round number
        last_round = BiddingRound.objects.order_by('-round_number').first()
        next_number = (last_round.round_number + 1) if last_round else 1

        BiddingRound.objects.create(round_number=next_number, is_active=True)
        messages.success(request, f"Round {next_number} has started!")
        return redirect('bidding')

    return redirect('home')


def bidding(request):
    current_round = BiddingRound.objects.filter(is_active=True).first()

    if not current_round:
        messages.info(request, "No active round right now. Start a new round.")
        return render(request, 'fund/bidding.html', {'current_round': None})

    active_participants = Participant.objects.filter(is_active=True)
    bids = Bid.objects.filter(bidding_round=current_round).select_related('participant')

    # quick lookup: participant_id -> bid
    bid_map = {b.participant.id: b for b in bids}

    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        bid_amount = request.POST.get('bid_amount', '').strip()

        try:
            participant = Participant.objects.get(id=participant_id, is_active=True)
        except Participant.DoesNotExist:
            messages.error(request, "Invalid participant.")
            return redirect('bidding')

        if not bid_amount:
            messages.error(request, "Please enter a bid amount.")
            return redirect('bidding')

        try:
            bid_amount = float(bid_amount)
            if bid_amount <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Bid amount must be a positive number.")
            return redirect('bidding')

        # check if already bid this round
        if Bid.objects.filter(participant=participant, bidding_round=current_round).exists():
            messages.warning(request, f"{participant.name} already placed a bid this round.")
            return redirect('bidding')

        Bid.objects.create(
            participant=participant,
            bidding_round=current_round,
            bid_amount=bid_amount
        )
        messages.success(request, f"Bid of {bid_amount} placed for {participant.name}!")
        return redirect('bidding')

    return render(request, 'fund/bidding.html', {
        'current_round': current_round,
        'active_participants': active_participants,
        'bid_map': bid_map,
        'bids': bids,
    })


def end_round(request):
    if request.method == 'POST':
        current_round = BiddingRound.objects.filter(is_active=True).first()

        if not current_round:
            messages.error(request, "No active round to end.")
            return redirect('home')

        bids = Bid.objects.filter(bidding_round=current_round).select_related('participant')

        if not bids.exists():
            messages.error(request, "No bids placed yet. Cannot end round.")
            return redirect('bidding')

        # highest bid wins
        top_bid = bids.order_by('-bid_amount').first()
        winner = top_bid.participant

        current_round.winner = winner
        current_round.is_active = False
        current_round.ended_at = timezone.now()
        current_round.save()

        # winner gets the chit, so they leave the pool
        winner.is_active = False
        winner.save()

        messages.success(request, f"Round {current_round.round_number} ended! Winner: {winner.name}")
        return redirect('home')

    return redirect('home')
