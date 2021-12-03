import os
import json
import requests
import subprocess
from websocket import create_connection

#Config (EDIT THIS ACCORDING TO YOUR USER NAME!!!)
spotify_path="C:\\Users\\YourUserName\\AppData\\Roaming\\Spotify\\Spotify.exe"

#Defining stuff
base_url = 'http://localhost:4693/json/list'
script = """
  var tag = document.createElement(\"style\"); 
  var text = document.createTextNode(\"[data-testid=\\\"test-ref-div\\\"] { display: none; } .GenericModal__overlay { display: none; } [data-testid=\\\"billboard-minimized\\\"] { display: none; } .k6onUQZSeZIsonJ4cSpK { display: none; } .hx2D0g_ursHte5bm62U2 { display: none; }\"); 
  document.getElementById(\"main\").appendChild(tag); 
  tag.setAttribute(\"id\", \"remove-ads\"); 
  tag.appendChild(text); 
  document.getElementsByClassName('ad-iframe')[0].remove(); 
  document.getElementsByClassName('MgL79SorehxR01FG_x8G')[0].innerHTML="Ads removed"; 
  document.getElementsByClassName('MgL79SorehxR01FG_x8G')[0].disabled=true; 
  """
payload = { 'id': 1337, 'method': 'Runtime.evaluate', 'params': {'expression': script} }

#Start spotify with open remote debugging port
subprocess.Popen([spotify_path, '--processStart', "Spotify.exe",
                  '--process-start-args', '--remote-debugging-port=4693'], cwd=os.path.dirname(spotify_path))

#Gather spotifys devtools websocket link
req = requests.get(base_url).json()
for a in req:
  ws_url = a.get('webSocketDebuggerUrl', 'ws://localhost:4693/devtools/page/{}'.format(a['id']))

#Create websocket and send the javascript payload
ws = create_connection(ws_url, timeout=100)
ws.send(json.dumps(payload))