

const BASE_URL="http://localhost:5000/api";


// GENERATE CUPCAKE HTML WITH GIVEN DATA


function makeCupcakeHTML(new_cupcake){
    
    return `
    <div data-cupcake-id="${new_cupcake.id}">
        
    <li>
    ${new_cupcake.flavor}/${new_cupcake.size}/${new_cupcake.rating}
        
            <img class="cupcake-img" src="${new_cupcake.image}" alt="(no image provided)">
        
            <button class="delete-cupcake">X</button>
    </li>
        </div>
        `;
        
    }



               

//show initial cupcakes on page


async function showCupcakesList(){
    const response=await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcakeData of response.data.cupcakes){
        let newCupcake=$(makeCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}



//handle form for adding of new cupcakes


$("#new-cupcake-form").on("submit", async function (evt){
    evt.preventDefault();

    let id=$("#id").val();
    let flavor=$("#flavor").val();
    let size=$("#size").val();
    let rating=$("#rating").val();
    let image=$("#image").val();

    const newCupcakeResponse=await axios.post(`${BASE_URL}/cupcakes`,{
      id,flavor,size,rating,image
    });

    let newCupcake=$(makeCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("new-cupcake-form").trigger("reset");
});



// DELETING A CUPCAKE 
$("#cupcakes-list").on("click", ".delete-cupcake",async function(evt){
evt.preventDefault();
let $cupcake=$(evt.target).closest("div");
let cupcakeId=$cupcake.attr("data-cupcake-id");

await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
$cupcake.remove();

});

$(showCupcakesList);