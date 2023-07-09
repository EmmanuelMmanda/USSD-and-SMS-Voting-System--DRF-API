from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from voting.models import Candidate, Position, Results, Vote, Election, Voter
from ussd.utils.sms import SMS
User = get_user_model()
sms = SMS()
from django.db.models import Sum


# handling a signal when a user is created
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Vote)
def update_results(sender, instance, **kwargs):
    # Get the related objects (Election, Position, and Candidate)
    election = 1  # Replace with the actual election ID
    # position = instance.Position

    # get all the positions
    positions = Position.objects.all()

    for position in positions:
        total_votes = Vote.objects.filter(Position=position).count()
        candidates = Candidate.objects.filter(position=position)

        for candidate in candidates:
            vote_count = Vote.objects.filter(
                Position=position,
                candidate=candidate
            ).count()
            vote_percentage = (vote_count / total_votes) * \
                100 if total_votes > 0 else 0

            # Update the results table for the specific candidate and position
            Results.objects.update_or_create(
                election_id=election,
                position=position,
                candidate=candidate,
                defaults={
                    'vote_count': vote_count,
                    'vote_percentage': vote_percentage
                }
            )

# check if election is completed 
@receiver(post_save, sender=Election)
def check_election_status(sender, instance, **kwargs):
    if instance.completed:
        result_sms = "🎉ARUSO Voting 2023 \n🎉"
        result_sms += "Results are out:\n"
        positions = Position.objects.all()

        for position in positions:
            candidates = Candidate.objects.filter(position=position)
            highest_vote_percentage = 0
            highest_vote_candidate = None

            # Retrieve total votes for the position from the Results model
            total_votes = Results.objects.filter(position=position).aggregate(Sum('vote_count'))['vote_count__sum'] or 0

            for candidate in candidates:
                vote_count = Vote.objects.filter(Position=position, candidate=candidate).count()
                vote_percentage = (vote_count / total_votes) * 100 if total_votes > 0 else 0

                if vote_percentage > highest_vote_percentage:
                    highest_vote_percentage = vote_percentage
                    highest_vote_candidate = candidate

            if highest_vote_candidate is not None:
                result_sms += f" {position.title.capitalize()} - {highest_vote_candidate.first_name} {highest_vote_candidate.last_name} ({round(highest_vote_percentage,2)}%),\n"

        result_sms = result_sms.rstrip(',')  # Remove the trailing comma
        print("result sms",result_sms)
        # Get phone numbers of all voters
        voters_phone_numbers = Voter.objects.values_list('phone_number', flat=True)
        print(voters_phone_numbers)
        voters_phone_numbers = list(voters_phone_numbers)
        # # Send the SMS to all voters
        sms.send(voters_phone_numbers, result_sms)

