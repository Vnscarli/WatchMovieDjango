from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class ReviewsPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 5
    
    
class ReviewsLOPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 5
    offset_query_param = 'start'
    

class ReviewsCPagination(CursorPagination):
    page_size = 5
    ordering = 'id'
    