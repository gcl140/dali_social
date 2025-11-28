from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from members.models import Member
from .models import Connection
from django.contrib.auth.decorators import login_required

@login_required
def connection_list(request):
    # In a real app, you'd get the logged-in member
    current_member = Member.objects.get(name=request.user.name)  # Temporary
    
    connections = Connection.objects.filter(
        (Q(from_member=current_member) | Q(to_member=current_member))
    )
    # connections = Connection.objects.all()
    pending_requests = Connection.objects.filter(
        to_member=current_member,
        status='pending'
    )
     
    context = {
        'connections': connections,
        'pending_requests': pending_requests,
        'current_member': current_member,
    }
    return render(request, 'connections/connection_list.html', context)

def send_connection_request(request, pk):
    to_member = get_object_or_404(Member, pk=pk)
    # In a real app, you'd get the logged-in member
    # from_member = Member.objects.filter_by().first()  # Temporary
    from_member = Member.objects.get(name=request.user.name)

    
    if from_member == to_member:
        messages.error(request, "You cannot connect with yourself.")
        return redirect('member_list')
    
    connection, created = Connection.objects.get_or_create(
        from_member=from_member,
        to_member=to_member,
        defaults={'status': 'pending'}
    )
    
    if created:
        messages.success(request, f"Connection request sent to {to_member.name}!")
    else:
        messages.info(request, f"Connection request already exists with {to_member.name}.")
    
    return redirect('member_detail', pk=to_member.pk)

def accept_connection_request(request, pk):
    connection = get_object_or_404(Connection, pk=pk)
    connection.status = 'accepted'
    connection.save()
    messages.success(request, f"You are now connected with {connection.from_member.name}!")
    return redirect('connection_list')

def reject_connection_request(request, pk):
    connection = get_object_or_404(Connection, pk=pk)
    connection.status = 'rejected'
    connection.save()
    messages.info(request, f"Connection request from {connection.from_member.name} rejected.")
    return redirect('connection_list')