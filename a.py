class OutputObject:

    def __init__(self, *args, **kwargs):
        pass



def obtainAttribute(sample, attributeString: str):
    baseObj = sample
    attrArray = attributeString.split(".")
    for string in attrArray:
        if(attrArray.index(string) == (len(attrArray) - 1)):
            return getattr(baseObj,string)
        else:
            baseObj = getattr(baseObj,string)
    return "failed"
