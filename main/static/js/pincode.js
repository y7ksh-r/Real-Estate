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
    function updateNearbyProperties(properties, nearby_city) {
        const container = document.getElementById("properties-container");
        container.innerHTML = ""; // Clear existing content
        document.getElementById("Nearby-city-name").innerText = `Near ${nearby_city}`; // Update city name
    
        properties.forEach(property => {
            const propertyDiv = document.createElement("div");
            propertyDiv.className = "property w-[180px] h-[310px] lg:w-[250px] lg:h-[428px] flex flex-col relative group";
    
            // Create the anchor tag wrapping the entire property div content
            const anchorTag = document.createElement("a");
            anchorTag.href = "/prop_view/" + property.id; // Link to the specific property page
            anchorTag.className = "w-full h-full"; // Make sure anchor tag covers the whole area
            anchorTag.style.display = "block"; // Make anchor tag a block element
    
            // Set the innerHTML of the anchor tag (wrap all content in it)
            anchorTag.innerHTML = `
                <div class="display h-full w-full overflow-hidden rounded-2xl">
                    <img src="/media/${property.main_img}" alt="Beautiful Family Home"
                        class="object-cover object-center w-full h-full group-hover:scale-110 duration-500">
                </div>
    
                <div class="description h-[43%] lg:h-[37%] lg:mt-[111%] w-full space-y-2 px-2 py-1 absolute bottom-0 backdrop-blur-lg rounded-2xl lg:space-y-4 text-sm">
                    <h2 class="font-semibold !text-xl price">₹ ${property.price2}</h2>
                    <div class="flex gap-x-5 h-6 overflow-hidden text-white">
                        <p>${property.title}</p>
                        <p>|</p>
                        <p>${property.bedrooms}BHK</p>
                    </div>
                    <p class="text-white">${property.city} - ${property.zip_code}</p>
                    <div class="flex justify-between items-center rounded-full border border-black px-2 -mx-1">
                        <span class="text-xs">More details</span>
                        <span class="group-hover:rotate-[360deg] duration-500">
                            <img src="/media/icons/arrow.png" alt="" class="h-6">
                        </span>
                    </div>
                </div>
            `;
    
            // Append the anchor tag to the property div
            propertyDiv.appendChild(anchorTag);
    
            // Append the property div to the container
            container.appendChild(propertyDiv);
        });
        container.style.overflowX = 'auto';  // Ensure overflow-x is enabled
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
