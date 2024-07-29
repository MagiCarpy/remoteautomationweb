
const lightForm = document.getElementById("lightForm");
const lightSwitch = document.querySelector("#lightSwitch")

lightSwitch.addEventListener(
    "change",
    (e) => {
        if (lightSwitch.checked) {
            document.getElementById("lightStatus").innerHTML = "🟢";
        }
        else {
            document.getElementById("lightStatus").innerHTML = " ";
        }
    }
)