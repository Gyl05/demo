import time

class MiniWeb:
    def __init__(self) -> None:
        self.URL_ROUTE = {
            "GET": {}
        }

    def get(self, route: str):  # 返回一个装饰器
        def route_decorator(func):
            self.URL_ROUTE["GET"][route] = func
            def new_func(*args, **kwargs):
                return func(*args, **kwargs)
            return new_func
        return route_decorator

app = MiniWeb()
print(app.URL_ROUTE)

@app.get('/login.py')
def login():
    return '登录' + time.ctime()

@app.get('/register.py')
def register():
    return '注册' + time.ctime()

def page_404():
    return '不存在的动态页面' + time.ctime()

print(app.URL_ROUTE)

def application(env, call_func):
    path_info = env.get("PATH_INFO")
    http_method = env.get("REQUEST_METHOD")
    call_func("200 OK", [("Content-Type", "text/html;charset=utf-8"), ("framework", "mini_web")])
    if path_info not in app.URL_ROUTE:
        call_func("404 not found", [("Content-Type", "text/html;charset=utf-8"), ("framework", "mini_web")])
        return page_404()
    return app.URL_ROUTE[http_method][path_info]()