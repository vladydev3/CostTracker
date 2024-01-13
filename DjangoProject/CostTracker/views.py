from django.shortcuts import render
from django.http import JsonResponse
from .models import Cost

def submit_cost(request):
    """
    Handles the submission of a cost.

    If the request method is POST, it creates a new cost with the category, amount, and date provided in the request.
    If the request method is not POST, it renders the 'submit_cost.html' template.

    Returns:
        JsonResponse: A message indicating the success of the cost creation if the request method is POST.
        HttpResponse: The rendered 'submit_cost.html' template if the request method is not POST.
    """
    if request.method == 'POST':
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        cost = Cost(category=category, amount=amount, date=date)
        cost.save()
        return JsonResponse({'message': 'Cost created successfully!'}, status=201)
    else :
        return render(request, 'CostTracker/submit_cost.html')

def upload_file(request):
    """
    Handles the uploading of a file to a cost.

    If the request method is POST, it attaches a file to the cost with the given ID.
    If the request method is not POST, it renders the 'upload_file.html' template.

    Returns:
        JsonResponse: A message indicating the success of the file upload if the request method is POST.
        HttpResponse: The rendered 'upload_file.html' template if the request method is not POST.
    """
    if request.method == 'POST':
        file = request.FILES['file']
        cost_id = request.POST['cost_id']
        cost = Cost.objects.get(id=cost_id)
        cost.file.save(file.name, file, save=True)
        return JsonResponse({'message': 'File uploaded successfully!'}, status=201)
    else:
        return render(request, 'CostTracker/upload_file.html')

def get_costs(request):
    """
    Retrieves a list of costs with optional filters for category, amount, and date.

    If the request method is GET, it retrieves all costs that match the provided filters.
    If no filters are provided, it retrieves all costs.
    If the request method is not GET, it renders the 'get_costs.html' template.

    Returns:
        JsonResponse: A list of costs that match the provided filters if the request method is GET.
        HttpResponse: The rendered 'get_costs.html' template if the request method is not GET.
    """
    if request.method == 'GET':
        if request.GET:
            category = request.GET.get('category')
            amount = request.GET.get('amount')
            date = request.GET.get('date')

            costs = Cost.objects.all()
            if category is not None and category != '':
                costs = costs.filter(category=category)
            if amount is not None and amount != '':
                try:
                    amount = float(amount)
                except ValueError:
                    return JsonResponse({'message': 'Amount must be a number'}, status=400)
                costs = costs.filter(amount=amount)
            if date is not None and date != '':
                costs = costs.filter(date=date)
            costs = list(costs.values())
            return JsonResponse(costs, safe=False)
        else:
            return render(request, 'CostTracker/get_costs.html')
    
def home(request):
    return render(request, 'CostTracker/home.html')

