from flask_restx import Namespace, Resource, fields

api = Namespace("cats", description="Cats related operations")

"""
Learning notes:
- The documentation for each of the functions in each class is automagically sourced by RestX into
    the swagger documentation. First line is shown in the collapsed view, all other lines of
    documentation show up in the expanded view.
- The namespace is the first part of the URI, and the api.route() extends that (thus giving you the
    full URI route to each API call)
"""

"""
Cat model. Defines which fields are required and optional for the data model.
Some sort of ID should be used.
"""
cat = api.model(
    "Cat",
    {
        "id": fields.String(required=True, description="The cat identifier"),
        "name": fields.String(required=True, description="The cat name"),
        "color": fields.String(required=True, description="Color of the cat")
    },
)

# Used in place of a proper backend (such as a database) for simplicity
CATS = [
    {"id": "felix", "name": "Felix", "color": "tabby"},
]

"""
Parser for editing a whole cat model. Requires the cat calready exist (so that we cna reference
it's id). All fields must be filled.
"""
cat_parser = api.parser()
cat_parser.add_argument(
    "name", type=str, required=True, help="Name of your cat", location="form"
    )
cat_parser.add_argument(
    "color", type=str, required=True, help="Color of your cat", location="form"
    )

"""
Patching a cat. Requires the cat exist, but does not require any of the fields to be filled
(only filled fields will be passed via the patch call)
"""
patch_cat_parser = api.parser()
patch_cat_parser.add_argument(
    "name", type=str, required=False, help="Name of your cat", location="form"
    )
patch_cat_parser.add_argument(
    "color", type=str, required=False, help="Color of your cat", location="form"
    )

"""
Note that this route is relative to the Namespace, defined above. Therefore this route is actually
URL/cats/
"""
@api.route("/")
class CatList(Resource):
    """
    Lists all the cats in the array.

    api.doc decorator adds documentation to swagger API reference page.
    api.marshall_list_with makes sure the list is returned properly formatted by the cat model.

    :return: List containing all the cats.
    :rtype: List
    """
    @api.doc("list_cats")
    @api.marshal_list_with(cat)
    def get(self):
        """List all cats"""
        return CATS

    """
    Adds a cat to the list.

    api.doc specifies the parser used to properly define the input and extract data from the post
    message.
    api.responses define the documentation for each response code type returned.

    :return: Custom message, HTTP response code
    :rtype: Tuple
    """
    @api.doc(parser=cat_parser)
    @api.response(201, "Cat created")
    @api.response(409, "Cat already exists")
    def post(self):
        """Add a new cat"""
        args = cat_parser.parse_args()
        for dict in CATS:
            if args["name"] in dict.values():
                return "Cat already exists", 409
        else:
            CATS.append(
                {"id": args["name"],
                 "name": args["name"],
                 "color": args["color"]}
                )
            return "Cat created", 201


"""
As above, this is relative to the root URL, thus all urls under this class appear at
URL/cats/{id}
api.param and api.response decorators on the class are passed to each method in the class to
properly document each method in the swagger API reference.
"""
@api.route("/<id>")
@api.param("id", "The cat identifier")
@api.response(404, "Cat not found")
class Cat(Resource):

    """
    Get cat with specified ID.

    If the cat is not found, returns a custom error message, and a 404 error code.
    api.doc defines the proper documentation for the swagger reference

    :return: Python String representation of the cat Dict Object with ID specified.
    :rtype: Dict String representation
    """
    @api.doc("get_cat")
    @api.marshal_with(cat)
    def get(self, id):
        """Fetch a cat given its identifier. """
        for cat in CATS:
            if cat["id"] == id:
                return cat
        return "Can not found", 404

    """
    Delete cat with specified ID and return HTTP code 204.

    If cat does not exist, return a custom error message, and a 404 error code.
    api.doc defines the proper documentation for the swagger reference
    api.response defines the proper documentation for the swagger reference to capture the
    different HTTP error codes that can be returned.

    :return: Custom message, HTTP return code
    :rtype: Tuple
    """
    @api.doc("delete_cat")
    @api.response(204, "Cat deleted")
    def delete(self, id):
        """ Delete a cat given it's identifier. """
        for cat in CATS:
            if cat["id"] == id:
                CATS.remove(cat)
                return "Cat deleted", 204
        return "Cat not found", 404

    """
    Update a cat with new data.

    api.doc defines the proper documentation for the swagger reference, both for update_cat and
    to define the parser used to interpret the put command.
    api.response defines the proper documentation for the swagger reference to capture the
    different HTTP error codes that can be returned.

    :return: Custom error message, HTTP return code
    :rtype: Tuple
    """
    @api.doc("update_cat")
    @api.doc(parser=cat_parser)
    @api.response(200, "Cat updated")
    @api.response(400, "Updating a cat requires a name and a color")
    def put(self, id):
        """ Update a cat given it's identifier. Requires a name and a color. """
        args = cat_parser.parse_args()

        for cat in CATS:
            if cat["id"] == id:
                if args["name"] is None or args["color"] is None:
                    return "Updating a cat requires a name and a color", 400
                else:
                    cat["name"] = args["name"]
                    cat["color"] = args["color"]
                return "Cat updated", 200
        return "Cat not found", 404

    """
    Update a cat with new data, not requiring all data to be updated.

    api.doc defines the proper documentation for the swagger reference, both for update_cat and
    to define the parser used to interpret the put command.
    api.response defines the proper documentation for the swagger reference to capture the
    different HTTP error codes that can be returned.

    :return: Custom error message, HTTP return code
    :rtype: Tuple
        """
    @api.doc("update_cat")
    @api.doc(parser=patch_cat_parser)
    @api.response(200, "Cat updated")
    def patch(self, id):
        """
        Patch a cat given it's identifier.
        Requires a name and / or a color.
        """
        args = patch_cat_parser.parse_args()

        for cat in CATS:
            if cat["id"] == id:
                if args["name"] is not None:
                    cat["name"] = args["name"]
                if args["color"] is not None:
                    cat["color"] = args["color"]
                return "Cat updated", 200
        return "Cat not found", 404
