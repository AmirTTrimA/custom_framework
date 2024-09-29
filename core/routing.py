def resolve(path):
    from app.urls import urlpatterns

    for pattern in urlpatterns:
        if pattern['path'] == path:
            return pattern['view'], pattern.get('kwargs', {})

    return None, None
