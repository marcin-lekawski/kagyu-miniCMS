# news/models.py
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.utils import timezone
from django.urls import reverse # Dodaj ten import

class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name="Tytuł aktualności")
    slug = models.SlugField(max_length=250, unique=True, blank=True,
                            help_text="Przyjazny adres URL, np. 'pierwsza-aktualnosc'. Zostaw puste, aby wygenerować automatycznie.")
    content = HTMLField(verbose_name="Treść aktualności")
    thumbnail = models.ImageField(upload_to='news_thumbnails/', blank=True, null=True, verbose_name="Obraz miniatury")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Data publikacji")
    is_published = models.BooleanField(default=True, verbose_name="Opublikowana?",
                                       help_text="Zaznacz, jeśli artykuł ma być widoczny publicznie.")
    is_pinned = models.BooleanField(default=False, verbose_name="Przypięta?",
                                    help_text="Zaznacz, aby przypiąć artykuł na górze listy.")
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