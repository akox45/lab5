from django.contrib import messages
from django.contrib.auth.models import User

class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process notifications before the view
        if request.user.is_authenticated and 'notifications' in request.session:
            user_notifications = [
                n for n in request.session['notifications']
                if n['user_id'] == request.user.id
            ]
            for notification in user_notifications:
                messages.success(request, notification['message'])
            # Remove processed notifications
            request.session['notifications'] = [
                n for n in request.session['notifications']
                if n['user_id'] != request.user.id
            ]
            request.session.modified = True

        response = self.get_response(request)
        return response 