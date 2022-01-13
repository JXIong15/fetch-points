from .models import Payer, Transaction, Spend
from .serializers import PayerSerializer, TransactionSerializer, SpendSerializer
from rest_framework import viewsets, status, filters
from rest_framework.response import Response


class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # customize POST to add 'remaining_points' field
    def create(self, request, *args, **kwargs):
        payer_id = request.data.get("payer")
        payer = Payer.objects.get(id=payer_id)
        points = request.data.get("points")
        new_payer_total = payer.total_points + points

        # checks if payer has enough points
        if new_payer_total < 0:
            text = "Not enough points. " + str(payer.name) + " only has " + str(payer.total_points) + " points available."
            return Response(text, status=status.HTTP_400_BAD_REQUEST)

        payer.total_points = new_payer_total
        payer.save()
        request.data["remaining_points"] = points

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SpendViewSet(viewsets.ModelViewSet):
    queryset = Spend.objects.all()
    serializer_class = SpendSerializer
