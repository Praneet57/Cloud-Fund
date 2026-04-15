# CloudFund — Chit Fund Bidding System

A simple Django web app for managing chit fund auctions (bidding rounds).

---

## Quick Setup

```bash
# 1. Clone / copy the project folder
cd cloudfund

# 2. Install Django
pip install django

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. (Optional) Create admin user
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

Open http://127.0.0.1:8000

---

## How It Works

1. Participants join using **Join Fund** (name + wallet address).
2. Agent clicks **Start New Round** from the Dashboard.
3. Each participant places a bid on the **Bidding** page.
4. Agent clicks **End Round** — highest bidder wins the chit.
5. Winner is marked inactive (they've received the fund).
6. Repeat until one participant is left.

---

## Project Structure

```
cloudfund/
├── manage.py
├── cloudfund/          ← project config
│   ├── settings.py
│   └── urls.py
└── fund/               ← main app
    ├── models.py       ← Participant, BiddingRound, Bid
    ├── views.py        ← all view logic
    ├── urls.py         ← URL routing
    ├── admin.py        ← admin registration
    └── templates/
        └── fund/
            ├── base.html
            ├── home.html
            ├── join.html
            ├── participants.html
            └── bidding.html
```

---

## Models

- **Participant** — name, wallet_address, is_active, joined_at
- **BiddingRound** — round_number, is_active, winner (FK), started_at, ended_at
- **Bid** — participant (FK), bidding_round (FK), bid_amount, placed_at

---

## URL Routes

| URL | View | Purpose |
|---|---|---|
| `/` | home | Dashboard |
| `/join/` | join_fund | Join the fund |
| `/participants/` | participants | List all participants |
| `/bidding/` | bidding | Place bids |
| `/start-round/` | start_round | Agent starts a round |
| `/end-round/` | end_round | Agent ends a round |
| `/admin/` | Django admin | DB management |
