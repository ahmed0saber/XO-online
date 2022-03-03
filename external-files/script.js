/*  LOADING  */
const myTimeout = setTimeout(loading, 1000);
function loading(){
    document.getElementsByClassName("loader")[0].style.display = "none";
    document.getElementsByTagName("main")[0].style.display = "flex";
    document.getElementsByTagName("header")[0].style.display = "flex";
}