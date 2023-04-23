from pyramid.view import view_config
from pyramid.response import Response
from benford import benford_fun
import csv
import json
from pyramid.config import Configurator

@view_config(route_name='home', renderer='templates/index.html')
def home_view(request):
    return {'title':'Benford Law','message':'Details provided in JSON if the law is satisfied. Else, a message is displayed saying the data does not follow Benford\'s Law.'}

@view_config(route_name="benford",renderer="json")
def benford(request):
    if request.method=='POST' and request.POST['file'].file:
        csv_file = request.POST['file'].file
        filename = request.POST['file'].filename 
        name, ext = filename.split('.')
        if not ext == 'csv':
            return {"Error": "Only takes CSV files."}
        else:
            data=[]
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                data.extend(row)

            valid,results = benford_fun(data)

            if valid== True:
                with open("uploads/benford.json", "w") as f:
                    json.dump(results, f)
                    return Response(json.dumps(results))
            else:
                return Response("Data doesn't follow the Benford's Law.")
    


if __name__ == '__main__':
    # Create a Pyramid app and define the /benford route
    config = Configurator()
    config.include('pyramid_jinja2')  # include the Jinja2 package
    config.include('pyramid_debugtoolbar')
    config.add_static_view(name='static',path='static')
    config.add_route('home', '/')
    config.add_route('benford', '/benford')
    config.scan()
    # Start the app on port 8080
    from wsgiref.simple_server import make_server
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()