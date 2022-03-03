var screen = document.getElementsByClassName("fullscreen")[0];
screen.style.minHeight = (window.innerHeight - 100);
screen.style.maxHeight = (window.innerHeight - 100);
screen.style.height = (window.innerHeight - 100);
console.log((window.innerHeight - 100))



var element = document.getElementById("msg_container");
element.scrollTop = element.scrollHeight;

function _start(){
    /*element.scrollTop = element.scrollHeight;*/
            smoothScroll()
            element.scrollTop = element.scrollHeight;
            fastScroll()
}

var scrolled = true;
async function _load() {
    var element = document.getElementById("msg_container");
    var dimension1 = element.scrollHeight;
    var oldest = element.querySelector('div').dataset.id
    var messages = await fetch(`{% url 'chat:older_messages' %}?id=${oldest}`)
    messages = await messages.json()
    var inner1 = element.innerHTML;
    for (message of messages) {
        var myobj = document.getElementById("loadmsgs");
        myobj.remove();
        var xx = "Load previous messages";
        if (message.sender.front_id == "{{user.front_id}}"){
            element.innerHTML = `<button onclick="_load()" id="loadmsgs">` + xx + `</button>` + `<div class="msg myMSG" data-id="${message.unique_id}">
            <div>
                <p>` + message.content + `</p>
                <span>` + message.date_sent + `</span>
            </div>
        </div>` + element.innerHTML;
        }else{
            element.innerHTML = `<button onclick="_load()" id="loadmsgs">` + xx + `</button>` + `
            <div class="msg" data-id="${message.unique_id}">
            <a href="${message.sender.profile_url}">
                <img src="` + message.sender.image + `">
            </a>
            <div>
                <h4>` + message.sender.name + `</h4>
                <p>` + message.content + `</p>
                <span>` + message.date_sent + `</span>
            </div>
        </div>` + element.innerHTML;
        }
    }
    if(element.innerHTML == inner1)
    {
        var myobj = document.getElementById("loadmsgs");
        myobj.remove();
        element.innerHTML = `<p id="nomore">No more previous messages</p>` + element.innerHTML;
    }
    var dimension2 = element.scrollHeight;
    element.scrollTop = dimension2 - dimension1;
}






var element = document.getElementById("msg_container");
element.addEventListener('scroll', function (event) {
    var element = event.target;
    if (element.scrollHeight - element.scrollTop === element.clientHeight) {
        scrolled = true;
    }
    else {
        scrolled = false;
    }
});

// websocket handling 
let protocol = window.location.protocol == "https:" ? "wss:" : "ws:"
let url = protocol + "//" + window.location.host + '/ws/chat/'
let start_socket = ()=>{

    const socket = new WebSocket(url)
    socket.onmessage = (data)=>{
        message = JSON.parse(data.data)
        if (message.sender.front_id == "{{user.front_id}}"){
            element.innerHTML +=`
            <div class="msg myMSG" data-id="${message.unique_id}">
                <div>
                    <p>` + message.content + `</p>
                    <span>` + message.date_sent + `</span>
                </div>
            </div>`
        }else{
            element.innerHTML +=`
            <div class="msg" data-id="${message.unique_id}">
                <a href="${message.sender.profile_url}">
                    <img src="` + message.sender.image + `">
                </a>
                <div>
                    <h4>` + message.sender.name + `</h4>
                    <p>` + message.content + `</p>
                    <span>` + message.date_sent + `</span>
                </div>
            </div>`
        }
        if (element.scrollTop > element.scrollHeight - 900){
            smoothScroll()
            element.scrollTop = element.scrollHeight;
            fastScroll()
        }
    }

    socket.onclose = ()=>{
        setTimeout(()=>{
            start_socket()
        }, 1000)
    }
    function _send() {
        var element = document.getElementById("msg_container");
        let message = document.getElementById("tx1").value
        socket.send(
            JSON.stringify({'message':message})
        )
        document.getElementById("tx1").value = "";
    }
    
    $("#send").click(function(){
        _send();
    });

    document.getElementById("tx1").onkeypress = e => {
    if (e.keyCode == 13){
        _send()
    }
}
}
start_socket()


let smoothScroll = ()=>{
    element.style.scrollBehavior = 'smooth'
}
let fastScroll = ()=>{
    element.style.scrollBehavior = 'auto'
}