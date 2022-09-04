// Submit post on submit
$('#post-form').on('submit', function(event){
  event.preventDefault();
  console.log("form submitted!")  // sanity check
  updateCSV();
});



// AJAX for posting

function updateCSV() {
  $('#message').html(
    `<div class="spinner-border text-primary d-flex m-auto" role="status">
          <span class="sr-only"></span>
        </div>`
  )
  var file = $('#formFileMultiple').prop('files')[0];
  console.log($('#formFileMultiple').prop('files'));
  var message = document.getElementById('message');
  var show_blank = document.getElementById('CSVTable')
  var formData = new FormData();
  formData.append("the_post", file)
  console.log(formData);
  $.ajax({
      url : "return-csv/", // the endpoint
      type : "POST", // http method
      contentType: false,
      processData: false,
      data: formData, // data sent with the post request
      enctype: 'multipart/form-data',

      // handle a successful response
      success : function(json) {
          message.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong>${json.message}</strong> Click on download button..
        </div>
          `
          json.my_arr.forEach(element => {
            show_blank.innerHTML += `<p>${element}</p>`
          });
      },

      // handle a non-successful response
      error : function(err) {
        message.innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
          <strong>Alright!</strong> ${err.message}
        </div>
          `
      }
  });
};
