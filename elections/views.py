from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    results = Result.objects.filter(election=election)

    context = {
        'page_title': election.title,
        'election': election,
        'candidates': candidates,
        'results': results,
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
    votes = Vote.objects.filter(candidate=candidate)

    context = {
        'page_title': candidate.name,
        'candidate': candidate,
        'votes': votes,
    }
    return render(request, 'elections/candidates/candidate_details.html', context=context)
