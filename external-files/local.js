var turn=0 , board=[];
var over = false;
for(var i=0;i<9;i++){
    board[i]='';
}

function done(x){
    var text = document.getElementById('des');
    var my_element = document.getElementsByClassName("grid")[x];
    if(board[x] == '' && !over){
        if(turn==0){
            my_element.classList.add("done");
            turn=1;
            my_element.textContent="X";
            text.innerHTML="Player O's turn";
            board[x]='X';
        }
        else if(turn==1){
            my_element.classList.add("done");
            turn=0;
            my_element.textContent="O";
            text.innerHTML="Player X's turn";
            board[x]='O';
        }
        if(check_win(board[x]))
        {
            document.getElementById('des').innerHTML=board[x]+' wins';
        }
        else if(check_draw())
        {
            document.getElementById('des').innerHTML='draw';
        }
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
    for(var i=0;i<=8;i++){
        document.getElementsByClassName("grid")[i].textContent = '';
        board[i]='';
        document.getElementsByClassName("grid")[i].classList.remove("done");
    }
    turn=0;
    over = false;
    document.getElementById('des').innerHTML="Player X's turn";
}