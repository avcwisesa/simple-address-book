from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

ADDRESSES = {
    '1': {
        'name': 'Imam Rachbini',
        'address': 'Jl. Margonda Raya',
        'phone_no': '770123456',
    },
}


def abort_if_address_doesnt_exist(addr_id):
    if addr_id not in ADDRESSES:
        abort(404, message="Address {} doesn't exist".format(addr_id))

parser = reqparse.RequestParser()
parser.add_argument('address', type=str)
parser.add_argument('name', type=str)
parser.add_argument('phone_no', type=str)


# address
# shows a single address item and lets you delete a address item
class Address(Resource):
    def get(self, addr_id):
        abort_if_address_doesnt_exist(addr_id)
        return ADDRESSES[addr_id]

    def delete(self, addr_id):
        abort_if_address_doesnt_exist(addr_id)
        del ADDRESSES[addr_id]
        return '', 204

    def put(self, addr_id):
        args = parser.parse_args()
        addr = {
            'name': args['name'],
            'address': args['address'],
            'phone_no': args['phone_no'],
        }
        ADDRESSES[addr_id] = addr
        return addr, 201


# AddressList
# shows a list of all ADDRESSES, and lets you POST to add new tasks
class AddressList(Resource):
    def get(self):
        return ADDRESSES

    def post(self):
        args = parser.parse_args()
        addr_id = int(max(ADDRESSES.keys()).lstrip('address')) + 1
        addr_id = '%i' % addr_id
        ADDRESSES[addr_id] = {
            'name': args['name'],
            'address': args['address'],
            'phone_no': args['phone_no'],
        }
        return ADDRESSES[addr_id], 201

##
## Actually setup the Api resource routing here
api.add_resource(AddressList, '/addresses')
api.add_resource(Address, '/addresses/<addr_id>')


if __name__ == '__main__':
    app.run(debug=True)