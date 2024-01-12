from django.http import JsonResponse
from .models import Cost

# View to submit a cost
def submit_cost(request):
    if request.method == 'POST':
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        cost = Cost(category=category, amount=amount, date=date)
        cost.save()
        return JsonResponse({'message': 'Cost created successfully!'}, status=201)

# View to upload a file to a cost
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        cost_id = request.POST['cost_id']
        cost = Cost.objects.get(id=cost_id)
        cost.file.save(file.name, file, save=True)
        return JsonResponse({'message': 'File uploaded successfully!'}, status=201)

# View to retrieve a list of costs with optional filters for category, amount and date
def get_costs(request):
    costs = Cost.objects.all()
    category = request.GET.get('category', None)
    amount = request.GET.get('amount', None)
    date = request.GET.get('date', None)
    if category is not None:
        costs = costs.filter(category=category)
    if amount is not None:
        costs = costs.filter(amount=float(amount))
    if date is not None:
        costs = costs.filter(date=date)
    costs = list(costs.values())
    return JsonResponse(costs, safe=False)