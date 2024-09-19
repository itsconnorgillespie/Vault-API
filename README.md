## Vault API

### Disclaimer

This application was created in under one week. With this in mind, there is no guarantee that the following application is secure or bug-free. If you encounter a bug in the application, feel free to submit an Issue and I will attempt to fix it as soon as possible. Thanks for understanding. 

### Flowchart

The following flowchart aims to illustrate the logical design of the application. This flowchart was employed to plan the communication protocols found within the Vault application. 

```mermaid
flowchart TD
  client([Client])
  traefik([Traefik])
  fastapi([FastAPI])
  mqtt([MQTT Broker])
  mysql([MySQL Database])
  pico([Pico W])
  smtp([SMTP Server])

  client -- Client HTTP/HTTPS traffic forwarded via TLS Termination Proxy. --> traefik
  traefik -- Traefik forwards HTTP/HTTPS traffic to Docker container. --> fastapi
  pico <-- Publishes temperature and humidity payload to MQTT topic. --> mqtt
  fastapi <-- Subscribes to MQTT topic. --> mqtt
  fastapi -- Payload stored to MySQL table when recieved from MQTT topic. --> mysql
  fastapi -- Notifies client if temperature and humidity surpasses maximum value. --> smtp
```

## License
[Vault-API](https://github.com/connorgillespie/Vault-API) © 2019 by [Connor Gillespie](https://github.com/connorgillespie) is licensed under [CC BY-NC-ND 4.0](http://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1)  
![Creative Commons SVG](http://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png)