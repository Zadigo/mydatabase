
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from slides import models
from slides.api import serializers


@api_view(http_method_names=['post'])
def create_slide(request, **kwargs):
    """Lets the user create a new slide"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    serializer = serializers.NewSlideForm(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save(user)
    serialized_data = serializers.SlideSerializer(instance=instance)
    return Response(data=serialized_data.data)


@api_view(http_method_names=['get'])
def list_slides(request, **kwargs):
    """Return all the slides created by the user"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    queryset = models.Slide.objects.filter(user=user)
    serializer = serializers.SlideSerializer(instance=queryset, many=True)
    return Response(data=serializer.data)


@api_view(http_method_names=['get'])
def slide_details(request, slide_id, **kwargs):
    user = get_object_or_404(models.USER_MODEL, pk=1)
    instance = get_object_or_404(
        models.Slide,
        user=user,
        slide_id=slide_id
    )
    serializer = serializers.SlideSerializer(instance=instance)
    return Response(data=serializer.data)


@api_view(http_method_names=['post'])
def update_slide(request, slide_id, **kwargs):
    """Update the information for a particular slide"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    slide = get_object_or_404(models.Slide, user=user, slide_id=slide_id)

    serializer = serializers.UpdateSlideForm(data=request.data, instance=slide)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    response_serializer = serializers.SlideSerializer(instance=slide)
    return Response(data=response_serializer.data)


@api_view(http_method_names=['get'])
def get_block(request, slide_id, block_id, **kwargs):
    """Return a specific block for a given slide"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    queryset = models.Block.objects.filter(
        slide__user=user,
        slide__slide_id=slide_id,
        block_id=block_id
    )
    if not queryset.exists():
        raise NotFound({'block_id': 'Block does not exist'})

    try:
        instance = queryset.get()
    except:
        raise ValidationError('An error occured')

    serializer = serializers.BlockSerializer(instance=instance)
    return Response(data=serializer.data)


@api_view(http_method_names=['post'])
def create_block(request, slide_id, **kwargs):
    """Creates a new block for the given slide"""
    serializer = serializers.BlockForm(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(models.USER_MODEL, pk=1)
    slide = get_object_or_404(models.Slide, user=user, slide_id=slide_id)

    block = slide.blocks.create(**serializer.validated_data)
    # Set these fields be able to act on every
    # column in the dataset by default
    sheet_connection = slide.sheets.latest('created_on')
    block.record_creation_columns = sheet_connection.columns
    block.record_update_columns = sheet_connection.columns
    block.search_columns = sheet_connection.columns
    block.save()

    create_serializer = serializers.BlockSerializer(instance=block)
    return Response(data=create_serializer.data)


@api_view(http_method_names=['post'])
def delete_block(request, slide_id, block_id, **kwargs):
    """Deletes a block on the given slide"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    instance = get_object_or_404(
        models.Block,
        slide__user=user,
        block_id=block_id,
        slide__slide_id=slide_id
    )
    serializer = serializers.SlideSerializer(instance=instance.slide_set.get())
    instance.delete()
    return Response(data=serializer.data)


@api_view(http_method_names=['post'])
def update_block(request, slide_id, block_id, **kwargs):
    """Update the configuration for a specific given block
    of the current slide"""
    serializer = serializers.BlockForm(data=request.data)
    serializer.is_valid(raise_exception=True)

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
    sheet = models.Sheet.objects.get(sheet_id=block.data_source)

    serializer = serializers.UpdateBlockColumnForm(
        data=request.data, instance=block)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'state': True})
