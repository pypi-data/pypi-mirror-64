import requests, json;
import sseclient as sse;
from .errors import *

class User:
    """ Класс, отвечающий за авторизацию пользоватедя или бота. Будет выброшено исключение при ошибке. """
    
    def __init__ (self, key):
    
        self.key = key;
        self.v = "1.0";
        self.domain = "https://api.yunnet.ru";
        
        result = json.loads(requests.post(self.domain, data = {
            "key": self.key,
            "v": self.v,
            "method": "users.get",
            "user_ids": "0,"
        }).text);
        
        if 'error' in result:
            raise AuthError(result['error']['error_message']);
        
        if result['items'][0]['account_type'] == 'bot':
            self.account_id = int(result['items'][0]['bot_id']);
        else:
            self.account_id = int(result['items'][0]['user_id']);

        return None;
        
    def setAPI (settings = {"domain": "https://api.yunnet.ru", "v": "1.0"}):
        self.domain = settings["domain"];
        self.v = settings["v"];
        
        return True;
        

class API (object):
    """Удобное обращение к методам. Простите за копирование кода :)"""

    __slots__ = ('_account', '_method');
    
    def __init__(self, unt, method = None):
        self._account = unt;
        self._method = method;
        
    def __getattr__(self, method):
        key = self._account.key;
        
        return API(self._account, (self._method + '.' if self._method else '') + method);
            
    def __call__(self, **kwargs):
    
        kwargs['method'] = ''.join(self.method._method.split('.method'));
        kwargs['v'] = self._account.v;
        kwargs['key'] = self._account.key;
  
        r = json.loads(requests.post(self._account.domain, data = kwargs).text);

        if 'error' in r:
            raise APIError('[' + str(r['error']['error_code']) + '] ' + r['error']['error_message']);
            
        return r;
        
class getLongPoll (API):
    """Класс для long poll!"""

    def __init__ (self, executor, SSE = False):
        if SSE:
            sseobj = self.getURL(executor, mode='sse');
            self.Poll = sse.SSEClient(sseobj);
            self.SSE = True;
        else:
            self.url = self.getURL(executor, mode='polling');
            self.SSE = False;
            self.last_event_id = '0';
        
        return None;
        
    def listen(self, callback):
        if self.SSE:
            for event in self.Poll.events():
                callback(json.loads(event.data));
        else:
            try:
                event = requests.get(self.url+'&last_event_id='+self.last_event_id);
                event.encoding = 'utf8';
                
                event = json.loads(event.text);
                
                self.last_event_id = str(event['last_event_id']);
            except requests.exceptions.ConnectionError:
                return self.listen(callback);
        
            callback(event);
            
            return self.listen(callback);
    
    def getURL (self, e, mode):
        url = e.realtime.connect(mode=mode)['response']['url'];
        if mode == 'polling':
            return url;
        
        return requests.get(url, stream=True);
        
class Uploader (API):
    """ Загрузчик файлов """
    
    def __init__ (self, e, path):
        self.path = path;
        self.e = e;
        
    def Upload(self):
        path = self.path;
        e = self.e;
        
        url = e.uploads.getUploadLink(type='image')['response']['url'];
        
        try:
            wrapper = open(path, 'rb');
        except OSError:
            try:
                with open('tmp', 'wb') as handle:
                    response = requests.get(path, stream=True);
                    
                    if not response.ok:
                       raise UploadError('Error while uploading');
                       
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)
                        
                wrapper = open(handle.name, 'rb');
                
            except:
                raise UploadError('Error while uploading');
        
        res = json.loads(requests.post(url, files = {'image':  wrapper}).text);
        
        if 'error' in res:
            raise UploadError('[' + str(res['error']['error_code']) + '] ' + res['error']['error_message']);
        
        return res;