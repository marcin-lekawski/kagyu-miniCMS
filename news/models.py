# news/models.py
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.utils import timezone
from django.urls import reverse # Dodaj ten import

class Article(models.Model):
    # --- Zaktualizowane opcje wyboru ---
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

    title = models.CharField(max_length=250, verbose_name="Tytuł posta")
    slug = models.SlugField(max_length=250, unique=True, blank=True,
                help_text="Przyjazny adres URL, np. 'nowy-kurs-medytacyjny'. Zostaw puste, aby wygenerować automatycznie.")
    content = HTMLField(verbose_name="Treść posta")
    thumbnail = models.ImageField(upload_to='news_thumbnails/', blank=True, null=True, verbose_name="Obraz miniatury")
    
    thumbnail_size = models.CharField(
        max_length=6, choices=SIZE_CHOICES, default='FULL', verbose_name="Rozmiar miniatury",
        help_text="Wybierz rozmiar wyświetlanej miniatury na liście postów."
    )
    # NOWE POLE NA NIESTANDARDOWĄ SZEROKOŚĆ
    thumbnail_custom_width = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Niestandardowa szerokość (px)",
        help_text="Wpisz szerokość w pikselach, jeśli powyżej wybrano 'Niestandardowy'."
    )
    thumbnail_alignment = models.CharField(
        max_length=6, choices=ALIGNMENT_CHOICES, default='CENTER', verbose_name="Wyrównanie miniatury",
        help_text="Wybierz pozycję miniatury względem tekstu."
    )

    published_date = models.DateTimeField(default=timezone.now, verbose_name="Data publikacji")
    is_published = models.BooleanField(default=True, verbose_name="Opublikowany?",
                help_text="Zaznacz, jeśli post ma być widoczny publicznie.")
    is_pinned = models.BooleanField(default=False, verbose_name="Przypięty?",
                help_text="Zaznacz, aby przypiąć post na górze listy. Posty nieprzypięte będą sortowane według daty publikacji.")
    pin_order = models.PositiveIntegerField(default=0, verbose_name="Kolejność przypięcia",
                help_text="Niższa liczba = wyższa pozycja na liście. Używane tylko dla przypiętych postów.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ZMIANA NAZEWNICTWA
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ['-published_date'] 

    # ... reszta metod (__str__, save, get_absolute_url) bez zmian ...
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})