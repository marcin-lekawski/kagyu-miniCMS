from pages.models import Page

def all_pages(request):
    """
    Dodaje listę wszystkich stron do kontekstu każdego żądania.
    """
    return {'all_pages': Page.objects.all().order_by('title')}