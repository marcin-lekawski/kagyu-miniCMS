# news/models.py
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.utils import timezone
from django.urls import reverse # Dodaj ten import

class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name="Tytuł artykułu/posta")
    slug = models.SlugField(max_length=250, unique=True, blank=True,
                help_text="Przyjazny adres URL, np. 'nowy-kurs-medytacyjny'. Zostaw puste, aby wygenerować automatycznie.")
    content = HTMLField(verbose_name="Treść artykułu/posta")
    thumbnail = models.ImageField(upload_to='news_thumbnails/', blank=True, null=True, verbose_name="Obraz miniatury")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Data publikacji")
    is_published = models.BooleanField(default=True, verbose_name="Opublikowana? artykuły nieopublikowane nie będą widoczne na stronie.",
                help_text="Zaznacz, jeśli artykuł ma być widoczny publicznie.")
    is_pinned = models.BooleanField(default=False, verbose_name="Przypięta?",
                help_text="Zaznacz, aby przypiąć artykuł na górze listy. Artykuły nieprzypięte będą sortowane według daty publikacji.")
    pin_order = models.PositiveIntegerField(default=0, verbose_name="Kolejność przypięcia",
                help_text="Niższa liczba = wyższa pozycja na liście. Używane tylko dla przypiętych artykułów.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Aktualność"
        verbose_name_plural = "Aktualności"
        # Sortowanie, które będzie używane domyślnie, ale zostanie nadpisane w widokach
        ordering = ['-published_date'] 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug}) # Zakłada, że masz url 'news:article_detail'