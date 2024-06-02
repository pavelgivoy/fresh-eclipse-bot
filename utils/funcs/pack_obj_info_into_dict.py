def pack_obj_info_into_dict(obj: object) -> dict:
    return dict(filter(lambda item: not item[0].startswith('_'),
                       obj.__dict__.items()))
