
"""
A Python client package for accessing data from an API that uses the Consumer Data Standards.

Generated using the Swagger-Codegen CLI from a Swagger specification file of the Consumer Data Standards. 

NOT part of the official Consumer Data Standards' Project, nor any API implementation of the Standards. 
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "cds-api-client"
VERSION = "0.0.1"

REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23"
]
    

setup(
    name=NAME,
    version=VERSION,
    description="Python client package for accessing data from an API that uses the Consumer Data Standards (CDS)",
    url="https://github.com/stephenmccalman/cds-python-api-client.git",
    author="Stephen McCalman",
    author_email="cds-api-client@googlegroups.com",
    keywords=["Swagger", "Consumer Data Standards"],
    license="BSD",
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=
    """
# CDS API CLIENT

A Python client package for accessing data from an API that follows the [Consumer Data Standards](https://consumerdatastandardsaustralia.github.io/standards).

You are welcome to [install](#installation) and [use](#basic-usage) this package. But before doing so:
* read about the [origin](#about-this-package) of this package; and
* consult API providers documentation for details on the availability of their API endpoints and data resources; and
* review the package's license.

Also, bear in mind that this package is NOT part of the official Consumer Data Standards' project, nor any API implementation of the Standards.

## Installation

To install:

```sh
pip install cds-api-client --user
```

You can install the latest of this package directly from Github (using pip):

```sh
pip install git+https://github.com/stephenmccalman/cds-python-api-client.git --user
```

## Basic usage

To access Products data from a bank API that follows the Consumer Data Standards:

```python
import cds
from cds.rest import ApiException
from pprint import pprint
configuration = cds.Configuration()
configuration.host = 'https://data.holder.com.au' + '/cds-au/v1'
api_client = cds.ApiClient(configuration)

products_api = cds.ProductsApi(api_client)

try:
    products_list = products_api.list_products(x_v='1')  # use x_v='2' from August 2020
except ApiException as e:
    print(e)
    
pprint(products_list.data)
```   

Replace `https://data.holder.com.au` with the API host address of a bank; see [api documentation pages](#api-documentation-pages).

## About this package

I generated this package with an open-source Java CLI (swagger-codegen-cli-2.4.12.jar) that I downloaded from the [Swagger Codegen Project](https://github.com/swagger-api/swagger-codegen/#generators)'s [Maven repository](https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.12/). 

The Swagger-Codegen CLI generates an API client package from a Swagger specification file; the specification file is a JSON- (or YAML-) formated text file that lists the endpoint paths and data (model) definitions of an API (or a group of APIs). 

The CLI generates the package's files from a set of templates that it fills with information it retrieves from the Swagger specification file.

To generate this package, I used a Swagger specification file of the Consumer Data Standards (1.2.0), which I downloaded from the Standards' [Github page](https://consumerdatastandardsaustralia.github.io/standards).
     
The CLI comes with a set of generic templates built in. Before generating this package, I extracted these templates from the CLI and modified a few of them to better document the package.

See the https://github.com/stephenmccalman/cds-python-api-client.git for further details.

## API documentation pages

Below lists the links to API documentation pages of the four major banks:

* [Commnonwealth Bank of Australia (CBA)](https://www.commbank.com.au/Developer/)
* [National Australia Bank (NAB)](https://developer.nab.com.au/products)
* [Australia and New Zealand (ANZ) Banking Group](https://www.anz.com.au/support/anz-apis/)
* [Westpac Banking Corporation (WBC)](https://www.westpac.com.au/about-westpac/innovation/open-banking/)

""",
    long_description_content_type="text/markdown"
)
