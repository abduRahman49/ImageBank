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


def apply_watermark(input_image_path, output_image_path, watermark_image_path):
    # Open the original image and watermark image
    image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)

    # Get the dimensions of the original image and watermark
    image_width, image_height = image.size
    watermark_width, watermark_height = watermark.size

    # Calculate the number of times to repeat the watermark in both dimensions
    x_repeat = image_width // watermark_width
    y_repeat = image_height // watermark_height

    # Create a transparent image with the same size as the original image
    transparent = Image.new("RGBA", image.size)

    # Paste the watermark at regular intervals to tile it
    for x in range(x_repeat):
        for y in range(y_repeat):
            # Calculate the position to paste the watermark
            position = (x * watermark_width, y * watermark_height)
            transparent.paste(watermark, position, watermark)

    # Save the watermarked image
    transparent.save(output_image_path)

