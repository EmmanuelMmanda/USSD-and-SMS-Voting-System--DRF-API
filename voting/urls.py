from django.urls import path
from voting.views import IndexView
from voting.views import ElectionsListView
from voting.views import ElectionDetailView
from voting.views import ElectionPositionsView
from voting.views import ElectionPositionsDetailView
from voting.views import CandidateListView,get_candidates_by_ids_with_positions
from voting.views import CandidateDetailView
from voting.views import VotersListView
from voting.views import VotersDetailView
from voting.views import VotesListView
from voting.views import VotesDetailView
from voting.views import VotesForElectionView
from voting.views import BallotsListView
from voting.views import BallotsDetailView
from voting.views import ResultsListView, GenerateResultsView
from voting.views import SettingsView, SettingsDetailView, getSeetingsByUser

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    # Elections urls based on our new views format
    path('elections/', ElectionsListView.as_view(), name='election-list'),
    path('elections/<int:pk>/', ElectionDetailView.as_view(), name='election-update'),
    # votes per election
    path('elections/<int:election_id>/votes/',
         VotesForElectionView.as_view(), name='votes-for-individual-election'),
    # results per election
    path('elections/<int:election_id>/results/',
         ResultsListView.as_view(), name='results-per-election'),
    # results for all elections
    path('elections/results/', GenerateResultsView.as_view(),
         name='all-elections-results'),

    # Positions
    path('elections/<int:election_id>/positions/',
         ElectionPositionsView.as_view(), name='positions'),
    path('elections/<int:election_id>/positions/<int:position_id>/',
         ElectionPositionsDetailView.as_view(), name='positions-detail'),

    # Candidates
    path('elections/<int:election_id>/candidates/',
         CandidateListView.as_view(), name='candidates'),
    path('elections/<int:election_id>/candidates/<int:candidate_id>/',
         CandidateDetailView.as_view(), name='candidate-update'),
    path('elections/<int:election_id>/getCandidatesByIDs/',
         get_candidates_by_ids_with_positions.as_view(), name='candidates-by-ids'),

    # # Voters
    path('voters/', VotersListView.as_view(), name='voter-list'),
    path('voters/<int:voter_id>/', VotersDetailView.as_view(), name='voter-update'),

    # # Votes
    path('votes/', VotesListView.as_view(), name='vote-create'),
    path('votes/<int:vote_id>/', VotesDetailView.as_view(), name='vote-update'),

    # Ballots
    path('ballots/', BallotsListView.as_view(), name='ballot-list'),
    path('ballots/<int:ballot_id>/',
         BallotsDetailView.as_view(), name='ballot-update'),

    # setting path
    path('settings/', SettingsView.as_view(), name='setting'),
    path('settings/<int:setting_id>/',
         SettingsDetailView.as_view(), name='setting-detail'),
    path('settings/user/<int:user_id>/',
         getSeetingsByUser.as_view(), name='getSetingsByUser'),


]
