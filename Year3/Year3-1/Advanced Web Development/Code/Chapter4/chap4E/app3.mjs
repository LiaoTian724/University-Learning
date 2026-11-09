// app4.mjs
// middlewares:
// morgan, which logs requests received
// compression, which compresses responses when necessary
// static, which serves static files

import { fileURLToPath } from 'url';
import { dirname } from 'path';
const __filename = fileURLToPath(import.meta.url);    // 获取当前 JavaScript 模块的 URL (当前 mjs 文件位置) /Volumes/E_disk/Year3.1/Code/Chapter4/chap4E/app3.mjs
const __dirname = dirname(__filename);    //从完整文件路径中提取所在文件夹的路径  /Volumes/E_disk/Year3.1/Code/Chapter4/chap4E

import express from 'express';
let app = express();

import morgan from 'morgan';  
import compression from 'compression';
app.use(morgan('tiny'));    // 自动记录浏览器向服务器发送的 HTTP 请求    GET /page1.html 200 1234 - 5 ms
app.use(compression());    // 压缩服务器返回给浏览器的数据，减少网络传输量
// 这三个都是 Middleware
// app.use(morgan('tiny'));
// app.use(compression());
// app.use(express.static(__dirname + '/public'));

app.get('/', (req, res) => {
  res.redirect('/page1.html');
});

// any file in '/public' has a name the matches the URL?
app.use(express.static(__dirname + '/public'));   // 实际访问page2.html匹配的是这行代码; 如果下面的 get 写在上面就是访问 get 了;

// try to move this route before the static middleware
app.get('/page2.html', (req, res) => {
  res.send('can you see this sentence?');
});

app.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
