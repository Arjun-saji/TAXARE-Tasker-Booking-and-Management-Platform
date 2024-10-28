from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from users.models import *
from django.db.models import Q
import logging
from .signals import notify_user, notify_tasker
from users.views import *
from django.views.decorators.csrf import csrf_exempt

# Set up logging
logger = logging.getLogger(__name__)

def taskfilter_view(request,service_id):
	print(f"Logged-in user 1111: {request.user}")
	#print(request.user)
	service=Service.objects.get(id=service_id)
	taskers=TaskerProfile.objects.filter(services=service)

	start_time=request.GET.get("start_time")
	end_time=request.GET.get("end_time")
	location=request.GET.get("location")

	if start_time and end_time:
		logger.info("Filtered taskers by location: %s", taskers)
		tasker=taskers.filter(Q(availability_start__lte=start_time),Q(availability_end__gte=end_time))
		
	if location:
		tasker=taskers.filter(city=location)
		logger.info("Filtered taskers by location: %s", taskers)


	context={"tasker":tasker,"service_id":service_id,"service": service}
	logger.info("Context prepared for rendering: %s", context)
	

	return render(request,"customer/cust_single.html",context)


@login_required
def book_service(request, tasker_id, service_id):
	tasker = get_object_or_404(TaskerProfile, id=tasker_id)
	service = get_object_or_404(Service, id=service_id)

	if request.method == "POST":
		date_booking = request.POST.get("date_booking")
		start_time = request.POST.get("start_time")
		end_time = request.POST.get("end_time")
		tasker_price_suggestion = request.POST.get("tasker_price_suggestion")
		customer_profile = get_object_or_404(CustomerProfile, user=request.user)
		
		print(f"Customer Profile User: {customer_profile.user}")
		print(f"Tasker User: {tasker.user}")
  
		try:
			# Create the booking
			booking = Booking.objects.create(
				customer=customer_profile,
				date_booking=date_booking,
				start_time=start_time,
				end_time=end_time,
				tasker_price_suggestion=tasker_price_suggestion,
				tasker=tasker,
				service=service
			)
			print(f"Type of tasker: {type(tasker)}")  # Should show TaskerProfile
			print(f"Type of customer: {type(customer_profile)}")  # Should show CustomerProfile


			# Notify user and tasker
			# notify_user(customer_profile.user, f"You have booked {tasker.user.username} for {service.name}")
			# notify_tasker(tasker, f"You have a new booking request from {customer_profile.user.username} for {service.name}")

			return redirect("success")

		except Exception as e:
			print(f"Error creating booking: {e}")  # Log the exception
			# Optionally, you could handle the error more gracefully here, e.g., by showing an error message.

	context = {"tasker": tasker, "service": service}
	return render(request, "customer/booking_service.html", context)


# @login_required
# def notifications_view(request):
# 	notifications = request.user.notifications.all()
# 	return render(request, 'notifications.html', {'notifications': notifications})
	
@csrf_exempt
@login_required
def mark_notification_as_read(request, notification_id):
	print(f"Marking notification {notification_id} as read")
	notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
	notification.is_read = True  # Mark as read
	notification.save()
	print("its working")
	return redirect('all_notifications')







		









