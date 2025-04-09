from datetime import datetime
from django.http import JsonResponse
from restaurants.models import Restaurant

def open_restaurants(request):
    datetime_string = request.GET.get('datetime')
    if not datetime_string:
        return JsonResponse({"error": "Missing 'datetime' parameter"}, status=400)

    try:
        input_datetime = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return JsonResponse({"error": "Invalid datetime format. Use 'YYYY-MM-DD HH:MM:SS'."}, status=400)

    input_day = input_datetime.strftime('%A')
    input_time = input_datetime.strftime('%H:%M')

    open_restaurants = []

    for restaurant in Restaurant.objects.all():
        hours = restaurant.hours.split(';')
        for hour in hours:
            if input_day in hour:
                time_range = hour.split(' ')[1]
                start_time, end_time = time_range.split('-')
                if start_time <= input_time <= end_time:
                    open_restaurants.append(restaurant.name)
                    break

    return JsonResponse({"open_restaurants": open_restaurants})