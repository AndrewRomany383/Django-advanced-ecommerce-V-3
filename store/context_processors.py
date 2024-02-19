from .models import Category



def menu_links(request):
    links = Category.objects.values('name', 'slug')
    return dict(links=links)



















