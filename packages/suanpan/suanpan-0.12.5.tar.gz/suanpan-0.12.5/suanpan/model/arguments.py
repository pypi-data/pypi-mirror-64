# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.components import Result
from suanpan.storage.arguments import Folder


class CommonModel(Folder):
    def __init__(self, key, type, version="latest", **kwargs):
        super(CommonModel, self).__init__(key, **kwargs)
        self.version = version
        self.modelType = type
        self.model = self.modelType()

    def load(self, args):
        super(CommonModel, self).load(args)
        if self.folderPath:
            self.value = self.model
        return self

    def transform(self, value):
        if not self.folderPath:
            return None
        self.model.load(self.folderPath)
        return self.model

    def clean(self):
        super(CommonModel, self).clean()
        if self.folderPath:
            self.value = self.model
        return self

    def save(self, result):
        model = result.value
        model.save(self.folderPath)
        return super(CommonModel, self).save(Result.froms(value=self.folderPath))


class HotReloadModel(CommonModel):
    def transform(self, value):
        if not self.folderName:
            return None
        self.model.loadFrom(self.folderName, version=self.version)
        return self.model

    def save(self, result):
        raise NotImplementedError("Not support save!")
