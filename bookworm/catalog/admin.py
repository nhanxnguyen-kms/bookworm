from django.contrib import admin

from bookworm.catalog.models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "price", "category")
    list_filter = ("category",)
    search_fields = ("title", "author")
    list_per_page = 10
    actions = ["make_price_zero"]

    def make_price_zero(self, queryset):
        queryset.update(price=0)

    make_price_zero.short_description = "Make selected books free"
