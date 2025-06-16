# pages/models.py
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.urls import reverse # Dodaj ten import

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł strony")
    slug = models.SlugField(max_length=200, unique=True, blank=True,
                            help_text="Przyjazny adres URL, np. 'o-nas'. Zostaw puste, aby wygenerować automatycznie.")
    content = HTMLField(verbose_name="Treść strony")


    #Pole do przesyłania obrazów.
    #upload_to='page_headers/': Określa podkatalog w MEDIA_ROOT, do którego będą przesyłane obrazy (np. media/page_headers/moj_obraz.jpg).
    #blank=True, null=True: Pozwala na pozostawienie tego pola pustego w formularzu i w bazie danych.
    header_image = models.ImageField(upload_to='page_headers/', blank=True, null=True, verbose_name="Obraz nagłówkowy")
    is_published = models.BooleanField(default=False, verbose_name="Opublikowana",
                                       help_text="Zaznacz, jeśli strona ma być widoczna publicznie.")
    order = models.IntegerField(default=0, verbose_name="Kolejność",
                                help_text="Kolejność wyświetlania w menu. Niższa liczba oznacza wyższą pozycję.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Strona"
        verbose_name_plural = "Strony"
        ordering = ['order', 'title'] # Zmieniono sortowanie na uwzględniające 'order'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'slug': self.slug}) # Zakłada, że masz url 'pages:detail'