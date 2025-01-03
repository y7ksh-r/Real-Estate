document.addEventListener("DOMContentLoaded", function () {
    // Function to fetch the user's location
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                // Fetch the pincode using the Nominatim API
                fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`)
                    .then(response => response.json())
                    .then(data => {
                        const pincode = data.address.postcode || "Pincode not found";
                        const city = data.address.city || data.address.town || data.address.village || "City not found";

                        // Send the pincode to the backend via AJAX
                        sendPincodeToBackend(pincode, city);
                    })
                    .catch(error => {
                       
                        document.getElementById("Nearby-city-name").innerText = `Switch On Location Of Better Results`;
                    });
            }, function (error) {
                console.error("Error getting location:", error);
                document.getElementById("Nearby-city-name").innerText = `Switch On Location For Better Results`;
            });
        } else {
            document.getElementById("Nearby-city-name").innerText = `Switch On Location For Better Results`;
        }
    }

    // Function to send pincode to the backend
    function sendPincodeToBackend(pincode,city) {
        fetch("/fetch_nearby_properties/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(), // Add CSRF token for security
            },
            body: JSON.stringify({ pincode: pincode , city: city}),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateNearbyProperties(data.properties,city);
                } else {
                    alert("No nearby properties found.");
                }
            })
            .catch(error => {
                console.error("Error sending pincode to backend:", error);
            });
    }

    // Function to update the page with nearby properties
    function updateNearbyProperties(properties,nearby_city) {
        const container = document.getElementById("properties-container");
        container.innerHTML = ""; // Clear existing content
        document.getElementById("Nearby-city-name").innerText = `Near ${nearby_city}`; // Update city name
        properties.forEach(property => {
            const propertyDiv = document.createElement("div");
            propertyDiv.className = "property w-[206px] h-[345px] lg:w-[280px] lg:h-[475px] flex flex-col relative group";
            
            propertyDiv.innerHTML = `
                <div class="display h-full w-full overflow-hidden rounded-3xl">
                    <a href="prop_view/${property.id}"><img src="/media/${property.main_img}" alt="Beautiful Family Home"
                        class="object-cover object-center w-full h-full group-hover:scale-110 duration-500"></a>
                </div>
                <a href="prop_view/${property.id}">
                <div class="description h-[41%] lg:h-[35%] bottom-0 w-full space-y-2 px-2 absolute backdrop-blur-lg rounded-3xl lg:space-y-4">
                    <h2 class="font-semibold text-2xl price">₹ ${property.price2}</h2>
                    <div class="flex gap-x-5 h-6 overflow-hidden text-white">
                        <p>${property.title}</p>
                        <p>|</p>
                        <p>${property.bedrooms}BHK</p>
                    </div>
                    <p class="text-white">${property.city} - ${property.zip_code}</p>
                    <div class="flex justify-between items-center rounded-3xl border border-black px-2 -mx-1 py-[2px]">
                        <span>More details</span>
                        <span class="group-hover:rotate-[360deg] duration-500">
                            <a href="prop_view/${property.id}"><img src="/media/icons/arrow.png"  class="group-hover:rotate-[360deg] duration-500 h-6" alt="" ></a>
                        </span>
                    </div>
                </div>
            `;
    
            container.appendChild(propertyDiv);
        });
    }

    // Function to get CSRF token from cookies
    function getCSRFToken() {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                return cookie.substring("csrftoken=".length, cookie.length);
            }
        }
        return "";
    }

    // Automatically fetch location on page load
    getLocation();
});
