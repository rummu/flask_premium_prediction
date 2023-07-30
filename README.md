
# NF - Premium Predict 

- Predict the Premium percentage using api
- [Website url](http://157.245.101.234/)
- [Jenkins Url](http://157.245.101.234:8080)


## Things used

- Dockerized the Flask app with Nginx to facilitate easier building and deployment.
- Used jenkins to automate ci/cd process 
- used github hooks


## Authors

- [@ain-py](https://www.github.com/ain-py)
- [@rummu](https://www.github.com/rummu)

## API Reference

#### Get premium percentage

```http
  POST /premium_percent
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_data` | `string` | **Required**: Json data of user |

