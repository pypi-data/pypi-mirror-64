
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin

from cap.decorators import short_description, template_list_item

from categories.models import Category


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):

    list_display = ['name', 'product_count', 'get_preview']

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

    @template_list_item('admin/list_item_preview.html', _('Preview'))
    def get_preview(self, item):
        return {'file': item.logo}

    @short_description(_('Product count'))
    def product_count(self, item):
        return item.products.count()
