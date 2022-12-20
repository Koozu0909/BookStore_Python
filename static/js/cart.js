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
            else
                alert("Hệ thống đang bị lỗi!")
        }).catch(err=> console.info(err))
    }
}

function updateCart(id, obj){
    if(obj.value == 0){
        obj.value = 1;
    }
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

function deleteCart(bookId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${bookId}`, {
            method: "delete",
            body :JSON.stringify({
                'book_id':bookId,
            }),
            headers:{
                'Content-Type':'application/json'
            }
        }).then(res => res.json()).then(data => {
            let cartNumber = document.getElementsByClassName('cart-number')
                for(let i =0; i <  cartNumber.length; i++){
                    cartNumber[i].innerText = data.total_quantity
                }

            let d2 = document.getElementById('total_amount')
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US")

            let c = document.getElementById(`cart${bookId}`)
            c.style.display = "none"
        }).catch(err => console.info(err)) // promise
    }
}