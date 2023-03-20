def are_not_included(fields, request):
    return list(map(lambda x: request.get(x), fields)).count(None) > 0
