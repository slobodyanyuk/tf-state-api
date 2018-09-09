# Simple Flask based RESTful API
A RESTful API application for parsing Terrafrom state data

This application receives Terrafrom state as JSON input, retrives **aws_security_group** entries from it and stores to inmemory hashtable.
Later you can update, retrive and delete data

## Installation & Run
You must have docker and docker-compose installed

```bash
# Download this project
git clone github.com/
# Change directory to project
cd 
# 
```

## API

#### /tfstate
* `GET` : Get Security Groups list
* `POST` : Create/Update Security Groups

#### /tfstate?vpc_id=<VPC id in AWS fromat>
* `GET` : Get Security Groups that reside in specific VPC

#### /tfstate?source_security_group_id=<SG id in AWS fromat>
* `GET` : Get Security Groups that reference specific SG in egress/ingress rules

#### /tfstate/:security_group
* `DELETE` : Delete a Security Group
