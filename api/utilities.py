from rest_framework.pagination import PageNumberPagination
from PIL import Image, ImageEnhance

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


def calculate_resolutions(original_width, original_height, scale_low=0.5, scale_medium=1.0, scale_high=2.0):
    # Calculate low resolution dimensions
    low_width = int(original_width * scale_low)
    low_height = int(original_height * scale_low)

    # Calculate medium resolution dimensions
    medium_width = int(original_width * scale_medium)
    medium_height = int(original_height * scale_medium)

    # Calculate high resolution dimensions
    high_width = int(original_width * scale_high)
    high_height = int(original_height * scale_high)

    return {
        "original": (original_width, original_height),
        "low": (low_width, low_height),
        "medium": (medium_width, medium_height),
        "high": (high_width, high_height)
    }


def resize_to_resolution(image_path, image_resolution, extension="jpg"):
    from PIL import Image
    # Open the original image
    original_image = Image.open(image_path)
    original_width, original_height = original_image.size
    # Define a list of resolutions you want to save
    new_resolution = calculate_resolutions(original_width, original_height)
    original_image.resize(new_resolution.get(image_resolution), Image.BILINEAR)
    file_output = f"media/resized_images/image.{extension}"
    original_image.save(file_output)
    # Save the resized image
    return file_output


def convert_to_format(image_path, image_format):
    if image_path.startswith('/'):
        image_path = image_path[1:]
    original_image = Image.open(image_path)
    formats = {
        "jpg": 'JPEG',
        "png": 'PNG'
    }
    
    # Define the file name based on the format (e.g., 'image.jpg', 'image.png', etc.)
    file_name = f'media/reformated_images/image.{formats.get(image_format).lower()}'
    
    # Save the image in the specified format
    original_image.save(file_name, format=formats.get(image_format))
    return file_name
