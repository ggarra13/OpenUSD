

def get_optional_timecode(usd_prim, usd_attr):
    attr = usd_prim.GetAttribute(usd_attr)
    if not attr:
        return None
    attr = attr.Get()
    if not attr:
        return None
    return attr.GetValue()

def get_timecode(usd_prim, usd_attr):
    attr = usd_prim.GetAttribute(usd_attr)
    if not attr:
        print(f'{usd_prim} Invalid timecode attribute "{usd_attr}"')
        return None
    attr = attr.Get()
    if not attr:
        print(f'{usd_prim} Invalid timecode "{usd_attr}" read attribute "{attr}"')
        return 0.0
    return attr.GetValue()


def get_double(usd_prim, usd_attr):
    attr = usd_prim.GetAttribute(usd_attr)
    if not attr:
        print(f'{usd_prim} Invalid double attribute "{usd_attr}"')
        return 0.0
    return attr.Get()

def get_asset(usd_prim, usd_attr):
    attr = usd_prim.GetAttribute(usd_attr)
    if not attr:
        print(f'{usd_prim} Invalid asset attribute "{usd_attr}"')
        return None
    attr = attr.Get()
    if not attr:
        print(f'{usd_prim} Invalid read asset "usd_attr" attribute "{attr}"')
        return None
    value = attr.path
    return value

def get_string(usd_prim, usd_attr):
    attr = usd_prim.GetAttribute(usd_attr)
    if not attr:
        print(f'{usd_prim} Invalid string attribute "{usd_attr}"')
        return None
    return attr.Get()

#
# Temporary comparison function as we don't load the omni libraries.
#
def is_a(usd_prim, usd_type):
    usd_type_name = usd_prim.GetTypeName()
    return usd_type_name == usd_type
