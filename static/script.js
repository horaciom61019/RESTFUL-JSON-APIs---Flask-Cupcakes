const API_BASE_URL = "http://127.0.0.1:5000/api";


/** Display cupcakes in data base */
async function displayCupcakes() {
    const response = await axios.get(`${API_BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes){
        let cupcake = $(generateHTML(cupcakeData));
        $(".cupcakes-list").append(cupcake);
    }
}


/** Generate cupcake's html from API */
function generateHTML(cupcake) {
    return `
        <div data-id="${cupcake.id}" class="col-md-4">
            <li>
                Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}
                <button class="delete-btn">X</button>
            </li>
            <img class="cupcake-img" src="${cupcake.image}" width="100px" alt="Oops! No image">
        </div>
    `;
}


/** handle form for submitting new cupcake */
$('.new-cupcake-form').on("submit", async function(evt){
    evt.preventDefault();

    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    // Sends and receive data to/from API 
    const newCupcakeResponse = await axios.post(`${API_BASE_URL}/cupcakes`, {flavor, rating, size, image });

    let newCupcake = $(generateHTML(newCupcakeResponse.data.cupcake));
    $(".cupcakes-list").append(newCupcake);
    $(".new-cupcake-form").trigger("reset");
});


/** handle request to delete a cupcake */
$(".cupcakes-list").on("click", ".delete-btn", async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-id");

  await axios.delete(`${API_BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});


// Starts webpage
$(displayCupcakes);
