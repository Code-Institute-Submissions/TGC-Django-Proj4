$('.nav-title').click(function(){
    $('.nav-content-Fantasy').slideToggle().toggleClass('active');
    console.log('click')
    if( $('.nav-content-Fantasy').hasClass('active')){
        $('.nav-title span').html('<i class="fa fa-minus" aria-hidden="true"></i>')
    }else{
        $('.nav-title span').html('<i class="fa fa-plus" aria-hidden="true"></i>')
    }
})
