from rest_framework.pagination import PageNumberPagination

class ImagePagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        # Call the parent class method to get the default paginated response
        response = super().get_paginated_response(data)

        # Add the number of pages to the response
        response.data['num_pages'] = self.page.paginator.num_pages
        return response

class LicencePagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        # Call the parent class method to get the default paginated response
        response = super().get_paginated_response(data)

        # Add the number of pages to the response
        response.data['num_pages'] = self.page.paginator.num_pages
        return response
