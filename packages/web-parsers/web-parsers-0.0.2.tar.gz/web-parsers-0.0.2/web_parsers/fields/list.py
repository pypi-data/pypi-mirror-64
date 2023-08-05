from .single import StringField, IntField, FloatField, DictField, RawField
import logging

logger = logging.getLogger(__name__)


class ListFieldTransformerBase(object):
    transformer_class = None

    def __init__(self, data=None):
        self.data = data
        self.validate_transformer()

    def validate_transformer(self):
        if self.transformer_class is None:
            raise NotImplementedError("transformer_class should be assigned for List type of FieldTransformer")

    def try_or_none(self):

        result_data_list = []
        for d in self.data:
            try:
                result_data = self.transformer_class(data=d).transform()
                result_data_list.append(result_data)
            except Exception as e:
                logger.debug("Failed to transform data `{d}` to `{klass_name}` type with "
                             "error `{error}`".format(d=d, klass_name=self.__class__.__name__, error=e))
        return result_data_list

    def transform(self):
        return self.try_or_none()


class ListStringField(ListFieldTransformerBase):
    transformer_class = StringField


class ListIntField(ListFieldTransformerBase):
    transformer_class = IntField


class ListFloatField(ListFieldTransformerBase):
    transformer_class = FloatField


class ListDictField(ListFieldTransformerBase):
    transformer_class = DictField


class ListRawField(ListFieldTransformerBase):
    transformer_class = RawField
