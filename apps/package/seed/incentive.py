# importing the module
import json
import os
from django.conf import settings

# Opening JSON file
INCENTIVE_BOOKS = []
with open(
    os.path.join(settings.BASE_DIR, "apps/package/seed/incentive_books.json")
) as json_file:
    INCENTIVE_BOOKS = json.load(json_file)
