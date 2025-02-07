def serializer_chars(s):
    return ''.join(f'{{{c}}}' for c in s)
