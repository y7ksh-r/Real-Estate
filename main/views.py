from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import*
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Abs
from django.contrib import messages
import boto3
from django.utils.http import url_has_allowed_host_and_scheme
from datetime import datetime,timedelta
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import json
import pyotp
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


def fetch_nearby_properties(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        pincode = data.get("pincode")
        nearby_city = data.get("city")
        if pincode:
            properties = Property.objects.filter(zip_code=pincode).values(
                'id', 'title', 'description', 'address', 'city', 'state', 'zip_code',
                'property_type', 'property_status', 'price', 'bedrooms', 'bathrooms',
                'square_feet', 'map_url', 'video', 'lot_size', 'year_built',
                'is_published', 'list_date', 'devloper', 'price2', 'main_img'
            )
            
            # Get the city of the first property to display

           
            return JsonResponse({"success": True, "properties": list(properties), "nearby_city": nearby_city})
        else:
            return JsonResponse({"success": False, "message": "Pincode not provided."})

    return JsonResponse({"success": False, "message": "Invalid request method."})

def special_page_filter(request,fid):
    if fid ==1:
     filter_name="Under Construction"
     properties=Property.objects.filter(property_status="underconstrution")
    if fid ==2:
     filter_name="Ready to Move"
     properties=Property.objects.filter(property_status="readytomove")
    if fid ==3:
        filter_name="Cost Efficient"
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
    return render(request,'special_filter_page.html',{'properties':properties,'filter_name':filter_name})
def contact_agent(request):
    if request.method == "GET":
        # Render the contact form page
        return render(request, 'contact_agent.html')

    if request.method == "POST":
        # Extract form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Check if a record with the same phone number already exists
        if agent_inquiry.objects.filter(phone=phone).exists():
            # Add an error message and redirect back
            messages.error(request, "OUR AGENT HAS ALREADY RECEIVED YOUR INQUIRY, PLEASE WAIT FOR THE RESPONSE.")
        else:
            # Save the inquiry
            inquiry = agent_inquiry(name=name, email=email, phone=phone, message=message)
            inquiry.save()

            # Add a success message
            messages.success(request, "OUR AGENT WILL CONTACT YOU SOON!")

        # Get the next_url (previous page)
        next_url = request.POST.get('next_url', '/')
        
        # Redirect back to the previous page or fallback to home
        return redirect(next_url)

    # Handle other HTTP methods
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
def load_projects(request):
    city_id = request.GET.get('city_id')
    projects = Property.objects.filter(city=city_id).all()

    return JsonResponse(list(projects.values('id', 'title')), safe=False)


def prop_view(request,pid):
  
   property = Property.objects.get(id=pid)
   t_photos=Photo.objects.filter(property=pid)
   photos=Photo.objects.filter(property=pid)[:4]
   total=len(t_photos)
   amenities=property.amenities.all()

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
   return render(request, 'prop_view.html', {'prop': property,'photos':photos,'remaining':total,"sp":similar_price_property,"sc":similar_price_city_property,'sd':similar_price_developer_property,'ss':similar_size_property,'amenities':amenities})
def otp_verification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_no = data.get('phone_no')
        data = json.loads(request.body)
    
        # Generate and send OTP with 10-minute validity (600 seconds)
        totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        otp = totp.now()
        print(otp)
        # Store the secret key and OTP expiration time in the session (valid for 10 minutes)
        request.session['otp_secret_key'] = totp.secret
        valid_date = datetime.now() + timedelta(minutes=5)
        request.session['valid_time'] = valid_date.isoformat()  # Store as ISO format for better consistency
        request.session['phone_no'] = phone_no

        # Create SNS client and send the OTP
        client = boto3.client('sns', 
            region_name="ap-south-1",
            aws_access_key_id="AKIA356SJVSG5OU6P4M3",
            aws_secret_access_key="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")
        message = f"VEFICATION CODE FOR NCPR INQUIRY IS: {otp}. It will expire in 5 minutes."

        try:
            client.publish(PhoneNumber=phone_no, Message=message)
            return JsonResponse({'success': True, 'message': "OTP sent successfully!"})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_otp = data.get('otp')
        print(entered_otp)
        otp_secret_key = request.session.get('otp_secret_key')
        valid_time = request.session.get('valid_time')
        # Check if OTP is still valid
        if otp_secret_key and valid_time:
            valid_time = datetime.fromisoformat(valid_time)
            if datetime.now() > valid_time:
                return JsonResponse({'success': False, 'error': "OTP has expired."})

            # Verify OTP
            totp = pyotp.TOTP(otp_secret_key, interval=300)
            if totp.verify(entered_otp):
                request.session['otp_verified'] = True  # Mark OTP as verified
                return JsonResponse({'success': True, 'message': "OTP verified successfully!"})
            else:
                return JsonResponse({'success': False, 'error': " INVALID OTP."})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
from django.shortcuts import redirect, render
from datetime import datetime
def abt_us(request):
    if not request.session.get('otp_verified'):
        return redirect('otp_verification')  # Redirect to OTP verification if not verified

    if request.method == 'POST':
        property = request.POST.get("property")
        property_id = request.POST.get("property_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone_no")
        email = request.POST.get("email")
        print(name)
        # Save the inquiry if OTP was verified
        if request.session.get('otp_verified'):
            inquiry = inq(name=name, contactno=phone, email=email, property=property)
            inquiry.save()

            # Clear the session after successful inquiry
            request.session.pop('otp_verified', None)
            request.session.pop('otp_secret_key', None)
            request.session.pop('valid_time', None)
            messages.success(request, 'Your inquiry has been submitted successfully!')
        return redirect(f'/prop_view/{property_id}')


    return render(request, 'inquiry_form.html')
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
