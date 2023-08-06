# Más Móvil Python API client

This Python API client provides access to Más Móvil's B2B REST API.

## Installation

### Requirements

* Python 3.8+

## Usage

### Login

To authenticate, you need to specify credentials which need to be set as environment variables with the following names:

```bash
'MM_BASEURL': 'https://api-grupomasmovil.cs86.force.com/cableOperadores/services/apexrest/api'
'MM_USER': 'user'
'MM_PASSWORD': 'pwd'
```
`MM_USER` and `MM_PASSWORD` must be replaced with your actual user credentials. 
For the moment, `MM_BASEURL` points to the testing environement.

### Session creation

The login is done when we create a session using the `Session.create` method:

```python
from pymasmovil.models.session import Session

session = Session.create()

print('Session created with id : {}'.format(session.session_id))
 
```

This `Session` instance should be kept, as is a required paramether for other package functionalities. The reason is that each API call needs to know the session in which the user is logged. 
Example (following the last code snippet): 


### Account usage

```python
from pymasmovil.models.account import Account

account_id = 'example-account-id'
account = Account.get(session, account_id)

```
To create a new account we need to use `Account.create` passing as key-word arguments with the new account information. The `Account` attributes are listed bellow, corresponding with the parameters (as strings) that could be sent when creating a new account (except `id`). 

```
town, surname, stair, roadType, roadNumber, roadName, region, province, postalCode, phone, name, id, flat, email, door, donorCountry, documentType, documentNumber, corporateName, buildingPortal
```
No attribute is compulsary, and parameter validation is done by the API at present.

```python
from pymasmovil.models.account import Account

account = Account.create(session, town='example-town', surname='sample-surname', phone='sample-phone')
```

### Order-item usage

Order-items can be accessed the same way it's done with accounts:

```python
from pymasmovil.models.order_items.py import OrderItem

order_item_id = 'example-order-item-Id'
order_item = OrderItem.get(session, order_item_id)
```

Concurrently, order-items can be created following the account creation example, but the structure of its attributes is a little more complicated. 
Since GET /order-item/:id response and the POST /order-item request don't match except for a few attributes, for the moment to create an order-item we require the minimum structure that the POST request can accept and that we can map to build an OrderItem instance.

The minimum structure is presented as the variable `sample-order-item-post-request`: 


```python
from pymasmovil.models.order_items.py import OrderItem

sample-order-item-post-request = {
    'lineInfo': [
        {
            'name': '',
            'surname': '',
            'phoneNumber': '',
            'documentType': '',
            'portabilityDate': '',
            'iccid_donante': '',
            'iccid': '',
        }
    ]
}

order_item = OrderItem.create(session, sample-order-item-post-request)

```

## Development

### Python version

We use [Pyenv](https://github.com/pyenv/pyenv) to fix the Python version and the virtualenv to develop the package.

You need to:

* Install and configure [`pyenv`](https://github.com/pyenv/pyenv)
* Install and configure [`pyenv-virtualenvwrapper`](https://github.com/pyenv/pyenv-virtualenvwrapper)
* Install the required Python version:

```
$ pyenv install 3.8.2
```

* Create the virtualenv:

```
$ pyenv virtualenv 3.8.2 pymasmovil
```

### Python packages requirements

 Install the Python packages in the virtual environment:

 ```
 $ pyenv exec pip install -r requirements.txt
 ```

## License

TBD
