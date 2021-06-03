



const sendSearchData= (val, ch, author) =>{
    console.log('aaaaaaaaaaaaaaaaaaaaasasdasd', origin)
    $.ajax({
        type: 'POST',
        url: 'search/',
        data:{
            'csrfmiddlewaretoken': csrf[0].value,
            'val':val,
            'check': ch,
            'author':author,
        },
        success: (res)=>{
            console.log('aaaaaaaaaaaaaaaaaaaaaaaaaaaa',res)
            const data = res.data
            resultsBox.innerHTML
            if(Array.isArray(data)){
                resultsBox.innerHTML = ""
                data.forEach(posts=>{
                    resultsBox.innerHTML += `
                        <a href="${url}${posts.pk}" class="item">
                            <div class="row mt-2 mb-2">
                                <div class="col-2">
                                    <img src="${posts.image}" class="game-img"/>
                                </div>
                                <div class="col-10">
                                    <h5>${posts.title}</h5>
                                    <p class="text-muted">${posts.author}</p>
                                </div>
                            </div>
                        </a>
                    `
                })
            }else{
                if(searchInput.value.length > 0){
                    resultsBox.innerHTML= `<b>${data}</b>`
                }else{
                    resultsBox.classList.add('not-visible')
                }
            }
        },
        error: (err)=>{
            console.log(err)
        }
    })
}

searchInput.addEventListener('keyup', e=>{
    //console.log(e.target.value)
    
    if(resultsBox.classList.contains('not-visible') ){
        resultsBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value,flexCheckDefault.checked,flexCheckAuthor.checked)
    
})

flexCheckDefault.addEventListener('click', ()=>{    
    sendSearchData(searchInput.value,flexCheckDefault.checked,flexCheckAuthor.checked)
})
flexCheckAuthor.addEventListener('click', ()=>{
    sendSearchData(searchInput.value,flexCheckDefault.checked,flexCheckAuthor.checked)
    
})

