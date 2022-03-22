def merge_list(lst, res=None):
    if res is None:
        res = []
    for el in lst:
        merge_list(el, res) if isinstance(el, list) else res.append(el)
    return res
