from rest_framework import generics , status
from .serializers import ParkingSpaceSerializer
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import ParkingSpaceSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from parking.models import ParkingSpace


# List all parking spaces
class ParkingSpaceListView(generics.ListAPIView):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer
    permission_classes = [IsAuthenticated]
        

# This View give additional information of particular parking space
class ParkingSpaceViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def detail_view(self, request, pk=None):
        parking_space = self.get_object()
        serializer = self.get_serializer(parking_space)
        return Response(serializer.data)


# This veiwset create parking space
class ParkingSpaceCreateView(generics.CreateAPIView):
    serializer_class = ParkingSpaceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            space_number = serializer.validated_data.get('space_number')
            is_available =  serializer.validated_data.get('is_available')
            is_reserved = serializer.validated_data.get('is_reserved')

            exist_parking = ParkingSpace.objects.filter(space_number=space_number).first()
            if exist_parking:
                return Response({'detail':'Space is already created'}, status=status.HTTP_400_BAD_REQUEST )

            serializer.save( space_number=space_number, is_available=is_available, is_reserved=is_reserved)
            return Response({'detial':'Parking Space created Successfully'})
        except e:
            return Response({'detail': 'Model Error!, Please varify model field and contraints'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )



class ParkingSpaceDeleteView(generics.DestroyAPIView):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer
    permission_classes = [IsAuthenticated]

    def destroy (self, request, *args, **kwargs):
        try:
            parking_space = self.get_object()
            parking_space.delete()
            return Response({'detail': 'Space removed successfully' } , status=status.HTTP_204_NO_CONTENT )
        except Exception as e:
            return Response({'detail': 'Space not found.'}, status=status.HTTP_404_NOT_FOUND)


class GetFirstAvailableParking(generics.ListAPIView):
    serializer_class = ParkingSpaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the first available parking space
        parking_space = ParkingSpace.objects.filter(is_available=True).first()
        
        # Return a single-item list or None if no parking space is available
        return [parking_space] if parking_space else []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        if queryset:
            parking_id = queryset[0].id
            return Response({"parking": parking_id}, status=200) # Return the first item as JSON response
        else:
            return Response({"detail": "No available parking slots found"}, status=404)
# def get_first_availablepark(request):
    # try:
    #     parking = ParkingSpace.objects.filter(is_available=True).first()

    #     if parking:
    #         print(parking   )
    #         # If a parking space is available, include it in the JSON response
    #         return JsonResponse({"detail": "Slot is Available", "parking": parking.id}, status=status.HTTP_200_OK)
    #     else:
    #         return JsonResponse({"detail": "No available parking slots found"}, status=status.HTTP_404_NOT_FOUND)
    # except Exception as e:
    #     return JsonResponse({"detail": "Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    