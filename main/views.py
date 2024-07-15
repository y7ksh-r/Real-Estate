from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import*
# Create your views here.
def home(request):
    list_proj=Property.objects.all()[:8]
    rtm=Property.objects.filter(property_status="underconstrution")[:4]
    uc=Property.objects.filter(property_status="readytomove")[:4]
    cities=Property.objects.values_list('city',flat=True)
    properties_with_efficiency = []
    for property in list_proj:
        if property.bedrooms > 0:  # Avoid division by zero
            efficiency = property.price / property.bedrooms
            properties_with_efficiency.append((property, efficiency))
    
    # Sort properties by cost efficiency
    properties_with_efficiency.sort(key=lambda x: x[1])
    
    # Extract sorted properties
    sorted_properties = [property for property, efficiency in properties_with_efficiency][:4]
    return render(request,'home.html',{'properties':list_proj,'cities':cities,'rtm':rtm,'uc':uc,'ce':sorted_properties})
def load_projects(request):
    city_id = request.GET.get('city_id')
    projects = Property.objects.filter(city=city_id).all()

    return JsonResponse(list(projects.values('id', 'title')), safe=False)
def filter_obj(request):
    city = request.GET.get("city")
    project = request.GET.get("project")
    price_range = request.GET.get("price_range")
    
    # Default min and max prices
    min_price = None
    max_price = None
    
    # Determine the min and max price based on the selected price range
    if price_range == '10':
        min_price = 1000000
        max_price = 2000000
    elif price_range == '20':
        min_price = 2000000
        max_price = 3000000 
    elif price_range == '30':
        min_price = 3000000
        max_price = 5000000
    elif price_range == '50':
        min_price = 5000000
        max_price = 7000000
    elif price_range == '70':
        min_price = 7000000
        max_price = 9999999
    elif price_range == '1':
        min_price = 10000000

    # Start with all properties
    properties = Property.objects.all()

    # Apply city filter if specified
    if city:
        properties = properties.filter(city=city)

    # Apply project filter if specified
    if project:
        properties = properties.filter(title=project)

    # Apply price range filter if specified
    if min_price is not None:
        properties = properties.filter(price__gte=min_price)
    if max_price is not None:
        properties = properties.filter(price__lte=max_price)
    cities=Property.objects.values_list('city',flat=True)

    return render(request, 'prop_filtter.html', {'properties': properties,'cities':cities})
def prop_view(request,pid):
   property = Property.objects.get(id=pid)
   t_photos=Photo.objects.filter(property=pid)
   photos=Photo.objects.filter(property=pid)[:4]
   total=len(t_photos)
   total=total-3
   return render(request, 'prop_view.html', {'prop': property,'photos':photos,'remaining':total})
def abt_us(request,pid):

    return render(request, 'contactus.html')
def more_img(request,pid):
    photos=Photo.objects.filter(property=pid)
    return render(request,'allphotos.html',{'photos':photos})
