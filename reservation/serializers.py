from rest_framework import serializers
from .models import Reservation, ReservationHistory
from entryexit.models import EntryExitRecord

class ReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reservation
        fields = "__all__"

class ReservationHistorySerializer(serializers.ModelSerializer):
    reservation_user = serializers.CharField(source='reservation.user.username')
    reservation_parking_space = serializers.CharField(source='reservation.parking_space.space_number')
    reservation_start_time = serializers.SerializerMethodField()
    reservation_end_time = serializers.SerializerMethodField()
    entry_time = serializers.SerializerMethodField()
    exit_time = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    class Meta:
        model = ReservationHistory
        fields = '__all__'
