/*
// Modals
*/

//Collection Modal
// Preview Collection Label


//Update collection preview in item creation
$(document).ready(function () {
  $("#collection").change(function() { 
    var collection_id = $(this).val(); 
    
    $.ajax({
      type: "GET",
      url: "/get_collection_data/",
      data: {'id': collection_id},
      datatype: 'json',
      success: function (response) {
        title = response['title']
        color = response['color']
        $("#previewCollectionLabel").text("Collection: " + title)
        $("#previewCollectionLabel").css('background-color', color)
        
        //Also update all collection lists in the "New Texture" modals
        updateProfileCollections() //TODO:- Needs implementing
      }
    });
  });
});


/*
// Update Profile Blocks
*/

function updateUploadModals() {
  updateTextureUploadModal();
  updatePresetUploadModal();
}

function updateTextureUploadModal() {
  $.ajax({
    type: "GET",
    url: "/update_texture_upload_modal/",
    success: function (response) {
      $('#textureUploadModal').html(response)
    }
  });
}

function updatePresetUploadModal() {
  $.ajax({
    type: "GET",
    url: "/update_preset_upload_modal/",
    success: function (response) {
      $('#presetUploadModal').html(response)
    }
  });
}

function updateProfileItems() {
  updateProfileTextures();
  updateProfilePresets();
}

function updateProfileTextures() {
  $.ajax({
    type: "GET",
    url: "/get_user_textures/",
    success: function (response) {
      $('#profile-textures-block').html(response)
    }
  });
}

function updateProfilePresets() {
  $.ajax({
    type: "GET",
    url: "/get_user_presets/",
    success: function (response) {
      $('#profile-presets-block').html(response)
    }
  });
}

function UpdateProfileFavourites() {
  $.ajax({
    type:"GET",
    url: "/update_profile_favourites/",
    success: function (response) {
      $('#profile-favourites-block').html(response)
      console.log("updating favourites")
    }
  });
}

function updateProfileCollections() {
  $.ajax({
    type: "GET",
    url: "/get_user_collections/",
    datatype: 'json',
    success: function (response) {
      console.log("Response: " + response)
    }
  });
}



/*
// Browse Form
*/

$(document).ready(function () {
  $('#browse-form').submit(function (e) {
    var url = "/search_items/";
    $.ajax({
      type: "POST",
      url: url,
      data: $('#browse-form').serialize(), // serializes the form's elements.
      success: function (response) {
        console.log(response)  // display the returned data in the console.
        $('#item-browse-block').html(response)
      }
    });
    e.preventDefault(); // block the traditional submission of the form.
  });

  // Inject our CSRF token into our AJAX request.
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
      }
    }
  })
});

