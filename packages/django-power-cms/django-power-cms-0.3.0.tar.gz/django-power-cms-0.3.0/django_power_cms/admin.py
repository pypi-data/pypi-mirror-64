from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse
from django.contrib.admin.options import csrf_protect_m
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django_readedit_switch_admin.admin import DjangoReadEditSwitchAdmin
from django_changelist_toolbar_admin.admin import DjangoChangelistToolbarAdminMixin
from django_visit_on_site_in_new_window.admin import DjangoVisitOnSiteInNewWindowAdmin
from django_cards_admin.admin import DjangoCardsAdminMixin
from django_msms_admin.admin import DjangoMsmsAdmin
from django_msms_admin.admin import DjangoSubclassAdmin
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from .models import Template
from .models import TemplateSlot
from .models import Site
from .models import Page
from .models import PageWidget
from .models import Widget
from .models import StaticHtmlWidget
from .models import CarouselWidget
from .models import CarouselWidgetImage
from .models import Theme
from .models import ThemeCss
from .models import ThemeJs
from .models import WidgetLink
from .models import StaticListWidget
from .models import StaticListItem
from .models import TopbarWidget
from .models import TopbarBrand
from .models import Article
from .models import ArticleContentImage
from .models import ArticleListWidget
from .models import ArticleDetailWidget

CURRENT_SIET_ID_SESSION_KEY = "django-power-cms-current-site-id"

class TemplateSlotInline(DjangoReadEditSwitchAdmin, admin.TabularInline):
    model = TemplateSlot
    extra = 0

class TemplateAdmin(DjangoReadEditSwitchAdmin, admin.ModelAdmin):
    list_display = ["name", "app_label", "template", "preview_image"]
    list_filter = ["app_label"]
    search_fields = ["name", "description", "template"]
    inlines = [
        TemplateSlotInline,
    ]


class ThemeCssInline(DjangoReadEditSwitchAdmin, admin.TabularInline):
    model = ThemeCss
    extra = 0

class ThemeJsInline(DjangoReadEditSwitchAdmin, admin.TabularInline):
    model = ThemeJs
    extra = 0

class ThemeAdmin(DjangoReadEditSwitchAdmin, admin.ModelAdmin):
    list_display = ["name", "description", "is_default"]
    list_filter = ["is_default"]
    search_fields = ["name", "description"]
    inlines = [
        ThemeCssInline,
        ThemeJsInline,
    ]

class SiteForm(ModelForm):
    class Meta:
        model = Site
        exclude = []
        widgets = {
            "published": DjangoToggleSwitchWidget(klass="django-toggle-switch-primary"),
        }

class SiteAdmin(
        DjangoReadEditSwitchAdmin,
        DjangoCardsAdminMixin,
        DjangoVisitOnSiteInNewWindowAdmin,
        admin.ModelAdmin):
    form = SiteForm
    result_cards_columns = 3
    list_display = ["name", "code", "published", "published_time", "preview_link"]
    search_fields = ["name", "code"]
    readonly_fields = ["published_time"]
    result_card_body_height = 200
    fieldsets = [
        (_("Basic Info"), {
            "fields": ["name", "code", "theme", "index_page_code"],
        }),
        (_("Publish State"), {
            "fields": ["published", "published_time"],
        }),
        (_("Other Config"), {
            "fields": ["favicon"],
        }),
    ]

    def preview_link(self, obj):
        return format_html(
            """<a href="{0}" target="_blank">{1}</a>""",
            obj.get_absolute_url(),
            _("Preview"),
        )

    preview_link.short_description = _("Preview")

    class Media:
        css = {
            "all": [
                "fontawesome/css/all.min.css",
            ]
        }

    def result_card_link_title(self, item):
        return _("Enter into Site Manager...")

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id:
            request.session[CURRENT_SIET_ID_SESSION_KEY] = object_id
        return super().changeform_view(request, object_id, form_url, extra_context)

class PageWidgetInline(DjangoReadEditSwitchAdmin, admin.TabularInline):
    model = PageWidget
    classes = ["tab-page-widgets"]

