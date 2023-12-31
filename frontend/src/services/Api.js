import axios from 'axios'

export default() => {
    return axios.create({
        baseURL:  'http://18.218.35.197:5050/'   /* AWS Prod Server: http://18.218.35.197:5050/    Testing Server: http://127.0.0.1:5050/  */,
        headers: {
            "Access-Control-Allow-Headers": "*", // this will allow all CORS requests
            //"Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
            "Content-Type": "application/json", // this shows the expected content type
            //'X-User-Identity': userIdentity
        }
    })
}
