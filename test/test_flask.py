import pytest
from flask import jsonify

from src.webapp import app
# pytest test/test_flask.py -W ignore::DeprecationWarning



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestFlaskApp:

    def test_homepage(self, client):
        response = client.get('/')
        assert response.status_code == 200

    
    def test_wrong_api(self, client):
        response = client.get('/index')
        assert response.status_code == 404
    
    def test_find_route_no_data(self, client):
        response =  client.post(
            '/find_route',
            data=None,
        )
        assert response.data.decode("utf-8") == "The request does not have all required fields"
        assert response.status_code == 400

    def test_find_route_wrong_request(self, client):
        response =  client.post(
            '/find_route',
            data="",
            follow_redirects=True
        )
        assert response.data.decode("utf-8") == "The request does not have all required fields"
        assert response.status_code == 400

    def test_find_route_with_no_arguments(self, client):
        response =  client.post(
            '/find_route',
            data=dict(),
            follow_redirects=True
        )
        assert response.data.decode("utf-8") == "The request does not have all required fields"
        assert response.status_code == 400
    

    # def test_find_route(self, client):
    #     with app.app_context():

    #         data_dict_ = {'source': '115 Brittany Manor Drive, Amherst, MA, USA', 
    #         'dest': 'Groff Park, Mill Lane, Amherst, MA, USA', 
    #         'algo': 'astar', 
    #         'percent': '150', 
    #         'elevationtype': 'minimize'}

    #         response =  client.post(
    #             '/find_route',
    #             data = data_dict_,
    #             follow_redirects=True
    #         )
    #         print(response)
    #         assert response.status_code == 200