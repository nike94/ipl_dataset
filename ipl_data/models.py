from django.db import models


class Matches(models.Model):

    id = models.IntegerField(primary_key=True)
    season = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    toss_winner = models.CharField(max_length=100)
    toss_decision = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    dl_applied = models.CharField(max_length=100)
    winner = models.CharField(max_length=100)
    win_by_runs = models.CharField(max_length=100)
    win_by_wickets = models.CharField(max_length=100)
    player_of_match = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    umpire1 = models.CharField(max_length=100)
    umpire2 = models.CharField(max_length=100)
    umpire3 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Deliveries(models.Model):

    match = models.ForeignKey(Matches, default=0, on_delete=models.CASCADE)
    inning = models.CharField(max_length=100)
    batting_team = models.CharField(max_length=100)
    bowling_team = models.CharField(max_length=100)
    over = models.CharField(max_length=100)
    ball = models.CharField(max_length=100)
    batsman = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)
    bowler = models.CharField(max_length=100)
    is_super_over = models.CharField(max_length=100)
    wide_runs = models.CharField(max_length=100)
    bye_runs = models.CharField(max_length=100)
    legbye_runs = models.IntegerField(default=0)
    noball_runs = models.IntegerField(default=0)
    penalty_runs = models.IntegerField(default=0)
    batsman_runs = models.IntegerField(default=0)
    extra_runs = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    player_dismissed = models.CharField(max_length=100)
    dismissal_kind = models.CharField(max_length=100)
    fielder = models.CharField(max_length=100)

    def __str__(self):
        return str(self.match_id)
