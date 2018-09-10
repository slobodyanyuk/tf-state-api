# Simple Flask based RESTful API
A RESTful API application for parsing Terrafrom state data

This application receives Terrafrom state as JSON input, retrives **aws_security_group** entries from it and stores to inmemory hashtable.
Later you can update, retrive and delete data

## Installation & Run
You must have docker and docker-compose installed

```bash
# Download this project
git clone git@github.com:slobodyanyuk/tf-state-api.git
# Change directory to project
cd tf-state-api
# Build and run the project
docker-compose up 
```

Upload sample data into the application
```bash
curl -H "Content-Type: application/json" -X POST -d@sample_data/terraform_test.tfstate http://127.0.0.1:8081/tfstate
```
List Security Groups
```bash
curl http://127.0.0.1:8081/tfstate
```
Get SG by VPC
```bash
curl http://127.0.0.1:8081/tfstate?vpc_id=vpc-000000aa
```
Get SG by referenced SG id
```bash
curl http://127.0.0.1:5000/tfstate?source_security_group_id=sg-0000000ab
```
Delete SG from API by name
```bash
curl -X DELETE http://127.0.0.1:8081/tfstate/aws_security_group.test2
```
Check results by listing Security Groups
```bash
curl http://127.0.0.1:8081/tfstate
```
Update data by uploading state again
```bash
curl -H "Content-Type: application/json" -X POST -d@sample_data/terraform_test.tfstate http://127.0.0.1:8081/tfstate
```
Check results by listing Security Groups
```bash
curl http://127.0.0.1:8081/tfstate
```
Test Nginx rate limit
```bash
ab -c 20 -n 100  http://127.0.0.1:8081/tfstate?vpc_id=vpc-000000aa
```

## API

#### /tfstate
* `GET` : Get Security Groups list
* `POST` : Create/Update Security Groups

#### /tfstate?vpc_id=\<VPC id in AWS fromat\>
* `GET` : Get Security Groups that reside in specific VPC

#### /tfstate?source_security_group_id=\<SG id in AWS fromat\>
* `GET` : Get Security Groups that reference specific SG in egress/ingress rules

#### /tfstate/:security_group
* `DELETE` : Delete a Security Group

## Tests
Tests to be run inside backend image
```
# Once docker image was built
docker run --rm tf-state-api_backend python3 test.py
```
