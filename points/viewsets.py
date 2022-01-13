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

    # custom POST to add receipt to Spend
    def create(self, request, *args, **kwargs):
        spending = request.data.get("points")
        total_transaction_points = sum(Transaction.objects.all().values_list("remaining_points", flat=True))
        receipt = []

        # checks to make sure we have enough spending power
        if spending > total_transaction_points:
            text = "Not enough points. We only have " + str(total_transaction_points) + " available."
            return Response(text, status=status.HTTP_400_BAD_REQUEST)

        for transaction in Transaction.objects.all():
            payer = transaction.payer
            # NEED TO ACCOUNT FOR IF PAYER IS ALREADY IN RECEIPT
            r = {
                "payer": payer.name,
                "points": 0
            }

            if transaction.remaining_points == 0:
                break
            elif transaction.remaining_points <= spending:
                r["points"] -= transaction.remaining_points
                spending -= transaction.remaining_points
                payer.total_points -= transaction.remaining_points
                transaction.remaining_points = 0
            else:
                r['points'] -= spending
                payer.total_points -= spending
                transaction.remaining_points -= spending
                transaction.save()
                spending = 0

            receipt.append(r)
            payer.save()

            if spending == 0:
                break

        # check receipt. remove any positive values from it

        request.data["receipt"] = receipt

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
