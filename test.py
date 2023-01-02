import requests
import io

# Download the image from the URL
response = requests.get(image_url)

# Convert the image to a BytesIO object
image_bytes = io.BytesIO(response.content)

# Store the image in cache
cache.set(key, image_bytes)

# Send the image in a post request
response = requests.post(url, data=image_bytes)
