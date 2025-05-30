from rest_framework import serializers

from core.models import Scan, Check, Finding


class ScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scan
        fields = ('id', 'status', 'created_at', 'updated_at', 'ended_at')
        read_only_fields = ('id', 'status', 'created_at', 'updated_at', 'ended_at')


class ScanStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scan
        fields = ('status',)


class CheckSerializer(serializers.ModelSerializer):
    scan = ScanSerializer(read_only=True)

    class Meta:
        model = Check
        fields = ('id', 'scan', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class FindingSerializer(serializers.ModelSerializer):
    check = CheckSerializer(read_only=True)

    class Meta:
        model = Finding
        fields = ('id', 'check', 'resource_id', 'description', 'severity', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
