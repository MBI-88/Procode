from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Class


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self) -> list:
        return ['cells:dashboar_list', 'cells:index', 'cells_api:showitems_api', ]

    def location(self, item: str) -> reverse:
        return reverse(item)
