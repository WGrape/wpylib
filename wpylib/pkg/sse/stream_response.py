"""
@File: stream_response.py
@Date: 2024/12/10 10:00
@Desc: 第三方流式响应模块
"""
from wpylib.util.x.xjson import stringify
from wpylib.pkg.sse.stream_queue import StreamQueue
from wpylib.util.http import COMMON_HTTP_CODE_SYS_ERROR
import threading
import queue

STREAM_MESSAGE_PING = "ping"


class StreamResponseGenerator(object):
    """
    流式响应生成器
    """

    def __init__(self, target, args=(), kwargs=None, queue_max: int = 20):
        if not kwargs:
            kwargs = {}
        self.queue = StreamQueue(queue_max)
        kwargs['queue'] = self.queue
        self.thread = threading.Thread(
            group=None,
            target=target,
            name='stream_response_generator_thread',
            args=args,
            kwargs=kwargs,
            daemon=True
        )

    def __iter__(self):
        self.thread.start()
        try:
            while self.queue.is_running():
                try:
                    e = self.queue.get(True, 3)
                except queue.Empty:
                    # websocket链接保活
                    self.queue.send_message(type_str=STREAM_MESSAGE_PING)
                    continue
                if not e:
                    continue
                if e["event"] == "message":
                    self.queue.task_done()
                    yield self._format_message(**e)
                    continue
                elif e["event"] == "message_end":
                    self.queue.task_done()
                    yield self._format_message(**e)
                    self.queue.close()
                    break
        except GeneratorExit:
            # 无法再yield
            # 此异常出现的时机为第三方sse断开连接导致无法yield, 该不可抗拒因素导致的异常无法处理，因此忽略该异常
            self.queue.close()
            self.thread.join(5)
            return
        except Exception as e:
            self.queue.send_message_end({"code": COMMON_HTTP_CODE_SYS_ERROR, "msg": "服务异常"})
            return
        finally:
            self.queue.close()
            self.thread.join(5)

    def _format_message(self, event, data):
        """
        格式化消息
        :param event: 事件
        :param data: 数据
        :return:
        """
        return "data: {}\n\n".format(stringify({
            "event": event,
            "data": data
        }))
