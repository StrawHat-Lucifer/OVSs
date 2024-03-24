from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Election, Candidate, Vote, Result

@login_required()
def home(request):
    active_elections = Election.objects.filter(is_active=True)
    past_elections = Election.objects.filter(is_active=False)

    context = {
        'page_title': 'Elections', 
        'active_elections': active_elections,
        'past_elections': past_elections,
    }
    return render(request, 'elections/elections.html', context=context)


@login_required()
def election_detail(request, pk):
    election = Election.objects.get(pk=pk)
    candidates = Candidate.objects.filter(election=election)
    total_votes = Vote.objects.filter(election=election).count()
    results = Result.objects.filter(election=election)
    voted = Vote.objects.filter(election=election, voter=request.user).exists()
    election_active = election.is_active and election.end_date > timezone.now()

    context = {
        'page_title': election.title,
        'election': election,
        'candidates': candidates,
        'total_votes:': total_votes,
        'results': results,
        'voted': voted,
        'election_active': election_active,
    }
    return render(request, 'elections/election_detail.html', context=context)


@login_required()
def election_candidates(request, pk):
    election = Election.objects.get(pk=pk)
    candidates = Candidate.objects.filter(election=election)

    context = {
        'page_title': election.title + ' - Candidates',
        'election': election,
        'candidates': candidates,
    }
    return render(request, 'elections/candidates/election_candidates.html', context=context)


@login_required()
def candidate_detail(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    votes = Vote.objects.filter(candidate=candidate).count()
    voted = Vote.objects.filter(election=candidate.election, voter=request.user).exists()
    age = timezone.now().year - candidate.dob.year
    rivals = Candidate.objects.filter(election=candidate.election).exclude(pk=candidate.pk).count()

    context = {
        'page_title': candidate.name,
        'candidate': candidate,
        'age': age,
        'votes': votes,
        'voted': voted,
        'rivals': rivals,
        'total_candidates': rivals + 1,
    }
    return render(request, 'elections/candidates/candidate_details.html', context=context)


@login_required()
def confirm_vote(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    election = candidate.election
    voter = request.user

    if request.method == 'POST':
        vote = Vote.objects.create(candidate=candidate, election=election, voter=voter)
        vote.save()
        messages.success(request, f'Vote for {candidate.name} accepted!')
        return redirect('election_detail', pk=election.pk)

    context = {
        'page_title': 'Confirm Vote',
        'candidate': candidate,
        'election': election,
    }

    return render(request, 'elections/votes/confirm_vote.html', context=context)



@login_required()
def confirm_vote_delete(request, pk):
    vote = Vote.objects.get(pk=pk)

    if request.method == 'POST':
        vote.delete()
        messages.success(request, f'Vote for {vote.candidate.name} deleted!')
        return redirect('vote_history')

    context = {
        'page_title': 'Delete Vote',
        'vote': vote,
    }

    return render(request, 'elections/votes/confirm_vote_delete.html', context=context)



@login_required()
def vote_history(request):
    votes = Vote.objects.filter(voter=request.user)

    context = {
        'page_title': 'Vote History',
        'votes': votes,
    }

    return render(request, 'elections/votes/vote_history.html', context=context)
