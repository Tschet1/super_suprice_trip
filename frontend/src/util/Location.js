import Axios from 'axios';

export const getLocation = async () => {
    if ("geolocation" in navigator) {
        // navigator.geolocation.getCurrentPosition();
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                return { latitude, longitude };
            },
            (error) => { return ipLookUp() })
    } else {
        console.error('Failed to retrieve location via navigator... using ip');
        const coords = ipLookUp();
        return coords;
    }
}

const ipLookUp = async () => {
    console.log("hi")
    Axios.get('http://ip-api.com/json').then(item => console.log(item));

}