# forpay_client  
SDK For Forpay  
API Link: [Forpay](https://api.forpay.pro/docs/overview)  
  
## Install
  
```
pip install forpay-client
```
  
## Usage  

```
from forpay_client.forpay import ForPayClient
client = ForPayClient(app_id='app_id', key_id='key_id', private_key='private_string')
reply, ok = client.get_currencies()
print(reply, ok)
```  
  
## License  

MIT © bozimeile  
