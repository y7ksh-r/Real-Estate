from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import*
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Abs
from django.contrib import messages
# Create your views here.
from firebase_admin import auth

def verify_otp(request):
    id_token = request.POST.get('id_token')

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        # Create session or perform other actions
        return JsonResponse({"status": "success", "uid": uid})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

def home(request):
    list_proj=Property.objects.all()[:8]
    rtm=Property.objects.filter(property_status="underconstrution")[:4]
    uc=Property.objects.filter(property_status="readytomove")[:4]
    cities=Property.objects.values_list('city',flat=True).distinct()   
    bedrooms=Property.objects.values_list('bedrooms',flat=True).distinct().order_by('bedrooms')
    cities=sorted(set(cities))
    print(cities)
    properties_with_efficiency = []
    for property in list_proj:
        if property.bedrooms > 0:  # Avoid division by zero
            efficiency = property.price / property.bedrooms
            properties_with_efficiency.append((property, efficiency))
    
    # Sort properties by cost efficiency
    properties_with_efficiency.sort(key=lambda x: x[1])
    
    # Extract sorted properties
    sorted_properties = [property for property, efficiency in properties_with_efficiency][:4]
    return render(request,'home.html',{'properties':list_proj,'cities':cities,'rtm':rtm,'uc':uc,'ce':sorted_properties,'bedrooms':bedrooms})

def special_page_filter(request,fid):
    if fid ==1:
     properties=Property.objects.filter(property_status="underconstrution")
    if fid ==2:
     properties=Property.objects.filter(property_status="readytomove")
    if fid ==3:
        list_proj=Property.objects.all()
        properties_with_efficiency = []
        for property in list_proj:
         if property.bedrooms > 0:  # Avoid division by zero
             efficiency = property.price / property.bedrooms
             properties_with_efficiency.append((property, efficiency))
    
    # Sort properties by cost efficiency
        properties_with_efficiency.sort(key=lambda x: x[1])
    
    # Extract sorted properties
        properties = [property for property, efficiency in properties_with_efficiency]
    return render(request,'special_filter_page.html',{'properties':properties})
def load_projects(request):
    city_id = request.GET.get('city_id')
    projects = Property.objects.filter(city=city_id).all()

    return JsonResponse(list(projects.values('id', 'title')), safe=False)


def prop_view(request,pid):
   property = Property.objects.get(id=pid)
   t_photos=Photo.objects.filter(property=pid)
   photos=Photo.objects.filter(property=pid)[:4]
   total=len(t_photos)
   total=total-3
   similar_price_property = Property.objects.annotate(
        price_difference=ExpressionWrapper(
            Abs(F('price') - property.price), output_field=FloatField()
        )
    ).exclude(id=property.id).order_by('price_difference').first()
   similar_price_city_property = Property.objects.filter(city=property.city).annotate(
        price_difference=ExpressionWrapper(
            Abs(F('price') - property.price), output_field=FloatField()
        )
    ).exclude(id=property.id).order_by('price_difference').first()

    # Find another property from the same developer with the closest price
   similar_price_developer_property = Property.objects.filter(devloper=property.devloper).annotate(
        price_difference=ExpressionWrapper(
            Abs(F('price') - property.price), output_field=FloatField()
        )
    ).exclude(id=property.id).order_by('price_difference').first()
   similar_size_property = Property.objects.filter(bedrooms=property.bedrooms).annotate(
        price_difference=ExpressionWrapper(
            Abs(F('price') - property.price), output_field=FloatField()
        )
    ).exclude(id=property.id).order_by('price_difference').first()
   return render(request, 'prop_view.html', {'prop': property,'photos':photos,'remaining':total,"sp":similar_price_property,"sc":similar_price_city_property,'sd':similar_price_developer_property,'ss':similar_size_property})
def abt_us(request):
    property=request.POST.get("property")
    name=request.POST.get("name")
    phone=request.POST.get("phone")
    email=request.POST.get("email")
    inquiry = inq(name=name, contactno=phone, email=email,property=property)
    inquiry.save()


    return redirect("/")
def more_img(request,pid):
    property = Property.objects.get(id=pid)
    photos=Photo.objects.filter(property=pid)
    return render(request,'allphotos.html',{'photos':photos,'property':property})

def filter_obj(request):
    city = request.GET.get("city")
    size = request.GET.get("size")
    price_range = request.GET.get("price_range")
    projects_in_city = Property.objects.filter(city=city).values_list('title', flat=True)
    
    price_ranges = {
        '10': (1000000, 2000000),
        '20': (2000000, 3000000),
        '30': (3000000, 5000000),
        '50': (5000000, 7000000),
        '70': (7000000, 9999999),
        '1': (10000000, None)
    }

    min_price, max_price = price_ranges.get(price_range, (None, None))

    # Start with all properties
    properties = Property.objects.all()

    # Apply city filter if specified and city is not 0
    if city and city != '0':
        properties = properties.filter(city=city)

    # Apply size filter if specified and size is not 0
    if size and size != '0':
        properties = properties.filter(bedrooms=size)

    # Apply price range filter if specified and price range is not 0
    if price_range and price_range != '0':
        if min_price is not None:
            properties = properties.filter(price__gte=min_price)
        if max_price is not None:
            properties = properties.filter(price__lte=max_price)

    # Retrieve distinct cities and sizes
    cities = Property.objects.values_list('city', flat=True).distinct()
    cities=sorted(set(cities))
    bedrooms = Property.objects.values_list('bedrooms', flat=True).distinct().order_by('bedrooms')

    # Apply additional filters based on projects in city, if applicable
    if projects_in_city:
        properties, selected_project_in_city = filter_by_projects_in_city(request, properties)

    # Apply additional filters and get the selected values
    properties, selected_property_types, selected_price_order, selected_status = filter_properties(request, properties)

    # Render the template with the combined filters and selected values
    return render(request, 'prop_filtter.html', {
        'properties': properties,
        'cities': cities,
        'bedrooms': bedrooms,
        'selected_city': city,
        'selected_size': size,
        'selected_price_range': price_range,
        'selected_property_types': selected_property_types,
        'selected_price_order': selected_price_order,
        'selected_status': selected_status,
        'property_type_options': ['house', 'apartment', 'villa', 'plot'],
        'status_options': ['under construction', 'ready to move'],
        'projects_in_city': projects_in_city,
        'selected_project_in_city': selected_project_in_city
    })



def filter_by_projects_in_city(request,properties):
    
    # Retrieve the list of project titles in the specified city
    projects_in_city = request.GET.getlist('projects_in_city')
    if projects_in_city:
        # Filter properties where the title is in the list of projects in the city
        properties = properties.filter(title__in=projects_in_city)
    return properties, projects_in_city


def filter_properties(request, properties):
    # Get additional filter values from the request
    property_types = request.GET.getlist('property_type')
    price_order = request.GET.get('price_order')
    status = request.GET.getlist('status')


    # Apply property type filter if specified
    if property_types:
        properties = properties.filter(property_type__in=property_types)

    # Apply status filter if specified
    if status:
        properties = properties.filter(property_status__in=status)

    # Apply sorting based on price if specified
    if price_order == 'low_to_high':
        properties = properties.order_by('price')
    elif price_order == 'high_to_low':
        properties = properties.order_by('-price')

    # Return the properties along with the selected filters
    return properties, property_types, price_order, status
def about(request):
    return render(request,'about.html')
def services(request):
    return render(request,'services.html')
def contact(request):
    return render(request,'contact.html')
