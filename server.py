import socket
import threading
import time
import random
import pickle
from logger import setup_logger, log_message
from utils import add_arrays, subtract_arrays

def handle_client(conn, addr, client_id):
    """Обработка одного клиента."""
    log_message(f"Клиент{client_id}: подключен")
    
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            
            request = pickle.loads(data)
            operation = request['operation']
            arr1 = request['arr1']
            arr2 = request['arr2']
            
            log_message(f"Клиент{client_id}: отправлен запрос на {operation}")
            
            # Эмуляция долгих вычислений
            time.sleep(random.uniform(1, 3))
            
            if operation == 'add':
                result = add_arrays(arr1, arr2)
            elif operation == 'subtract':
                result = subtract_arrays(arr1, arr2)
            else:
                result = None
            
            response = {'result': result}
            conn.send(pickle.dumps(response))
            
            log_message(f"Клиент{client_id}: выполнена {operation}")
            
        except Exception as e:
            log_message(f"Клиент{client_id}: ошибка - {e}")
            break
    
    conn.close()
    log_message(f"Клиент{client_id}: отключен")

def start_server(host='127.0.0.1', port=65432):
    """Запуск сервера."""
    setup_logger()
    log_message("Сервер запущен")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        
        client_counter = 0
        
        while True:
            conn, addr = s.accept()
            client_counter += 1
            thread = threading.Thread(target=handle_client, args=(conn, addr, client_counter))
            thread.start()

if __name__ == "__main__":
    start_server()