const search_results = document.querySelector("#search_results")
const input_search = document.querySelector("#input_search")
let my_timer = null

// setTimeout - runs only 1 time
// setInterval - runs forever in intervals
function search(){
    clearInterval(my_timer)
    if (input_search.value != ""){
        my_timer = setTimeout( async function(){
            try{                
                const search_for = input_search.value
                const conn = await fetch(`/search?q=${search_for}`)
                const data = await conn.json()
                search_results.innerHTML = ""
                console.log(data)
                data.forEach(item => {
                    const a = `<div class="instant-item" mix-get="/items/${item.item_pk}">
                                <img src="/static/images/${item.item_image}">
                                <a href="/${item.item_name}">${item.item_name}</a>
                                </div>`
                    search_results.insertAdjacentHTML("beforeend", a)
                })
                mix_convert()
                search_results.classList.remove("hidden")
            }catch(err){
                console.error(err)
            }
        }, 500 )
    }else{
        search_results.innerHTML = ""
        search_results.classList.add("hidden")
    }
}



addEventListener("click", function(event){
    if( ! search_results.contains(event.target) ){
        search_results.classList.add("hidden")
    }
    if( input_search.contains(event.target) ){
        search_results.classList.remove("hidden")
    }
})

function add_markers_to_map(data){
    console.log(data)
    data = JSON.parse(data)
    console.log(data)
    data.forEach(item=>{
        L.marker([item.item_latitude, item.item_longitude]).addTo(map)    
        .bindPopup(item.item_name)    
        .openPopup()        
    })

}


function onMarkerClick(event) {
    alert("Marker clicked at " + event.latlng);
}


document.getElementById('btn_items').onclick = () => {
    document.getElementById('items_admin').classList.remove('hidden');
    document.getElementById('single_item_admin').classList.remove('hidden');
    document.getElementById('users').classList.add('hidden');
    document.getElementById('single_user').classList.add('hidden');
};
document.getElementById('btn_users').onclick = () => {
    document.getElementById('items_admin').classList.add('hidden');
    document.getElementById('single_item_admin').classList.add('hidden');
    document.getElementById('users').classList.remove('hidden');
    document.getElementById('single_user').classList.remove('hidden');
};