from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.utils import timezone # Do pola daty publikacji

# Create your models here.

#published_date: Pozwoli na planowanie publikacji i sortowanie chronologiczne. 
#thumbnail: Dodatkowe pole na obrazek miniatury, przydatne do wyświetlania listy aktualności.

class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name="Tytuł aktualności")
    slug = models.SlugField(max_length=250, unique=True, blank=True,
                            help_text="Przyjazny adres URL, np. 'pierwsza-aktualnosc'. Zostaw puste, aby wygenerować automatycznie.")
    content = HTMLField(verbose_name="Treść aktualności")
    # Pole dla obrazu wiodącego (thumbnail)
    thumbnail = models.ImageField(upload_to='news_thumbnails/', blank=True, null=True, verbose_name="Obraz miniatury")
    # Data publikacji, domyślnie bieżąca data i czas
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Data publikacji")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aktualność"
        verbose_name_plural = "Aktualności"
        # Sortowanie od najnowszych do najstarszych
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)