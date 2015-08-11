from itertools import chain, combinations, permutations

__author__ = 'ahmetdal'


class Handler(object):
    handlers = {}

    @classmethod
    def dispatch(cls, workflow_object, field, *args, **kwargs):
        kwargs.pop('signal', None)
        kwargs.pop('sender', None)
        handlers = cls.get_handlers(workflow_object, field, *args, **kwargs)
        for handler in handlers:
            handler['handler'](object=workflow_object, field=field, *args, **kwargs)

    @classmethod
    def register(cls, handler, workflow_object, field, override=False, *args, **kwargs):
        hash = cls.get_hash(workflow_object, field, *args, **kwargs)
        if override or hash not in cls.handlers:
            cls.handlers[hash] = cls.get_handler(handler, workflow_object, field, *args, **kwargs)

    @classmethod
    def get_handler(cls, handler, workflow_object, field, *args, **kwargs):
        return {'handler': handler, 'workflow_object_pk': workflow_object.pk, 'field': field}

    @classmethod
    def get_hash(cls, workflow_object, field, *args, **kwargs):
        return (str(workflow_object.pk) if workflow_object else '') + (field or '')

    @classmethod
    def get_handlers(cls, workflow_object, field, *args, **kwargs):
        handlers = []
        for c in cls.powerset(kwargs.keys()):
            skwargs = {}
            for f in c:
                skwargs[f] = kwargs.get(f)
            handler = cls.handlers.get(cls.get_hash(workflow_object, field, **skwargs))
            if handler:
                handlers.append(handler)
        return handlers

    @classmethod
    def powerset(cls, iterable):
        xs = list(iterable)
        # note we return an iterator rather than a list
        return chain.from_iterable(permutations(xs, n) for n in range(len(xs) + 1))
