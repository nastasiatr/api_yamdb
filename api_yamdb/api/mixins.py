from rest_framework import mixins, viewsets


class MixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass