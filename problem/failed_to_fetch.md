
## Problem

Failed to fetch
TypeError: Failed to fetch at getPlaces (webpack-internal...

## Description:

後端在容器裡，服務名稱是 backend，對應的容器內部網路可以用 http://backend:5000 訪問，而前端 JS 是運行在瀏覽器裡的，它不是在容器裡，而是在本機上。

```js
const API = "http://backend:5000";
```

所以這裡的 backend 瀏覽器無法解析這個名字，所以 fetch 就失敗，出現 Failed to fetch。

## Solution:

不要用容器名稱，用本機映射端口就好。
