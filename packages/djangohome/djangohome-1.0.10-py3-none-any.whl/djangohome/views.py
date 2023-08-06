from itertools import chain
from django.shortcuts import render
from django.views.generic import ListView
""" Import from External Apps. """
from djangopost.models import ArticleModel
from djangoarticle.models import ArticleModelScheme


# Create your homepage views here.
class HomePageView(ListView):
    template_name = "djangoadmin/djangohome/homepage_view.html"
    slug_url_kwarg = "tag_slug"
    context_object_name = "article_filter"

    def get_queryset(self):
        post = ArticleModel.objects.published().filter(is_promote=False)[0:2]
        article = ArticleModelScheme.objects.published().filter(is_promote=False)[0:2]
        article_filter = chain(post, article)
        return article_filter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access for promoted content.
        post_promoted = ArticleModel.objects.promoted().filter(is_trend=False)[0:2]
        article_promoted = ArticleModelScheme.objects.promoted().filter(is_trend=False)[0:2]
        context['is_promoted'] = chain(post_promoted, article_promoted)
        # Access for promotional content.
        post_promo = ArticleModel.objects.promotional()[0:3]
        article_promo = ArticleModelScheme.objects.promotional()[0:3]
        context['promo'] = chain(post_promo, article_promo)
        # Access for trending content.
        post_trending = ArticleModel.objects.trending()[0:2]
        article_trending = ArticleModelScheme.objects.trending()[0:2]
        context['is_trending'] = chain(post_trending, article_trending)
        # return for templating.
        return context
