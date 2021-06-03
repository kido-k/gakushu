import axios from 'axios'

export default (_, inject) => {
  inject('getApi', async (url, callback, errorCallBack) => {
    const option = {
      headers: {
        Accept: 'application/json',
      },
    }

    await axios
      .get(url, option)
      .then((response) => {
        console.log('<<<<<<<<<< response!!!' + url)
        console.log(response.data)
        callback()
      })
      .catch((error) => {
        console.log('<<<<<<<<<< error!!!' + url)
        console.log(error)
        errorCallBack(error)
      })
  })
}
