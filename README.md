<html>
  <body>
    <h1>Remote Automation Website</h1>
    <p>Used to remotely control devices from the site</p>
    <b>Concept: </b>
    <p>
      Uses local Raspberry Pi that sends intervaled get requests to API of online website to check a toggle value. The status recieved signals a relay switch to turn a device on or off.
    </p>
    <p>
      Probably not the best way to implement this, but does circumvent the dangers of port forwarding. Security can be improved later (not the important part right now).
    </p>
  </body>
</html>
