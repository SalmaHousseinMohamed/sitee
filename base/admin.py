from django.contrib import admin
from .models import Category, Product, Image ,User , Comment 


admin.site.register(User)
admin.site.register(Comment)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ImageInline(admin.TabularInline):
    model = Image
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'description',
        'location',
        'condition',
        'price',
    )
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_thumbnail')

    def image_thumbnail(self, obj):
        # Display a thumbnail of the image
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-width: 100px; max-height: 100px;" />'
        return '(No image)'
    image_thumbnail.short_description = 'Thumbnail'
    image_thumbnail.allow_tags = True
