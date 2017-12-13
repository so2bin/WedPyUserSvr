#######################################
#   generate a ordered number for beautified images
#   number is consisted with [0-9a-zA-Z]
#
import re
# from exceptions import ParameterError

IMG_NO_LEN = 4
RE_IMG_NO_PATTERN = '^[0-9A-Z]{%s}' % IMG_NO_LEN
RE_OBJ_IMG_NO = re.compile(RE_IMG_NO_PATTERN)
DEF_START_IMG_NO = '0'*IMG_NO_LEN


def _Z9No_1(startNo, idx, grsVal):
    """
    returned: no = startNo + 1, where the no is a string consisted with 0-9,A-Z
    the progressive rule is:
        9+1=>A, Z+1=>10, 19+2=>1A, 1Z+1=>20,....
    """
    if grsVal < 0:   # error
        return None
    if idx < -1:
        return None
    if idx == -1:
        if grsVal > 0:  # add one position(progessive)
            return str(grsVal)
        else:
            return None
    if grsVal == 0:  # no progressive
        return startNo[:(idx+1)]
    # grsVal == 1
    cChr = startNo[idx]
    if cChr == '9':
        nxtChr = 'A'
        preChr = _Z9No_1(startNo, idx-1, 0)
        return preChr + nxtChr if preChr else nxtChr
    elif cChr == 'Z':
        nxtChr = '0'
        preChr = _Z9No_1(startNo, idx-1, 1)
        return preChr + nxtChr if preChr else nxtChr
    else:
        vChr = ord(cChr)
        nxtChr = chr(vChr + grsVal)
        preChr = _Z9No_1(startNo, idx-1, 0)
        return preChr + nxtChr if preChr else nxtChr


def geneImgNos(start=DEF_START_IMG_NO, num=1):
    """
        generate image number list with start,
            the no. capacity will be (10+26)^4 = 1679616, or not limited
        @params num: number
        return: list, like: ['0000', '0001', '0002', ...]
    """
    if start != DEF_START_IMG_NO and not RE_OBJ_IMG_NO.match(start):
        raise ParameterError('Invalid start image number when generate')
    nos = []
    curNo = start
    for i in range(num):
        curNo = _Z9No_1(curNo, len(curNo)-1, 1)
        nos.append(curNo)
    return nos
