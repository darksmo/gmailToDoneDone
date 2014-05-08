(function(){
    addToDDFunc = function () {

        var getSelectedHtml = function () {                                          
            var html = "";                                                           
            if (typeof window.getSelection != "undefined") {                         
                var sel = window.getSelection();                                     
                if (sel.rangeCount) {                                                
                    var container = document.createElement("div");                   
                    for (var i = 0, len = sel.rangeCount; i < len; ++i) {            
                        container.appendChild(sel.getRangeAt(i).cloneContents());    
                    }                                                                
                    html = container.innerHTML;                                      
                }                                                                    
            } else if (typeof document.selection != "undefined") {                   
                if (document.selection.type == "Text") {                             
                    html = document.selection.createRange().htmlText;                
                }                                                                    
            }                                                                        
            return html;                                                             
        }; 

        var issueBody = getSelectedHtml();
        if (issueBody === "") {
            issueBody = $(gmail.dom.email_contents()[0]).text();
        }

        $.ajax({
            type:"POST",
            url: "http://localhost:8011",
            dataType : 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                "title" : gmail.get.email_subject().replace(/DoneDone IT!.*$/g, ''),
                "description" : issueBody
            })
        })
        .done(function(data) {
            if (typeof data === 'object' && data.hasOwnProperty('status')) {
                if (data.status === 'ok') {
                    $('#addToDDLink').css('background','#2B792B');
                }
                else {
                    $('#addToDDLink').css('background','red');
                    alert("An Error occurred!");
                }
            }
        });
    };

    // the minimum version of jQuery we want
    var v = "1.10.0";

    // check prior inclusion and version
    if (window.jQuery === undefined || window.jQuery.fn.jquery < v) {
        var done = false;
        var script = document.createElement("script");
        script.src = "//ajax.googleapis.com/ajax/libs/jquery/" + v + "/jquery.min.js";
        script.onload = script.onreadystatechange = function(){
            if (!done && (!this.readyState || this.readyState == "loaded" || this.readyState == "complete")) {
                done = true;
                initMyBookmarklet();
            }
        };
        document.getElementsByTagName("head")[0].appendChild(script);
    } else {
        initMyBookmarklet();
    }

    function initMyBookmarklet() {
        (window.myBookmarklet = function() {
            $.getScript('https://raw.githubusercontent.com/KartikTalwar/gmail.js/master/gmail.min.js', function () {
                $('#gbqfb').css('background', '#F26F21');

                // the Gmail object
                window.gmail = Gmail();
                gmail.observe.on('open_email', function () {
                    var added = 0;
                    var timer = setInterval(function (){
                        if (added > 0) {
                            clearInterval(timer);
                        }
                        else {
                            var domArray = gmail.dom.email_subject();
                            if (domArray.length > 0) {
                                domArray[0].innerHTML += ['<a id="addToDDLink" href="#" onclick="addToDDFunc(); return false">DoneDone IT!</a>',
                                    '<style> #addToDDLink { display: block; background: #F26F21; width: 136px; text-align: center; border-radius: 5px; color: white; text-decoration: none; cursor: pointer; cursor: hand; padding: 7px; font-weight: bold; float: left; margin: 8px; } </style>'
                                ].join('');
                                added = 1;
                            }     
                        }
                    }, 1000);
                });
            });
        })();
    }

})();

