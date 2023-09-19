from .models import Reservation
from django.db import transaction 
from .serializers import ReservationSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationListCreateView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes= [IsAuthenticated]

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            user = self.request.user
            parking_space = serializer.validated_data.get('parking_space')

            # Check if a reservation already exists for the same user and parking space
            existing_reservation = Reservation.objects.filter(user=user, parking_space=parking_space).first()
            
            if existing_reservation  : 
                return Response({'detail': 'This space is already reserved'}, status=status.HTTP_400_BAD_REQUEST)

            user_type = self.request.session.get('user_type', 'guest')
            if user_type == 'employee':
                end_time = datetime.now() + timedelta(hours=8)
            else:
                end_time = datetime.now() + timedelta(hours=1)

            serializer.save(user=user, start_time=datetime.now(), end_time=end_time)
            # Update the corresponding ParkingSpace object's is_reserved field to True
            parking_space.is_reserved = True
            parking_space.is_available= False
            parking_space.save()
            return Response({'detail': 'Reservation created successfully.', "space":parking_space }, status=status.HTTP_201_CREATED)
        except e:
            return Response({'detail': "Model Error!, Please varify model's field and contraints"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


class ReservationCancelView(generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            reservation = self.get_object()
            # Check if the user has the permission to cancel the reservation
            if reservation.user == request.user:
                parking_space = reservation.parking_space
                parking_space.is_available=True;
                parking_space.is_reserved = False;

                parking_space.save()

                reservation.delete()
                return Response({'detail': 'Reservation canceled successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'You do not have permission to cancel this reservation.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e :
            return Response({'detail': 'Reservation not found.'}, status=status.HTTP_404_NOT_FOUND)


