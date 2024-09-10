from rest_framework import serializers
from .models import Item, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  # Include 'id' if you want to reference tags by their ID

class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)  # Nested serializer for tags

    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        item = Item.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            item.tags.add(tag)
        return item

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
        instance.time_estimate = validated_data.get('time_estimate', instance.time_estimate)
        instance.save()

        # Update tags
        instance.tags.clear()  # Clear existing tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)

        return instance