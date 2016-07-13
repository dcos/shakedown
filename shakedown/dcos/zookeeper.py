from shakedown import *


def delete_zk_node(node_name):
    znode_url = "{}/exhibitor/exhibitor/v1/explorer/znode/{}".format(dcos_url(), node_name)
    response = http.delete(znode_url)

    if 200 <= response.status_code < 300:
        return True
    else:
        return False
