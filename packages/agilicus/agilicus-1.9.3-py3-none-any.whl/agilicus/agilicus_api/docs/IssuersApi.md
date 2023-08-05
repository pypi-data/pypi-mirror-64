# agilicus_api.IssuersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clients_delete**](IssuersApi.md#clients_delete) | **DELETE** /v1/issuers/{issuer_id}/clients/{client_id} | Delete a client
[**clients_get**](IssuersApi.md#clients_get) | **GET** /v1/issuers/{issuer_id}/clients/{client_id} | Get client
[**clients_post**](IssuersApi.md#clients_post) | **POST** /v1/issuers/{issuer_id}/clients | Create a client
[**clients_put**](IssuersApi.md#clients_put) | **PUT** /v1/issuers/{issuer_id}/clients/{client_id} | Update a client
[**clients_query**](IssuersApi.md#clients_query) | **GET** /v1/issuers/{issuer_id}/clients | Query Clients
[**issuers_delete**](IssuersApi.md#issuers_delete) | **DELETE** /v1/issuers/{issuer_id} | Delete an Issuer
[**issuers_get**](IssuersApi.md#issuers_get) | **GET** /v1/issuers/{issuer_id} | Get issuer
[**issuers_post**](IssuersApi.md#issuers_post) | **POST** /v1/issuers | Create an issuer
[**issuers_put**](IssuersApi.md#issuers_put) | **PUT** /v1/issuers/{issuer_id} | Update an issuer
[**issuers_query**](IssuersApi.md#issuers_query) | **GET** /v1/issuers | Query Issuers


# **clients_delete**
> clients_delete(issuer_id, client_id)

Delete a client

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
client_id = '1234' # str | client_id path

    try:
        # Delete a client
        api_instance.clients_delete(issuer_id, client_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **client_id** | **str**| client_id path | 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Client was deleted |  -  |
**404** | Issuer/Client does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_get**
> IssuerClient clients_get(issuer_id, client_id)

Get client

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
client_id = '1234' # str | client_id path

    try:
        # Get client
        api_response = api_instance.clients_get(issuer_id, client_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **client_id** | **str**| client_id path | 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return client by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_post**
> IssuerClient clients_post(issuer_id, issuer_client)

Create a client

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
issuer_client = agilicus_api.IssuerClient() # IssuerClient | IssuerClient

    try:
        # Create a client
        api_response = api_instance.clients_post(issuer_id, issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **issuer_client** | [**IssuerClient**](IssuerClient.md)| IssuerClient | 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created client |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_put**
> IssuerClient clients_put(issuer_id, client_id, issuer_client)

Update a client

Update a client

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
client_id = '1234' # str | client_id path
issuer_client = agilicus_api.IssuerClient() # IssuerClient | Issuer client

    try:
        # Update a client
        api_response = api_instance.clients_put(issuer_id, client_id, issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **client_id** | **str**| client_id path | 
 **issuer_client** | [**IssuerClient**](IssuerClient.md)| Issuer client | 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Client was updated |  -  |
**404** | Issuer/Client does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clients_query**
> list[IssuerClient] clients_query(issuer_id, limit=limit)

Query Clients

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Query Clients
        api_response = api_instance.clients_query(issuer_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->clients_query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**list[IssuerClient]**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return clients list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_delete**
> issuers_delete(issuer_id)

Delete an Issuer

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path

    try:
        # Delete an Issuer
        api_instance.issuers_delete(issuer_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Issuer was deleted |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_get**
> Issuer issuers_get(issuer_id)

Get issuer

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path

    try:
        # Get issuer
        api_response = api_instance.issuers_get(issuer_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuer by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_post**
> Issuer issuers_post(issuer)

Create an issuer

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer = agilicus_api.Issuer() # Issuer | Issuer

    try:
        # Create an issuer
        api_response = api_instance.issuers_post(issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created issuer |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_put**
> Issuer issuers_put(issuer_id, issuer)

Update an issuer

Update an issuer

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
issuer = agilicus_api.Issuer() # Issuer | Issuer

    try:
        # Update an issuer
        api_response = api_instance.issuers_put(issuer_id, issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issuer was updated |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issuers_query**
> list[Issuer] issuers_query(limit=limit, issuer=issuer)

Query Issuers

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.IssuersApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
issuer = 'example.com' # str | Organisation issuer (optional)

    try:
        # Query Issuers
        api_response = api_instance.issuers_query(limit=limit, issuer=issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->issuers_query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 

### Return type

[**list[Issuer]**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuers list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

