import axios from 'axios'

export default() => {
    return axios.create({
        baseURL:  'http://127.0.0.1:5050/'   /* API Server Link:  http://18.223.162.208/   `http://18.223.162.208:5050/`  */,
        headers: {
            "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
            //"Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
            "Content-Type": "application/json", // this shows the expected content type
            //'X-User-Identity': userIdentity
        }
    })
}