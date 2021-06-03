console.log('post Category js')

const postsBox = document.getElementById('posts-box')
const spinnerBox = document.getElementById('spinner-box')
const loadBtn = document.getElementById('load-btn')
const endBox = document.getElementById('end-box')

const postForm = document.getElementById('post-form')
const title = document.getElementById('id_title')
const body = document.getElementById('id_body')
const category = document.querySelector('.select');


const csrf = document.getElementsByName('csrfmiddlewaretoken')

const url = window.location.href



const alertBox = document.getElementById('alert-box')

const dropozone = document.getElementById('my-dropzone')
const addBtn = document.getElementById('add-btn')
const closeBtns = [...document.getElementsByClassName('add-modal-close')]
const flexCheckDefault = document.getElementById('flexCheckDefault')
const flexCheckAuthor = document.getElementById('flexCheckAuthor')
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')


const resultsBox = document.getElementById('results-box')


const getCookie =(name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const deleted = localStorage.getItem('title')


const likeUnlikePosts = ()=> {
    const likeUnlikeForms = [...document.getElementsByClassName('like-unlike-forms')]
    likeUnlikeForms.forEach(form=> form.addEventListener('submit', e=>{
        e.preventDefault()
        const clickedId = e.target.getAttribute('data-form-id')
        const clickedBtn = document.getElementById(`like-unlike-${clickedId}`)

        $.ajax({
            type: 'POST',
            url: window.location.origin+"/like-unlike/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'pk': clickedId,
            },
            success: function(response){
                console.log(response)
                clickedBtn.textContent = response.liked ? `Unlike (${response.count})`: `Like (${response.count})`
            },
            error: function(error){
                console.log(error)
            }
        })

    }))
}

let newPostId = null
    
postForm.addEventListener('submit', e=>{
    e.preventDefault()
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'title': title.value,
            'body': body.value,
            'category':category.value
        },
        success: function(response){
            console.log(response);

            newPostId = response.id
            
            likeUnlikePosts()
            // $('#addPostModal').modal('hide')
            
            addBtn.disabled = true
            // postForm.reset()
        },
        error: function(error){
            console.log(error)
            handelAlerts('danger', 'ups...something went wrong')
        }
    })
})

const closemodal = document.getElementById('close-modal')
closemodal.addEventListener('click',()=>{
    location.reload();
})
addBtn.addEventListener('click', ()=> {
    
    dropozone.classList.remove('not-visible')

 })

 closeBtns.forEach(btn=> btn.addEventListener('click', ()=>{
     postForm.reset()
     if (!dropozone.classList.contains('not-visible')) {
         dropozone.classList.add('not-visible')
     }
     const myDropzone = Dropzone.forElement("#my-dropzone")
     myDropzone.removeAllFiles(true)
 }))

 Dropzone.autoDiscover = false
 const myDropzone = new Dropzone('#my-dropzone', {
     url: window.location.origin+'/upload/',
     init: function() {
         this.on('sending', function(file, xhr, formData){
             formData.append('csrfmiddlewaretoken', csrftoken)
             formData.append('new_post_id', newPostId)
         })
     },
     maxFiles: 15,
     maxFilesize: 40,
     acceptedFiles: '.png, .jpg, .jpeg'
 })




