String = str
DateTimeOffset = str
Uri = str


def getattrIgnoreCase(obj, attr, default=None):
    for i in dir(obj):
        if i.lower() == attr.lower():
            return getattr(obj, attr, default)
    return default


dtype_converter = {
    'int': 'int64',
    'bigint': 'int64',
    'long': 'int64',
    'float':'decimal',
    'double': 'double',
    'decimal.Decimal': 'decimal',
    'string': 'string',
    'bool': 'boolean',
    'datetime': 'dateTime',
    'timestamp': 'dateTime'
}