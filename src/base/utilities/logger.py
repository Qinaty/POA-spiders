import logging

# 配置日志格式和显示等级，仅在本模块内使用，外部不可见
_FORMAT = '[%(name)-10s] %(levelname)-8s: %(message)s'
_LEVEL = logging.DEBUG


class Logger:
    def __init__(self):
        formatter = logging.Formatter(fmt=_FORMAT)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.addHandler(handler)
        self._logger.setLevel(_LEVEL)
