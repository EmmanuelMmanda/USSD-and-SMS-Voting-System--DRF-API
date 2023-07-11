from django.contrib import admin


from .models import Results, Settings, Voter, Election, Position, Candidate, Vote


class VoterAdmin(admin.ModelAdmin):
    list_display = ('university_id', 'gender', 'phone_number', 'has_vote')
    search_fields = ('university_id', 'first_name',
                     'last_name', 'email', 'phone_number')
    list_filter = ('gender',)


class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'election')
    search_fields = ('title',  'election__title')
    list_filter = ('election',)


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'position')
    search_fields = ('first_name', 'last_name', 'position__title')
    list_filter = ('position__election',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'get_position',
                    'vote_value', 'time_cast')
    search_fields = ('voter__university_id',
                     'voter__first_name', 'voter__last_name')
    list_filter = ('voter', 'vote_value')

    def get_position(self, obj):
        return obj.Position
    get_position.short_description = 'Position'


class ResultsAdmin(admin.ModelAdmin):
    list_display = ('position', 'candidate', 'vote_count', 'vote_percentage')
    search_fields = ('position__title', 'candidate__first_name',
                     'candidate__last_name')
    list_filter = ('position__election',)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('language', 'user', 'updated_at')


admin.site.register(Voter, VoterAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Settings, SettingsAdmin)

# Modify the admin site header and title
admin.site.site_header = "Election Admin Panel"
admin.site.site_title = "Election Admin Panel"
