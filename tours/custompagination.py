from rest_framework.pagination import LimitOffsetPagination

#TODO add pagination limit to settings.py
class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    max_limit = 5
