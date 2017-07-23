from flask.ext.restful import reqparse

user_data_parser = reqparse.RequestParser()
user_data_parser.add_argument('username', type=str, required=True)
user_data_parser.add_argument('password', type=str, required=True)

eld_get_parser = reqparse.RequestParser()
eld_get_parser.add_argument('page', type=int, location=['args', 'headers'])
eld_get_parser.add_argument('user', type=str, location=['args', 'headers'])

eld_post_parser = reqparse.RequestParser()
eld_post_parser.add_argument(
    'token',
    type=str,
    required=False,
    help="Auth token is required to submit data"
)

eld_post_parser.add_argument(
    'user_id',
    type=int,
    required=True,
    help="Need current user"
)

eld_post_parser.add_argument(
    'company_id',
    type=int,
    required=True,
    help="Need current company"
)

eld_post_parser.add_argument(
    'longitude',
    type=int,
    required=False,
    help="Need current longitude"
)
eld_post_parser.add_argument(
    'latitude',
    type=int,
    required = False,
    action='append'
)


eld_post_parser.add_argument(
    'rpm',
    type=int,
    required=False,
    action='append'
)

eld_post_parser.add_argument(
    'daterecorded',
    type=str,
    required=False,
    action='append'
)
