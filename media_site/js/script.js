
    // One way to initialize plugin code
	jQuery(document).ready(function() {
    	
    	jQuery("ul.messages").hide().slideDown();
    	
    	
    	jQuery('#serious-map').hover(function () {
	
    jQuery('#serious-info').stop(true, true).fadeTo("slow",1);

    
	
	}, function(){
		jQuery('#serious-info').fadeTo("normal",0.4);
//	    setTimeout(function() {
//	    	jQuery('#serious-info').fadeTo("normal",0.4);
//	    }, 1000);
	    }
	);
	
    });

   
