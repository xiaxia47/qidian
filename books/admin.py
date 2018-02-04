from django.contrib import admin
from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['book_type','book_sub_type','book_name','author','total_words','changed_tag']
    search_fields = ['book_name','author']
    list_filter = ['book_type']
    

admin.site.register(Book, BookAdmin)
