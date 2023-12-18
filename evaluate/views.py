from django.shortcuts import render,redirect
import requests
from main_p.models import Users


app_name = 'evaluate'


def evaluate_detail(request, user_id):
    api_url = f'http://localhost:8000/evaluate/api/personal_evaluation/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    evaluates = api_response.get('evaluates')
    avg_score = api_response.get('avg_score')

    return render(request, 'evaluate/evaluate_detail.html',
                  {'user_id': user_id, 'avg_score': avg_score, 'evaluates': evaluates})

def evaluate_user(request, user_id):
    api_url = f'http://localhost:8000/evaluate/api/evaluate/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    received_buyers = api_response.get('receive_buyers')
    given_sellers = api_response.get('given_sellers')
    return render(request, 'evaluate/evaluate_user.html', {'user_id': user_id,
                                                           'received_buyers': received_buyers, 'given_sellers': given_sellers})


def write_review(request, user_id, target_id):
    target_user = Users.objects.get(userid= target_id)
    if request.method == 'POST':
        api_url = f'http://localhost:8000/evaluate/api/post/{user_id}/{target_id}'
        score = request.POST.get('score')
        comment = request.POST.get('comment')
        api_response = requests.post(api_url, data={'ranking': score, 'comment': comment})
        api_response = api_response.json()
        return redirect('evaluate:evaluate_detail', user_id=target_id)
    return render(request, 'evaluate/evaluate_write.html', {'user_id': user_id, 'target_user': target_user})
