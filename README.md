**This is a styled wrapper for Python's http.server** `python -m http.server 8080`<br>
which can be used to share files from your device to other devicies on the same network.<br>
![](demo.png)<br>
this styled wrapper can overcome the default crude style of the http server <br>
using a custom html, css (:<br>

Note:-<br>
you should download my custom python & js modules from: https://github.com/ibrahemesam/udf<br>
then save them inside a 'udf' folder beside the 'main.py' file<br>
(inside the root of this repo, do: `git clone https://github.com/ibrahemesam/udf`) <br>

Requirements:-<br>
`python -m pip install websockets`<br>
`nodejs` required by`npm install -g http-server`<br>

Usage:-<br>
make an alias for the 'main.py' file eg:<br>
`alias dirshare="python '/path/to/main.py'"`<br>
then:<br>
`dirshare ./` or `dirshare` to share the current working directory<br>
or<br>
`dirshare /path/to/any/folder` to share that specific folder<br>
