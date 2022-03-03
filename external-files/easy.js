var picked;
var b;
var turn=0 , board=[];
var over = false;
for(var i=0;i<9;i++){
    board[i]='';
}

function pickit(a)
{
    picked = a;
    if(picked=='X'){
        b='O';
    }
    else{
        b='X';
        turn=1;
        done(auto());
    }
    document.getElementById("pickxo").style.display = 'none';
    document.getElementsByClassName("logo-container")[0].style.display = 'none';
    document.getElementById("play").style.display = 'block';
    document.getElementById("picked").innerHTML = 'You picked ' + picked ;
}

function done(x){
    console.log(x);
    if(board[x] == '' && !over){
        if(turn==0){
            var my_element = document.getElementsByClassName("grid")[x];
            console.log("you played");
            turn=1;
            my_element.textContent=picked;
            my_element.classList.add("done");
            board[x]=picked;
        }
        else if(turn==1){
            var my_element = document.getElementsByClassName("grid")[x];
            console.log("bot played");
            turn=0;
            my_element.textContent=b;
            my_element.classList.add("done");
            board[x]=b;
        }
        
        if(check_win(board[x])){
            document.getElementById('picked').innerHTML=board[x]+' wins';
        }
        else if(check_draw()){
            document.getElementById('picked').innerHTML='draw';
        }
        if(turn==1 && !check_draw() && !check_win('X') && !check_win('O')){
            var delayInMilliseconds = 600;
            setTimeout(function() {
                done(auto());
            }, delayInMilliseconds);
        }
    }
}

function auto()
{
    var bot = Math.floor(Math.random() * 9);
    console.log("random : "+bot);
    if(board[bot]==''){
        return ''+bot+'';
    }
    else{
        return auto();
    }
}

function check_win(player)
{
    for(var i=0;i<=2;i++){
        if(board[i]==board[i+3]&&board[i]==board[i+6]&&board[i]==player){
            over = true;
            return true;
        }
    }
    for(var i=0;i<=6;i+=3){
        if(board[i]==board[i+1]&&board[i]==board[i+2]&&board[i]==player){
            over = true;
            return true;
        }
    }
    if(board[0]==board[4]&&board[0]==board[8]&&board[0]==player){
        over = true;
        return true;
    }
    if(board[2]==board[4]&&board[2]==board[6]&&board[2]==player){
        over = true;
        return true;
    }
}

function check_draw()
{
    for(var i=0;i<9;i++){
        if(board[i]==''){
            return false;
        }
    }
    over = true;
    return true;
}

function restart()
{
    document.getElementById("play").style.display = 'none';
    document.getElementById("pickxo").style.display = 'flex';
    document.getElementsByClassName("logo-container")[0].style.display = 'flex';
    for(var i=0;i<=8;i++){
        document.getElementsByClassName("grid")[i].textContent = '';
        board[i]='';
        document.getElementsByClassName("grid")[i].classList.remove("done");
    }
    turn=0;
    over = false;
}