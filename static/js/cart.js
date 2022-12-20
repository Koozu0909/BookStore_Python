function addToCart(id,name,price,image){
    fetch('/api/add-cart',{
        method:'post',
        body :JSON.stringify({
            'id':id,
            'name':name,
            'price':price,
            'image':image,
            
        }),
        headers:{
            'Content-Type':'application/json'
        }

    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
        console.log(data.name)

        let cartNumber = document.getElementsByClassName('cart-number')
        for(let i =0; i <  cartNumber.length; i++){
            cartNumber[i].innerText = data.total_quantity
        }
       
    }).catch(function(err){
        console.info(err)
    })
}



function pay(){
    if(confirm('Xac nhan thanh toan')==true){
        fetch('/api/pay',{
            method:'post',
        }).then(res => res.json()).then(data=>{
            if(data.code =200){
                location.reload()
            }
        }).catch(err=> console.info(err))
    }
}

function updateCart(id, obj){
    fetch('/api/update-cart',{
        method:'put',
        body :JSON.stringify({
            'id':id,
            'quantity': parseInt(obj.value)
        }),
        headers:{
            'Content-Type':'application/json'
        }
    }).then(res => res.json()).then(data=>{
        let cartNumber = document.getElementsByClassName('cart-number')
        for(let i =0; i <  cartNumber.length; i++){
            cartNumber[i].innerText = data.total_quantity
        }
        let amount = document.getElementById('total_amount')
        amount.innerText = data.total_amount
    }).catch(err=> console.info(err))
}
