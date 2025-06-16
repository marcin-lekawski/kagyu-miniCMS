# site_config/models.py
from django.db import models
from tinymce.models import HTMLField

class HeaderContent(models.Model):
    """
    Model do przechowywania treści nagłówka strony.
    Zaprojektowany tak, aby istniał tylko jeden rekord (singleton).
    """
    site_name = HTMLField(max_length=200, verbose_name="Nazwa Strony/Ośrodka", blank=True,
                                 help_text="Główna nazwa strony wyświetlana w nagłówku. Możesz używać formatowania HTML.")
    # tagline = HTMLField(max_length=255, verbose_name="Slogan/Podtytuł", blank=True, # Zmieniono na HTMLField
    #                           help_text="Krótki slogan lub opis wyświetlany pod nazwą strony. Możesz używać formatowania HTML.")
    logo = models.ImageField(upload_to='site_config/logos/', blank=True, null=True, verbose_name="Logo strony",
                             help_text="Obraz logo wyświetlany w nagłówku.")
    header_background_image = models.ImageField(upload_to='site_config/header_bgs/', blank=True, null=True,
                                                 verbose_name="Obraz tła nagłówka",
                                                 help_text="Obraz używany jako tło dla sekcji nagłówka strony.")

    class Meta:
        verbose_name = "Zawartość Nagłówka"
        verbose_name_plural = "Zawartość Nagłówka"

    def __str__(self):
        return "Globalna Zawartość Nagłówka"

    def save(self, *args, **kwargs):
        if self.__class__.objects.exists() and not self.pk:
            existing = self.__class__.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

class FooterContent(models.Model):
    """
    Model do przechowywania treści stopki strony.
    Zaprojektowany tak, aby istniał tylko jeden rekord (singleton).
    """
    copyright_text = HTMLField(verbose_name="Tekst praw autorskich", blank=True,
                               help_text="Tekst informacji o prawach autorskich (np. © 2023 Twoja Nazwa).")
    address = HTMLField(verbose_name="Adres ośrodka", blank=True,
                        help_text="Pełny adres ośrodka, może zawierać formatowanie HTML.")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Adres E-mail",
                                      help_text="Główny adres e-mail do kontaktu.")
    contact_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numer Telefonu",
                                     help_text="Numer telefonu kontaktowego.")

    zobacz_tez_html = HTMLField(blank=True, verbose_name="Sekcja 'Zobacz też' (HTML)",
                                help_text="Wprowadź listę linków w formacie HTML (np. &lt;ul&gt;&lt;li&gt;&lt;a href='/url/'&gt;Tekst&lt;/a&gt;&lt;/li&gt;&lt;/ul&gt;).")
    osrodki_w_poblizu_html = HTMLField(blank=True, verbose_name="Sekcja 'Ośrodki w pobliżu' (HTML)",
                                        help_text="Wprowadź listę linków do ośrodków w pobliżu w formacie HTML (np. &lt;ul&gt;&lt;li&gt;&lt;a href='/url/'&gt;Tekst&lt;/a&gt;&lt;/li&gt;&lt;/ul&gt;).")
    bank_info_html = HTMLField(blank=True, verbose_name="Informacje Bankowe (HTML)",
                               help_text="Wprowadź wszystkie dane bankowe w jednym bloku HTML (np. nazwa banku, numer konta, SWIFT/BIC, tytuł przelewu).")

    class Meta:
        verbose_name = "Zawartość stopki"
        verbose_name_plural = "Zawartości stopki"

    def __str__(self):
        return "Globalna Zawartość Stopki" # Zmieniono dla spójności

    def save(self, *args, **kwargs):
        # Nadpisujemy metodę save, aby upewnić się, że w bazie istnieje tylko jeden rekord.
        if self.__class__.objects.exists() and not self.pk:
            existing = self.__class__.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)