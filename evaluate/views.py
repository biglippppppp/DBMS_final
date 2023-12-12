from django.shortcuts import render,redirect

class FakeEvaluate:
        def __init__(self, evaluatorUserID, evaluatedUserID, ranking, rankingDate, comment, avg_score):
            self.evaluatorUserID = evaluatorUserID
            self.evaluatedUserID = evaluatedUserID
            self.ranking = ranking
            self.rankingDate = rankingDate
            self.comment = comment
            self.avg_score = avg_score

app_name = 'evaluate'


def evaluate_detail(request, user_id):
    evaluate1 = FakeEvaluate('0001', '0050', 4, '2023/10/03', 'Good!', 3.5)
    evaluate2 = FakeEvaluate('0001', '0100', 5, '2021/01/23', '交貨速度快', 4.5)
    evaluate3 = FakeEvaluate('0001', '7073', 2, '20222/05/24', '二手書品質極差', 3)
    return render(request, 'evaluate/evaluate_detail.html', {'user_id': evaluatedUserID, 'avg_score': avg_score, 'evaluates': evaluates})
    
def evaluate_buyers(request):
    received_buyers = Order.objects.filter(seller=request.user).values('buyer').distinct()
    return render(request, 'evaluate/evaluate_detail.html', {'received_buyers': received_buyers})

def evaluate_sellers(request):
    given_sellers = Order.objects.filter(buyer=request.user).values('seller').distinct()
    return render(request, 'evaluate/evaluate_detail.html', {'given_sellers': given_sellers})
    
def write_review(request, target_user):
    return render(request, 'evaluate_write.html', {'target_user': target_user})