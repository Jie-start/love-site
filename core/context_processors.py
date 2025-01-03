def relationship_requests(request):
    if request.user.is_authenticated:
        pending_count = request.user.received_requests.filter(status='pending').count()
        return {'pending_requests_count': pending_count}
    return {'pending_requests_count': 0} 