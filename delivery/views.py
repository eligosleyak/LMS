from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Delivery
from .form import StartDeliveryForm, AssignDeliveryForm
from users.models import User
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_rider:
        return redirect('rider-queue')
    return render(request, 'dashboard/dashboard.html')

@login_required
def start_delivery(request):
    if request.method == 'POST':
        form = StartDeliveryForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.sender = request.user
            var.save()
            request.session['delivery'] = var.pk
            context = {}
            return render(request, 'dashboard/dashboard.html', context)
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('start-delivery')
    else:
        form = StartDeliveryForm()
        context = {'form': form}
        return render(request, 'delivery/start_delivery.html', context)


@login_required
def active_delivery(request):
    obj = Delivery.objects.filter(sender=request.user)
    context = {'obj': obj}
    return render(request, 'delivery/active_delivery.html', context)


@login_required
def delivery_history(request):
    obj = Delivery.objects.filter(sender=request.user)
    context = {'obj': obj}
    return render(request, 'delivery/delivery_history.html', context)


@login_required
def assign_delivery(request, pk):
    obj = Delivery.objects.get(pk=pk)
    if request.method == 'POST':
        form = AssignDeliveryForm(request.POST, instance=obj)
        if form.is_valid():
            var = form.save(commit=False)
            var.has_rider = True
            var.save()
            messages.success(request, f'{var.rider} assigned to deliver')
            return redirect('delivery-queue')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('delivery-queue')
    else:
        form = AssignDeliveryForm(instance=obj)
        form.fields['rider'].queryset = User.objects.filter(is_rider=True)
        context = {'form': form, 'obj': obj}
        return render(request, 'delivery/assign_delivery.html', context)


@login_required
def delivery_queue(request):
    obj = Delivery.objects.filter(is_verified=True).order_by('-date_created')
    context = {'obj': obj}
    return render(request, 'delivery/delivery_queue.html', context)


@login_required
def rider_queue(request):
    obj = Delivery.objects.filter(rider=request.user, is_verified=True)
    context = {'obj': obj}
    return render(request, 'delivery/rider_queue.html', context)


@login_required
def complete_delivery(request, pk):
    obj = Delivery.objects.get(pk=pk)
    obj.is_delivered = True
    obj.save()
    messages.success(request, 'Package delivered')
    print(f'Email sent to {obj.sender}')
    return redirect('rider-queue')


@login_required
def delete_delivery(request, pk):
    delivery = Delivery.objects.get(pk=pk)
    delivery.delete()
    return redirect('delivery-queue')

