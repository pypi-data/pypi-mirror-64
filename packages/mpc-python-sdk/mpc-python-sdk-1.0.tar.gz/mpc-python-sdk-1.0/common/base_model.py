# -*- coding: utf-8 -*-
import json
import sys


class BaseModel(object):
    """Base class for all models."""

    def _serialize(self):
        """
        Get all params which are not None and transfer the
        BaseModel object to JSON serializable object.
        """
        def dfs(obj):
            if isinstance(obj, BaseModel):
                d = vars(obj)
                return {k: dfs(d[k]) for k in d if dfs(d[k]) is not None}
            elif isinstance(obj, list):
                return [dfs(o) for o in obj if dfs(o) is not None]
            else:
                return obj.encode("UTF-8") if isinstance(obj, type(u"")) and sys.version_info[0] == 2 else obj

        return dfs(self)

    def _deserialize(self, params):
        return None

    def to_json_string(self):
        """Serialize obj to a JSON formatted str, ensure_ascii is true"""
        return json.dumps(self, ensure_ascii=False)

    def from_json_string(self, jsonStr):
        """Deserialize a JSON formatted str to a Python object"""
        if jsonStr != "":
            params = json.loads(jsonStr)
            self._deserialize(params)

    def __repr__(self):
        return "%s" % self.to_json_string()

