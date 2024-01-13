from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Cost
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class SubmitCostView(LoginRequiredMixin, APIView):
    @swagger_auto_schema(responses={201: openapi.Response(description="Cost created successfully!", schema=openapi.Schema(type=openapi.TYPE_OBJECT))})
    def post(self, request):
        try:
            category = request.POST['category']
            amount = request.POST['amount']
            date = request.POST['date']
            cost = Cost(category=category, amount=amount, date=date)
            cost.save()
            return JsonResponse({'message': 'Cost created successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get(self, request):
        return render(request, 'CostTracker/submit_cost.html')


class UploadFileView(LoginRequiredMixin, APIView):
    @swagger_auto_schema(responses={201: openapi.Response(description="File uploaded successfully!", schema=openapi.Schema(type=openapi.TYPE_OBJECT))})
    def post(self, request):
        try:
            file = request.FILES['file']
            cost_id = request.POST['cost_id']
            cost = Cost.objects.get(id=cost_id)
            cost.file.save(file.name, file, save=True)
            return JsonResponse({'message': 'File uploaded successfully!'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Cost not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get(self, request):
        return render(request, 'CostTracker/upload_file.html')


class GetCostsView(LoginRequiredMixin, APIView):
    @swagger_auto_schema(responses={200: openapi.Response(description="A list of costs", schema=openapi.Schema(type=openapi.TYPE_OBJECT))})
    def get(self, request):
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def home(request):
    return render(request, 'CostTracker/home.html')