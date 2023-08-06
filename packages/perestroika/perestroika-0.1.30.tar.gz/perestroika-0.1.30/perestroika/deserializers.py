import json
from json import JSONDecodeError

from accordion import expand

from perestroika.context import Context
from perestroika.exceptions import BadRequest
from perestroika.utils import multi_dict_to_dict


class Deserializer:
    def get_data(self, request, method_handler, **kwargs):
        raise NotImplementedError()

    def deserialize(self, request, method_handler, **kwargs):
        data = self.get_data(request, method_handler, **kwargs)

        if not data.get("items") and request.method.lower() in ["post", "put", "patch"]:
            raise BadRequest(message="Need data for processing")

        return Context(
            request=request,

            order=data.get("order", {}),

            user_filter=data.get("filter", {}),
            user_exclude=data.get("exclude", {}),

            project=data.get("project", []),

            items=data.get("items", []),
            queryset=method_handler.queryset,
            meta=data.get("meta", {}),
        )


class DjangoDeserializer(Deserializer):
    def get_data(self, request, method_handler, **kwargs):
        try:
            data = json.loads(request.body)
            data = expand(data)
        except JSONDecodeError:
            data = {}

        get_data = multi_dict_to_dict(request.GET)
        get_data = expand(get_data)
        data.update(get_data)

        post_data = multi_dict_to_dict(request.POST)
        post_data = expand(post_data)
        data.update(post_data)

        return data


class JSONDeserializer(Deserializer):
    def get_data(self, request, method_handler, **kwargs):
        return kwargs.get("json_data", {})
