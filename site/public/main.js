function sun_pos(percent){
    let sun = document.getElementById('sun');
    if(percent>1 || percent<=0){sun.style.display = 'none'; sun.style.bottom = '0vw'; sun.style.right = '0vw';}
    else{
        let x=83*percent;
        let y=x*Math.tan(36*Math.PI/180*(1-percent));
        sun.style.display = 'block';
        sun.style.left = `${x}vw`;
        sun.style.bottom = `${y}vw`;
    }
}

function moon_pos(percent){
    let moon = document.getElementById('moon');
    if(percent>1 || percent<=0){moon.style.display = 'none'; moon.style.bottom = '0vw'; moon.style.right = '0vw';}
    else{
        let x=83*percent;
        let y=x*Math.tan(36*Math.PI/180*(1-percent));
        moon.style.display = 'block';
        moon.style.left = `${x}vw`;
        moon.style.bottom = `${y}vw`;
    }
}

function wind_dir(deg){
    let compas = document.getElementById('compas')
    compas.style.transform = `rotate(${deg}deg)`
}

function searchOpen(){
    let search_block = document.getElementById('searchBox');
    let dspl = search_block.style.display;
    if (dspl=='none'){search_block.style.display = 'block';}
    else{search_block.style.display = 'none';}
}
searchOpen()

document.addEventListener('click', function(event){
    if(event.target.id == 'searchBox' || event.target.classList.contains('location')){searchOpen()}
})