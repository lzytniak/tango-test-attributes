from flask import Flask, Response

import PyTango, json

app = Flask(__name__)

# routes
@app.route('/devices/<domain>/<family>/<member>')
def get_device(domain, family, member):
    device = (domain+'/'+family+'/'+member)
    proxy = PyTango.DeviceProxy(device)

    state, status = proxy.read_attributes(["state", "status"])

    dev_info = proxy.info()

    imp_info = proxy.import_info()
    info = dict(
        classname=dev_info.dev_class,
        exported=imp_info.exported
    )
    attributes = list(proxy.get_attribute_list())
    data = json.dumps(dict(state=str(state.value),
                           status=status.value,
                           info=info, attributes=attributes))
    return Response(data, mimetype="application/json")

@app.route('/devices/<domain>/<family>/<member>/attributes')
def get_device_attributes(domain, family, member):
    device = (domain+'/'+family+'/'+member)
    proxy = PyTango.DeviceProxy(device)

    attributes = list(proxy.get_attribute_list())
    data = json.dumps(dict(attributes=attributes))
    return Response(data, mimetype="application/json")

@app.route('/devices/<domain>/<family>/<member>/attributes/<attribute>')
def get_device_attribute(domain, family, member, attribute):
    device = (domain+'/'+family+'/'+member)
    proxy = PyTango.DeviceProxy(device)

    device_attribute = proxy.read_attribute(attribute)
    value = str(device_attribute.value)
    data = json.dumps(dict(name=device_attribute.name,
                           value=value))
    return Response(data, mimetype="application/json")

if __name__ == '__main__':
    app.run()

