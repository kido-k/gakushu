import axios from 'axios'

export default (_, inject) => {
  inject('postApi', async (url, callback, errorCallBack, postData) => {
    const option = {
      headers: {
        Accept: 'application/json',
      },
    }

    await axios
      .post(url, postData, option)
      .then((response) => {
        console.log('<<<<<<<<<< response!!!' + url)
        console.log(response.data)
        callback(response.data)
      })
      .catch((error) => {
        console.log('<<<<<<<<<< error!!!' + url)
        console.log(error)
        errorCallBack(error)
      })
  })
}
