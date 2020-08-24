## 说明

该方式只能下载小鹅通 **已付费** 视频（需要登录），因为小鹅通播放器不能满足我的需求，所以才找到这种方式下载。

**如果有侵犯到任何人利益的，可提 issue 我删除代码**

## 环境需求

1. bash
2. wget
3. php

安装方法自行百度

## 使用说明

`./edownload.sh <referer> <m3u8_url> <ts_url> <filename>`

请使用 Google Chrome 获取以下参数：

1. 新建空白页，右击在菜单中选择 `inspect` ，进入 DevTools 后点击 Network
2. 将小鹅通播放页面地址复制到新标签页并打开
3. 在 Filter 栏中输入 `ts` 可以看到多个后缀名为 ts 的链接，选择任一链接复制，该链接为 `ts_url` 。然后点击该链接在右侧框中的 Headers - Request Headers 中找到 referer 字段，复制该值为 `referer` 。（其他值会随着课程变化而变化，该值每次不用重新获取）
4. 在 Filter 栏中输入 `m3u8` 可以看到一个后缀名为 m3u8 的链接，该链接为 `m3u8_url`

参数获取方式可能不够详细，如有疑问可以先参考 特别鸣谢 部分的链接

## 特别鸣谢

使用了这位兄弟的教程写的脚本，[如何下载与解密小鹅通、腾讯课堂等平台的付费视频 - 网络技术 - 天才小网管](https://www.qinyuanyang.com/post/240.html)