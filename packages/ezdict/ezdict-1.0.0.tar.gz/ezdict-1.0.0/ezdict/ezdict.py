__all__ = ["EZDict"]


class EZDict(dict):
    """
    EZDict is a wrapper around 'dict' that allows direct attribute accessing through .<attr> and tasks like grouping,
    or counting be preformed easier.

    Create:
        EZDict(<anything dict() can take>)
    """
    def __init__(self, seq=None, **kwargs):
        """
        Create a new EZDict. Essentially the same definition as 'dict()', except with a few keyword arguments reserved
        for customizing EZDict.
        """
        create_with = {}
        if seq is None:
            for key, value in kwargs.items():
                create_with[key] = EZDict(value) if isinstance(value, dict) else value
        else:
            actual_seq = seq.items() if isinstance(seq, dict) else seq
            for key, value in actual_seq:
                create_with[key] = EZDict(value) if isinstance(value, dict) else value

        super().__init__(create_with)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        self[key] = value

    def incrementer(self, key, increment=1):
        """
        If the key is present, increment. Otherwise, set `key`=`increment`
        Replaces:
            if key in dict:
                dict[key] += increment or 1
            else:
                dict[key] = increment or 1
        :param key: Key to add or increment
        :param increment: Value to increment by/initial value
        """
        if key in self:
            self[key] += increment
        else:
            self[key] = increment

    def appender(self, key, value):
        """
        If the key is present, append the value. Otherwise, set `key`=[`value`]
        Replaces:
            if key in dict:
                dict[key].append(value)
            else:
                dict[key] = [value]
        :param key: Key to add or append value to
        :param value: Value to append to list or use as basis
        """
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]


if __name__ == "__main__":
    append = EZDict()
    increment = EZDict()

    for i in range(10):
        append.appender(i % 2, i)
        increment.incrementer(i % 2)

    print(append)
    print(increment)
