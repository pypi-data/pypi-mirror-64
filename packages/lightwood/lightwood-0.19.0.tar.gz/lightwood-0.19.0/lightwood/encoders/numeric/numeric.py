import torch
import math
import logging


class NumericEncoder:

    def __init__(self, data_type=None, is_target=False):
        self._type = data_type
        self._min_value = None
        self._max_value = None
        self._mean = None
        self._pytorch_wrapper = torch.FloatTensor
        self._prepared = False
        self._is_target = is_target

    def prepare_encoder(self, priming_data):
        if self._prepared:
            raise Exception('You can only call "prepare_encoder" once for a given encoder.')

        count = 0
        abs_count = 0
        value_type = 'int'
        for number in priming_data:
            try:
                number = float(number)
            except Exception:
                continue

            if math.isnan(number):
                err = 'Lightwood does not support working with NaN values !'
                logging.error(err)
                raise Exception(err)

            self._min_value = number if self._min_value is None or self._min_value > number else self._min_value
            self._max_value = number if self._max_value is None or self._max_value < number else self._max_value

            count += number
            abs_count += abs(number)

            if int(number) != number:
                value_type = 'float'

        self._type = value_type if self._type is None else self._type
        self._mean = count / len(priming_data)
        self._abs_mean = abs_count / len(priming_data)
        self._prepared = True

    def encode(self, data):
        if not self._prepared:
            raise Exception('You need to call "prepare_encoder" before calling "encode" or "decode".')
        ret = []

        for number in data:
            try:
                try:
                    number = float(number)
                except:
                    # Some data cleanup for an edge case that shows up a lot when lightwood isn't used with mindsdb
                    number = float(number.replace(',', '.'))
            except:
                #logging.warning('It is assuming that  "{what}" is a number but cannot cast to float'.format(what=number))

                number = None

            if self._is_target:
                vector = [0] * 2
                try:
                    vector[0] = number/self._abs_mean
                    #vector[0] = number
                    vector[1] = math.log(abs(number)) if number > 0 else -100
                except:
                    logging.warning(f'Got unexpected value for numerical target value: "{number}" !')
                    # @TODO For now handle this by setting to zero as a hotfix,
                    # but we need to figure out why it's happening and fix it properly later
                    vector = [0] * 2

            else:
                vector = [0] * 2
                if number is None:
                    vector[1] = 0
                else:
                    vector[1] = 1
                    vector[0] = number / self._abs_mean

            ret.append(vector)

        return self._pytorch_wrapper(ret)

    def decode(self, encoded_values):
        ret = []
        for vector in encoded_values.tolist():
            if self._is_target:
                if not math.isnan(vector[0]):
                    linear_value = vector[0]
                    real_value = linear_value * self._abs_mean
                    #real_value = linear_value
                else:
                    logging.warning(f'Occurance of `nan` value in encoded numerical value: {vector}')
                    real_value = None

                if self._type == 'int' and real_value is not None:
                    real_value = int(round(real_value))
            else:
                is_zero = False
                is_negative = False
                real_value = vector[0] * self._abs_mean
                if not math.isnan(vector[3]):
                    is_none = True if abs(round(vector[3])) == 0 else False
                else:
                    logging.warning(f'Occurance of `nan` value in encoded numerical value: {vector}')
                    is_none = True

                if is_none:
                    real_value = None
                if is_zero:
                    real_value = 0

            ret.append(real_value)

        return ret


if __name__ == "__main__":
    data = [1, 1.1, 2, -8.6, None, 0]

    encoder = NumericEncoder()

    encoder.prepare_encoder(data)
    encoded_vals = encoder.encode(data)

    assert(sum(encoded_vals[4]) == 0)
    assert(sum(encoded_vals[0]) == 1)
    assert(encoded_vals[1][1] > 0)
    assert(encoded_vals[2][1] > 0)
    assert(encoded_vals[3][1] > 0)
    for i in range(0, 4):
        assert(encoded_vals[i][3] == 1)
    assert(encoded_vals[4][3] == 0)

    decoded_vals = encoder.decode(encoded_vals)

    for i in range(len(encoded_vals)):
        if decoded_vals[i] is None:
            assert(decoded_vals[i] == data[i])
        else:
            assert(round(decoded_vals[i], 5) == round(data[i], 5))
