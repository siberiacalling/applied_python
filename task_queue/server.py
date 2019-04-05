import socket
import argparse
from datetime import datetime
import pickle
import collections
import os


class Task:
    def __init__(self, length, data, number_of_task):
        self.length = length
        self.data = data
        self.id = number_of_task
        self.time = None

    def check_time_for_get(self, timeout):
        if self.time is None:
            self.time = datetime.now()
            return True
        if (datetime.now() - self.time).seconds > timeout:
            return True


class Queues:
    def __init__(self):
        self._data = collections.defaultdict(Queue)
        self._number_of_task = 0

    def add_task(self, command_params):
        self._number_of_task += 1
        new_task = Task(command_params[2], command_params[3], str(self._number_of_task))
        self._data[command_params[1]].add_task(new_task)
        self.get_last_id_after_restore()
        return str(self._number_of_task)

    def check_task(self, queue_name, task_id):
        if queue_name not in self._data:
            return False
        result = self._data[queue_name].check_task(task_id)
        return result

    def get_task(self, queue_name, timeout):
        if queue_name not in self._data:
            return None
        task = self._data[queue_name].get_task(timeout)
        return task

    def ack_task(self, queue_name, task_id):
        if queue_name not in self._data:
            return False
        result = self._data[queue_name].ack_task(task_id)
        return result

    def save(self, path):
        with open(path + 'queue.bkp', 'wb') as f:
            pickle.dump(self._data, f)

    def restore(self, path):
        try:
            f = open(path + 'queue.bkp', 'rb')
            backup = pickle.load(f)
        except FileNotFoundError:
            print('Backup file "queue.bkp" isn\'t found')
        except EOFError:
            print('Backup file "queue.bkp" is empty.')
        else:
            f.close()
            self._data = backup
            self._number_of_task = self.get_last_id_after_restore()
            print('Restored successfully.')

    def get_last_id_after_restore(self):
        all_max_ids = []
        for key in self._data.keys():
            queue = self._data[key]
            max_id_in_queue = queue.get_max_id_in_queue()
            all_max_ids.append(max_id_in_queue)
        last_id = max(all_max_ids)
        return last_id


class Queue:

    def __init__(self):
        self._data = collections.OrderedDict()

    def add_task(self, new_task):
        self._data[new_task.id] = new_task

    def check_task(self, task_id):
        return task_id in self._data

    def get_task(self, timeout):
        for key in self._data.keys():
            task = self._data[key]
            if task.check_time_for_get(timeout):
                return task

    def ack_task(self, task_id):
        if task_id not in self._data:
            return False
        del self._data[task_id]
        return True

    def get_max_id_in_queue(self):
        all_id_in_queue = []
        for key in self._data.keys():
            all_id_in_queue.append(int(key))
        max_id = max(all_id_in_queue)
        return max_id


class TaskQueueServer:
    def __init__(self, ip, port, path, timeout):
        self._ip = ip
        self._port = port
        self._path = path
        self._timeout = timeout
        self._queues = Queues()

    def run(self):
        with socket.socket() as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self._ip, self._port))
            sock.listen(1)
            if os.path.isfile(self._path + "queue.bkp") and os.path.getsize(self._path) != 0:
                self._queues.restore(self._path)
            while 1:
                conn, addr = sock.accept()
                print("New connection from " + addr[0])
                data = self.recvall(conn)
                if not data:
                    continue
                try:
                    raw_command = data.decode("utf-8")
                    answer = self.process_command(raw_command, self._timeout)
                    conn.send(bytes(answer, 'utf-8'))
                except Exception as e:
                    print(e)

                finally:
                    conn.close()

    def process_command(self, raw_command, timeout):
        command_params = raw_command.split()

        if command_params[0] == 'ADD' and len(command_params) == 4:
            task_id = self._queues.add_task(command_params)
            return '{}\n'.format(task_id)

        if command_params[0] == 'IN' and len(command_params) == 3:
            result = self._queues.check_task(command_params[1], command_params[2])
            return 'YES' if result else 'NO'

        if command_params[0] == 'GET' and len(command_params) == 2:
            task = self._queues.get_task(command_params[1], timeout)
            if task is None:
                return 'None'
            else:
                return '{0}\n {1} {2}'.format(task.id, task.length, task.data)

        if command_params[0] == 'ACK' and len(command_params) == 3:
            result = self._queues.ack_task(command_params[1], command_params[2])
            return 'YES' if result else 'NO'

        if command_params[0] == 'SAVE' and len(command_params) == 1:
            self._queues.save(self._path)
            return 'OK'

        return 'ERROR'

    @staticmethod
    def recvall(sock):
        buff_size = 4096
        data = b''
        while True:
            part = sock.recv(buff_size)
            data += part
            if len(part) < buff_size:
                break
        return data


def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip adress')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
