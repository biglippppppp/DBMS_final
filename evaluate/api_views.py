from rest_framework.views import APIView
from rest_framework.response import Response
from main_p.models import Evaluate
from main_p.models import Users
from main_p.models import WantOrder
from main_p.models import SaleOrder
from main_p.models import Sell
from main_p.models import LookFor
from main_p.models import ReceiveWant
from main_p.models import ReceiveSale
from rest_framework import serializers
from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework import status



class EvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluate
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class PersonalEvaluationAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        evaluates = Evaluate.objects.filter(evaluateduserid=user_id)
        avg_score = Evaluate.avg_score(user_id)
        serializer = EvaluateSerializer(evaluates, many=True)
        return Response({'evaluates': serializer.data, 'user_id':user_id, 'avg_score': avg_score})

class EvlueateAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        received_buyers = []
        given_sellers = []
        sale_orders = SaleOrder.objects.filter(userid=user_id)
        for order in sale_orders:
            sells = Sell.objects.filter(orderid=order.orderid)
            for sell in sells:
                if sell.status == 'Finished':
                    try:
                        receive_sale = ReceiveSale.objects.get(orderid=order.orderid)
                        receiver_id = receive_sale.userid.userid
                        received_buyers.append(Users.objects.get(userid=receiver_id))
                        break
                    except ReceiveSale.DoesNotExist:
                        pass


        want_orders = WantOrder.objects.filter(userid=user_id)
        for order in want_orders:
            lfs = LookFor.objects.filter(orderid=order.orderid)
            for lf in lfs:
                if lf.status == 'Finished':
                    try:
                        receive_want = ReceiveWant.objects.get(orderid=order.orderid)
                        receiver_id = receive_want.userid.userid
                        given_sellers.append(Users.objects.get(userid=receiver_id))
                        break
                    except ReceiveWant.DoesNotExist:
                        pass

        buy_serializer = UsersSerializer(received_buyers, many=True)
        sell_serializer = UsersSerializer(given_sellers, many=True)

        return Response({'receive_buyers':buy_serializer.data, 'given_sellers':sell_serializer.data, 'user_id':user_id})

class PostEvaluationAPIView(APIView):
    def post(self, request, user_id, target_id, *args, **kwargs):
        # 处理 POST 请求中的用户名和密码
        ranking = request.data.get('ranking')
        comment = request.data.get('comment')

        user = Users.objects.get(userid=user_id)
        target = Users.objects.get(userid=target_id)
        target_user = target.username
        current_datetime = timezone.now()
        # If you only want the date part
        current_date = current_datetime.date()
        print(user_id, target_id, ranking, current_date, comment)


        try:
            Evaluate.objects.create(evaluatoruserid=user, evaluateduserid=target, ranking=ranking, rankdate=current_date, comment=comment)


        except IntegrityError as e:

            print(f"IntegrityError occurred: {e}")

            return Response({'error': 'IntegrityError occurred'}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:

            print(f"An exception occurred: {e}")

            return Response({'error': 'An exception occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'target_user': target_user})