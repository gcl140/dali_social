

import random as _random

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member
from .serializers import MemberSerializer

MEMBERS_PER_PAGE = 12


def _querystring_without_page(request):
    params = request.GET.copy()
    params.pop('page', None)
    return params.urlencode()


@login_required
def member_list(request):
    members_qs = Member.objects.all()

    # Filtering
    role = request.GET.get('role')
    year = request.GET.get('year')
    search = request.GET.get('search')

    if role:
        if role == 'dev': members_qs = members_qs.filter(dev=True)
        elif role == 'des': members_qs = members_qs.filter(des=True)
        elif role == 'pm': members_qs = members_qs.filter(pm=True)
        elif role == 'core': members_qs = members_qs.filter(core=True)
        elif role == 'mentor': members_qs = members_qs.filter(mentor=True)

    if year:
        members_qs = members_qs.filter(year=year)

    if search:
        members_qs = members_qs.filter(
            Q(name__icontains=search) |
            Q(major__icontains=search) |
            Q(minor__icontains=search) |
            Q(home__icontains=search)
        )

    # Stable random order: shuffle filtered ids with a URL seed so pagination
    # stays consistent across page clicks. New seed each fresh visit.
    seed = request.GET.get('seed') or str(_random.randint(0, 2**31 - 1))
    shuffled_ids = list(members_qs.order_by('pk').values_list('pk', flat=True))
    _random.Random(seed).shuffle(shuffled_ids)

    paginator = Paginator(shuffled_ids, MEMBERS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    page_ids = list(page_obj.object_list)
    by_pk = Member.objects.in_bulk(page_ids)
    members = [by_pk[pk] for pk in page_ids if pk in by_pk]

    # Carry the seed in pagination/filter links so reshuffles don't happen mid-session.
    qs_params = request.GET.copy()
    qs_params.pop('page', None)
    qs_params['seed'] = seed
    querystring = qs_params.urlencode()

    context = {
        'members': members,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1),
        'querystring': querystring,
        'seed': seed,
        'current_role': role,
        'current_year': year,
        'search_query': search,
    }
    return render(request, 'members/member_list.html', context)

@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    context = {'member': member}
    return render(request, 'members/member_detail.html', context)

@login_required
def search_members(request):
    query = request.GET.get('q', '')
    if query:
        members = Member.objects.filter(
            Q(name__icontains=query) |
            Q(major__icontains=query) |
            Q(minor__icontains=query) |
            Q(home__icontains=query) |
            Q(favorite_dartmouth_tradition__icontains=query)
        ).order_by('name')
    else:
        members = Member.objects.all().order_by('name')

    paginator = Paginator(members, MEMBERS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'members': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1),
        'querystring': _querystring_without_page(request),
        'query': query,
    }
    return render(request, 'members/search_results.html', context)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'major', 'minor', 'home']
    ordering_fields = ['name', 'year', 'created_at']


# @login_required
# def profile_update(request, member_id=None):
#     # If no member_id provided, assume current user's profile
#     if member_id:
#         member = get_object_or_404(Member, id=member_id)
#     else:
#         # You'll need to adjust this based on how Members are linked to Users
#         # This is a placeholder - adjust according to your User-Member relationship
#         member = get_object_or_404(Member, name=request.user.username)
    
#     # Check if user has permission to edit this profile
#     # You might want to add more sophisticated permission checks
#     # if not request.user.is_staff and str(member.name) != request.user.username:
#     #     messages.error(request, "You don't have permission to edit this profile.")
#     #     return redirect('member_list')
    
#     if request.method == 'POST':
#         form = MemberProfileForm(request.POST, instance=member)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('member_detail', pk=member.pk)
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = MemberProfileForm(instance=member)
    
#     context = {
#         'form': form,
#         'member': member,
#         'is_editing': True,
#     }
#     return render(request, 'members/profile_update.html', context)

@login_required
def profile_update(request, member_id=None):
    # If editing someone else
    if member_id:
        member = get_object_or_404(Member, id=member_id)

    else:
        # Auto-link Members to Users by username, create if missing
        member, created = Member.objects.get_or_create(
            name=request.user.name,
            defaults={
                "year": "2024",    # or whatever default
            }
        )

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('member_detail', pk=member.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MemberProfileForm(instance=member)

    context = {
        'form': form,
        'member': member,
        'is_editing': True,
    }
    return render(request, 'members/profile_update.html', context)

# You might also want a profile view (similar to your existing function but for Member model)
@login_required
def profile_view(request, member_id=None):

    # Viewing a specific member
    if member_id:
        member = get_object_or_404(Member, id=member_id)

    else:
        # Viewing your own profile
        try:
            member = Member.objects.get(name=request.user.name)
        except Member.DoesNotExist:
            messages.error(request, "Your member profile is missing. Please complete setup.")
            return redirect('member_edit_create')

    context = {
        'member': member,
        'is_editing': False,
    }
    return render(request, 'members/member_detail.html', context)
