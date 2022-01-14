from .models import Payer, Transaction, Spend
from .serializers import PayerSerializer, TransactionSerializer, SpendSerializer
from rest_framework import viewsets, status, filters
from rest_framework.response import Response


class PayerViewSet(viewsets.ModelViewSet):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer

    def create(self, request, *args, **kwargs):
        if len(request.data) == 2:
            if request.data['total_points'] < 0:
                return Response("Payer Points cannot be negative.", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("timestamp")
    serializer_class = TransactionSerializer

    # customize POST to add 'remaining_points' field
    def create(self, request, *args, **kwargs):
        payer_id = request.data.get("payer")
        payer = Payer.objects.get(id=payer_id)
        points = int(request.data.get("points"))
        new_payer_total = payer.total_points + points

        # checks if payer has enough points
        if new_payer_total < 0:
            text = f"Not enough points. {payer.name} only has {payer.total_points} points available."
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
            text = f"Not enough points. We only have {total_transaction_points} available."
            return Response(text, status=status.HTTP_400_BAD_REQUEST)

        for transaction in Transaction.objects.all().order_by("timestamp"):
            payer = transaction.payer
            r = {
                "payer": payer.name,
                "points": 0
            }

            # checks if player already exists in receipt
            if len(receipt) != 0:
                for item in receipt:
                    if item['payer'] == payer.name:
                        r = item
                        receipt.pop(receipt.index(item))

            if transaction.remaining_points != 0:
                if transaction.remaining_points <= spending:
                    r["points"] -= transaction.remaining_points
                    spending -= transaction.remaining_points
                    payer.total_points -= transaction.remaining_points
                    transaction.remaining_points = 0
                elif transaction.remaining_points > spending:
                    r['points'] -= spending
                    payer.total_points -= spending
                    transaction.remaining_points -= spending
                    spending = 0

            if r['points'] != 0:
                receipt.append(r)

            transaction.save()
            payer.save()

            if spending == 0:
                break

        # prevents positive values in receipt
        for item in receipt:
            if item['points'] > 0 or item['points'] == 0:
                receipt.pop(receipt.index(item))

        request.data["receipt"] = receipt
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
