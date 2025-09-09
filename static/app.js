// Search functionality
const search_results = document.querySelector("#search_results")
const input_search = document.querySelector("#input_search")

// Show search results when the user types in the search input
if (search_results && input_search) {
    let my_timer = null
    
    
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
                                    <img src="/static/uploads/${item.item_image}">
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
    
    // Add event listener to the search input
    addEventListener("click", function(event){
        if( ! search_results.contains(event.target) ){
            search_results.classList.add("hidden")
        }
        if( input_search.contains(event.target) ){
            search_results.classList.remove("hidden")
        }
    })
}


// Map
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

// Initialize the map
function onMarkerClick(event) {
    alert("Marker clicked at " + event.latlng);
}


// Form validation
document.addEventListener("DOMContentLoaded", () => {
  // Go through all <form> elements on the page
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", e => {
      let isValid = true;

      // Check all inputs in the current form
      form.querySelectorAll("input[type=text], input[type=email], input[type=password], input[type=number]").forEach(input => {
        if (input.value.trim() === "") {
          input.classList.add("error"); 
          isValid = false;
        } else {
          input.classList.remove("error");
        }
      });

      if (!isValid) {
        // Stop form-submit if something is empty
        e.preventDefault();
      }
    });
  });
});
