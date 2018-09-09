import unittest
from app import application

class BasicTests(unittest.TestCase):

    def setUp(self):
        application.config['TESTING'] = True
        self.application = application.test_client()
        self.sample = {
            "terraform_version": "0.11.1",
            "modules": [{
                "resources": {
                    "aws_security_group.test1": {
                        "primary": {
                            "attributes": {
                                "vpc_id": "vpc-000000aa",
                                "ingress.0000000000.security_groups.0000000000": "sg-0000000aa"
                            }
                        }
                    },
                    "aws_security_group.test2": {
                        "primary": {
                            "attributes": {
                                "vpc_id": "vpc-000000aa",
                                "ingress.0000000000.security_groups.0000000000": "sg-0000000ab"
                            }
                        }
                    }
                }
            }]
        }
        self.assertEqual(application.debug, False)

    def tearDown(self):
        pass

    def test_1_empty_resp(self):
        response = self.application.get('/tfstate')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'[]\n')

    def test_2_post_state(self):
        response = self.application.post('/tfstate', json=self.sample)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"success":true}\n')

    def test_3_sgs_list(self):
        response = self.application.get('/tfstate')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'["aws_security_group.test1","aws_security_group.test2"]\n')

    def test_4_vpc_id_search(self):
        response = self.application.get('/tfstate?vpc_id=vpc-000000aa')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json().keys()), 2)

    def test_5_sg_id_search(self):
        response = self.application.get('/tfstate?source_security_group_id=sg-0000000ab')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json().keys()), 1)

    def test_6_delete(self):
        response = self.application.delete('/tfstate/aws_security_group.test2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"success":true}\n')

    def test_7_vpc_id_search(self):
        response = self.application.get('/tfstate?vpc_id=vpc-000000aa')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json().keys()), 1)

if __name__ == "__main__":
    unittest.main()