from rest_framework import serializers

from apps.blog.models import Blog, Category, Tag


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = (
            # model fields
            'id', 'image', 'category', 'tags', 'published_date', 'blog_publish_type',

            # English fields
            'title_en', 'description_en', 'meta_title_en', 'meta_keywords_en',
            'meta_description_en', 'og_title_en', 'og_description_en', 'og_locale_en',
            'og_type_en',

            # Nepali fields
            'title_ne', 'description_ne', 'meta_title_ne', 'meta_keywords_ne',
            'meta_description_ne', 'og_title_ne', 'og_description_ne', 'og_locale_ne', 'og_type_ne',
        )


class BlogTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id', 'name_en', 'name_ne'
        )


class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'name_en', 'name_ne'
        )
