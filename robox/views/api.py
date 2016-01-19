import logging
from http import client

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from robox.models import DataFile
from robox.utils import upload_files, validate_barcode

_logger = logging.getLogger(__name__)


class EntryField(serializers.RelatedField):
    def to_representation(self, value):
        return {meta_data.key: meta_data.value for meta_data in value.metadata_set.all()}


class FileSerializer(serializers.ModelSerializer):
    data = EntryField(many=True, read_only=True, source='entry_set')

    class Meta:
        model = DataFile
        fields = ('barcode', 'format', 'upload_time', 'data')


class StandardPaginationClass(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class FileViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = FileSerializer
    pagination_class = StandardPaginationClass

    def get_queryset(self):
        queryset = DataFile.objects.all()

        barcodes = self.request.query_params.get("barcode")

        if barcodes:
            query_filter = None
            for barcode in barcodes.split(","):
                if query_filter:
                    query_filter |= Q(barcode__iexact=barcode)
                else:
                    query_filter = Q(barcode__iexact=barcode)
            queryset = queryset.filter(query_filter)

        return queryset

    @atomic()
    def create(self, request, *args, **kwargs):
        barcode = request.data.get('barcode')
        files = request.FILES

        try:
            validate_barcode(barcode)

            database_files = upload_files(barcode, [file for file in files.values()])

            return Response({"results": [FileSerializer(database_file).data for database_file in database_files]},
                            status=client.CREATED)
        except ValidationError:
            return Response({'error': 'Invalid barcode', 'barcode': barcode}, status=client.UNPROCESSABLE_ENTITY)
