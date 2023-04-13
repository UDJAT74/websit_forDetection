let imgs=document.querySelectorAll("img");
imgs.forEach(img =>{
    img.addEventListener("click",()=>{
        if(img.classList.contains("clicked")){
            img.classList.remove("clicked");
        }
        else{
            img.classList.add("clicked");
        }
//        img.style.width="100%";
//        img.style.height="650px";
    });
})