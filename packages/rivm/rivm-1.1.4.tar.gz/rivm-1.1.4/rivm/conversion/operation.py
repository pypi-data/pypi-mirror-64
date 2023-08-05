import abc
import enum

from rivm.conversion.constants import INVALID


class Operation(abc.ABC):
    """
    Operation base.
    """

    @abc.abstractmethod
    def apply(self, data_frame):
        """
        Apply this operation on the given `data_frame`.
        :param data_frame: a `pandas.DataFrame` to process.
        """
        pass


class RemoveDuplicateRows(Operation):
    """
    Remove all duplicates from the dataset based on a `unique_on` column.
    """

    def __init__(self, *unique_on):
        self._unique_on = [header.value for header in unique_on]

    def apply(self, data_frame):
        data_frame.drop_duplicates(
            subset=self._unique_on,
            keep='first',
            inplace=True,  # Modify the input data_frame directly.
        )
        return data_frame


class RemoveEmptyRows(Operation):
    """
    Remove all empty rows from the databaset based on a `empty_on` column.
    """

    def __init__(self, *empty_on):
        self._empty_on = [header.value for header in empty_on]

    def apply(self, data_frame):
        data_frame.dropna(
            axis=0,  # Drop rows which contain missing values.
            how='any',
            subset=self._empty_on,
            inplace=True,  # Modify the input data_frame directly.
        )
        return data_frame


class RemoveInvalidRows(Operation):
    """
    """

    def __init__(self, *invalid_on):
        self._invalid_on = [header.value for header in invalid_on]

    def apply(self, data_frame):
        for header in self._invalid_on:
            data_frame.drop(
                data_frame.index[data_frame[header] == INVALID],
                inplace=True,  # Modify the input data_frame directly.
            )
        return data_frame


class RemoveValidRows(Operation):
    """
    """

    def __init__(self, *valid_on):
        self._valid_on = [header.value for header in valid_on]

    def apply(self, data_frame):
        for header in self._valid_on:
            data_frame.drop(
                data_frame.index[data_frame[header] != INVALID],
                inplace=True,  # Modify the input data_frame directly.
            )
        return data_frame


class RemoveRowsNotContaining(Operation):
    """
    """

    def __init__(self, header, not_containing):
        self._header = header.value
        self._not_containing = []
        for enum_or_string in not_containing:
            if isinstance(enum_or_string, enum.Enum):
                self._not_containing.append(enum_or_string.value)
            else:
                self._not_containing.append(enum_or_string)

    def apply(self, data_frame):
        data_frame.drop(
            data_frame.index[
                ~data_frame[self._header].isin(self._not_containing)
            ],
            inplace=True,  # Modify the input data_frame directly.
        )
        return data_frame


class RemoveRowsContaining(Operation):
    """
    """

    def __init__(self, header, containing):
        self._header = header.value
        self._containing = []
        for enum_or_string in containing:
            if isinstance(enum_or_string, enum.Enum):
                self._containing.append(enum_or_string.value)
            else:
                self._containing.append(enum_or_string)

    def apply(self, data_frame):
        data_frame.drop(
            data_frame.index[
                data_frame[self._header].isin(self._containing)
            ],
            inplace=True,  # Modify the input data_frame directly.
        )
        return data_frame


class RemoveColumns(Operation):
    """
    """

    def __init__(self, *headers):
        self._headers = [header.value for header in headers]

    def apply(self, data_frame):
        data_frame.drop(
            labels=self._headers,
            axis=1,
            inplace=True,  # Modify the input data_frame directly.
        )
        return data_frame
