from pynput.keyboard import Key, Listener
from threading import Lock, Thread
import API.msg as msg
from bluetooth import BluetoothSocket as Socket, RFCOMM
from bluetooth.ble import GATTRequester
from time import sleep

lock = Lock()
orders = []
stop_orders = []
speed = 0
running = True

def key_to_order(key: Key, speed: int):
    if key == Key.left:
        return msg.left(speed)
    elif key == Key.right:
        return msg.right(speed)
    elif key == Key.up:
        return msg.forward(speed)
    elif key == Key.down:
        return msg.backward(speed)
    else:
        return None


def key_to_stop_order(key: Key):
    if key == Key.left:
        return msg.stop_left()
    elif key == Key.right:
        return msg.stop_right()
    elif key in (Key.up, Key.down):
        return msg.stop_move()
    else:
        return None

def on_press(key):
    global running, orders, speed, lock
    # print(f'{key} pressed')
    lock.acquire()
    if key in (Key.left, Key.right, Key.up, Key.down):
        if key not in orders:
            orders.append(key)
    elif str(key) in (f'\'{i}\'' for i in range(8)):
        print(f'changing speed {speed} --> {int(chr(key.vk))}')
        speed = int(chr(key.vk))
    else:
        print(str(key))
    lock.release()

def on_release(key):
    global running, orders, speed, lock
    # print(f'{key} release')
    if key == Key.esc:
        running = False
        return False
    elif key in (Key.left, Key.right, Key.up, Key.down):
        lock.acquire()
        if key in orders:
            orders.remove(key)
        stop_orders.append(key)
        lock.release()


def server(addr, port, ble=False):
    global running
    print(f'Creating {"BLE" if ble else "BL"} connection')
    if not ble:
        sock = Socket(RFCOMM)
        sock.connect((addr, port))
    else:
        sock = GATTRequester(addr)
    while running:
        lock.acquire()
        data = b''.join((key_to_order(order, speed) for order in orders))
        data += b''.join((key_to_stop_order(order) for order in stop_orders))
        stop_orders.clear()
        lock.release()
        if not ble:
            sock.send(data)
        else:
            for b in data:
                sock.write_by_handle(port, bytes([b]))
        sleep(.02)
    sock.close()

# t = Thread(name='Bluetooth daemon', target=server, args=('C6:D4:B3:59:C2:62', 0x000b), kwargs={'ble': True})
t = Thread(name='Bluetooth daemon', target=server, args=('00:13:EF:D5:D3:A2', 1))
t.start()

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    t.join()