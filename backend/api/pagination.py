from rest_framework.pagination import PageNumberPagination
from foodgram_shapalin.settings import PAGES


class RecipePagination(PageNumberPagination):
    page_size = PAGES
    page_size_query_param = 'limit'
