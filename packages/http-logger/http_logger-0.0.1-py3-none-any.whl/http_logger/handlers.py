import logging

import threading

def reqthread(h, data):
    h.send(data.encode('utf-8'))
    h.getresponse()    #can't do anything with the result

class HTTPAuthTokenHandler(logging.Handler):
    """
    A class which sends records to a Web server, using either GET or
    POST semantics.
    """
    def __init__(self, host, url, method="GET", secure=False, credentials=None,
                 context=None, log_name=None, auth_key=None):
        assert log_name, "HTTPAuthTokenHandler requires a log_name argument"
        self.log_name = log_name
        assert auth_key,  "HTTPAuthTokenHandler requires an auth_key argument"
        self.auth_key = auth_key
        """
        Initialize the instance with the host, the request URL, and the method
        ("GET" or "POST")
        """
        logging.Handler.__init__(self)
        method = method.upper()
        if method not in ["GET", "POST"]:
            raise ValueError("method must be GET or POST")
        if not secure and context is not None:
            raise ValueError("context parameter only makes sense "
                             "with secure=True")
        self.host = host
        self.url = url
        self.method = method
        self.secure = secure
        self.credentials = credentials
        self.context = context

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz Glasner.
        """
        return record.__dict__

    def getConnection(self, host, secure):
        """
        get a HTTP[S]Connection.
        Override when a custom connection is required, for example if
        there is a proxy.
        """
        import http.client
        if secure:
            connection = http.client.HTTPSConnection(host, context=self.context)
        else:
            connection = http.client.HTTPConnection(host)
        return connection

    def emit(self, record):
        """
        Emit a record.
        Send the record to the Web server as a percent-encoded dictionary
        """
        try:
            import urllib.parse
            host = self.host
            h = self.getConnection(host, self.secure)
            url = self.url + "?name={}".format(str(self.log_name))
            data = urllib.parse.urlencode(self.mapLogRecord(record))
            if self.method == "GET":
                raise NotImplementedError("USE GET PLZ")
                if (url.find('?') >= 0):
                    sep = '&'
                else:
                    sep = '?'
                url = url + "%c%s" % (sep, data)
            h.putrequest(self.method, url)
            # support multiple hosts on one IP address...
            # need to strip optional :port from host, if present
            i = host.find(":")
            if i >= 0:
                host = host[:i]
            # See issue #30904: putrequest call above already adds this header
            # on Python 3.x.
            # h.putheader("Host", host)
            if self.method == "POST":
                h.putheader("Content-type",
                            "application/x-www-form-urlencoded")
                h.putheader("Authorization",f"Token {self.auth_key}")
                h.putheader("Content-length", str(len(data)))
            if self.credentials:
                import base64
                s = ('%s:%s' % self.credentials).encode('utf-8')
                s = 'Basic ' + base64.b64encode(s).strip().decode('ascii')
                h.putheader('Authorization', s)
            h.endheaders()
            t = threading.Thread(target=reqthread, args=(h,data,))
            t.daemon = True
            t.start()
        except Exception:
            self.handleError(record)