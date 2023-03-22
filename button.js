$(document).ready(function() {
    $("#myButton").click(function() {
      var buttonValue = $(this).value;
      var data = { "buttonValue": buttonValue };
      $.ajax({
        type: "POST",
        url: "save.php",
        data: JSON.stringify(data),
        success: function(response) {
          console.log(response);
        },
      });
    });
  });
  