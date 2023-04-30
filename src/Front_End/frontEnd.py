import socket
import json
from threading import Thread
from dataSettings import *
from flask import Flask, request
from cache import *
import os
import time

app = Flask(__name__)
fAddr = frontEndService_addr
oAddr = orderService_addr
cAddr = catalogService_addr
order_ports = [6000, 6001, 6002]
order_Addr_list = []
for port in order_ports:
    order_Addr_list.append(port)

cSAddr = (os.getenv("PG_HostC", "3.88.183.128"), 7090)
cache = SimpleCache(3)
leader_port = 6000


@app.route('/lookUp', methods=['GET'])
def get_request():
    # handle GET request from client
    stockName = request.args.get('stockName')

    # check cache first
    if cache.inCache(stockName):
        stock_in_cache = json.loads(cache.getStock(stockName))
        price, quantity = stock_in_cache['price'], stock_in_cache['quantity']
        print(price)
        payload = json.dumps(
            {
                "data": {
                    'stockName': stockName,
                    'price': price,
                    'quantity': quantity
                }
            }
        )

        payload = json.dumps(payload)
        return payload
    else:
        # connect with catalog service
        s = socket.socket()
        s.connect(cSAddr)
        # forward the request to catalog service
        lookup_msg = 'Lookup {stock_name}'.format(stock_name=stockName)
        s.send(lookup_msg.encode())
        lookup_response = s.recv(1024).decode('utf-8')
        s.close()

        status_code = lookup_response.split('/')[0]
        res_msg = lookup_response.split('/')[1]

        if status_code == "200":
            # handle successful lookup from catalog
            reply = json.dumps(res_msg)
            replyTemp = json.loads(res_msg)
            stockInCache = json.dumps(
                {
                    "stockName": replyTemp['data']['stockName'],
                    "price": replyTemp['data']['price'],
                    "quantity": replyTemp['data']['quantity']
                }
            )
            print(reply)
            cache.add(stockInCache)
            return reply
        else:
            reply = json.dumps(res_msg)
            return reply


@app.route('/order', methods=['POST'])
def post_request():
    data = request.get_json()
    data = json.loads(data)

    stockName = data['stockName']
    quantity = data['quantity']
    tradeType = data['type']
    if cache.inCache(stockName):
        if tradeType == "buy":
            cache.updateStock(stockName, quantity, False)
        else:
            cache.updateStock(stockName, quantity, True)

    s = socket.socket()
    s.connect((os.getenv("PG_HostO", "3.88.183.128"), leader_port))
    order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
                                                                   stock_name=stockName)
    s.send(order_msg.encode())
    order_response = s.recv(1024).decode('utf-8')
    s.close()

    status_code = order_response.split("/")[0]
    res_msg = order_response.split("/")[1]
    if status_code == "200":
        reply = json.dumps(res_msg)
        return reply
    else:
        reply = json.dumps(res_msg)
        if cache.inCache(stockName):
            if tradeType == "buy":
                cache.updateStock(stockName, quantity, True)
            else:
                cache.updateStock(stockName, quantity, False)
        return reply


def health_check():
    while True:
        try:
            s = socket.socket()
            s.connect((os.getenv("PG_HostO", "3.88.183.128"), leader_port))
            health_check_msg = 'healthCheck'
            s.send(health_check_msg.encode())
            health_response = s.recv(1024).decode('utf-8')
            print(health_response)
            if health_response != 'alive ' + str(leader_port):
                leader_election()
            time.sleep(2)
        except:
            # server has crashed or network error occurred
            print('Server has crashed or network error occurred')
            break


def leader_election():
    # Send health check msg to order services
    global leader_port
    health_check_msg = 'healthCheck'
    alive_port = []
    for p in order_Addr_list:
        s = socket.socket()
        s.settimeout(5)
        try:
            s.connect((os.getenv("PG_HostO", "3.88.183.128"), p))
            s.send(health_check_msg.encode())
            health_response = s.recv(1024).decode('utf-8')
            status = health_response.split(" ")[0]
            if status == 'alive':
                alive_port.append(p)
            s.close()
        except:
            print(f"Could not connect to server {p}")
            s.close()
            continue

    alive_port.sort(reverse=True)
    leader_port = alive_port[0]


if __name__ == '__main__':
    port = 6060
    leader_election()
    print(leader_port)
    Thread(target=health_check).start()
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
