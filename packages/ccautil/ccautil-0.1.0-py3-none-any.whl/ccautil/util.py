def decomplexifyhms(tim, index, labels, labindex, oplen, colons=False):
    """Secondary function to remove some of the complexity of the hms function.
    Do not call this function directly
    Args:
        tim: list
        index: int
        labels: list
        labindex: int
        oplen: int
        colons: Bool
    Returns:
        list:
    """
    try:
        op = []
        if colons:
            delim = ":"
        else:
            delim = " " if labindex == 2 else ", "
            if index == 3:
                delim = " " if labindex == 2 else " and "
        if oplen > 0:
            op.append(delim)
        if colons:
            sval = padStr(str(tim[index]), pad="0")
        else:
            if labindex == 2:
                sval = str(tim[index]) + labels[labindex][index]
            else:
                sval = displayValue(tim[index], labels[labindex][index], zero=False)
        op.append(sval)
        return op
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def hms(secs, small=True, short=True, single=False, colons=False):
    """Convert `secs` to days, hours, minutes and seconds.
    if `small` is True then only return the higher values
    if they are > zero
    if `short` is True then the labels are their short form
    if `single` is True then the labels are single letters
    if `colons` is True then the output is of the form:
         01:03:23
    Args:
        secs: int the number of seconds
        small: Bool do not return day, hours or mins if they are zero
        short: Bool use short labels
        single: Bool use single letter labels
        colons: Bool return a string of the form 01:32:24
    Returns:
        str:
    """
    try:
        labs = [
            ["day", "hour", "minute", "second"],
            ["day", "hour", "min", "sec"],
            ["d", "h", "m", "s"],
        ]

        tim = [0, 0, 0, 0]
        units = [60 * 60 * 24, 60 * 60, 60]
        rem = secs
        for index in range(3):
            tim[index], rem = reduceTime(units[index], rem)
        tim[3] = rem
        op = []
        started = not small
        if single:
            cnlabs = 2
        else:
            cnlabs = 1 if short else 0
        for cn in range(4):
            if not started and tim[cn] > 0:
                started = True
            if started:
                op += decomplexifyhms(tim, cn, labs, cnlabs, len(op), colons)
        msg = addToString("", op)
        return msg
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)
