cocaine-TornadoProxy
====================

Welcome to cocaine cloud through HTTP

# configuration

By default configuration path is **/etc/cocaine/cocaine-tornado-proxy.conf**

```js
{
    "instances" : 20, /* insances of services per app */
    "refresh_timeout" : 90, /* reconnection frequency of services */
    "timeouts" : {
            "A" : 1, /* as B */
            "B" : 5, /* deadline timeout for B's request */
            "C" : 4, /* as B */
            "default" : 0.5 /* default deadline */
}
```
