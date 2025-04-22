"""
@File: stream_queue.py
@Date: 2024/12/10 10:00
@Desc: 第三方队列模块
"""
from wpylib.util.x.xtyping import is_none
import queue
import time


class StreamQueue(queue.Queue):
    """
    StreamQueue流式队列
    """

    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self.running = True

    def close(self):
        """
        关闭队列
        :return:
        """
        self.join()
        self.running = False

    def is_running(self):
        """
        是否正在运行
        :return:
        """
        return self.running

    def put(self, item, block=True, timeout=None):
        """
        阻塞放入队列
        :param item: 队列元素
        :param block: 是否阻塞
        :param timeout: 超时时间
        :return:
        """
        raise RuntimeError("Stream cannot use put method, using send_message or send_message_end instead")

    def put_nowait(self, item):
        """
        非阻塞放入队列
        :param item: 队列元素
        :return:
        """
        raise RuntimeError(
            "Stream cannot use put_nowait method, using send_message_nowait or send_message_end_nowait instead"
        )

    def send_message(self, type_str: str, item: dict = None, name="", is_show=True, block=True, timeout=None) -> float:
        """
        阻塞发送消息
        :param type_str: 消息类型
        :param item: 队列元素
        :param name: 名称
        :param is_show: 前端是否展示
        :param block: 是否阻塞
        :param timeout: 超时时间
        :return:
        """
        if not self.running:
            raise RuntimeError("stream queue already closed.")
        if is_none(item):
            item = {}

        # 发送消息
        data = {
            "event": "message",
            "data": {
                "type": type_str,
                "name": name,
                "is_show": is_show,
                "item": item
            }
        }
        super().put(item=data, block=block, timeout=timeout)
        return time.time()

    def send_message_end(self, data: dict, block=True, timeout=None) -> float:
        """
        阻塞发送结束消息
        :param data: 消息内容
        :param block: 是否阻塞
        :param timeout: 超时时间
        :return:
        """
        if not self.running:
            raise RuntimeError("stream queue already closed.")
        super().put(item={"event": "message_end", "data": data}, block=block, timeout=timeout)
        self.close()
        return time.time()


class NoneQueue(StreamQueue):
    """
    空队列
    """

    def send_message(self, type_str: str, item: dict = None, name="", is_show=True, block=True, timeout=None) -> float:
        return time.time()

    def send_message_end(self, data: dict, block=True, timeout=None):
        return time.time()
