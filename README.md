# BasitApi

RESTful API oluşturmanızda size yardımcı olan basit bir kütüphane. Django'nun
sınıf temelli View yapısı üzerine kurulu. Bir RESTful API'de olması gereken
bazı temel özellikleri sunar ve başka da bir işe karışmaz.

Sunduğu bazı temel özellikler:

*   *Bağlantıdaki method parametresi ile HTTP_METHOD başlığının ezilmesi.*

    Bazı istemciler sadece bazı metodları göndermekle kısıtlandırılabilirler. Bu
    türlü bir durumda API'nin doğru çalışabilmesi için bağlantı içinde *method*
    isimli parametreyi kullanabilirsiniz. Bu parametre ile HTTP_METHOD ezilir ve
    gönderdiğiniz method parametresindeki değere göre işlemler yürütülür.

*   *Her zaman 200 HTTP kodu ile dönüş.*

    Bazı istemciler sadece bazı hata kodlarına yanıt verebilirler. BasitApi bu tür durumlar için
    *suppress_response_codes* parametresine destek vermekte. Bu parametre değeri
    1 olarak gönderildiğinde durumu ne olursa olsun tüm yanıtlar 200 kodu ile
    gönderilmekte.

*   *Yanıt formatı.*

    Hem *Accept* başlık bilgisine hem de bağlantı dosya son ekine göre yanıt
    formatı ayarlanabilmekte.


## Kurulum

PyPi üzerinden kurulum için aşağıdaki komutu kullanabilirsiniz:

```
$ pip install basitapi
```

Github üzerinden kurulum için aşağıdaki komutu kullanabilirsiniz:

```
$ pip install -e git://github.com/omerucel/basitapi.git#egg=basitapi
```

## Kullanım

### settings.py

```python
INSTALLED_APPS=(
    ...
    'basitapi'
)
```

### urls.py

Bağlantı dosya son ekine göre yanıt formatını ayarlamak istemiyorsanız
bağlantılarınızı *format_suffix_patterns* ile tekrar formatlamanıza gerek yok!

```python
from basitapi.urlpatterns import format_suffix_patterns
from appname.views import ViewName

urlpatterns = patterns(
    url(r'^foo', ViewName.as_view()),
    ...
)

urlpatterns = format_suffix_patterns(urlpatterns)
```

### views.py

```python

from basitapi.exception import ApiException
from basitapi.response import ApiResponse
from basitapi.views import ApiView

class ViewName(ApiView):
    def get(self, request):
        return ApiResponse({
            'result' : 'data'
        })

    def post(self, request):
        raise ApiException('Bir hata olustu', status=403, application_code=1111)
```
