# site_config/admin.py
from django.contrib import admin
from tinymce.widgets import TinyMCE
from django import forms
from .models import HeaderContent, FooterContent
from django.utils.html import format_html, strip_tags

# Formularz dla HeaderContent
class HeaderContentAdminForm(forms.ModelForm):
    site_name = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 5}))
    # USUNIĘTO: tagline = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 5}))

    class Meta:
        model = HeaderContent
        fields = '__all__'

@admin.register(HeaderContent)
class HeaderContentAdmin(admin.ModelAdmin):
    form = HeaderContentAdminForm
    # USUNIĘTO 'tagline_preview' z list_display
    list_display = ('site_name_preview', 'logo_preview', 'header_bg_preview') 

    fieldsets = (
        (None, {
            # USUNIĘTO 'tagline' z fields
            'fields': ('site_name', 'logo', 'header_background_image'), 
            'description': "Nazwa strony/ośrodka wyświetlana w nagłówku. Obrazy dla logo i tła nagłówka."
        }),
    )

    def site_name_preview(self, obj):
        return strip_tags(obj.site_name)[:50] + "..." if obj.site_name else "Brak nazwy"
    site_name_preview.short_description = "Nazwa strony (podgląd)"

    # USUNIĘTO: metodę tagline_preview
    # def tagline_preview(self, obj):
    #     return strip_tags(obj.tagline)[:50] + "..." if obj.tagline else "Brak sloganu"
    # tagline_preview.short_description = "Slogan (podgląd)"

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 50px; height:auto;" />', obj.logo.url)
        return "Brak logo"
    logo_preview.short_description = "Podgląd Logo"

    def header_bg_preview(self, obj):
        if obj.header_background_image:
            return format_html('<img src="{}" style="width: 50px; height:auto;" />', obj.header_background_image.url)
        return "Brak tła"
    header_bg_preview.short_description = "Podgląd Tła Nagłówka"

    def has_add_permission(self, request):
        return not HeaderContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# Formularz dla FooterContent (bez zmian w tej sekcji, jest poprawna)
class FooterContentAdminForm(forms.ModelForm):
    copyright_text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 5}))
    address = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    zobacz_tez_html = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    osrodki_w_poblizu_html = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    bank_info_html = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    class Meta:
        model = FooterContent
        fields = '__all__'

@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    form = FooterContentAdminForm
    list_display = ('copyright_text_preview', 'contact_email', 'contact_phone')
    
    fieldsets = (
        ('Podstawowe Informacje Kontaktowe', {
            'fields': ('copyright_text', 'address', 'contact_email', 'contact_phone'),
            'description': "Podstawowe dane kontaktowe ośrodka."
        }),
        ('Sekcje Linków w Stopce', {
            'fields': (
                'zobacz_tez_html',
                'osrodki_w_poblizu_html'
            ),
            'description': "Wprowadź treści sekcji linków w stopce (np. listy linków)."
        }),
        ('Informacje o Wsparciu (Konto Bankowe)', {
            'fields': ('bank_info_html',),
            'description': "Wprowadź wszystkie dane bankowe w jednym bloku HTML."
        }),
    )

    def copyright_text_preview(self, obj):
        return strip_tags(obj.copyright_text)[:50] + "..." if obj.copyright_text else "Brak"
    copyright_text_preview.short_description = "Tekst praw autorskich (podgląd)"

    def has_add_permission(self, request):
        return not FooterContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False