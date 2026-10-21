import json

# Campos de cada tabla. Todos son opcionales: se puede enviar solo una parte.
FIELDS = {
    "user": ["username", "email", "password_hash"],
    "recipe": ["user_id", "title", "description", "prep_time", "cook_time", "servings"],
    "category": ["name"],
    "ingredient": ["name"],
    "rating": ["user_id", "recipe_id", "stars", "comment"],
    "favorite": ["user_id", "recipe_id"],
    "follow": ["follower_id", "followed_id"],
    "recipe_category": ["recipe_id", "category_id"],
    "recipe_ingredient": ["recipe_id", "ingredient_id", "quantity", "unit"],
    "recipe_image": ["recipe_id", "image_url"],
    "recipe_step": ["recipe_id", "step_number", "instruction", "image_url"],
}


class Request:
    def __init__(self, table, data=None):
        self.table = table
        # Nos quedamos solo con los campos que existen en la tabla
        self.data = {key: value for key, value in (data or {}).items() if key in FIELDS[table]}

    def to_json(self):
        """Request -> texto JSON."""
        return json.dumps(self.data)

    @staticmethod
    def from_json(table, text):
        """Texto JSON -> Request."""
        return Request(table, json.loads(text) if text else {})
