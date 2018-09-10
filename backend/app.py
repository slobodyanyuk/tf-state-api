from flask import Flask
from flask_restful import Api
from resources.controller import TfStateSgs
from db.inmem import InMem

application = Flask(__name__)
application.config['tf_version'] = '0.11.3'
api = Api(application)

db = InMem()

api.add_resource(TfStateSgs, '/tfstate',
        resource_class_kwargs={'db': db})
api.add_resource(TfStateSgs, '/tfstate/<string:resource_id>',
                 endpoint='resourcefull',
                 resource_class_kwargs={'db': db})

# Used to run app with Flask built in web server locally
if __name__ == '__main__':
    application.debug = True
    application.run(host = '0.0.0.0',port=5000)
