from common.model import MongoModel, get_mongo_pool


class UserModel(MongoModel):
    def __init__(self, **kwargs):
        super().__init__(
            get_mongo_pool("eff-publish"), "user", **kwargs
        )