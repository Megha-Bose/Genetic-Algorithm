import json
import requests
import numpy as np

API_ENDPOINT = 'http://10.4.21.156'
MAX_DEG = 11
SECRET_KEY='jg3q0CzLVQl9Jsf4PmLIUjuxMK4yU7Vh4b6FzthUbocuLqpvGG'

vector_overfit = [0.0, -1.457990220064754e-12, -2.2898007842769645e-13, 4.620107525277624e-11, -1.7521481289918844e-10, -1.8366976965696096e-15, 8.529440604118815e-16, 2.2942330256117977e-05, -2.0472100298772093e-06, -1.597928341587757e-08, 9.982140340891233e-10]
vector_29 = [
                0.0,
                -1.4709674148197378e-12,
                9.458679750040452e-14,
                5.94423542227152e-11,
                -2.2653991408652525e-10,
                -1.48230540861011e-15,
                7.011819656124058e-16,
                2.5296736507025282e-05,
                -1.676070771376038e-06,
                -1.3683227552671525e-08,
                7.533411281712756e-10
            ]
vector_start = [
                    0.0,
                    -1.480069708489244e-12,
                    9.94931131796432e-14,
                    5.90268406709987e-11,
                    -1.0780047433314992e-10,
                    -1.2371033759122053e-15,
                    -9.6624985767082e-17,
                    2.6357565162742792e-05,
                    -1.5686157913082572e-06,
                    -1.426733732328146e-08,
                    7.239407993539595e-10
                ]

vector_rank_8 = [
                    0.0,
                    -1.636269914275464e-12,
                    1.1387845708098366e-13,
                    6.438196812672346e-11,
                    -1.0245544007424188e-10,
                    -9.860172743032326e-16,
                    -1.2802827441370585e-16,
                    0.0,
                    -1.836392570609916e-06,
                    0.0,
                    7.29667055051756e-10
                ]

vector_rank_12 = [
                        0.0,
                        -1.597105924245191e-12,
                        2.198934018367277e-14,
                        3.491044484088095e-11,
                        6.855029194610278e-13,
                        0.0,
                        -6.726699633209086e-17,
                        0.0,
                        -1.7670843276135381e-06,
                        0.0,
                        6.955956541923088e-10
                    ]

def urljoin(root, path=''):
    if path: root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root

def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id':id, 'vector':vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response

def get_errors(id, vector):
    # print("DFSFSF")
    # print(vector)
    for i in vector: assert 0<=abs(i)<=10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))

def get_overfit_vector(id):
    return json.loads(send_request(id, vector_overfit, 'getoverfit'))

# Replace 'SECRET_KEY' with your team's secret key (Will be sent over email)
# if __name__ == "__main__":
#     print(get_errors(SECRET_KEY, get_overfit_vector(SECRET_KEY)))
#     print(get_overfit_vector(SECRET_KEY))

def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector: assert 0<=abs(i)<=10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')

# # Replace 'SECRET_KEY' with your team's secret key (Will be sent over email)
# if __name__ == "__main__":
#     print(get_errors('SECRET_KEY', get_overfit_vector('SECRET_KEY')))
#     print(get_overfit_vector('SECRET_KEY'))
#     print(submit('SECRET_KEY', get_overfit_vector('SECRET_KEY')))
