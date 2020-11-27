
    // বার বার রিডাইরেক্ট হতে বিরত রাখতে নিচের ফাংশনটি কাজ করবে ।।।

$(document).on('click','.add-cart',function() {
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('Product Id :', productId, 'Action :', action);
    if (user == 'AnonymousUser'){
        // উজার যখন 'AnonymousUser' হয় তখন নিচের ফাংশনটি কাজ করবে ।।

        addCookieItem(productId,action)
    }else{
            // এক্ষেত্রে উজার এ.জে.এক্স ব্যবহ্নার করে ডাটা ভিউতে পাঠাবে ।। সাথে রিলোড হবে ।। 
        $.ajax({
        
            type: 'POST',
            url: '/com/add/',
            data:{'productId':productId,'action':action, csrfmiddlewaretoken: getCookie("csrftoken")},
            cache: false,
            success: function (json){
                console.log(json)
                location.reload()
            },
            error:function(xhr,errmsg,err){
    
            }
            
        });    
    }
});

function addCookieItem(productId,action){
    console.log('Function is working!!!')
    if(action == 'inc'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }
        else{
            console.log('increase prouduct Quantity')
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'dec') {
        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[productId]            
        }
    }
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
            console.log('product addedd in cart..')
        }
    } 
    console.log('cart:',cart)

        // ** নিচের লাইনটি উপরের ডাটা গুলো কুকিজ হিসাবে সংরক্ষণ করবে ।। যা 'base.html' এর সাথে সংযুক্ত।।
    document.cookie = 'cart=' +JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}
// var addBtns = document.getElementsByClassName('add-cart').addEventListener('click',function(e){
//     var productId = this.dataset.product
//     var action = this.dataset.action
//     sendToview(productId, action)
// })
//     function sendToview(productId, action){
//         console.log('We are sending data..')
//         var url = 'add/'

//         fetch(url,{
//             method:'POST',
//             headers:{
//                 'Content-Type':'application/json',

//             },
//             body:{'productId':productId, 'action':action
//         }
//         .then((response) => {
//             console.log('data:',data)
//             return response.json()
//         })
//         .then((data)=>{
//             console.log('data:',data)
//         })
//         })
//     }