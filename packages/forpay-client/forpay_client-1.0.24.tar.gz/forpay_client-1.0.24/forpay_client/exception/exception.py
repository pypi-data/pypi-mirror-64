from .err_msg import get_msg


class ForPayBaseException(Exception):
    """Basic exceptions definition for forpay"""

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        s = "ServerError"
        s += "\nCode: {code}".format(code=self.errcode)
        s += "\nMsg: {msg}".format(msg=self.errmsg)
        return s


class ForPayException(ForPayBaseException):
    def __init__(
            self,
            errcode=None,
            errmsg=None,
            sub_code=None,
            sub_msg=None,
    ):
        """
        :param errcode: 错误码
        :param errmsg: 错误码描述
        :param sub_code: 业务状态码
        :param sub_msg: 业务错误描述
        """
        super().__init__(errcode, errmsg)
        self.sub_code = sub_code
        self.sub_msg = sub_msg

    def __str__(self):
        s = "ServerError"
        s += "\nCode: {code}".format(code=self.errcode)
        s += "\nMsg: {msg}".format(msg=self.errmsg)
        s += "\nSubCode: {sub_code}".format(sub_code=self.sub_code)
        s += "\nSubMsg: {sub_msg}".format(sub_msg=self.sub_msg)
        return s


class ClientException(ForPayBaseException):
    def __init__(self, errcode):
        self.errcode = errcode

    def __str__(self):
        s = "ClientError"
        s += "\nCode: {code}".format(code=self.errcode)
        s += "\nMsg: {msg}".format(msg=get_msg(self.errcode))
        return s
