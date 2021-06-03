
const postBox   = document.getElementById('post-box')
const alertBox  = document.getElementById('alert-box')
const backBtn   = document.getElementById('back-btn')
const updateBtn = document.getElementById('update-btn')
const deleteBtn = document.getElementById('delete-btn')

const url       = window.location.href+ "data/"
const url2       = window.location.href

const updateUrl = window.location.href+ "update/"
const deleteUrl = window.location.href+ "delete/"

const updateForm = document.getElementById('update-form')
const deleteForm = document.getElementById('delete-form')

const spinnerBox= document.getElementById('spinner-box')

const titleInput = document.getElementById('id_title')
const bodyInput  = document.getElementById('id_body')
const categoryinput = document.querySelector('.select');
const visibleInput = document.getElementById('id_visible')

const csrf = document.getElementsByName('csrfmiddlewaretoken')
const dropozone = document.getElementById('my-dropzone')
let newPostId = null
const flexCheckDefault = document.getElementById('flexCheckDefault')
const flexCheckAuthor = document.getElementById('flexCheckAuthor')
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')


const resultsBox = document.getElementById('results-box')
const closeBtn = document.getElementById('close-btn')
closeBtn.addEventListener('click',()=>{
    location.reload()
})
updateBtn.addEventListener('click',()=>{
    const categoryinput = document.querySelector('.select');
    
    categoryinput.setAttribute("disabled", "disabled");
})

backBtn.addEventListener('click', ()=>{
    history.back()
})

$.ajax({
    type: 'GET',
    url: url,
    success: function (response){
        console.log('LOADING ',response.data)
        const data = response.data
        if(data.logged_in !== data.author){
            console.log('diff')
        } else {
            console.log('same')
            updateBtn.classList.remove('not-visible')
            deleteBtn.classList.remove('not-visible')

        }
        const titleEl = document.createElement('h3')
        titleEl.setAttribute('class', 'mt-3')
        titleEl.setAttribute('id', 'title')

        const bodyEl = document.createElement('p')
        bodyEl.setAttribute('class', 'mt-1')
        bodyEl.setAttribute('id', 'body')

        titleEl.textContent = data.title
        bodyEl.textContent  = data.body
        console.log('CAAAAAA   ',data['category'])

        
        
        
        
        newPostId=data.id
        postBox.appendChild(titleEl)
        postBox.appendChild(bodyEl)

        titleInput.value = data.title
        bodyInput.value  = data.body
        categoryinput.value =data['category']         
        if( data['visible']==false ){visibleInput.checked=false}else{visibleInput.checked=true}
        spinnerBox.classList.add('not-visible')
    },
    error: function(error){
        console.log(error)
    }
})


updateForm.addEventListener('submit', e=>{
    e.preventDefault()

    const title = document.getElementById('title')
    const body  = document.getElementById('body')
    const category =document.querySelector('.select');    
    const visible = document.getElementById('id_visible')
    
    $.ajax({
        type: "POST",
        url: updateUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'title':titleInput.value,
            'body': bodyInput.value,
            'category': categoryinput.value,//categoryinput.options[category.value].text,
            'visible': visible.checked

        },
        success: function(response){
            console.log(response)
            handelAlerts('success', 'post has been updated')
            title.textContent = response.title
            body.textContent  = response.body
            console.log('resssss ', response.category)
            newPostId = response.id
            //dropozone.classList.remove('not-visible')
        },
        error: function(error){
            console.log(error)
        }
    })

})


deleteForm.addEventListener('submit',e=>{
    e.preventDefault()

    $.ajax({
        type: "POST",
        url: deleteUrl,
        data:{
            'csrfmiddlewaretoken': csrf[0].value,
        },
        success: function(response){
            window.location.href= window.location.origin
            localStorage.setItem('title', titleInput.value)
        },
        error: function(error){
            console.log(error)
        }

    })

})

Dropzone.autoDiscover = false

const myDropzone = new Dropzone('#my-dropzone', {
    
    url: 'upload/',
    init:function() {

        this.on('sending', function(file, xhr, formData){
            formData.append('csrfmiddlewaretoken', csrf[0].value)
            formData.append('new_post_id', newPostId)
            console.log(url2)
            
        })
        
    },
    maxFiles: 15,
    maxFilesize: 40,
    acceptedFiles: '.png, .jpg, .jpeg'
})






const sendSearchData= (val, ch, author) =>{
    
    $.ajax({
        type: 'POST',
        url: window.location.origin+'/search/',
        data:{
            'csrfmiddlewaretoken': csrf[0].value,
            'val':val,
            'check': ch,
            'author':author,
        },
        success: (res)=>{
            
            const data = res.data
            resultsBox.innerHTML
            if(Array.isArray(data)){
                resultsBox.innerHTML = ""
                data.forEach(posts=>{
                    resultsBox.innerHTML += `
                        <a href="${window.location.origin}/${posts.pk}" class="item">
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

