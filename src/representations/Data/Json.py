from representations.Representation import Representation
from utils.MainUtils import parse_json, list_conversation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
from representations.ExtractStrategy import ExtractStrategy

class Json(Representation):
    category = "Data"

    @classmethod
    def declare(cls):
        params = {}
        params["object"] = ObjectArgument({
            "docs": {
                "definition": '__json_object_given_from_code'
            },
            "type": "object",
        })
        params["text"] = StringArgument({
            "docs": {
                "definition": '__json_text_given_from_code'
            },
        })

        return params

    class Extractor(ExtractStrategy):
        async def extractByText(self, i = {}):
            json_text = i.get('text')
            __obj = parse_json(json_text)

            out = self.contentUnit({
                'content': __obj,
            })

            return [out]

        async def extractByObject(self, i = {}):
            json_object = list_conversation(i.get('object'))
            out = []
            
            for i in json_object:
                out.append(self.contentUnit({
                    'content': i,
                }))

            return out

        def extractWheel(self, i = {}):
            if 'object' in i:
                return 'extractByObject'
            elif 'text' in i:
                return 'extractByText'
