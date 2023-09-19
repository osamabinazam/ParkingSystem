from rest_framework import viewsets
from .models import EntryExitRecord
from .serializers import EntryExitRecordSerializer

class EntryExitRecordViewSet(viewsets.ModelViewSet):
    queryset = EntryExitRecord.objects.all()
    serializer_class = EntryExitRecordSerializer
