from django.contrib import admin

import models


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "pub_date", "published")
    ordering = ("-pub_date",)
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
