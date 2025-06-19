from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField

class Page(models.Model):
    # Opcje wyboru dla nowych pól
    SIZE_CHOICES = [
        ('S', 'Mała (do 200px)'),
        ('M', 'Średnia (do 350px)'),
        ('L', 'Duża (do 500px)'),
        ('FULL', 'Pełna szerokość'),
        ('CUSTOM', 'Niestandardowy (własna szerokość)'),
    ]
    ALIGNMENT_CHOICES = [
        ('LEFT', 'Do lewej'),
        ('RIGHT', 'Do prawej'),
        ('CENTER', 'Na środku'),
    ]

    # Twoje oryginalne pola
    title = models.CharField(max_length=200, verbose_name="Tytuł strony")
    slug = models.SlugField(max_length=200, unique=True, blank=True,
                            help_text="Przyjazny adres URL, np. 'o-nas'. Zostaw puste, aby wygenerować automatycznie.")
    content = HTMLField(verbose_name="Treść strony")
    header_image = models.ImageField(upload_to='page_headers/', blank=True, null=True, verbose_name="Obraz nagłówkowy")
    is_published = models.BooleanField(default=False, verbose_name="Opublikowana",
                                       help_text="Zaznacz, jeśli strona ma być widoczna publicznie.")
    order = models.IntegerField(default=0, verbose_name="Kolejność",
                                help_text="Kolejność wyświetlania w menu. Niższa liczba oznacza wyższą pozycję.")
    
    # Nowe pola dla miniatur
    thumbnail = models.ImageField(upload_to='pages_thumbnails/', blank=True, null=True, verbose_name="Obraz miniatury")
    thumbnail_size = models.CharField(
        max_length=6, choices=SIZE_CHOICES, default='FULL', verbose_name="Rozmiar miniatury"
    )
    thumbnail_custom_width = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Niestandardowa szerokość (px)",
        help_text="Wpisz szerokość w pikselach, jeśli powyżej wybrano 'Niestandardowy'."
    )
    thumbnail_alignment = models.CharField(
        max_length=6, choices=ALIGNMENT_CHOICES, default='CENTER', verbose_name="Wyrównanie miniatury"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Twoje oryginalne ustawienia Meta
        verbose_name = "Strona"
        verbose_name_plural = "Strony"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'slug': self.slug})