import json
import pathlib
from typing import Generic, TypeVar

import pandas
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework import generics
from datasources import models as sheets_models
from slides import models
from slides.api import serializers
from django.contrib.auth import get_user_model
from rest_framework import status

S = TypeVar('S', bound='models.Slide')


class ListSlides(generics.ListAPIView):
    queryset = models.Slide.objects.filter(user=1)
    serializer_class = serializers.SlideSerializer


class CreateSlide(generics.CreateAPIView):
    queryset = models.Slide.objects.filter(user=1)
    serializer_class = serializers.NewSlideForm

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        qs = self.get_queryset()
        serializer = serializers.SlideSerializer(instance=qs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SlideDetails(generics.RetrieveAPIView):
    queryset = models.Slide.objects.filter(user=1)
    serializer_class = serializers.SlideSerializer
    lookup_field = 'slide_id'
    lookup_url_kwarg = 'slide_id'


class UpdateSlide(generics.UpdateAPIView):
    queryset = models.Slide.objects.filter(user=1)
    serializer_class = serializers.UpdateSlideForm
    lookup_field = 'slide_id'
    lookup_url_kwarg = 'slide_id'


class GetBlock(generics.RetrieveAPIView):
    queryset = models.Slide.objects.filter(user=1)
    serializer_class = serializers.BlockSerializer
    lookup_field = 'slide_id'
    lookup_url_kwarg = 'slide_id'

    def get_object(self):
        slide: models.Slide = super().get_object()
        block_id = self.kwargs['block_id']
        return get_object_or_404(slide.blocks.all(), block_id=block_id)


class CreateBlock(generics.CreateAPIView):
    queryset = models.Slide.objects.filter(user=1)
    serializer_class = serializers.BlockForm
    lookup_field = 'slide_id'
    lookup_url_kwarg = 'slide_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        slide: models.Slide = super().get_object()
        context['slide_id'] = slide.slide_id
        return context


class DeleteBlock(Generic[S], generics.DestroyAPIView):
    queryset = models.Slide.objects.all()
    serializer_class = serializers.BlockSerializer
    lookup_field = 'slide_id'
    lookup_url_kwarg = 'slide_id'

    def get_queryset(self) -> S:
        qs = super().get_queryset()
        user = get_user_model().objects.first()
        return qs.filter(user=user)

    def get_object(self):
        qs = self.get_queryset()
        block_id = self.kargs['block_id']
        return get_object_or_404(qs, block_id=block_id)


# @api_view(http_method_names=['post'])
# def delete_block(request, slide_id, block_id, **kwargs):
#     """Deletes a block on the given slide"""
#     user = get_object_or_404(models.USER_MODEL, pk=1)
#     instance = get_object_or_404(
#         models.Block,
#         slide__user=user,
#         block_id=block_id,
#         slide__slide_id=slide_id
#     )
#     serializer = serializers.SlideSerializer(instance=instance.slide_set.get())
#     instance.delete()
#     return Response(data=serializer.data)


@api_view(http_method_names=['post'])
def update_block(request, slide_id, block_id, **kwargs):
    """Update the configuration for a specific given block
    of the current slide"""
    serializer = serializers.BlockForm(data=request.data)
    serializer.is_valid(raise_exception=True)

    # TODO: Use authentication request.user
    user = get_object_or_404(models.USER_MODEL, pk=1)
    block = models.Block.objects.get(
        slide__user=user,
        slide__slide_id=slide_id,
        block_id=block_id
    )

    for key, value in serializer.data.items():
        setattr(block, key, value)
    block.save()

    update_serializer = serializers.BlockSerializer(instance=block)
    return Response(data=update_serializer.data)


@api_view(http_method_names=['post'])
def update_block_column(request, slide_id, block_id, **kwargs):
    """Update the configuration for a given column
    in the selected block"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    block = models.Block.objects.get(
        slide__user=user,
        slide__slide_id=slide_id,
        block_id=block_id
    )
    sheet = models.DataSource.objects.get(data_source_id=block.data_source)

    serializer = serializers.UpdateBlockColumnForm(
        data=request.data,
        instance=block
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    block_serializer = serializers.BlockSerializer(instance=block)
    return Response(data=block_serializer.data)


@api_view(http_method_names=['get'])
def view_final_slide(request, slide_id, **kwargs):
    """This shows the end user the final slide
    with the data and the different filters that
    were implemented by the creator on the data"""
    slide = get_object_or_404(
        models.Slide,
        slide_id=slide_id,
        active=True
    )
    sheet = get_object_or_404(
        sheets_models.DataSource,
        data_source_id=slide.data_source_id
    )
    file = sheet.csv_file.open(mode='r')
    df = pandas.read_csv(file)
    file.close()

    # For each block, will process the data
    # in the dataframe using the data filters
    # specified for the specific block-section
    final_df = None
    return_data = {}
    for block in slide.blocks:
        data_filters = block.conditions['filters']
        for data_filter in data_filters:
            column = data_filter['column']
            operator = data_filter['operator']
            value = data_filter['value']

            if final_df is None:
                final_df = df

            if operator == 'contains':
                final_df = final_df[final_df[column].isin([value]) == True]


@api_view(http_method_names=['post'])
def filter_slide_data(request, **kwargs):
    serializer = serializers.SlideFilteringForm(data=request.data)
    serializer.is_valid(raise_exception=True)
    slide = serializer.save()

    initial_data = serializer.validated_data['data'].copy()
    try:
        results = initial_data['results']
    except:
        raise ValidationError('The data to format is not formatted correctly')

    query_conditions = {
        'Is': '{column} == "{value}"',
        'Is not': '{column} != "{value}"',
        'Contains': '"{value}" in {column}',
        'Does not contain': '"{value}" not in {column}'
        # Is within
        # Is before
        # Is after
        # Is on or before
        # Is on or after
        # Today
        # Tomorrow
        # Yesterday
        # One week ago
        # One week from now
        # One month ago
        # One month from now
        # Number of days ago
        # Number of days from now
        # Exact date
    }

    df = pandas.DataFrame(results)

    filtered_df = None
    for item in serializer.validated_data['conditions']:
        query_condition = query_conditions[item['operator']]
        data_query = query_condition.format(
            column=item['column'],
            value=item['value']
        )
        if filtered_df is None:
            filtered_df = df.query(data_query)
        else:
            filtered_df = filtered_df.query(data_query)
    final_data = filtered_df.to_json(force_ascii=False, orient='records')
    initial_data['results'] = json.loads(final_data)
    return Response(initial_data)


@api_view(http_method_names=['post'])
def search_slide_data(request, slide_id, **kwargs):
    data = []
    search = request.data.get('q')

    if search is not None:
        slide = models.Slide.objects.get(slide_id=slide_id)
        file = slide.slide_data_source.csv_file.open(mode='r')
        df = pandas.read_csv(file)
        file.close()

        def search_columns(row):
            return search in (row[column] for column in df.columns)

        df['found'] = df.apply(search_columns, axis=1)
        df = df[df['found'] == True]
        data = json.loads(df.to_json(orient='records'))
    return Response(data)
