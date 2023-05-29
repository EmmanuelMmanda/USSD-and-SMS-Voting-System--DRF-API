from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from voting.models import Candidate, Position, Results, Vote, Election

User = get_user_model()


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
