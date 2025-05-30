from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    """
    Default pagination class for our API
    """
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 1000
    page_query_param = 'page'
