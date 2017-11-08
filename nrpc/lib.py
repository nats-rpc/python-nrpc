class InvalidSubject(Exception):
    pass


def parse_subject(
    package_subject, package_params_count,
    service_subject, service_params_count, subject,
):
    package_subject = package_subject.split('.') if package_subject else []
    service_subject = service_subject.split('.')

    minlen = len(package_subject) + package_params_count + \
        len(service_subject) + service_params_count + 1

    tokens = subject.split('.')

    if len(tokens) < minlen:
        raise InvalidSubject(
            "subject must contain %s tokens at least, got %s" % (
                minlen, subject))

    if tokens[:len(package_subject)] != package_subject:
        raise InvalidSubject(
            "subject should start with %s" % '.'.join(package_subject))

    tokens = tokens[len(package_subject):]

    package_params = tokens[:package_params_count]
    tokens = tokens[package_params_count:]

    if tokens[:len(service_subject)] != service_subject:
        raise InvalidSubject(
            "subject should contain %s, got %s" % (
                '.'.join(service_subject), subject))

    tokens = tokens[len(service_subject):]

    service_params = tokens[:service_params_count]
    tokens = tokens[service_params_count:]

    name = tokens[0]

    return package_params, service_params, name, tokens[1:]


def parse_subject_tail(method_params_count, tail):
    if len(tail) < method_params_count:
        raise InvalidSubject("subject tail is too short")
    method_params = tail[:method_params_count]
    tail = tail[method_params_count:]
    if len(tail) == 0:
        encoding = "protobuf"
    elif len(tail) == 1:
        encoding = tail[0]
    elif len(tail) > 1:
        raise InvalidSubject("subject tail is too long")
    return method_params, encoding
