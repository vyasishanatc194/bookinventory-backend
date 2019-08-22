# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from inventory.models import Category, BooksInventory, BookImages

class CategoryAdmin(admin.ModelAdmin):
    pass

class BooksInventoryAdmin(admin.ModelAdmin):
    pass

class BookImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(BooksInventory, BooksInventoryAdmin)
admin.site.register(BookImages, BookImagesAdmin)
