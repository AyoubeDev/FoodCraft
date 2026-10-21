# Campos que se devuelven de cada tabla (user no devuelve password_hash)
RESPONSE_FIELDS = {
    "user": ["user_id", "username", "email", "created_at"],
    "recipe": ["recipe_id", "user_id", "title", "description", "prep_time", "cook_time", "servings", "created_at"],
    "category": ["category_id", "name"],
    "ingredient": ["ingredient_id", "name"],
    "rating": ["rating_id", "user_id", "recipe_id", "stars", "comment", "created_at"],
    "favorite": ["user_id", "recipe_id"],
    "follow": ["follower_id", "followed_id"],
    "recipe_category": ["recipe_id", "category_id"],
    "recipe_ingredient": ["recipe_id", "ingredient_id", "quantity", "unit"],
    "recipe_image": ["image_id", "recipe_id", "image_url"],
    "recipe_step": ["step_id", "recipe_id", "step_number", "instruction", "image_url"],
}


class Response:
    def __init__(self, status, body=None):
        self.status = status
        self.body = body  # dict, list o None


class ResponseBuilder:
    @staticmethod
    def to_dict(table, entity):
        return {name: getattr(entity, name) for name in RESPONSE_FIELDS[table]}

    @staticmethod
    def ok(table, entity):
        return Response(200, ResponseBuilder.to_dict(table, entity))

    @staticmethod
    def ok_list(table, entities):
        return Response(200, [ResponseBuilder.to_dict(table, e) for e in entities])

    @staticmethod
    def created(table, entity):
        return Response(201, ResponseBuilder.to_dict(table, entity))

    @staticmethod
    def no_content():
        return Response(204)

    @staticmethod
    def bad_request(message):
        return Response(400, {"error": message})

    @staticmethod
    def not_found(message="Not found"):
        return Response(404, {"error": message})

    @staticmethod
    def server_error(message="Internal error"):
        return Response(500, {"error": message})
