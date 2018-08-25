#! /usr/bin/python
# -*- coding: utf-8 -*-

import wrapt

import tensorflow as tf

from tensorlayer.decorators.utils import get_network_obj

__all__ = [
    'auto_parse_inputs', 'auto_reset_temp_attrs', 'force_return_self', 'layer_autoregister',
    'overwrite_layername_in_network'
]


def force_return_self(func):
    """decorator to overwrite return value with `self` object"""

    def func_wrapper(self, *args, **kwargs):
        """decorator wrapper function"""
        func(self, *args, **kwargs)

        return self

    return func_wrapper


def auto_reset_temp_attrs(func):
    """decorator to overwrite return value with `self` object"""

    def func_wrapper(self, *args, **kwargs):
        """decorator wrapper function"""
        self._temp_data = {
            'inputs': None,
            'outputs': None,
            'local_weights': [],
            'local_drop': [],
        }

        return func(self, *args, **kwargs)

    return func_wrapper


def auto_parse_inputs(func):
    """decorator to overwrite return value with `self` object"""

    def func_wrapper(self, *args, **kwargs):
        """decorator wrapper function"""
        super(self.__class__, self).compile(args[0])  # args[0] => prev_layer

        return func(self, *args, **kwargs)

    return func_wrapper


@wrapt.decorator
def layer_autoregister(wrapped, instance, args, kwargs):

    cls = wrapped(*args, **kwargs)

    try:
        network_obj = get_network_obj()

        if network_obj is not None:
            network_obj.register_new_layer(instance)

    except Exception as e:
        print("Except Type 2: %s - Error: %s" % (type(e), str(e)))
        pass

    return cls


@wrapt.decorator
def overwrite_layername_in_network(wrapped, instance, args, kwargs):

    cls = wrapped(*args, **kwargs)

    try:

        network_obj = get_network_obj()
        result_scope = ""

        if network_obj is not None:
            current_var_scope = tf.get_default_graph().get_name_scope()

            for i_varscope, i_modelscope in zip(current_var_scope.split("/"), network_obj.model_scope.split("/")):
                if i_varscope != i_modelscope:
                    result_scope += i_varscope + "/"

            instance.name = result_scope + instance.name

    except Exception as e:
        print("Except Type 3: %s - Error: %s" % (type(e), str(e)))
        pass

    return cls
