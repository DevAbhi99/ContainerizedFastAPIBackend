import pytest
import requests


baseUrl='http://127.0.0.1:4500'


@pytest.mark.getTest
def testGetMethod():
    response=requests.get(f'{baseUrl}/getData')
    body=response.json()

    assert response.status_code==200
    assert body[0]['id']==1
    assert body[0]['name']=='Subhayan'
    assert body[0]['age']==23
    assert body[0]['priority']==2


@pytest.mark.postTest
def testPostMethod():
    payload={'name':'Karan', 'age':22, 'priority':3}
    response1=requests.post(f'{baseUrl}/sendData', json=payload)
    body1=response1.json()

    assert response1.status_code==200
    assert body1['message']=='Data inserted successfully'

    response2=requests.get(f'{baseUrl}/getData')

    body2=response2.json()

    assert body2['message']=='Data inserted successfully'

    assert body2[1]['id']==2
    assert body2[1]['name']=='Karan'
    assert body2[1]['age']==22
    assert body2[1]['priority']==3


@pytest.mark.updateTest
def testUpdateMethod():

    payload={'name':'Mohit', 'age':22, 'priority':3}

    response1=requests.put(f'{baseUrl}/updateData', json=payload)

    body1=response1.json()

    assert response1.status_code==200

    assert body1['message']=='Data updated successfully'

    response2=requests.get(f'{baseUrl}/getData')

    body2=response2.json()

    assert body2['message']=='Data updated successfully'

    assert body2['name']=='Mohit'


@pytest.mark.deleteTest
def testDeleteMethod():

    response1=requests.delete(f'{baseUrl}/deleteData')

    body1=response1.json()

    assert response1.status_code==200

    assert body1['message']=='Data deleted successfully'


@pytest.mark.clearTest
def testClearMethod():

    response1=requests.delete(f'{baseUrl}/clearData')

    body1=response1.json()

    assert response1.status_code==200

    assert body1['message']=='Data cleared successfully'