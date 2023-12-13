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
    # Fix the variable names here
    evaluatedUserID = evaluate1.evaluatedUserID
    avg_score = evaluate1.avg_score
    evaluates = [evaluate1, evaluate2, evaluate3]
    
    return render(request, 'evaluate/evaluate_detail.html', {'user_id': evaluatedUserID, 'avg_score': avg_score, 'evaluates': evaluates})
    
def evaluate_buyers(request):
    received_buyers = Order.objects.filter(seller=request.user).values('buyer').distinct()
    return render(request, 'evaluate/evaluate_detail.html', {'received_buyers': received_buyers})

def evaluate_sellers(request):
    given_sellers = Order.objects.filter(buyer=request.user).values('seller').distinct()
    return render(request, 'evaluate/evaluate_detail.html', {'given_sellers': given_sellers})
"""  
def evaluate_user(request):
    return render(request, 'evaluate/evaluate_user.html')
"""  
def evaluate_user(request, user_id):
    if request.method == 'POST':
        # Process form data and save to the database
        return render(request, 'evaluate/evaluate_user.html', {'user_id': user_id})
    else:
        return render(request, 'evaluate/evaluate_user.html', {'user_id': user_id})
    
def write_review(request, user_id):
    return render(request, 'evaluate_write.html', {'user_id': user_id})