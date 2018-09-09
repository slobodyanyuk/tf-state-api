import re
from flask_restful import Resource
from flask import Flask, request, jsonify, current_app, make_response

class TfStateSgs(Resource):

    def __init__(self, db):
        self.data = db

    def delete(self, resource_id):
        try:
            self.data.delete(resource_id)
            return jsonify({'success':True})
        except KeyError:
            return make_response(jsonify({'success':False}), 404)

    def get(self):
        sgs = self.data.get()
        resp = {}
        if request.args.get('source_security_group_id'):
            for sg in sgs:
                for attribute in sgs[sg]['primary']['attributes']:
                    if re.match(r'^(egress|ingress)\.\d+\.security_groups\.\d+',
                                attribute):
                        if sgs[sg]['primary']['attributes'][attribute] ==\
                                request.args.get('source_security_group_id'):
                            resp.update({sg: sgs[sg]})
            return jsonify(resp)
        elif request.args.get('vpc_id'):
            for sg in sgs:
                for attribute in sgs[sg]['primary']['attributes']:
                    if attribute == 'vpc_id':
                        if sgs[sg]['primary']['attributes'][attribute] ==\
                                request.args.get('vpc_id'):
                            resp.update({sg: sgs[sg]})
            return jsonify(resp)
        else:
            return jsonify(list(self.data.get().keys()))

    def post(self):
        payload = request.get_json()
        if payload['terraform_version'] != current_app.config['tf_version']:
            return make_response(jsonify({'message':'Unspuported Terraform state file',
                                          'success':False}), 400)
        for module in payload['modules']:
            for resource in module['resources']:
                if resource.startswith('aws_security_group.'):
                    self.data.set({resource: module['resources'][resource]})
        return jsonify({'success':True})