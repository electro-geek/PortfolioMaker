from .models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip tracking for static files and admin
        if not request.path.startswith('/static/') and not request.path.startswith('/admin/'):
            try:
                # Get IP address
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                # Create visitor record
                Visitor.objects.create(
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    path=request.path,
                    session_key=request.session.session_key if request.session else None
                )
            except Exception as e:
                # Silently fail to not interrupt the user experience
                print(f"Error tracking visitor: {e}")

        response = self.get_response(request)
        return response
