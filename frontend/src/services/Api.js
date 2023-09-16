import axios from 'axios'

export default() => {
    return axios.create({
        baseURL:  `https://localhost:7299/api/`      /* API Server Link  */,
        headers: {
            //"Access-Control-Allow-Headers": "*", // this will allow all CORS requests
            //"Access-Control-Allow-Methods": 'OPTIONS,POST,GET', // this states the allowed methods
            "Content-Type": "application/json", // this shows the expected content type
            //'X-User-Identity': userIdentity
        }
    })
}