import os


class EnvTypes():
    """Can configure the prefix of environment,
        delimitation between env value and env type, name used
        for different env types: strings, integers, booleans,
        lists, tuples and dictionaries.
        """

    def __init__(self, **kwargs):
        # Field Delimitation
        if not kwargs.get('field_del'):
            self.field_del = '_'
        else:
            self.field_del = kwargs.get('field_del')

        # Value Delimitation
        if not kwargs.get('value_del'):
            self.value_del = '; _'
        else:
            self.value_del = kwargs.get('value_del')

        # Prefix
        if not kwargs.get('prefix'):
            self.prefix = 'DJANGO' + self.field_del
        else:
            self.prefix = kwargs.get('prefix').upper() + self.field_del

        # Strings
        if not kwargs.get('env_str'):
            self.env_str = 'str'
        else:
            self.env_str = kwargs.get('env_str').lower()

        # Integers
        if not kwargs.get('env_int'):
            self.env_int = 'int'
        else:
            self.env_int = kwargs.get('env_int').lower()

        # Booleans
        if not kwargs.get('env_bool'):
            self.env_bool = 'bool'
        else:
            self.env_bool = kwargs.get('env_bool').lower()

        # Lists
        if not kwargs.get('env_list'):
            self.env_list = 'list'
        else:
            self.env_list = kwargs.get('env_list').lower()

        # List delimitation
        if not kwargs.get('list_del'):
            self.list_del = ', '
        else:
            self.list_del = kwargs.get('list_del')

        # # Tuples
        if not kwargs.get('env_tuple'):
            self.env_tuple = 'tuple'
        else:
            self.env_tuple = kwargs.get('env_tuple').lower()

        # Tuple delimitation
        if not kwargs.get('tuple_del'):
            self.tuple_del = ', '
        else:
            self.tuple_del = kwargs.get('tuple_del')

        # # Dictionaries
        if not kwargs.get('env_dict'):
            self.env_dict = 'dict'
        else:
            self.env_dict = kwargs.get('env_dict').lower()

        # Dictionary delimitation
        if not kwargs.get('dict_del'):
            self.dict_del = ': '
        else:
            self.dict_del = kwargs.get('dict_del')

        # Empty Value
        if not kwargs.get('empty_value'):
            self.empty_value = 'empty'
        else:
            self.empty_value = kwargs.get('empty_value')

        # None Value
        if not kwargs.get('none_value'):
            self.none_value = 'none'
        else:
            self.none_value = kwargs.get('none_value')

    def set_env(self, field_name):
        self.field_name = field_name.upper()
        self.field = self.prefix + self.field_name
        self.value = os.getenv(self.field).split(self.value_del)[0]
        self.object_type = os.getenv(self.field).split(self.value_del)[1]

        if self.object_type == self.env_str:
            if self.value == self.none_value:
                return None
            elif self.value == self.empty_value:
                return ''
            return str(self.value)
        elif self.object_type == self.env_int:
            return int(self.value)
        elif self.object_type == self.env_bool:
            if self.value == 'True':
                return True
            return False
        elif self.object_type == self.env_list:
            if self.value.__contains__(self.list_del):
                return list(self.value.split(self.list_del))
            else:
                if self.value == self.empty_value:
                    return []
                return [self.value]
        elif self.object_type == self.env_tuple:
            if self.value.__contains__(self.tuple_del):
                return tuple(self.value.split(self.tuple_del))
            else:
                if self.value == self.empty_value:
                    return tuple()
                return tuple(self.value)
        elif self.object_type == self.env_dict:
            if self.value == self.empty_value:
                return {}
            self.key = self.value.split(self.dict_del)[0]
            self.value = self.value.split(self.dict_del)[1]
            return {self.key: self.value}
        else:
            return