class PageAdmin(
        DjangoReadEditSwitchAdmin,
        DjangoChangelistToolbarAdminMixin,
        DjangoVisitOnSiteInNewWindowAdmin,
        DjangoTabbedChangeformAdmin,
        DraggableMPTTAdmin,
        admin.ModelAdmin):
    list_display = ["tree_actions", "display_title", "display_page_url", "template", "preview_link"]
    list_display_links = ["display_title"]

    def display_title(self, obj):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            obj._mpttfield('level') * self.mptt_level_indent,
            obj.name,
        )
    display_title.short_description = _('Title')

    def display_page_url(self, obj):
        return "page:{0}:{1}".format(obj.site.code, obj.code)
    display_page_url.short_description = _("Display Page URL") 

    def preview_link(self, obj):
        return format_html(
            """<a href="{0}" target="_blank">{1}</a>""",
            obj.get_absolute_url(),
            _("Preview"),
        )
    preview_link.short_description = _("Preview")

    def get_queryset(self, request):
        site_id = request.session[CURRENT_SIET_ID_SESSION_KEY]
        if site_id:
            queryset = super().get_queryset(request).filter(site__id=int(site_id))
            return queryset
        else:
            return None

    fieldsets = [
        (None, {
            "fields": ["site", "parent", "name", "code"],
            "classes": ["tab-basic"],
        }),
        (None, {
            "fields": ["template", "theme"],
            "classes": ["tab-site-styles"],
        }),
        (_("Publish Status"), {
            "fields": ["published", "published_time"],
            "classes": ["tab-publish"],
        })
    ]
    inlines = [
        PageWidgetInline,
    ]

    tabs = [
        (_("Page Basic Settings"), ["tab-basic", "tab-site-style", "tab-publish"]),
        (_("Page Template & Theme Settings"), ["tab-site-styles"]),
        (_("Page Widgets Settings"), ["tab-page-widgets"]),
    ]
class WidgetLinkInline(admin.TabularInline):
    model = WidgetLink
    extra = 0

class StaticHtmlWidgetAdmin(DjangoSubclassAdmin, admin.ModelAdmin):
    list_dipslay = ["name"]
    inlines = [
        WidgetLinkInline,
    ]

class CarouselWidgetImageInline(admin.TabularInline):
    model = CarouselWidgetImage
    extra = 0

class CarouselWidgetAdmin(DjangoSubclassAdmin, admin.ModelAdmin):
    list_dipslay = ["name"]
    inlines = [
        WidgetLinkInline,
        CarouselWidgetImageInline,
    ]

class StaticListItemInline(admin.StackedInline):
    model = StaticListItem
    extra = 0
    fieldsets = [
        [None, {
            "fields": [
                ("title", "url"),
                ("target", "order"),
                ("label", "label_class"),
            ]
        }]
    ]

class StaticListWidgetAdmin(DjangoSubclassAdmin, admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        WidgetLinkInline,
        StaticListItemInline,
    ]

class TopbarBrandInline(admin.TabularInline):
    model = TopbarBrand
    extra = 0

class TopbarWidgetAdmin(DjangoSubclassAdmin, DjangoChangelistToolbarAdminMixin, admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        WidgetLinkInline,
        TopbarBrandInline,
    ]


class ArticleContentImageInline(admin.TabularInline):
    model = ArticleContentImage
    extra = 0
    fieldsets = [
        (None, {
            "fields": ["image", "image_link"],
        }),
    ]
    readonly_fields = ["image_link"]
    classes = ["tab-content-images"]

class ArticleAdmin(
        DjangoReadEditSwitchAdmin,
        DraggableMPTTAdmin,
        DjangoTabbedChangeformAdmin,
        DjangoChangelistToolbarAdminMixin,
        admin.ModelAdmin):
    list_display = ["tree_actions", "display_title", "published", "published_time"]
    list_display_links = ["display_title"]


    def display_title(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title,
        )
    display_title.short_description = _('Title')

    fieldsets = [
        (None, {
            "fields": ["site", "parent", "title", "description", "label"],
            "classes": ["tab-basic"],
        }),
        (_("Article Publish Settings"), {
            "fields": ["published", "published_time"],
            "classes": ["tab-publish"]
        }),
        (None, {
            "fields": ["content", "preview_image", "show_preview_image"],
            "classes": ["tab-content"],
        }),

    ]
    inlines = [
        ArticleContentImageInline
    ]

    tabs = [
        (_("Article Basic Settings"), ["tab-basic", "tab-publish"]),
        (_("Article Content Settings"), ["tab-content"]),
        (_("Article Content Image Settigns"), ["tab-content-images"]),
    ]

class WidgetAdmin(DjangoMsmsAdmin, DjangoChangelistToolbarAdminMixin, admin.ModelAdmin):
    list_display = ["name", "type_name"]
    list_filter = ["type_name"]
    search_fields = ["name"]

    
class ArticleListWidgetAdmin(DjangoSubclassAdmin, admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        WidgetLinkInline,
    ]

class ArticleDetailWidgetAdmin(DjangoSubclassAdmin, admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        WidgetLinkInline,
    ]



admin.site.register(Template, TemplateAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(CarouselWidget, CarouselWidgetAdmin)
admin.site.register(StaticHtmlWidget, StaticHtmlWidgetAdmin)
admin.site.register(StaticListWidget, StaticListWidgetAdmin)
admin.site.register(TopbarWidget, TopbarWidgetAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleListWidget, ArticleListWidgetAdmin)
admin.site.register(ArticleDetailWidget, ArticleDetailWidgetAdmin)
