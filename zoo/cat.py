from flask_restx import Namespace, Resource, fields

api = Namespace("cats", description="Cats related operations")

cat = api.model(
    "Cat",
    {
        "id": fields.String(required=True, description="The cat identifier"),
        "name": fields.String(required=True, description="The cat name"),
        "color": fields.String(required=True, description="Color of the cat")
    },
)

CATS = [
    {"id": "felix", "name": "Felix", "color": "tabby"},
]

add_cat_parser = api.parser()
add_cat_parser.add_argument(
    "name", type=str, required=True, help="Name of your cat", location="form"
    )
add_cat_parser.add_argument(
    "color", type=str, required=True, help="Color of your cat", location="form"
    )

update_cat_parser = api.parser()
update_cat_parser.add_argument(
    "name", type=str, required=False, help="Name of your cat", location="form"
    )
update_cat_parser.add_argument(
    "color", type=str, required=False, help="Color of your cat", location="form"
    )


@api.route("/")
class CatList(Resource):
    @api.doc("list_cats")
    @api.marshal_list_with(cat)
    def get(self):
        """List all cats"""
        return CATS

    @api.doc(parser=add_cat_parser)
    @api.response(201, "Cat created")
    @api.response(409, "Cat already exists")
    def post(self):
        """Add a new cat"""
        args = add_cat_parser.parse_args()
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


@api.route("/<id>")
@api.param("id", "The cat identifier")
@api.response(404, "Cat not found")
class Cat(Resource):
    @api.doc("get_cat")
    @api.marshal_with(cat)
    def get(self, id):
        """Fetch a cat given its identifier"""
        for cat in CATS:
            if cat["id"] == id:
                return cat
        return "Can not found", 404

    @api.doc("delete_cat")
    @api.response(204, "Cat deleted")
    def delete(self, id):
        """ Delete a cat given it's identifier """
        for cat in CATS:
            if cat["id"] == id:
                CATS.remove(cat)
                return "Cat deleted", 204
        return "Cat not found", 404

    @api.doc("update_cat")
    @api.doc(parser=update_cat_parser)
    @api.response(200, "Cat updated")
    def put(self, id):
        """ Update a cat given it's identifier """
        args = update_cat_parser.parse_args()

        for cat in CATS:
            if cat["id"] == id:
                if args["name"] != "":
                    cat["name"] = args["name"]
                if args["color"] != "":
                    cat["color"] = args["color"]
                return "Cat updated", 200
        return "Cat not found", 404
