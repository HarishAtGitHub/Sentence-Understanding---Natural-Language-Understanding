var app = angular.module('MyApp',['ngMaterial', 'ngMessages', 'material.svgAssetsCache']);

app.config(['$mdThemingProvider', function($mdThemingProvider) {
  
    $mdThemingProvider.theme('input')
      .primaryPalette('blue')
      .accentPalette('pink')
      .dark();
  }
]);

app.controller('TitleController', function($scope) {
  $scope.title = 'Ask Sparkey !';
});

app.controller('AppCtrl', function($scope) {
  var imagePath = 'img/list/60.jpeg';
});

var spanWidth = jQuery('#search').width();
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
final_transcript = '';
recognition.onresult = function(event) {
    var interim_transcript = '';

    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = final_transcript;
    console.log(final_transcript);
    if(final_transcript.trim().startsWith("Sparky")) {
         value = final_transcript.replace("Sparky",'');
         jQuery("#search").val(value);
         analyse(value);
    }
    final_transcript = ''
}

function analyse(text_input) {
    $.ajax({
       method: "POST",
       url: "/ml/api/v1.0/answer",
       data: JSON.stringify({ text: text_input }),
       contentType: 'application/json',
       success: function(msg){
          console.log(msg);
          //jQuery('span#result').text(JSON.stringify(msg, null, '\t'));
          jQuery('textarea').text(JSON.stringify(msg, null, '\t'));
       }
    })
}

recognition.start();
