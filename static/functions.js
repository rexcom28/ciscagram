const handelAlerts = (type, msg)=> {
    
    //
    alertBox.innerHTML= `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${msg}!
            <button id="modalBtn" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>        
    `
    
    //
    setTimeout(()=>{
        const modal_Btn = document.getElementById('modalBtn')
        modal_Btn.click()
    }, 3500)
}
