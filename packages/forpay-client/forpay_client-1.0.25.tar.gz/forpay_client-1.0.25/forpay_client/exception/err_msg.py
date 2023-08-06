__dict = dict(
    SDK_PRIVATE_FILE_NOT_EXIST='Private file not exist',
    SDK_PUBLIC_FILE_NOT_EXIST='Public file not exist'
)


def get_msg(errcode):
    return __dict.get(errcode)
