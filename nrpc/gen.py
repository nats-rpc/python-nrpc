import sys
import os

from . import nrpc_pb2 as nrpc
from .tmpl import template
from google.protobuf.compiler import plugin_pb2 as plugin

PY2 = sys.version_info.major == 2


class Generator:
    def __init__(self, request):
        self.request = request

    def lookup_fd(self, pkg):
        for fd in self.request.proto_file:
            if fd.package == pkg:
                return fd
        return None

    def get_fd_mod(self, fd):
        return os.path.splitext(fd.name)[0].replace("/", ".") + '_pb2'

    def get_mod_alias(self, mod):
        return mod.replace('_', '__').replace('.', '_dot_')

    def lookup_type(self, name):
        if not name.startswith('.'):
            raise ValueError(
                "lookup_type only accepts fully qualified names. Got '%s'" %
                name)
        path = name.lstrip('.').split('.')
        pkg = path
        fd = None
        while fd is None and len(pkg) > 1:
            pkg = pkg[:-1]
            fd = self.lookup_fd('.'.join(pkg))
        if fd is None:
            return None, None

        path = path[len(pkg):]

        return self.get_fd_mod(fd), '.'.join(path)

    def get_type(self, name):
        mod, tname = self.lookup_type(name)
        return '%s.%s' % (self.get_mod_alias(mod), tname)

    def extra_imports(self):
        pbmods = set()
        for sd in self.fd.service:
            for md in sd.method:
                for t in (md.input_type, md.output_type):
                    mod, _ = self.lookup_type(t)
                    pbmods.add(mod)
        return [(x, self.get_mod_alias(x)) for x in pbmods]

    def get_pkg_subject(self, fd):
        if fd.options.HasExtension(nrpc.packageSubject):
            return fd.options.Extensions[nrpc.packageSubject]
        return fd.package

    def get_pkg_params(self, fd):
        e = fd.options.Extensions[nrpc.packageSubjectParams]
        if e:
            return e
        return []

    def get_svc_subject(self, sd):
        s = sd.options.Extensions[nrpc.serviceSubject]
        if s:
            return s
        r = self.fd.options.Extensions[nrpc.serviceSubjectRule]
        if r == nrpc.COPY:
            return sd.name
        elif r == nrpc.TOLOWER:
            return sd.name.lower()
        raise Exception("Unknown subject rule %s" % r)

    def get_svc_params(self, sd):
        e = sd.options.Extensions[nrpc.serviceSubjectParams]
        if e is not None:
            return e
        return []

    def get_mt_subject(self, md):
        s = md.options.Extensions[nrpc.methodSubject]
        if s:
            return s
        r = self.fd.options.Extensions[nrpc.methodSubjectRule]
        if r == nrpc.COPY:
            return md.name
        elif r == nrpc.TOLOWER:
            return md.name.lower()
        raise Exception("Unknown subject rule %s" % r)

    def get_mt_params(self, md):
        e = md.options.Extensions[nrpc.methodSubjectParams]
        if e is not None:
            return e
        return []

    def mt_has_streamed_reply(self, md):
        s = md.options.Extensions[nrpc.streamedReply]
        if s:
            return s
        return False

    def get_fd(self, name):
        return next((fd for fd in self.request.proto_file if fd.name == name),
                    None)

    def generate(self):
        response = plugin.CodeGeneratorResponse()

        for f in self.request.file_to_generate:
            self.fd = self.get_fd(f)
            pbmod = os.path.splitext(self.fd.name)[0] + "_pb2"
            try:
                out_file = response.file.add()
                out_file.name = os.path.splitext(self.fd.name)[0] + "_nrpc.py"
                out_file.content = template.render(
                    g=self, fd=self.fd, pbmod=pbmod)
            finally:
                self.fd = None
        return response


def main():
    stdin = sys.stdin if PY2 else sys.stdin.buffer
    stdout = sys.stdout if PY2 else sys.stdout.buffer
    request = plugin.CodeGeneratorRequest.FromString(stdin.read())
    generator = Generator(request)
    response = generator.generate()
    stdout.write(response.SerializeToString())
